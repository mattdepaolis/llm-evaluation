#!/usr/bin/env python3
"""
Model configuration utilities for LLM evaluation.
"""

from typing import Dict, Any, List, Optional, Union
from ..utils.gpu import get_available_gpus

def build_model_args(
    model_type: str,
    model_name: str,
    quantize: bool = False,
    quantization_method: Optional[str] = None,
    dtype: Optional[str] = None,
    max_model_len: Optional[int] = None,
    tensor_parallel_size: int = 1,
    gpu_memory_utilization: float = 0.9,
    vllm_quantization: Optional[str] = None,
    additional_model_args: Optional[str] = None
) -> str:
    """
    Build model arguments string based on model type and configuration.
    """
    if model_type == "vllm":
        # vLLM model_args format
        model_args = [f"pretrained={model_name}"]
        
        if tensor_parallel_size > 1:
            model_args.append(f"tensor_parallel_size={tensor_parallel_size}")
        
        if dtype:
            model_args.append(f'dtype={dtype}')
        
        if max_model_len:
            model_args.append(f"max_model_len={max_model_len}")
            
        # Add GPU memory utilization
        model_args.append(f"gpu_memory_utilization={gpu_memory_utilization}")
        
        # Add quantization for vLLM if specified
        if vllm_quantization:
            model_args.append(f"quantization={vllm_quantization}")
    else:
        # Standard HF model_args format
        model_args = [f"pretrained={model_name}"]
        
        if quantize:
            # Map our quantization method to proper HuggingFace parameters
            if quantization_method == "4bit":
                model_args.append("load_in_4bit=True")
            elif quantization_method == "8bit":
                model_args.append("load_in_8bit=True")
            elif quantization_method in ["nf4", "fp4"]:
                model_args.append("load_in_4bit=True")
                model_args.append(f"bnb_4bit_quant_type={quantization_method}")
            elif quantization_method == "int8":
                model_args.append("load_in_8bit=True")
            elif quantization_method == "int4":
                model_args.append("load_in_4bit=True")
    
    # Add additional model args if specified
    if additional_model_args:
        model_args.extend(additional_model_args.split(','))
        
    return ",".join(model_args)

def check_gpu_requirements(model_type: str, tensor_parallel_size: int) -> None:
    """
    Check if enough GPUs are available for tensor parallelism.
    Raises ValueError if not enough GPUs are available.
    """
    if model_type == "vllm" and tensor_parallel_size > 1:
        available_gpus = get_available_gpus()
        if available_gpus < tensor_parallel_size:
            raise ValueError(
                f"Not enough GPUs available for tensor parallelism. "
                f"Requested {tensor_parallel_size} GPUs but only {available_gpus} available. "
                f"Please reduce tensor_parallel_size to {available_gpus} or fewer."
            ) 