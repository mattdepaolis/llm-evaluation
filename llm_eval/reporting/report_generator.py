#!/usr/bin/env python3
"""
Report generation utilities for LLM evaluation.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any, List, Union
import numpy as np
from collections import defaultdict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Import the professional report generator
try:
    from .professional_report_generator import generate_professional_report, generate_professional_report_from_json
    PROFESSIONAL_REPORTS_AVAILABLE = True
except ImportError:
    PROFESSIONAL_REPORTS_AVAILABLE = False
    print("Warning: Professional report generator not available")

# Define CET timezone
try:
    CET = ZoneInfo("Europe/Berlin")
except ZoneInfoNotFoundError:
    print("Warning: Timezone 'Europe/Berlin' not found. Using system default timezone for fallback report naming.")
    CET = None

def get_reports_dir():
    """Get the path to the reports directory, creating it if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(script_dir))
    reports_dir = os.path.join(parent_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

def get_results_dir():
    """Get the path to the results directory, creating it if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(script_dir))
    results_dir = os.path.join(parent_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

def format_code_blocks(text):
    """Add markdown code formatting for multi-line or code-like text."""
    if not text:
        return text

    if isinstance(text, list):
        text = str(text)

    # If text is multi-line or has certain special characters, wrap in code blocks
    if '\n' in text or re.search(r'[{}\[\]()]', text) or '```' in text:
        if '```' in text:
            return text  # If it already has code formatting, leave it
        return f"```\n{text}\n```"
    return text

def create_ascii_bar_chart(data, title="", max_width=50):
    """
    Create a simple ASCII bar chart for the report.
    
    Args:
        data: Dictionary of {label: value} pairs to plot
        title: Title for the chart
        max_width: Maximum width of the bars
        
    Returns:
        ASCII representation of the bar chart
    """
    if not data:
        return ""
        
    # Find maximum value to scale the bars
    max_val = max(data.values())
    
    # Calculate bar widths
    bars = {}
    for label, value in data.items():
        # Scale the bar width to fit within max_width
        width = int((value / max_val) * max_width) if max_val > 0 else 0
        bars[label] = "█" * width + f" {value:.2f}"
    
    # Determine the longest label for alignment
    longest_label = max(len(label) for label in data.keys())
    
    # Build the chart
    chart = []
    if title:
        chart.append(f"### {title}")
        chart.append("")
    
    chart.append("```")
    for label, bar in bars.items():
        # Pad the label for alignment
        padded_label = label.ljust(longest_label)
        chart.append(f"{padded_label} | {bar}")
    chart.append("```")
    chart.append("")
    
    return "\n".join(chart)

def generate_markdown_report(results_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """
    Generate a markdown report directly from evaluation results.
    
    Args:
        results_data: The evaluation results data
        output_path: Optional specific output path for the report
    
    Returns:
        Path to the generated markdown report
    """
    # Extract model name from results
    model_name = results_data.get('config', {}).get('model_args', '').replace('pretrained=', '')
    if not model_name:
        model_name = "unknown_model"

    # Start building the markdown content
    markdown = [
        f"# Evaluation Report: {model_name}",
        f"Generated on {(datetime.now(CET) if CET else datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]

    # Add enhanced Model Configuration section
    markdown.append("## Model Configuration\n")
    config = results_data.get('config', {})
    
    # Create a table for configuration details
    config_table = ["| Parameter | Value |", "| --------- | ----- |"]
    
    # Add model name and arguments
    if 'model_args' in config:
        config_table.append(f"| Model | {config['model_args']} |")
        
        # Try to extract model parameters from model_args or other parts of config
        model_info = {}
        
        # Look for parameters information in model_args or other config fields
        if isinstance(config.get('model_info'), dict):
            model_info = config.get('model_info', {})
        
        # Add model parameters if available
        if 'parameters' in model_info:
            config_table.append(f"| Parameters | {model_info['parameters']} |")
        elif 'num_parameters' in model_info:
            config_table.append(f"| Parameters | {model_info['num_parameters']} |")
        
        # Add model architecture if available
        if 'architecture' in model_info:
            config_table.append(f"| Architecture | {model_info['architecture']} |")
        
        # Add model context length if available
        if 'context_length' in model_info:
            config_table.append(f"| Context Length | {model_info['context_length']} |")
    
    # Add generation parameters with more details
    if 'generation_args' in config:
        gen_args = config['generation_args']
        config_table.append(f"| **Generation Settings** | |")
        
        # Add common generation parameters
        if 'temperature' in gen_args:
            config_table.append(f"| Temperature | {gen_args['temperature']} |")
        
        if 'top_p' in gen_args:
            config_table.append(f"| Top-p | {gen_args['top_p']} |")
            
        if 'top_k' in gen_args:
            config_table.append(f"| Top-k | {gen_args['top_k']} |")
            
        if 'num_beams' in gen_args:
            config_table.append(f"| Beam Search Size | {gen_args['num_beams']} |")
            
        if 'max_tokens' in gen_args or 'max_new_tokens' in gen_args:
            max_tokens = gen_args.get('max_tokens', gen_args.get('max_new_tokens', 'N/A'))
            config_table.append(f"| Max Tokens | {max_tokens} |")
            
        # Add other generation parameters
        for key, value in gen_args.items():
            if key not in ['temperature', 'top_p', 'top_k', 'num_beams', 'max_tokens', 'max_new_tokens'] and isinstance(value, (int, float, str, bool)):
                config_table.append(f"| {key} | {value} |")
    
    # Add evaluation parameters
    if 'eval_args' in config:
        eval_args = config['eval_args']
        config_table.append(f"| **Evaluation Settings** | |")
        
        if 'num_samples' in eval_args:
            config_table.append(f"| Number of Samples | {eval_args['num_samples']} |")
            
        for key, value in eval_args.items():
            if key != 'num_samples' and isinstance(value, (int, float, str, bool)):
                config_table.append(f"| {key} | {value} |")
    
    if len(config_table) == 2:
        config_table.append("| *No configuration details found* | - |")
    
    markdown.extend(config_table)
    markdown.append("")

    # Add Task Category Summary section with visual ASCII charts
    if 'normalized_scores' in results_data:
        markdown.append("## Task Category Performance Summary\n")
        
        # Group normalized scores by task category
        task_categories = defaultdict(list)
        category_averages = {}
        
        for k, v in results_data['normalized_scores'].items():
            if isinstance(v, (int, float)):
                # Extract category from task name
                if k.startswith('normalized_'):
                    if '_average' in k:
                        category = k.replace('normalized_', '').replace('_average', '')
                        category_averages[category] = v
                    else:
                        parts = k.replace('normalized_', '').split('_')
                        
                        # Special handling for IFEVAL category
                        if 'ifeval' in k:
                            category = 'ifeval'
                            
                            # Add average score if this is the main IFEVAL metric
                            if k == 'normalized_leaderboard_ifeval':
                                category_averages['ifeval'] = v
                        else:
                            category = parts[0]
                            
                        task_categories[category].append((k, v))
        
        # Create a visual ASCII chart for category averages
        if category_averages:
            # Filter out 'overall' for the category chart
            category_chart_data = {k.upper(): v for k, v in category_averages.items() if k != 'overall'}
            
            # Ensure categories appear in a consistent order
            ordered_categories = {}
            for cat in ['bbh', 'gpqa', 'ifeval', 'musr', 'math']:
                if cat.upper() in category_chart_data:
                    ordered_categories[cat.upper()] = category_chart_data[cat.upper()]
            
            # Add any other categories not in our predefined order
            for cat, val in category_chart_data.items():
                if cat not in ordered_categories:
                    ordered_categories[cat] = val
                    
            markdown.append(create_ascii_bar_chart(ordered_categories, "Category Performance"))
            
            # Add overall score if available
            if 'overall' in category_averages:
                overall_score = category_averages['overall']
                markdown.append(f"**OVERALL SCORE: {overall_score:.2f}**\n")
        
        # Create a summary table with highlighted rows for category averages
        summary_table = ["| Category | Task | Score |", "| -------- | ---- | ----- |"]
        
        for category, tasks in sorted(task_categories.items()):
            # Skip 'overall' as it will be added at the end
            if category == 'overall':
                continue
                
            # Add category name
            if category in category_averages:
                avg_score = category_averages[category]
                summary_table.append(f"| **{category.upper()}** | **Average** | **{avg_score:.2f}** |")
            else:
                summary_table.append(f"| **{category.upper()}** | | |")
            
            # Add individual tasks
            for task_name, score in sorted(tasks):
                # Extract the specific task name from the full normalized name
                task_parts = task_name.split('_')
                task_display = '_'.join(task_parts[2:]) if len(task_parts) > 2 else task_parts[-1]
                summary_table.append(f"| {category} | {task_display} | {score:.2f} |")
        
        # Add overall average at the end if available
        if 'overall' in category_averages:
            summary_table.append(f"| **OVERALL** | **Average** | **{category_averages['overall']:.2f}** |")
        
        markdown.extend(summary_table)
        markdown.append("")

        # For each category with multiple tasks, create a separate chart
        for category, tasks in sorted(task_categories.items()):
            if len(tasks) > 1:
                task_scores = {t[0].split('_')[-1]: t[1] for t in tasks}
                if task_scores:
                    markdown.append(create_ascii_bar_chart(task_scores, f"{category.upper()} Tasks"))
    
    # Show summary of metrics per task
    markdown.append("## Detailed Metrics\n")
    metrics_table = ["| Task | Metric | Value |", "| ---- | ------ | ----- |"]
    
    # Each entry in data['results'] is a dictionary
    for tname, tmetrics in results_data.get('results', {}).items():
        for k, v in tmetrics.items():
            if isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool):
                # exclude stderrs
                if 'stderr' in k.lower():
                    continue
                val_str = f"{v:.4f}" if isinstance(v, float) else str(v)
                metrics_table.append(f"| {tname} | {k} | {val_str} |")
    
    if len(metrics_table) == 2:
        metrics_table.append("| *No numeric metrics found* | - | - |")
    
    markdown.extend(metrics_table)
    markdown.append("")

    # Show normalized scores if available
    if 'normalized_scores' in results_data:
        markdown.append("## Normalized Scores\n")
        norm_table = ["| Benchmark | Score |", "| --------- | ----- |"]
        
        for k, v in results_data['normalized_scores'].items():
            if isinstance(v, (int, float)):
                norm_table.append(f"| {k} | {v:.2f} |")
        
        if len(norm_table) == 2:
            norm_table.append("| *No normalized scores found* | - |")
        
        markdown.extend(norm_table)
        markdown.append("")

    # 3) Show sample details per task if available
    if 'samples' in results_data:
        markdown.append("# Task Samples\n")
        
        for task_name, samples_list in results_data.get('samples', {}).items():
            markdown.append(f"## {task_name}\n")
            
            # Display up to 2 samples per task
            displayed_samples = 0
            max_samples = 2  # Default number of samples to display
            
            # For math and GPQA tasks, ensure we show at least 2 samples if available
            if task_name.startswith('leaderboard_math_') or task_name.startswith('leaderboard_gpqa_'):
                max_samples = min(2, len(samples_list))  # Show up to 2 samples
            
            for sample in samples_list:
                if displayed_samples >= max_samples:
                    break
                
                # Check if this is a valid sample with enough information
                if not sample or not isinstance(sample, dict):
                    continue
                
                # Track if we've actually shown this sample
                has_shown_sample = False
                
                markdown.append(f"### Sample {displayed_samples + 1}\n")
                
                # Display question/prompt
                question = None
                if 'doc' in sample:
                    doc = sample['doc']
                    if isinstance(doc, dict):
                        if 'prompt' in doc:  # For IFEval
                            question = doc['prompt']
                        elif 'input' in doc:  # For many tasks
                            question = doc['input']
                        elif 'question' in doc:  # For question-answering tasks
                            question = doc['question']
                        elif 'Question' in doc:  # For GPQA tasks which use capitalized "Question"
                            question = doc['Question']
                        elif 'context' in doc and 'query' in doc:  # For some QA tasks
                            question = f"Context: {doc['context']}\n\nQuery: {doc['query']}"
                        elif 'problem' in doc and task_name.startswith('leaderboard_math_'):  # For math tasks
                            question = doc['problem']
                        elif task_name.startswith('leaderboard_gpqa_'):  # For GPQA tasks
                            if 'Question' in doc:
                                question = doc['Question']
                            elif 'question' in doc:
                                question = doc['question']
                            elif 'query' in doc:
                                question = doc['query']
                
                if question:
                    has_shown_sample = True
                    # For BBH tasks, don't truncate the question as it contains essential information
                    if task_name.startswith('leaderboard_bbh_'):
                        # Don't truncate BBH tasks at all
                        pass
                    elif len(question) > 1500:
                        # For other tasks, use a larger limit (1500 instead of 500)
                        question = question[:1500] + "..."
                    markdown.append(f"**Question:**\n\n{format_code_blocks(question)}\n")
                
                # Display multiple choice options if available
                choices = None
                if 'doc' in sample:
                    doc = sample['doc']
                    if isinstance(doc, dict):
                        if 'choices' in doc:
                            choices = doc['choices']
                        elif 'options' in doc:
                            choices = doc['options']
                        elif task_name.startswith('leaderboard_gpqa_'):
                            # For GPQA tasks, construct choices from individual choice fields
                            if all(f'choice{i}' in doc for i in range(1, 5)):
                                choices = [
                                    f"(A) {doc['choice1']}",
                                    f"(B) {doc['choice2']}",
                                    f"(C) {doc['choice3']}",
                                    f"(D) {doc['choice4']}",
                                ]
                            elif 'Correct Answer' in doc and any(f'Incorrect Answer {i}' in doc for i in range(1, 4)):
                                choices = [
                                    f"Incorrect Answer 1: {doc.get('Incorrect Answer 1', '')}",
                                    f"Incorrect Answer 2: {doc.get('Incorrect Answer 2', '')}",
                                    f"Incorrect Answer 3: {doc.get('Incorrect Answer 3', '')}",
                                    f"Correct Answer: {doc.get('Correct Answer', '')}"
                                ]
                
                if choices:
                    has_shown_sample = True
                    if isinstance(choices, list):
                        choices_str = "\n".join(choices)
                    else:
                        choices_str = str(choices)
                    markdown.append(f"**Choices:**\n\n{format_code_blocks(choices_str)}\n")
                
                # Display ground truth
                ground_truth = None
                if 'doc' in sample:
                    doc = sample['doc']
                    if isinstance(doc, dict):
                        if 'target' in doc:
                            ground_truth = doc['target']
                        elif 'answer' in doc:
                            if task_name.startswith('leaderboard_math_'):  # For math tasks
                                ground_truth = doc['answer']
                            elif task_name.startswith('leaderboard_gpqa_'):  # For GPQA tasks
                                ground_truth = f"The correct answer is {doc['answer']}"
                        elif 'Correct Answer' in doc and task_name.startswith('leaderboard_gpqa_'):
                            ground_truth = f"The correct answer is: {doc['Correct Answer']}"
                        elif 'label' in doc:
                            ground_truth = doc['label']
                        elif 'correct_answer' in doc:
                            ground_truth = doc['correct_answer']
                elif 'target' in sample:
                    ground_truth = sample['target']
                
                if ground_truth:
                    has_shown_sample = True
                    markdown.append(f"**Ground Truth:**\n\n{format_code_blocks(ground_truth)}\n")
                
                # Display model response
                response = None
                if 'filtered_resps' in sample and sample['filtered_resps']:
                    response = sample['filtered_resps'][0]
                elif 'resps' in sample and sample['resps']:
                    if isinstance(sample['resps'][0], list):
                        response = sample['resps'][0][0]
                    else:
                        response = sample['resps'][0]
                
                if response:
                    has_shown_sample = True
                    correctness = ""
                    if 'exact_match' in sample:
                        correctness = " (Correct)" if sample['exact_match'] == 1.0 else " (Incorrect)"
                    
                    filter_name = sample.get('filter', 'default')
                    
                    # Special handling for BBH tasks which have a specific response format
                    if task_name.startswith('leaderboard_bbh_') and isinstance(response, list) and len(response) == 2:
                        confidence_score, is_correct = response
                        
                        # Try to determine which option the model chose
                        selected_option = None
                        selected_score = None
                        
                        # For BBH tasks, the model selects the option with the highest confidence score
                        if 'filtered_resps' in sample and len(sample['filtered_resps']) > 1:
                            possible_options = ['(A)', '(B)', '(C)', '(D)', '(E)']
                            
                            # Find which option has the highest confidence
                            best_score = float('-inf')
                            best_index = None
                            
                            for i, resp in enumerate(sample['filtered_resps']):
                                if i < len(possible_options) and isinstance(resp, list) and len(resp) >= 1:
                                    score = resp[0]
                                    if score > best_score:
                                        best_score = score
                                        best_index = i
                            
                            if best_index is not None:
                                selected_option = possible_options[best_index]
                                selected_score = best_score
                        
                        # Check if the selection matches the ground truth
                        is_correct_selection = False
                        if 'doc' in sample and 'target' in sample['doc'] and selected_option:
                            target = sample['doc']['target']
                            is_correct_selection = (selected_option == target)
                        
                        # Format response to show selection and confidence clearly
                        if selected_option and selected_score is not None:
                            formatted_response = f"Selected option: {selected_option}\nConfidence score: {selected_score}\nCorrect: {is_correct_selection}"
                        else:
                            formatted_response = f"Confidence score: {confidence_score}\nCorrect: {is_correct}"
                        
                        markdown.append(f"**Model Response [{filter_name}]{correctness}:**\n\n{format_code_blocks(formatted_response)}\n")
                        
                        # If we have confidence scores for all options, display them
                        if 'filtered_resps' in sample and len(sample['filtered_resps']) > 1:
                            scores_by_option = {}
                            possible_options = ['(A)', '(B)', '(C)', '(D)', '(E)']
                            
                            # Collect scores for each option, up to the length of filtered_resps
                            for i, resp in enumerate(sample['filtered_resps']):
                                if i < len(possible_options) and isinstance(resp, list) and len(resp) >= 1:
                                    scores_by_option[possible_options[i]] = resp[0]
                            
                            if scores_by_option:
                                scores_text = "Confidence scores for all options:\n"
                                for opt, score in scores_by_option.items():
                                    # Highlight the selected option
                                    if opt == selected_option:
                                        scores_text += f"{opt}: {score} (SELECTED)\n"
                                    else:
                                        scores_text += f"{opt}: {score}\n"
                                markdown.append(f"**Option Confidence Scores:**\n\n{format_code_blocks(scores_text)}\n")
                    else:
                        markdown.append(f"**Model Response [{filter_name}]{correctness}:**\n\n{format_code_blocks(response)}\n")
                
                # Only count this as a displayed sample if we actually showed something
                if has_shown_sample:
                    displayed_samples += 1
                    markdown.append("---\n")
    
    # Determine output path if not specified
    if not output_path:
        reports_dir = get_reports_dir()
        # Use CET for timestamp if available
        now = datetime.now(CET) if CET else datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(reports_dir, f"report_{model_name}_{timestamp}.md")
    
    # Save markdown to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(markdown))
    
    print(f"Markdown report generated: {output_path}")
    return output_path

def get_simplified_leaderboard_filename(model_name: str, timestamp: Optional[str] = None) -> str:
    """
    Generate a simplified filename for leaderboard evaluation results.
    
    Args:
        model_name: Name of the model being evaluated
        timestamp: Optional timestamp string. If not provided, current CET time will be used.
        
    Returns:
        A simplified filename string for leaderboard evaluations
    """
    if not timestamp:
        # Generate a new timestamp using CET
        now = datetime.now(CET) if CET else datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
    
    # Create a simplified basename for leaderboard tasks
    return f"results_{model_name}_leaderboard_{timestamp}"

def generate_report(
    results: Dict[str, Any],
    json_path: str,
    generate_markdown: bool = True,
    use_professional_format: bool = True
) -> Optional[str]:
    """
    Generate a report from evaluation results.
    
    Args:
        results: The evaluation results
        json_path: Path to the JSON results
        generate_markdown: Whether to generate a markdown report
        use_professional_format: Whether to use the enhanced professional report format
        
    Returns:
        Path to the markdown report if generated, None otherwise
    """
    if not generate_markdown:
        return None
    
    try:
        # Try professional format first if available and requested
        if use_professional_format and PROFESSIONAL_REPORTS_AVAILABLE:
            try:
                basename = os.path.basename(json_path)
                basename = os.path.splitext(basename)[0]
                
                # Check if this is a leaderboard evaluation for filename formatting
                is_leaderboard = False
                if 'config' in results and 'tasks' in results['config']:
                    tasks = results['config']['tasks']
                    if isinstance(tasks, str) and 'leaderboard' in tasks:
                        is_leaderboard = True
                    elif isinstance(tasks, list) and any('leaderboard' in task for task in tasks if isinstance(task, str)):
                        is_leaderboard = True
                
                # For leaderboard tasks, simplify the filename
                if is_leaderboard:
                    model_name = results.get('config', {}).get('model_args', '').replace('pretrained=', '')
                    if not model_name:
                        model_name = "unknown_model"
                        
                    timestamp_match = re.search(r'_(\d{8}_\d{6})(?:_|$)', basename)
                    if timestamp_match:
                        timestamp = timestamp_match.group(1)
                    else:
                        now = datetime.now(CET) if CET else datetime.now()
                        timestamp = now.strftime('%Y%m%d_%H%M%S')
                        
                    basename = f"results_{model_name}_leaderboard_{timestamp}"
                
                reports_dir = get_reports_dir()
                professional_report_path = os.path.join(reports_dir, f"{basename}_professional_report.md")
                
                # Generate professional report
                result_path = generate_professional_report(results, professional_report_path)
                if result_path:
                    print(f"✅ Professional report generated successfully: {result_path}")
                    return result_path
                else:
                    print("⚠️ Professional report generation failed, falling back to standard format")
            except Exception as prof_error:
                print(f"⚠️ Professional report generation error: {prof_error}")
                print("📄 Falling back to standard report format")
        
        # Fall back to standard markdown report generation
        basename = os.path.basename(json_path)
        basename = os.path.splitext(basename)[0]
        
        # Check if this is a leaderboard evaluation
        is_leaderboard = False
        if 'config' in results and 'tasks' in results['config']:
            tasks = results['config']['tasks']
            if isinstance(tasks, str) and 'leaderboard' in tasks:
                is_leaderboard = True
            elif isinstance(tasks, list) and any('leaderboard' in task for task in tasks if isinstance(task, str)):
                is_leaderboard = True
        
        # For leaderboard tasks, simplify the filename by using the model name and timestamp only
        if is_leaderboard:
            # Extract the model name from results
            model_name = results.get('config', {}).get('model_args', '').replace('pretrained=', '')
            if not model_name:
                model_name = "unknown_model"
                
            # Look for a timestamp in the basename
            timestamp_match = re.search(r'_(\d{8}_\d{6})(?:_|$)', basename)
            if timestamp_match:
                timestamp = timestamp_match.group(1)
            else:
                # Generate a new timestamp using CET
                now = datetime.now(CET) if CET else datetime.now()
                timestamp = now.strftime('%Y%m%d_%H%M%S')
                
            # Create a simplified basename for leaderboard tasks
            basename = f"results_{model_name}_leaderboard_{timestamp}"
        
        reports_dir = get_reports_dir()
        report_path = os.path.join(reports_dir, f"{basename}_report.md")
        
        generate_markdown_report(results, report_path)
        return report_path
    except Exception as e:
        print(f"Error during report generation: {e}")
        
        # Try to fall back to the external script if direct generation fails
        try:
            module_name = "generate_evaluation_report"
            script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            report_script = os.path.join(script_dir, f"{module_name}.py")
            reports_dir = get_reports_dir()
            
            subprocess.run(["python", report_script, json_path, "--output_dir", reports_dir], check=True)
            
            # Derive the report path
            basename = os.path.basename(json_path)
            basename = os.path.splitext(basename)[0]
            report_path = os.path.join(reports_dir, f"{basename}_report.md")
            
            return report_path if os.path.exists(report_path) else None
        except Exception as fallback_error:
            print(f"Fallback report generation also failed: {fallback_error}")
            return None 