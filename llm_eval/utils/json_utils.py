#!/usr/bin/env python3
"""
JSON utilities for LLM evaluation.
"""

import json
import numpy as np
from typing import Any, Dict

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle numpy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        if hasattr(obj, 'dtype'):
            return str(obj)
        if hasattr(obj, '__dict__'):
            return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        try:
            return super(NumpyEncoder, self).default(obj)
        except TypeError:
            return str(obj)

def clean_for_json(obj: Any) -> Any:
    """Recursively clean an object to ensure it's JSON serializable."""
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif hasattr(obj, 'dtype'):
        return str(obj)
    elif hasattr(obj, '__dict__'):
        return clean_for_json({k: v for k, v in obj.__dict__.items() 
                              if not k.startswith('_')})
    else:
        return str(obj)

def save_json(data: Dict, output_path: str) -> None:
    """Save data to JSON file with proper encoding."""
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, cls=NumpyEncoder)
    print(f"Results saved to {output_path}") 