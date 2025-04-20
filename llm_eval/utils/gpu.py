#!/usr/bin/env python3
"""
GPU utilities for LLM evaluation.
"""

import gc

# Add check for GPU availability
try:
    import torch
    def get_available_gpus():
        """Get the number of available GPUs."""
        if not torch.cuda.is_available():
            return 0
        return torch.cuda.device_count()
        
    def clear_gpu_memory():
        """Clear GPU memory to free up VRAM."""
        if torch.cuda.is_available():
            print("Clearing GPU memory...")
            torch.cuda.empty_cache()
            gc.collect()
            print("GPU memory cleared.")
except ImportError:
    def get_available_gpus():
        """Fallback if torch is not available."""
        return 0
        
    def clear_gpu_memory():
        """Fallback if torch is not available."""
        print("torch not available, skipping GPU memory cleanup") 