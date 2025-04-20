#!/usr/bin/env python3
"""
Score normalization utilities for LLM evaluation.
"""

import numpy as np
from typing import Dict, Any, List, Union, Optional

def normalize_within_range(value, lower_bound=0, higher_bound=1):
    """Normalize a value within a given range to percentage (0-100)."""
    return (np.clip(value - lower_bound, 0, None)) / (higher_bound - lower_bound) * 100

def _extract_numeric_score(metrics_dict):
    """
    Helper to find a numeric 'score' from a dictionary of metrics.
    Looks for common keys like 'acc', 'acc_norm', 'exact_match','score' first.
    If none found, returns the first numeric field found, or 0.0 if none.
    """
    # Attempt known keys:
    for possible_key in ["acc","acc_norm","exact_match","score"]:
        if possible_key in metrics_dict:
            val = metrics_dict[possible_key]
            if isinstance(val, (float, int, np.integer, np.floating)):
                return float(val)
    # fallback: find first numeric
    for k, v in metrics_dict.items():
        if isinstance(v, (float, int, np.integer, np.floating)):
            return float(v)
    return 0.0

def normalize_scores(results):
    """
    Normalize scores for different benchmarks, including all leaderboard tasks:
     - BBH tasks (leaderboard_bbh_*)
     - GPQA tasks (leaderboard_gpqa_*)
     - MMLU-Pro tasks (leaderboard_mmlu_pro)
     - MUSR tasks (leaderboard_musr_*)
     - IFEval tasks (leaderboard_ifeval)
     - Math-lvl-5 tasks (leaderboard_math_*_hard)
    """
    from ..tasks.task_config import BBH_SUBTASKS, MUSR_SUBTASKS
    
    if 'results' not in results:
        return {}
    
    normalized_scores = {}
    raw_results = results['results']
    benchmark_scores = []
    
    # Process all leaderboard BBH tasks
    bbh_scores = []
    for task_name, metrics_dict in raw_results.items():
        if task_name.startswith("leaderboard_bbh_"):
            raw_score = _extract_numeric_score(metrics_dict)
            # Most BBH tasks are multiple choice with varying options (typically 2-5)
            # We'll assume a default of 4 options if we can't determine
            num_choices = 4
            subtask = task_name.replace("leaderboard_bbh_", "")
            if subtask in BBH_SUBTASKS:
                num_choices = BBH_SUBTASKS[subtask]
            
            lower_bound = 1/num_choices
            normalized_score = normalize_within_range(raw_score, lower_bound, 1.0)
            bbh_scores.append(normalized_score)
            normalized_scores[f'normalized_{task_name}'] = normalized_score
    
    # Also process classic BBH tasks (for compatibility)
    for task_name, metrics_dict in raw_results.items():
        if task_name.startswith("bbh_cot_fewshot_"):
            # parse out subtask
            subtask = task_name.replace("bbh_cot_fewshot_","")
            if subtask in BBH_SUBTASKS:
                num_choices = BBH_SUBTASKS[subtask]
                raw_score = _extract_numeric_score(metrics_dict)
                lower_bound = 1/num_choices
                normalized_score = normalize_within_range(raw_score, lower_bound, 1.0)
                bbh_scores.append(normalized_score)
                normalized_scores[f'normalized_{task_name}'] = normalized_score
    
    # if there's a top-level 'bbh' or 'leaderboard_bbh' result
    for bbh_key in ['bbh', 'leaderboard_bbh']:
        if bbh_key in raw_results:
            top_bbh_score = _extract_numeric_score(raw_results[bbh_key])
            # let's store it as a percentage
            normalized_scores[f'normalized_{bbh_key}'] = top_bbh_score * 100.0
            bbh_scores.append(top_bbh_score*100.0)
    
    if bbh_scores:
        normalized_scores['normalized_bbh_average'] = sum(bbh_scores)/len(bbh_scores)
        benchmark_scores.append(normalized_scores['normalized_bbh_average'])
    
    # GPQA tasks
    gpqa_scores = []
    for task_name, metrics_dict in raw_results.items():
        if task_name.startswith("leaderboard_gpqa_"):
            raw_score = _extract_numeric_score(metrics_dict)
            # GPQA is 4-choice multiple choice
            normalized_score = normalize_within_range(raw_score, 0.25, 1.0)
            gpqa_scores.append(normalized_score)
            normalized_scores[f'normalized_{task_name}'] = normalized_score
    
    if gpqa_scores:
        normalized_scores['normalized_gpqa_average'] = sum(gpqa_scores)/len(gpqa_scores)
        benchmark_scores.append(normalized_scores['normalized_gpqa_average'])
    
    # MMLU-PRO tasks
    if 'mmlu_pro' in raw_results:
        raw_score = _extract_numeric_score(raw_results['mmlu_pro'])
        val = normalize_within_range(raw_score, 0.1, 1.0)
        normalized_scores['normalized_mmlu_pro'] = val
        benchmark_scores.append(val)
    
    if 'leaderboard_mmlu_pro' in raw_results:
        raw_score = _extract_numeric_score(raw_results['leaderboard_mmlu_pro'])
        # MMLU-Pro has 10 choices, so chance level is 0.1
        val = normalize_within_range(raw_score, 0.1, 1.0)
        normalized_scores['normalized_leaderboard_mmlu_pro'] = val
        benchmark_scores.append(val)
    
    # IFEval
    for ifeval_key in ['ifeval', 'leaderboard_ifeval']:
        if ifeval_key in raw_results:
            prompt_strict = 0.0
            inst_strict = 0.0
            ifeval_dict = raw_results[ifeval_key]
            
            for key in ifeval_dict:
                if 'prompt_level_strict_acc' in key:
                    value = ifeval_dict[key]
                    if value != 'N/A' and isinstance(value, (int, float, str)):
                        try:
                            prompt_strict = float(value)
                        except (ValueError, TypeError):
                            pass
                elif 'inst_level_strict_acc' in key:
                    value = ifeval_dict[key]
                    if value != 'N/A' and isinstance(value, (int, float, str)):
                        try:
                            inst_strict = float(value)
                        except (ValueError, TypeError):
                            pass

            # store them as percentage
            normalized_scores[f'normalized_{ifeval_key}_prompt'] = prompt_strict*100
            normalized_scores[f'normalized_{ifeval_key}_inst'] = inst_strict*100
            normalized_scores[f'normalized_{ifeval_key}'] = (prompt_strict*100 + inst_strict*100)/2
            benchmark_scores.append(normalized_scores[f'normalized_{ifeval_key}'])
    
    # MUSR tasks
    musr_scores = []
    # Handle regular MUSR tasks
    for subtask_key, num_choices in MUSR_SUBTASKS.items():
        if subtask_key in raw_results:
            raw_score = _extract_numeric_score(raw_results[subtask_key])
            lower_bound = 1/num_choices
            normalized_score = normalize_within_range(raw_score, lower_bound, 1.0)
            musr_scores.append(normalized_score)
            normalized_scores[f'normalized_{subtask_key}'] = normalized_score
    
    # Handle leaderboard MUSR tasks
    for task_name, metrics_dict in raw_results.items():
        if task_name.startswith("leaderboard_musr_"):
            raw_score = _extract_numeric_score(metrics_dict)
            # Extract subtask from leaderboard_musr_*
            subtask = task_name.replace("leaderboard_musr_", "")
            # Default to 4 choices if not found
            num_choices = MUSR_SUBTASKS.get(f"musr_{subtask}", 4)
            lower_bound = 1/num_choices
            normalized_score = normalize_within_range(raw_score, lower_bound, 1.0)
            musr_scores.append(normalized_score)
            normalized_scores[f'normalized_{task_name}'] = normalized_score
    
    if musr_scores:
        normalized_scores['normalized_musr_average'] = sum(musr_scores)/len(musr_scores)
        benchmark_scores.append(normalized_scores['normalized_musr_average'])
    
    # Math-lvl-5 tasks
    math_scores = []
    for task_name, metrics_dict in raw_results.items():
        if task_name.startswith("leaderboard_math_") and task_name.endswith("_hard"):
            raw_score = _extract_numeric_score(metrics_dict)
            # Math is a generative task, normalize from 0 to 1
            normalized_score = raw_score * 100
            math_scores.append(normalized_score)
            normalized_scores[f'normalized_{task_name}'] = normalized_score
    
    if math_scores:
        normalized_scores['normalized_math_average'] = sum(math_scores)/len(math_scores)
        benchmark_scores.append(normalized_scores['normalized_math_average'])
    
    # overall average
    if benchmark_scores:
        normalized_scores['normalized_overall_average'] = sum(benchmark_scores)/len(benchmark_scores)
    
    return normalized_scores 