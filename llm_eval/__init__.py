"""
LLM Evaluation package for running comprehensive evaluations of language models.

This package provides a modular framework for evaluating language models
on various benchmarks and tasks.
"""

__version__ = "0.1.0"

# Import key functionality for easier access
from .evaluation.evaluator import evaluate_model
from .evaluation.enhanced_evaluator import enhanced_evaluate_model
from .tasks.task_config import list_available_tasks, TASK_NAME_MAPPING
from .normalization.score_normalizer import normalize_scores
from .reporting.report_generator import generate_report

# Expose the leaderboard tasks
LEADERBOARD_TASKS = TASK_NAME_MAPPING['LEADERBOARD']

# Provide direct access to the main function
from .main import main
