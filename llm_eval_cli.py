#!/usr/bin/env python3
"""
Command-line entry point for LLM evaluation.
"""

import argparse
import sys

from llm_eval.main import main
from llm_eval import LEADERBOARD_TASKS

def run_leaderboard():
    """Run the leaderboard evaluation with command-line arguments."""
    # Convert sys.argv to use leaderboard tasks
    for i, arg in enumerate(sys.argv):
        if arg == "--tasks" and i+1 < len(sys.argv):
            # Check if the next argument is "leaderboard" or similar
            next_arg = sys.argv[i+1].lower()
            if next_arg in ["leaderboard", "benchmark", "all"]:
                sys.argv[i+1] = "LEADERBOARD"
        elif arg == "--leaderboard":
            # Remove the --leaderboard argument and ensure --tasks LEADERBOARD is set
            sys.argv.pop(i)
            
            # Check if --tasks already exists
            task_index = -1
            for j, a in enumerate(sys.argv):
                if a == "--tasks":
                    task_index = j
                    break
            
            if task_index >= 0:
                # Replace existing tasks
                sys.argv[task_index+1] = "LEADERBOARD"
            else:
                # Add --tasks LEADERBOARD
                sys.argv.append("--tasks")
                sys.argv.append("LEADERBOARD")
            break
    
    # Proceed with normal main function
    main()

if __name__ == "__main__":
    # If --leaderboard is in arguments, use run_leaderboard
    if "--leaderboard" in sys.argv:
        run_leaderboard()
    else:
        main() 