#!/usr/bin/env python3
"""
Task configurations for LLM evaluation.
"""

# Task configurations
BBH_SUBTASKS = {
    "sports_understanding": 2,
    "tracking_shuffled_objects_three_objects": 3,
    "navigate": 2,
    "snarks": 2,
    "date_understanding": 6,
    "reasoning_about_colored_objects": 18,
    "object_counting": 19,
    "logical_deduction_seven_objects": 7,
    "geometric_shapes": 11,
    "web_of_lies": 2,
    "movie_recommendation": 6,
    "logical_deduction_five_objects": 5,
    "salient_translation_error_detection": 6,
    "disambiguation_qa": 3,
    "temporal_sequences": 4,
    "hyperbaton": 2,
    "logical_deduction_three_objects": 3,
    "causal_judgement": 2,
    "formal_fallacies": 2,
    "tracking_shuffled_objects_seven_objects": 7,
    "ruin_names": 6,
    "penguins_in_a_table": 5,
    "boolean_expressions": 2,
    "tracking_shuffled_objects_five_objects": 5
}

MUSR_SUBTASKS = {
    'leaderboard_musr_murder_mysteries': 2,
    'leaderboard_musr_object_placements': 5,
    'leaderboard_musr_team_allocation': 3
}

# Task categorization 
TASK_NAME_MAPPING = {
    'MMLU': ['mmlu', 'mmlu_stem', 'mmlu_humanities', 'mmlu_social_sciences', 'mmlu_other'],
    'MMLU-PRO': ['mmlu_pro', 'leaderboard_mmlu_pro'],
    'ARC': ['arc_easy', 'arc_challenge'],
    'BBH': ['bbh', 'leaderboard_bbh'],
    'GPQA': ['gpqa_main_zeroshot', 'gpqa_diamond_zeroshot', 'gpqa_extended_zeroshot', 'leaderboard_gpqa_main', 'leaderboard_gpqa_diamond', 'leaderboard_gpqa_extended'],
    'IFEval': ['ifeval', 'leaderboard_ifeval'],
    'MUSR': list(MUSR_SUBTASKS.keys()) + ['leaderboard_musr_murder_mysteries', 'leaderboard_musr_object_placements', 'leaderboard_musr_team_allocation'],
    'HumanEval': ['humaneval'],
    'TruthfulQA': ['truthfulqa_mc', 'truthfulqa_mc2'],
    'GSM8K': ['gsm8k'],
    'MATH': ['math', 'leaderboard_math_algebra_hard', 'leaderboard_math_counting_and_prob_hard', 'leaderboard_math_geometry_hard', 'leaderboard_math_intermediate_algebra_hard', 'leaderboard_math_num_theory_hard', 'leaderboard_math_prealgebra_hard', 'leaderboard_math_precalculus_hard'],
    'LEADERBOARD': [
        # BBH (3-shots, multichoice)
        'leaderboard_bbh_boolean_expressions', 'leaderboard_bbh_causal_judgement', 'leaderboard_bbh_date_understanding',
        'leaderboard_bbh_disambiguation_qa', 'leaderboard_bbh_formal_fallacies', 'leaderboard_bbh_geometric_shapes',
        'leaderboard_bbh_hyperbaton', 'leaderboard_bbh_logical_deduction_five_objects', 'leaderboard_bbh_logical_deduction_seven_objects',
        'leaderboard_bbh_logical_deduction_three_objects', 'leaderboard_bbh_movie_recommendation', 'leaderboard_bbh_navigate',
        'leaderboard_bbh_object_counting', 'leaderboard_bbh_penguins_in_a_table', 'leaderboard_bbh_reasoning_about_colored_objects',
        'leaderboard_bbh_ruin_names', 'leaderboard_bbh_salient_translation_error_detection', 'leaderboard_bbh_snarks',
        'leaderboard_bbh_sports_understanding', 'leaderboard_bbh_temporal_sequences', 'leaderboard_bbh_tracking_shuffled_objects_five_objects',
        'leaderboard_bbh_tracking_shuffled_objects_seven_objects', 'leaderboard_bbh_tracking_shuffled_objects_three_objects', 'leaderboard_bbh_web_of_lies',
        
        # GPQA (0-shot, multichoice)
        'leaderboard_gpqa_main', 'leaderboard_gpqa_diamond', 'leaderboard_gpqa_extended',
        
        # MMLU-Pro (5-shots, multichoice)
        'leaderboard_mmlu_pro',
        
        # MUSR (0-shot, multichoice)
        'leaderboard_musr_murder_mysteries', 'leaderboard_musr_object_placements', 'leaderboard_musr_team_allocation',
        
        # IFEval (0-shot, generative)
        'leaderboard_ifeval',
        
        # Math-lvl-5 (4-shots, generative, minerva version)
        'leaderboard_math_algebra_hard', 'leaderboard_math_counting_and_prob_hard', 'leaderboard_math_geometry_hard',
        'leaderboard_math_intermediate_algebra_hard', 'leaderboard_math_num_theory_hard', 'leaderboard_math_prealgebra_hard',
        'leaderboard_math_precalculus_hard'
    ]
}

TASK_DESCRIPTIONS = {
    'MMLU': 'Multiple choice QA covering 57 subjects across STEM, humanities, social sciences',
    'MMLU-PRO': 'Advanced version of MMLU with more challenging questions',
    'ARC': 'AI2 Reasoning Challenge (ARC) dataset with elementary/middle school science questions',
    'BBH': 'BIG-Bench Hard tasks - challenging subset of BIG-Bench benchmark',
    'GPQA': 'Graduate-level multiple-choice questions in biology, physics, and chemistry',
    'IFEval': 'Instruction Following Evaluation benchmark for measuring response quality',
    'MUSR': 'Multi-step reasoning tasks with murder mysteries, object placement, and team allocation',
    'HumanEval': 'Hand-written programming problems to evaluate code generation',
    'TruthfulQA': 'Questions where models might generate false or misleading answers',
    'GSM8K': 'Grade school math word problems requiring multi-step reasoning',
    'MATH': 'Challenging competition mathematics problems with step-by-step solutions',
    'LEADERBOARD': 'Comprehensive evaluation suite used in the Open LLM Leaderboard, including BBH, GPQA, MMLU-Pro, MUSR, IFEval, and Math-lvl-5'
}

def list_available_tasks():
    """Display available task groups for evaluation."""
    print("\nAVAILABLE TASK GROUPS:")
    
    # Print each task group and description
    for task_name, description in TASK_DESCRIPTIONS.items():
        task_count = len(TASK_NAME_MAPPING.get(task_name, []))
        print(f"\n{task_name}: {description}")
        print(f"   Contains {task_count} tasks. You can use '{task_name}' directly to run all tasks in this group.")
    
    print("\nSPECIFIC TASK NAMES TO USE WITH --tasks:")
    for group, tasks in TASK_NAME_MAPPING.items():
        print(f"\n{group}: {', '.join(tasks[:3])}{'...' if len(tasks) > 3 else ''}")
    
    if 'BBH' in TASK_NAME_MAPPING:
        print("\nFor BBH subtasks, use format: bbh_<subtask_name>")
        bbh_examples = list(BBH_SUBTASKS.keys())[:5]
        print(f"Examples: {', '.join(['bbh_' + s for s in bbh_examples])}...")
    
    print("\nHOW TO SPECIFY MULTIPLE TASKS:")
    print("You can specify multiple tasks in either of these ways:")
    print("1. Space-separated: --tasks mmlu gsm8k")
    print("2. Comma-separated: --tasks mmlu,gsm8k")
    print("3. Mixed: --tasks mmlu,gsm8k arc_challenge")
    print("4. Use task group names: --tasks LEADERBOARD")
    print("\nAll formats are equivalent. The evaluator will run each task in sequence.") 