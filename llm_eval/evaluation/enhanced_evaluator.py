#!/usr/bin/env python3
"""
Enhanced evaluation service that captures model text outputs.
"""

import os
import sys
import json
import signal
import re
import random
import numpy as np
from typing import List, Optional, Dict, Any, Union, Tuple

# Add lm-evaluation-harness to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "lm-evaluation-harness"))

try:
    from lm_eval import evaluator
    from lm_eval.api.model import LM
    from lm_eval.api.registry import get_model
    from lm_eval.tasks import get_task_dict
    from lm_eval.utils import make_table
except ImportError:
    raise ImportError("lm-evaluation-harness not found. Please make sure it is installed.")

from ..models.model_config import build_model_args, check_gpu_requirements
from ..utils.gpu import clear_gpu_memory
from ..utils.json_utils import clean_for_json, save_json
from ..normalization.score_normalizer import normalize_scores
from ..reporting.report_generator import generate_report as create_report, get_reports_dir, get_results_dir

def extract_choice_from_arguments(arguments: List[List[str]], best_choice_index: int) -> str:
    """
    Extract the actual choice text from the arguments based on the selected choice index.
    
    Args:
        arguments: List of argument lists containing prompts and expected responses
        best_choice_index: Index of the choice with highest score
        
    Returns:
        The actual choice text selected by the model
    """
    if not arguments or best_choice_index >= len(arguments):
        return f"Choice {best_choice_index}"
    
    # Get the argument list for the best choice
    choice_args = arguments[best_choice_index]
    if len(choice_args) >= 2:
        # The second element usually contains the expected response
        response = choice_args[1].strip()
        
        # Clean up the response - extract just the answer part
        if response.startswith(' '):
            response = response[1:]  # Remove leading space
            
        return response
    
    return f"Choice {best_choice_index}"

def decode_model_responses(sample: Dict[str, Any], task_name: str) -> str:
    """
    Decode model responses from logits to actual text choices.
    
    Args:
        sample: Sample data containing responses and arguments
        task_name: Name of the task being evaluated
        
    Returns:
        Decoded text response from the model
    """
    try:
        # Get the response scores
        if "resps" not in sample or not sample["resps"]:
            return "[No response data]"
        
        responses = sample["resps"]
        
        # Find the choice with the highest score (lowest negative logit)
        best_choice_index = 0
        best_score = float('-inf')
        
        for i, response_data in enumerate(responses):
            if isinstance(response_data, list) and len(response_data) > 0:
                if isinstance(response_data[0], list) and len(response_data[0]) >= 2:
                    # This is [score, bool] format
                    score = response_data[0][0]
                    if score > best_score:
                        best_score = score
                        best_choice_index = i
                else:
                    # This might be a simple score
                    score = response_data[0] if isinstance(response_data[0], (int, float)) else float('-inf')
                    if score > best_score:
                        best_score = score
                        best_choice_index = i
        
        # Extract the actual choice text from arguments
        if "arguments" in sample and sample["arguments"]:
            model_choice = extract_choice_from_arguments(sample["arguments"], best_choice_index)
            return model_choice
        
        # Fallback: just return the choice index
        return f"Choice {best_choice_index}"
        
    except Exception as e:
        print(f"Warning: Could not decode response for {task_name}: {e}")
        return "[ERROR: Could not decode response]"

def enhanced_evaluate_model(
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
    seed: Optional[int] = 42
) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Evaluate a language model on specified tasks with enhanced output capture.
    
    This function captures both the standard evaluation metrics and the actual
    text outputs generated by the model for each sample.
    """
    print(f"Enhanced evaluation - capturing model text outputs")
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
    
    # Set random seed for reproducible sample selection
    if seed is not None:
        print(f"Setting random seed to {seed} for reproducible sample selection")
        random.seed(seed)
        np.random.seed(seed)
        # Try to set torch seed if available
        try:
            import torch
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
        except ImportError:
            pass  # torch not available, that's okay
    
    # Run evaluation
    try:
        print(f"Starting enhanced evaluation on {len(tasks)} tasks: {', '.join(tasks)}")
        results = evaluator.simple_evaluate(**lm_eval_args)
        
        # Process results and enhance with decoded text outputs
        print("Processing results and extracting model text outputs...")
        enhanced_results = enhance_results_with_text_outputs(results)
        
        # Process results
        clean_results = clean_for_json(enhanced_results)
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
                    
                    # Generate report directly in organized location to avoid task reports in legacy location
                    if use_professional:
                        from ..reporting.professional_report_generator import generate_professional_report
                        generate_professional_report(clean_results, report_path)
                        print(f"✅ Professional report generated: {report_path}")
                    else:
                        generated_report = create_report(clean_results, output_path, generate_markdown=True, use_professional_format=False)
                        # Move the generated report to our organized location if it was created elsewhere
                        if generated_report and generated_report != report_path:
                            import shutil
                            try:
                                shutil.move(generated_report, report_path)
                                print(f"✅ Report generated: {report_path}")
                            except Exception as e:
                                print(f"Warning: Could not move report to organized location: {e}")
                        else:
                            print(f"✅ Report generated: {report_path}")
                        
                    # Log organized evaluation info
                    print(f"✅ Organized evaluation saved to: {eval_folder}")
            else:
                # Using legacy structure, convert to organized
                from ..main import generate_organized_evaluation_paths
                
                # Extract model info to generate organized paths
                model_name_from_config = clean_results.get('config', {}).get('model_args', model_name)
                if '=' in str(model_name_from_config):
                    model_name_from_config = model_name
                    
                eval_folder, organized_results_path, organized_report_path = generate_organized_evaluation_paths(
                    model_name=model_name_from_config,
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
            return enhanced_results, final_output_path
        
        # Clear GPU memory before returning
        clear_gpu_memory()
        return enhanced_results, None
        
    except Exception as e:
        print(f"Error during enhanced evaluation: {e}")
        # Clear GPU memory on error as well
        clear_gpu_memory()
        raise 

def enhance_results_with_text_outputs(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance evaluation results by adding decoded text outputs to sample data.
    
    Args:
        results: Raw evaluation results from lm-evaluation-harness
        
    Returns:
        Enhanced results with text outputs included
    """
    enhanced_results = results.copy()
    
    # Process each task's samples - they are stored at the top level in "samples"
    if "samples" in results:
        print("Found samples section, processing text outputs...")
        
        for task_name, task_samples in results["samples"].items():
            if isinstance(task_samples, list) and len(task_samples) > 0:  # Task has sample-level data
                print(f"Processing text outputs for task: {task_name} ({len(task_samples)} samples)")
                
                for i, sample in enumerate(task_samples):
                    if isinstance(sample, dict) and "resps" in sample:
                        try:
                            # Decode the model responses to text
                            model_output = decode_model_responses(sample, task_name)
                            
                            # Add the text output to the sample
                            sample["model_output"] = model_output
                            
                            # Also add a comparison with the target if available
                            if "target" in sample:
                                target = str(sample["target"]).strip().lower()
                                output = model_output.strip().lower()
                                sample["output_matches_target"] = (output == target)
                            else:
                                sample["output_matches_target"] = False
                            
                        except Exception as e:
                            print(f"Warning: Could not decode response for {task_name} sample {i}: {e}")
                            sample["model_output"] = "[ERROR: Could not decode response]"
                            sample["output_matches_target"] = False
    else:
        print("Warning: No 'samples' section found in results")
    
    return enhanced_results 