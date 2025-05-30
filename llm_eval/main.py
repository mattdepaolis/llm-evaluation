#!/usr/bin/env python3
"""
Main entry point for LLM evaluation.
"""

import argparse
import sys
import os
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

from .evaluation.evaluator import evaluate_model
from .tasks.task_config import TASK_NAME_MAPPING, BBH_SUBTASKS, list_available_tasks
from .utils.gpu import get_available_gpus
from .reporting.report_generator import get_results_dir

def process_tasks(tasks_input: List[str]) -> List[str]:
    """
    Process tasks from command line input, handling both comma-separated and space-separated values.
    
    Args:
        tasks_input: List of task specifications from command line
        
    Returns:
        List of valid task names
    """
    # Process tasks - handle both comma-separated and space-separated task names
    task_list = []
    for task_item in tasks_input:
        # Split by comma if present
        if ',' in task_item:
            task_list.extend([t.strip() for t in task_item.split(',') if t.strip()])
        else:
            task_list.append(task_item.strip())
    
    # Validate and expand tasks
    valid_tasks = []
    all_available_tasks = []
    
    # Build list of all available individual tasks
    for group, tasks in TASK_NAME_MAPPING.items():
        all_available_tasks.extend(tasks)
    
    # Add BBH subtasks
    for subtask in BBH_SUBTASKS.keys():
        all_available_tasks.append(f"bbh_{subtask}")
    
    for task in task_list:
        # Check if task is a task group name
        if task.upper() in TASK_NAME_MAPPING:
            # Add all tasks in the group
            group_tasks = TASK_NAME_MAPPING[task.upper()]
            print(f"Expanding task group '{task.upper()}' to {len(group_tasks)} individual tasks")
            valid_tasks.extend(group_tasks)
        # Check if task is an individual task name
        elif task in all_available_tasks:
            valid_tasks.append(task)
        else:
            print(f"Warning: Unknown task '{task}'. Skipping.")
    
    if not valid_tasks:
        raise ValueError("No valid tasks specified. Use --list_tasks to see available tasks.")
    
    return valid_tasks


def generate_output_path(model_name: str, model_type: str, tasks: List[str], 
                         quantize: bool = False, quantization_method: Optional[str] = None) -> str:
    """
    Generate an output path for the evaluation results.
    
    Args:
        model_name: Name of the model
        model_type: Type of the model (hf/vllm)
        tasks: List of tasks
        quantize: Whether quantization is enabled
        quantization_method: Quantization method
    
    Returns:
        Generated output path
    """
    model_name_short = model_name.split('/')[-1]
    tasks_str = '_'.join(tasks)
    if len(tasks_str) > 40:
        tasks_str = tasks_str[:37] + '...'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Add backend and quantization info to filename
    backend_suffix = f"_{model_type}"
    quant_suffix = f"_quant_{quantization_method}" if quantize and model_type == "hf" else ""
    filename = f"results_{model_name_short}{backend_suffix}{quant_suffix}_{tasks_str}_{timestamp}.json"
    
    # Place in the results directory
    results_dir = get_results_dir()
    return os.path.join(results_dir, filename)


def main():
    """Main entry point for the LLM evaluator."""
    parser = argparse.ArgumentParser(description="Evaluate language models using lm-evaluation-harness")
    parser.add_argument("--model", type=str, default="hf", help="Model provider (hf or vllm)")
    parser.add_argument("--model_name", type=str, help="Model name or path")
    parser.add_argument("--tasks", type=str, nargs="+", help="Tasks to evaluate on (space or comma separated)")
    parser.add_argument("--leaderboard", action="store_true", help="Run the full leaderboard evaluation suite")
    parser.add_argument("--num_fewshot", type=int, default=0, help="Number of examples in few-shot context")
    parser.add_argument("--batch_size", type=str, default="1", help="Batch size for evaluation ('auto' or number)")
    parser.add_argument("--device", type=str, default="cuda", help="Device to run on (cuda/cpu or specific cuda device like cuda:0)")
    parser.add_argument("--output", type=str, help="Path to save results as JSON")
    parser.add_argument("--num_samples", type=str, help="Number of samples per task ('all' or number)")
    parser.add_argument("--list_tasks", action="store_true", help="List available task groups and exit")
    parser.add_argument("--no_report", action="store_true", help="Skip generating markdown report")
    
    # Add quantization options
    parser.add_argument("--quantize", action="store_true", help="Enable model quantization for HF models")
    parser.add_argument(
        "--quantization_method", 
        type=str, 
        choices=["4bit", "8bit", "nf4", "fp4", "int8", "int4"], 
        default="4bit",
        help="Quantization method to use when --quantize is enabled"
    )
    
    # Add vLLM-specific options
    parser.add_argument("--dtype", type=str, choices=["float16", "bfloat16", "float32"], help="Data type for vLLM")
    parser.add_argument("--max_model_len", type=int, help="Maximum sequence length for vLLM")
    parser.add_argument(
        "--tensor_parallel_size", 
        type=int, 
        default=1,
        help="Number of GPUs to use for tensor parallelism with vLLM"
    )
    
    # Add GPU memory utilization option
    parser.add_argument("--gpu_memory_utilization", type=float, default=0.9, help="GPU memory utilization for vLLM (0.0 to 1.0)")
    
    # Add vLLM quantization option
    parser.add_argument("--vllm_quantization", type=str, choices=["awq", "squeezellm", "gptq"], 
                       help="Quantization method for vLLM (for pre-quantized models)")
    
    # Add additional model args option
    parser.add_argument("--additional_model_args", type=str, help="Additional arguments to pass to the model in the format key=value,key2=value2,...")
    
    # Add report format option
    parser.add_argument("--report_format", type=str, choices=["standard", "professional"], default="professional", 
                       help="Report format to use: 'professional' for enhanced visual reports or 'standard' for basic reports")

    args = parser.parse_args()
    
    # Handle special command modes
    if args.list_tasks:
        list_available_tasks()
        return
    
    # If leaderboard flag is set, override tasks
    if args.leaderboard:
        print("Running full leaderboard evaluation suite")
        args.tasks = ["LEADERBOARD"]
    
    # Check required arguments for evaluation
    if not args.model_name or not args.tasks:
        parser.error("--model_name and --tasks are required for evaluation")
    
    # Validate tensor_parallel_size for vLLM
    if args.model == "vllm" and args.tensor_parallel_size > 1:
        available_gpus = get_available_gpus()
        if available_gpus < args.tensor_parallel_size:
            parser.error(
                f"Not enough GPUs available for tensor parallelism. "
                f"Requested {args.tensor_parallel_size} GPUs but only {available_gpus} available. "
                f"Please reduce --tensor_parallel_size to {available_gpus} or fewer."
            )
    
    # Ensure dtype=float16 for AWQ quantization
    if args.model == "vllm" and args.vllm_quantization == "awq":
        if args.dtype is None or args.dtype != "float16":
            print("Warning: AWQ quantization only supports float16. Setting --dtype to float16.")
            args.dtype = "float16"
    
    # Process task list
    valid_tasks = process_tasks(args.tasks)
    
    # Check if we're running leaderboard tasks and preserve default few-shot settings
    is_leaderboard_task = False
    if "LEADERBOARD" in args.tasks or args.leaderboard:
        is_leaderboard_task = True
        # Only set this flag, we'll handle it later when passing to evaluate_model
        print("Running leaderboard tasks with their default few-shot settings")
    
    # Process num_samples argument
    num_samples = None
    if args.num_samples:
        if args.num_samples.lower() == 'all':
            num_samples = 'all'
        else:
            try:
                num_samples = int(args.num_samples)
            except ValueError:
                print(f"Warning: Invalid value for num_samples: {args.num_samples}. Using all samples.")
                num_samples = 'all'
    
    # Process batch_size argument
    batch_size = args.batch_size
    if batch_size != "auto":
        try:
            batch_size = int(batch_size)
        except ValueError:
            print(f"Warning: Invalid batch_size value: {batch_size}. Using default of 1.")
            batch_size = 1
    
    # Generate output path if not provided
    output_path = args.output
    if not output_path:
        output_path = generate_output_path(
            model_name=args.model_name,
            model_type=args.model,
            tasks=valid_tasks,
            quantize=args.quantize,
            quantization_method=args.quantization_method
        )
        print(f"Auto-generated output path: {output_path}")
    
    # Run evaluation
    try:
        evaluate_model(
            model_type=args.model,
            model_name=args.model_name,
            tasks=valid_tasks,
            num_fewshot=args.num_fewshot,
            batch_size=batch_size,
            device=args.device,
            output_path=output_path,
            num_samples=num_samples,
            generate_report=not args.no_report,
            quantize=args.quantize if args.model == "hf" else False,
            quantization_method=args.quantization_method if args.quantize and args.model == "hf" else None,
            dtype=args.dtype,
            max_model_len=args.max_model_len,
            tensor_parallel_size=args.tensor_parallel_size,
            gpu_memory_utilization=args.gpu_memory_utilization,
            vllm_quantization=args.vllm_quantization,
            additional_model_args=args.additional_model_args,
            preserve_default_fewshot=is_leaderboard_task,
            report_format=args.report_format
        )
    except KeyboardInterrupt:
        print("\nEvaluation interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error during evaluation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 