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
from .enhanced_evaluator import enhanced_evaluate_model

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
    report_format: str = "professional",
    capture_text_outputs: bool = True,
    seed: Optional[int] = 42
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
        capture_text_outputs: Whether to capture model text outputs (default: True)
        seed: Random seed for reproducible sample selection (default: 42)
        
    Returns:
        Tuple of (evaluation results, output path)
    """
    
    # Use enhanced evaluator by default to capture text outputs
    if capture_text_outputs:
        print("Using enhanced evaluation to capture model text outputs...")
        return enhanced_evaluate_model(
            model_type=model_type,
            model_name=model_name,
            tasks=tasks,
            num_fewshot=num_fewshot,
            batch_size=batch_size,
            device=device,
            output_path=output_path,
            num_samples=num_samples,
            generate_report=generate_report,
            quantize=quantize,
            quantization_method=quantization_method,
            dtype=dtype,
            max_model_len=max_model_len,
            tensor_parallel_size=tensor_parallel_size,
            gpu_memory_utilization=gpu_memory_utilization,
            vllm_quantization=vllm_quantization,
            additional_model_args=additional_model_args,
            preserve_default_fewshot=preserve_default_fewshot,
            report_format=report_format,
            seed=seed
        )
    
    # Fallback to original evaluation (without text output capture)
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
        
        # Save results using organized structure
        if output_path:
            # Check if we're using the organized structure (path contains "evaluations/")
            if "evaluations/" in output_path:
                # Already using organized structure
                save_json(clean_results, output_path)
                final_output_path = output_path
                
                # Generate report in the same folder
                if generate_report:
                    eval_folder = os.path.dirname(output_path)
                    report_path = os.path.join(eval_folder, "report.md")
                    use_professional = (report_format == "professional")
                    generated_report = create_report(clean_results, output_path, generate_markdown=True, use_professional_format=use_professional)
                    
                    # Move the generated report to our organized location if it was created elsewhere
                    if generated_report and generated_report != report_path:
                        import shutil
                        try:
                            shutil.move(generated_report, report_path)
                            print(f"✅ Professional report generated: {report_path}")
                        except Exception as e:
                            print(f"Warning: Could not move report to organized location: {e}")
                    else:
                        print(f"✅ Professional report generated: {report_path}")
                        
                    # Log organized evaluation info
                    print(f"✅ Organized evaluation saved to: {eval_folder}")
            else:
                # Using legacy structure, convert to organized
                from ..main import generate_organized_evaluation_paths
                
                # Extract model info to generate organized paths
                eval_folder, organized_results_path, organized_report_path = generate_organized_evaluation_paths(
                    model_name=model_name,
                    model_type=model_type,
                    tasks=tasks,
                    quantize=quantize,
                    quantization_method=quantization_method
                )
                
                # Save to organized structure
                save_json(clean_results, organized_results_path)
                final_output_path = organized_results_path
                
                # Generate report in organized location
                if generate_report:
                    use_professional = (report_format == "professional")
                    # Save report directly to organized location
                    from ..reporting.professional_report_generator import generate_professional_report
                    generate_professional_report(clean_results, organized_report_path)
                    print(f"✅ Professional report generated: {organized_report_path}")
                
                print(f"✅ Organized evaluation saved to: {eval_folder}")
            
            # Clear GPU memory before returning
            clear_gpu_memory()
            
            # Return the final output path along with results
            return results, final_output_path
        
        # Clear GPU memory before returning
        clear_gpu_memory()
        return results, None
    except Exception as e:
        print(f"Error during evaluation: {e}")
        # Clear GPU memory on error as well
        clear_gpu_memory()
        raise 