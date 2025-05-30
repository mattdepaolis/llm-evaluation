#!/usr/bin/env python3
"""
Core evaluation service for LLM evaluation.
"""

import os
import sys
import json
import signal
from typing import List, Optional, Dict, Any, Union, Tuple

# Add lm-evaluation-harness to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "lm-evaluation-harness"))

try:
    from lm_eval import evaluator
except ImportError:
    raise ImportError("lm-evaluation-harness not found. Please make sure it is installed.")

from ..models.model_config import build_model_args, check_gpu_requirements
from ..utils.gpu import clear_gpu_memory
from ..utils.json_utils import clean_for_json, save_json
from ..normalization.score_normalizer import normalize_scores
from ..reporting.report_generator import generate_report as create_report, get_reports_dir, get_results_dir

# Signal handler for keyboard interrupt
def signal_handler(sig, frame):
    print("\nEvaluation interrupted by user. Cleaning up...")
    clear_gpu_memory()
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

def evaluate_model(
    model_type: str,
    model_name: str,
    tasks: List[str],
    num_fewshot: int = 0,
    batch_size: Union[int, str] = 1,
    device: str = "cuda",
    output_path: Optional[str] = None,
    num_samples: Union[int, str] = None,
    generate_report: bool = True,
    quantize: bool = False,
    quantization_method: Optional[str] = None,
    dtype: Optional[str] = None,
    max_model_len: Optional[int] = None,
    tensor_parallel_size: int = 1,
    gpu_memory_utilization: float = 0.9,
    vllm_quantization: Optional[str] = None,
    additional_model_args: Optional[str] = None,
    preserve_default_fewshot: bool = False,
    report_format: str = "professional"
) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Evaluate a language model on specified tasks.
    
    Args:
        model_type: Model provider (hf or vllm)
        model_name: Model name or path
        tasks: Tasks to evaluate on
        num_fewshot: Number of examples in few-shot context
        batch_size: Batch size for evaluation
        device: Device to run on (cuda/cpu)
        output_path: Path to save results as JSON
        num_samples: Number of samples per task
        generate_report: Whether to generate a markdown report
        quantize: Enable model quantization for HF models
        quantization_method: Quantization method to use
        dtype: Data type for vLLM
        max_model_len: Maximum sequence length for vLLM
        tensor_parallel_size: Number of GPUs for tensor parallelism
        gpu_memory_utilization: GPU memory utilization (0.0 to 1.0)
        vllm_quantization: Quantization method for vLLM
        additional_model_args: Additional arguments for the model
        preserve_default_fewshot: Whether to preserve default few-shot settings for tasks
        report_format: Report format to use ('professional' or 'standard')
        
    Returns:
        Tuple of (evaluation results, output path)
    """
    print(f"Evaluating model type: {model_type}")
    print(f"Model: {model_name}")
    print(f"Tasks: {', '.join(tasks)}")
    print(f"Device: {device}, Few-shot examples: {num_fewshot}")
    print(f"Batch size: {batch_size}")
    
    if num_samples is not None and num_samples != "all":
        print(f"Using {num_samples} samples per task")
    
    # Check GPU availability for tensor parallelism
    check_gpu_requirements(model_type, tensor_parallel_size)
    
    # Build model args based on the model type
    if model_type == "vllm":
        print("Using vLLM backend for faster inference")
        print(f"GPU memory utilization: {gpu_memory_utilization:.2f}")
        
        if vllm_quantization:
            print(f"Using vLLM with {vllm_quantization.upper()} quantization")
    elif quantize:
        print(f"Using quantization method: {quantization_method}")
    
    # Build model args string
    model_args_str = build_model_args(
        model_type=model_type,
        model_name=model_name,
        quantize=quantize,
        quantization_method=quantization_method,
        dtype=dtype,
        max_model_len=max_model_len,
        tensor_parallel_size=tensor_parallel_size,
        gpu_memory_utilization=gpu_memory_utilization,
        vllm_quantization=vllm_quantization,
        additional_model_args=additional_model_args
    )
    
    # Set up arguments for lm-evaluation-harness
    lm_eval_args = {
        "model": model_type,
        "model_args": model_args_str,
        "tasks": tasks,
        "batch_size": batch_size,
        "device": device,
        "use_cache": None,
    }
    
    # Only set num_fewshot globally if not preserving defaults
    if not preserve_default_fewshot:
        lm_eval_args["num_fewshot"] = num_fewshot
        
    # Add sample limit if specified
    if num_samples is not None and num_samples != "all":
        lm_eval_args["limit"] = int(num_samples)
    
    # If we're preserving defaults for leaderboard tasks, inform the user
    if preserve_default_fewshot:
        print("Using default few-shot settings for each task:")
        print("  - BBH tasks: 3-shot")
        print("  - GPQA tasks: 0-shot")
        print("  - MMLU-Pro tasks: 5-shot")
        print("  - MUSR tasks: 0-shot")
        print("  - IFEval tasks: 0-shot")
        print("  - Math-lvl-5 tasks: 4-shot")
    
    # Run evaluation
    try:
        print(f"Starting evaluation on {len(tasks)} tasks: {', '.join(tasks)}")
        results = evaluator.simple_evaluate(**lm_eval_args)
        
        # Process results
        clean_results = clean_for_json(results)
        normalized_results = normalize_scores(clean_results)
        clean_results['normalized_scores'] = normalized_results
        
        # Save results
        if output_path:
            # Ensure the path is in the results directory
            if not os.path.isabs(output_path):
                results_dir = get_results_dir()
                output_path = os.path.join(results_dir, output_path)
            
            save_json(clean_results, output_path)
            
            # Generate markdown report if requested
            report_path = None
            if generate_report:
                use_professional = (report_format == "professional")
                report_path = create_report(clean_results, output_path, generate_markdown=True, use_professional_format=use_professional)
            
            # Clear GPU memory before returning
            clear_gpu_memory()
            
            # Return the output path along with results
            return results, output_path
        
        # Clear GPU memory before returning
        clear_gpu_memory()
        return results, None
    except Exception as e:
        print(f"Error during evaluation: {e}")
        # Clear GPU memory on error as well
        clear_gpu_memory()
        raise 