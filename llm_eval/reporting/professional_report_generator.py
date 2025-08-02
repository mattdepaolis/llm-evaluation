#!/usr/bin/env python3
"""
Professional Report Generator for LLM Evaluation
Creates visually appealing and comprehensive evaluation reports with enhanced readability.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any, List, Union, Tuple
import numpy as np
from collections import defaultdict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Define CET timezone
try:
    CET = ZoneInfo("Europe/Berlin")
except ZoneInfoNotFoundError:
    print("Warning: Timezone 'Europe/Berlin' not found. Using system default timezone.")
    CET = None

def get_reports_dir():
    """Get the path to the reports directory, creating it if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(script_dir))
    reports_dir = os.path.join(parent_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

def create_performance_badge(score: float, threshold_good: float = 70.0, threshold_fair: float = 50.0) -> str:
    """Create a performance badge based on score."""
    if score >= threshold_good:
        return "🟢 **EXCELLENT**"
    elif score >= threshold_fair:
        return "🟡 **GOOD**"
    else:
        return "🔴 **NEEDS IMPROVEMENT**"

def create_progress_bar(score: float, max_score: float = 100.0, width: int = 20) -> str:
    """Create a visual progress bar for scores."""
    percentage = min(score / max_score, 1.0) if max_score > 0 else 0
    filled = int(percentage * width)
    empty = width - filled
    
    if percentage >= 0.7:
        color = "🟩"
    elif percentage >= 0.5:
        color = "🟨"
    else:
        color = "🟥"
    
    bar = "█" * filled + "░" * empty
    return f"{color} {bar} {score:.1f}%"

def create_comparison_chart(data: Dict[str, float], title: str = "", max_width: int = 40) -> str:
    """Create an enhanced ASCII comparison chart with better visualization."""
    if not data:
        return ""
    
    max_val = max(data.values()) if data else 1
    
    chart = []
    if title:
        chart.append(f"### 📊 {title}")
        chart.append("")
    
    chart.append("```")
    chart.append("Performance Distribution:")
    chart.append("")
    
    # Sort by score for better visualization
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
    for label, value in sorted_data:
        # Create a visual bar
        percentage = (value / max_val) if max_val > 0 else 0
        bar_length = int(percentage * max_width)
        bar = "█" * bar_length
        
        # Add performance indicator
        if percentage >= 0.8:
            indicator = "🟢"
        elif percentage >= 0.6:
            indicator = "🟡"
        else:
            indicator = "🔴"
        
        # Format the line
        padded_label = label.ljust(15)
        chart.append(f"{indicator} {padded_label} │{bar.ljust(max_width)} │ {value:.1f}")
    
    chart.append("```")
    chart.append("")
    
    return "\n".join(chart)

def create_detailed_metrics_table(metrics: Dict[str, Any]) -> List[str]:
    """
    Create a detailed metrics table with task names, versions, filters, n-shot, metrics, values, and stderr.
    Similar to the format used in LM Evaluation Harness official outputs.
    """
    if not metrics:
        return []
    
    table_lines = [
        "## 📊 Detailed Results",
        "",
        "| Tasks | Version | Filter | n-shot | Metric | | Value | | Stderr |",
        "| ----- | ------- | ------ | ------ | ------ |-| ----- |-| ------ |"
    ]
    
    # Group tasks by their base name for better organization
    task_groups = {}
    
    for task_name, task_metrics in metrics.items():
        if isinstance(task_metrics, dict) and any(key not in ['alias', ' '] for key in task_metrics.keys()):
            # Extract base task group (remove specific suffixes)
            if task_name == 'leaderboard':
                continue  # Skip the aggregate entry
            
            # Determine task group
            if task_name.startswith('leaderboard_bbh_'):
                group = 'BBH'
            elif task_name.startswith('leaderboard_math_'):
                group = 'Math'
            elif task_name.startswith('leaderboard_gpqa_'):
                group = 'GPQA'
            elif task_name.startswith('leaderboard_musr_'):
                group = 'MUSR'
            elif task_name == 'leaderboard_ifeval':
                group = 'IFEval'
            elif task_name == 'leaderboard_mmlu_pro':
                group = 'MMLU-Pro'
            else:
                group = 'Other'
            
            if group not in task_groups:
                task_groups[group] = []
            task_groups[group].append((task_name, task_metrics))
    
    # Process each group
    for group_name in ['BBH', 'GPQA', 'MMLU-Pro', 'MUSR', 'IFEval', 'Math', 'Other']:
        if group_name not in task_groups:
            continue
            
        # Add group header
        if len(task_groups[group_name]) > 1:
            table_lines.append(f"| **{group_name}** | | | | | | | | |")
        
        # Sort tasks within group
        sorted_tasks = sorted(task_groups[group_name], key=lambda x: x[0])
        
        for task_name, task_metrics in sorted_tasks:
            # Extract task display name
            display_name = task_name.replace('leaderboard_', '').replace('_', ' ').title()
            if len(display_name) > 40:
                display_name = display_name[:37] + "..."
            
            # Determine version (always 1.0 for now)
            version = "1.0"
            
            # Determine filter (always "none" for these tasks)
            filter_type = "none"
            
            # Determine n-shot based on task type
            n_shot = ""
            if task_name.startswith('leaderboard_bbh_'):
                n_shot = "3"
            elif task_name.startswith('leaderboard_math_'):
                n_shot = "4" 
            elif task_name.startswith('leaderboard_gpqa_'):
                n_shot = "0"
            elif task_name.startswith('leaderboard_musr_'):
                n_shot = "0"
            elif task_name == 'leaderboard_ifeval':
                n_shot = "0"
            elif task_name == 'leaderboard_mmlu_pro':
                n_shot = "5"
            
            # Extract metrics
            metrics_found = []
            for metric_key, value in task_metrics.items():
                if metric_key in ['alias', ' ']:
                    continue
                    
                # Parse metric name and filter
                if ',' in metric_key:
                    metric_name, _ = metric_key.split(',', 1)
                else:
                    metric_name = metric_key
                
                # Skip stderr metrics for now, we'll handle them separately
                if '_stderr' in metric_name:
                    continue
                
                # Get corresponding stderr if available
                stderr_key = f"{metric_name}_stderr,none"
                stderr_value = task_metrics.get(stderr_key, "N/A")
                
                # Format the value
                if isinstance(value, (int, float)):
                    if value <= 1.0:
                        formatted_value = f"{value:.4f}"
                    else:
                        formatted_value = f"{value:.2f}"
                else:
                    formatted_value = str(value)
                
                # Format stderr
                if stderr_value == "N/A" or stderr_value is None:
                    formatted_stderr = "N/A"
                elif isinstance(stderr_value, (int, float)):
                    formatted_stderr = f"{stderr_value:.4f}"
                else:
                    formatted_stderr = str(stderr_value)
                
                # Determine direction indicator
                direction = "↑"  # Most metrics are "higher is better"
                
                metrics_found.append((metric_name, formatted_value, formatted_stderr, direction))
            
            # Add rows for each metric
            for i, (metric_name, formatted_value, formatted_stderr, direction) in enumerate(metrics_found):
                if i == 0:
                    # First row includes task info
                    table_lines.append(
                        f"| {display_name} | {version} | {filter_type} | {n_shot} | {metric_name} | {direction} | {formatted_value} | ± | {formatted_stderr} |"
                    )
                else:
                    # Subsequent rows are indented
                    table_lines.append(
                        f"|  | | | | {metric_name} | {direction} | {formatted_value} | ± | {formatted_stderr} |"
                    )
    
    table_lines.append("")
    table_lines.append("**Notes:**")
    table_lines.append("- ↑ indicates higher values are better")
    table_lines.append("- Version refers to the task format version")
    table_lines.append("- Filter shows any applied filtering (none = no filtering)")
    table_lines.append("- n-shot indicates the number of few-shot examples used")
    table_lines.append("- Stderr shows standard error where available")
    table_lines.append("")
    
    return table_lines

def create_evaluation_config_section(num_samples: Union[int, str] = 50, sample_size_note: str = "") -> List[str]:
    """
    Create a configuration section explaining evaluation parameters.
    """
    config_lines = [
        "### ⚙️ **Evaluation Configuration**",
        "",
        "| Parameter | Value | Description |",
        "| --------- | ----- | ----------- |",
    ]
    
    # Handle dynamic sample size display
    if isinstance(num_samples, int):
        config_lines.extend([
            f"| **Text Output Sample Size** | {num_samples} per task | Number of samples for generation analysis |",
            f"| **Sample Selection** | Random | Randomly selected from test sets |",
            f"| **Matching Method** | Exact String | Case-sensitive exact matching |",
            "",
            "**📝 Notes**:",
            f"- **Sample size impact**: Current sample size provides statistical reliability",
        ])
        
        # Add confidence interval information for known sample sizes
        if num_samples >= 30:
            margin_error = round(1.96 * 0.5 / (num_samples**0.5) * 100, 1)
            config_lines.append(f"- **Confidence level**: {num_samples} samples provide ~{margin_error}% margin of error at 95% confidence")
        else:
            config_lines.append(f"- **Confidence level**: {num_samples} samples provide limited statistical confidence")
            
        config_lines.append("- **Recommendation**: Consider 100+ samples for production evaluation")
        
    else:
        # Handle unknown or variable sample sizes
        config_lines.extend([
            f"| **Text Output Sample Size** | {num_samples} | Number of samples for generation analysis |",
            f"| **Sample Selection** | Random | Randomly selected from test sets |",
            f"| **Matching Method** | Exact String | Case-sensitive exact matching |",
            "",
            "**📝 Notes**:",
            "- **Sample size impact**: Statistical reliability depends on actual sample size used",
            "- **Recommendation**: Verify sample sizes meet your evaluation requirements",
        ])
    
    if sample_size_note:
        config_lines.extend([
            "",
            f"**📊 Detection Results**: {sample_size_note}",
        ])
    
    config_lines.append("")
    
    return config_lines

def extract_model_info(config: Dict[str, Any]) -> Dict[str, Any]:
    """Extract comprehensive model information from config."""
    model_info = {
        "name": "Unknown Model",
        "parameters": "Not specified",
        "architecture": "Not specified", 
        "context_length": "Not specified",
        "backend": "Unknown",
        "quantization": "None",
        "device_mapping": "Single GPU"
    }
    
    # Extract model name and details
    if 'model_args' in config:
        model_args = config['model_args']
        if 'pretrained=' in model_args:
            model_info["name"] = model_args.replace('pretrained=', '').split(',')[0]
        
        # Check for device mapping
        if 'device_map=auto' in model_args:
            model_info["device_mapping"] = "Multi-GPU (Auto)"
        
        # Check for quantization
        if 'load_in_4bit' in model_args or '4bit' in model_args:
            model_info["quantization"] = "4-bit"
        elif 'load_in_8bit' in model_args or '8bit' in model_args:
            model_info["quantization"] = "8-bit"
    
    # Extract backend information
    if 'model' in config:
        model_info["backend"] = config['model'].upper()
    
    # Try to infer model size from name
    name_lower = model_info["name"].lower()
    if "7b" in name_lower:
        model_info["parameters"] = "~7 billion"
    elif "13b" in name_lower:
        model_info["parameters"] = "~13 billion"
    elif "70b" in name_lower:
        model_info["parameters"] = "~70 billion"
    elif "3b" in name_lower:
        model_info["parameters"] = "~3 billion"
    elif "1b" in name_lower:
        model_info["parameters"] = "~1 billion"
    
    # Try to infer architecture from model name
    if "llama" in name_lower:
        model_info["architecture"] = "Llama (Transformer)"
    elif "mistral" in name_lower:
        model_info["architecture"] = "Mistral (Transformer)"
    elif "gemma" in name_lower:
        model_info["architecture"] = "Gemma (Transformer)"
    elif "gpt" in name_lower:
        model_info["architecture"] = "GPT (Transformer)"
    
    return model_info

def generate_executive_summary(results_data: Dict[str, Any]) -> List[str]:
    """Generate an executive summary section."""
    summary = [
        "## 📋 Executive Summary",
        ""
    ]
    
    # Calculate overall performance
    metrics = results_data.get('results', {})
    if metrics:
        # Get primary accuracy scores
        scores = []
        for task, task_metrics in metrics.items():
            for metric_name, value in task_metrics.items():
                if 'acc' in metric_name.lower() and 'stderr' not in metric_name.lower():
                    if isinstance(value, (int, float)):
                        scores.append(value * 100)  # Convert to percentage
        
        if scores:
            avg_score = np.mean(scores)
            max_score = np.max(scores)
            min_score = np.min(scores)
            
            # Create performance assessment
            performance_badge = create_performance_badge(avg_score)
            
            summary.extend([
                f"🎯 **Overall Performance:** {performance_badge}",
                f"📊 **Average Score:** {avg_score:.1f}%",
                f"📈 **Best Performance:** {max_score:.1f}%",
                f"📉 **Lowest Performance:** {min_score:.1f}%",
                f"📏 **Score Range:** {max_score - min_score:.1f} points",
                ""
            ])
            
            # Add performance insights
            summary.append("### 🔍 Key Insights")
            
            if avg_score >= 80:
                summary.append("✅ **Strong overall performance** across evaluated tasks")
            elif avg_score >= 60:
                summary.append("⚡ **Moderate performance** with room for improvement")
            else:
                summary.append("🔧 **Performance below expectations** - consider fine-tuning or model selection")
            
            if max_score - min_score > 30:
                summary.append("📊 **High variance** in task performance - model shows task-specific strengths")
            else:
                summary.append("📊 **Consistent performance** across different task types")
            
            summary.append("")
    
    return summary

def format_sample_display(sample: Dict[str, Any], task_name: str, sample_num: int) -> List[str]:
    """Format a sample display with enhanced readability."""
    display = [f"### 📝 Sample {sample_num}", ""]
    
    # Extract and format question
    question = None
    if 'doc' in sample and isinstance(sample['doc'], dict):
        doc = sample['doc']
        for key in ['question', 'prompt', 'input', 'problem']:
            if key in doc:
                question = doc[key]
                break
    
    if question:
        # Clean and format the question
        if len(question) > 800:
            question = question[:800] + "..."
        
        display.extend([
            "#### ❓ Question",
            "```text",
            question,
            "```",
            ""
        ])
    
    # Extract and format choices
    choices = None
    if 'doc' in sample and isinstance(sample['doc'], dict):
        doc = sample['doc']
        if 'choices' in doc:
            choices = doc['choices']
        elif 'options' in doc:
            choices = doc['options']
    
    if choices:
        display.append("#### 📋 Answer Choices")
        if isinstance(choices, dict) and 'text' in choices and 'label' in choices:
            for i, (text, label) in enumerate(zip(choices['text'], choices['label'])):
                display.append(f"**{label}.** {text}")
        elif isinstance(choices, list):
            for i, choice in enumerate(choices):
                label = chr(65 + i)  # A, B, C, D...
                display.append(f"**{label}.** {choice}")
        display.append("")
    
    # Extract ground truth
    ground_truth = None
    if 'doc' in sample and isinstance(sample['doc'], dict):
        doc = sample['doc']
        for key in ['target', 'answer', 'answerKey']:
            if key in doc:
                ground_truth = doc[key]
                break
    elif 'target' in sample:
        ground_truth = sample['target']
    
    if ground_truth:
        display.extend([
            "#### ✅ Expected Answer",
            f"**{ground_truth}**",
            ""
        ])
    
    # ✅ NEW: Display enhanced model output if available (from enhanced evaluator)
    if 'model_output' in sample:
        model_output = sample['model_output']
        
        # Get correctness status from enhanced evaluation
        is_correct = False
        if 'output_matches_target' in sample:
            is_correct = sample['output_matches_target']
        
        status_icon = "✅" if is_correct else "❌"
        status_text = "Correct" if is_correct else "Incorrect"
        
        display.extend([
            f"#### 🤖 Model Output ({status_icon} {status_text})",
            "",
            f"**Response:** `{model_output}`",
            ""
        ])
        
        # Add analysis if we have both target and model output
        if ground_truth and 'output_matches_target' in sample:
            if is_correct:
                display.extend([
                    "💬 **Analysis:** The model correctly identified the answer.",
                    ""
                ])
            else:
                display.extend([
                    f"💬 **Analysis:** The model responded with `{model_output}` but the correct answer is `{ground_truth}`.",
                    ""
                ])
    
    # Extract and format raw model response (only if we don't have enhanced model_output)
    elif 'filtered_resps' in sample and sample['filtered_resps']:
        response = sample['filtered_resps'][0]
        is_correct = False
        
        # Check correctness
        if 'exact_match' in sample:
            is_correct = sample['exact_match'] == 1.0
        
        status_icon = "✅" if is_correct else "❌"
        status_text = "Correct" if is_correct else "Incorrect"
        
        display.extend([
            f"#### 🤖 Model Response ({status_icon} {status_text})",
            f"**{response}**",
            ""
        ])
    elif 'resps' in sample and sample['resps']:
        response = sample['resps'][0]
        
        display.extend([
            f"#### 🤖 Model Response",
            f"**{response}**",
            ""
        ])
    
    display.append("---")
    display.append("")
    
    return display

def format_task_sample_display(sample: Dict[str, Any], task_name: str, sample_num: int) -> List[str]:
    """Format a sample display for task-specific reports with the user's requested format."""
    display = []
    
    # Extract question/prompt
    question = None
    if 'doc' in sample and isinstance(sample['doc'], dict):
        doc = sample['doc']
        # Try different field names for the question
        for key in ['input', 'question', 'prompt', 'problem', 'narrative']:
            if key in doc:
                question = doc[key]
                break
    
    # Format the question section
    if question:
        display.extend([
            f"📝 Sample {sample_num}",
            "❓ Question"
        ])
        
        # Clean up the question - handle multiple choice formatting
        formatted_question = question.strip()
        
        # For multiple choice questions, format the options nicely
        if 'doc' in sample and isinstance(sample['doc'], dict):
            doc = sample['doc']
            if 'options' in doc and isinstance(doc['options'], list):
                # Add the question text
                display.append(formatted_question.split('Options:')[0].strip())
                display.append("Options:")
                # Add formatted options
                for i, option in enumerate(doc['options']):
                    display.append(f"\t•\t{option}")
            else:
                display.append(formatted_question)
        else:
            display.append(formatted_question)
        
        display.append("")
    
    # Extract expected answer
    ground_truth = None
    if 'target' in sample:
        ground_truth = sample['target']
    elif 'doc' in sample and isinstance(sample['doc'], dict):
        doc = sample['doc']
        for key in ['target', 'answer', 'answerKey']:
            if key in doc:
                ground_truth = doc[key]
                break
    
    if ground_truth:
        display.extend([
            "✅ Expected Answer",
            f"{ground_truth}",
            ""
        ])
    
    # Extract model output and correctness
    model_output = None
    is_correct = False
    
    if 'model_output' in sample:
        model_output = sample['model_output']
        if 'output_matches_target' in sample:
            is_correct = sample['output_matches_target']
    
    if model_output is not None:
        status_icon = "✅" if is_correct else "❌"
        status_text = "Correct" if is_correct else "Incorrect"
        
        display.extend([
            f"🤖 Model Output ({status_icon} {status_text})",
            f"Response: {model_output}",
            ""
        ])
        
        # Add analysis
        if ground_truth:
            if is_correct:
                display.extend([
                    "💬 Analysis:",
                    "The model correctly identified the answer.",
                    ""
                ])
            else:
                display.extend([
                    "💬 Analysis:",
                    f"The model responded with \"{model_output}\" but the correct answer is \"{ground_truth}\".",
                    ""
                ])
    
    display.append("⸻")
    display.append("")
    
    return display

def generate_task_specific_reports(results_data: Dict[str, Any], base_output_dir: str) -> List[str]:
    """Generate separate reports for each evaluation task."""
    
    if 'samples' not in results_data:
        print("❌ No samples found in results data. Cannot generate task-specific reports.")
        return []
    
    # Extract model information
    config = results_data.get('config', {})
    model_info = extract_model_info(config)
    
    # Create task-specific reports directory
    task_reports_dir = os.path.join(base_output_dir, "task_reports")
    os.makedirs(task_reports_dir, exist_ok=True)
    
    generated_reports = []
    
    for task_name, samples_list in results_data['samples'].items():
        if not isinstance(samples_list, list) or len(samples_list) == 0:
            continue
        
        # Create clean task name for display
        display_task_name = task_name.replace('leaderboard_', '').replace('_', ' ').title()
        
        # Start building the task report
        report = [
            f"# 📚 Task Report: {display_task_name}",
            "",
            f"**Model:** {model_info['name']}",
            f"**Generated:** {(datetime.now(CET) if CET else datetime.now()).strftime('%B %d, %Y at %H:%M:%S')}",
            f"**Total Samples:** {len(samples_list)}",
            "",
            "---",
            ""
        ]
        
        # Add task performance summary
        correct_count = 0
        total_count = len(samples_list)
        
        for sample in samples_list:
            if isinstance(sample, dict) and 'output_matches_target' in sample:
                if sample['output_matches_target']:
                    correct_count += 1
        
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
        performance_badge = create_performance_badge(accuracy)
        
        report.extend([
            f"## 📊 Task Performance Summary",
            "",
            f"| Metric | Value |",
            f"| ------ | ----- |",
            f"| **Total Samples** | {total_count} |",
            f"| **Correct Responses** | {correct_count} |",
            f"| **Accuracy** | {accuracy:.1f}% |",
            f"| **Performance** | {performance_badge} |",
            "",
            "---",
            ""
        ])
        
        # Add all samples for this task
        for i, sample in enumerate(samples_list, 1):
            if isinstance(sample, dict):
                formatted_sample = format_task_sample_display(sample, task_name, i)
                report.extend(formatted_sample)
        
        # Add footer
        report.extend([
            "---",
            "",
            f"**Task:** {display_task_name}",
            f"**Model:** {model_info['name']}",
            f"**Generated by:** LLM Evaluation Framework",
            f"**Timestamp:** {datetime.now().isoformat()}"
        ])
        
        # Write the task report
        safe_task_name = re.sub(r'[^\w\-_]', '_', task_name.lower())
        task_report_path = os.path.join(task_reports_dir, f"{safe_task_name}_report.md")
        
        try:
            with open(task_report_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report))
            
            print(f"✅ Task report generated: {task_report_path}")
            generated_reports.append(task_report_path)
            
        except Exception as e:
            print(f"❌ Error generating task report for {task_name}: {e}")
    
    return generated_reports

def generate_professional_report(results_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """Generate a professional, visually appealing evaluation report."""
    
    # Determine actual sample size used early in the function - improved detection
    actual_sample_size = 0
    sample_sizes = []
    
    # Method 1: Check samples section (most reliable)
    if results_data.get('samples'):
        for task_name, samples_list in results_data['samples'].items():
            if isinstance(samples_list, list) and len(samples_list) > 0:
                sample_sizes.append(len(samples_list))
    
    # Method 2: Check config for limit parameter
    if not sample_sizes and results_data.get('config'):
        config = results_data['config']
        # Check for various ways the limit might be stored in config
        if 'limit' in config:
            try:
                sample_sizes.append(int(config['limit']))
            except (ValueError, TypeError):
                pass
        
        # Check in model_args string for limit parameter
        model_args = config.get('model_args', '')
        if 'limit=' in str(model_args):
            try:
                limit_part = str(model_args).split('limit=')[1].split(',')[0].split(' ')[0]
                sample_sizes.append(int(limit_part))
            except (ValueError, IndexError):
                pass
    
    # Method 3: Try to infer from results structure
    if not sample_sizes and results_data.get('results'):
        # Check if any task results have sample count information
        for task_name, task_results in results_data['results'].items():
            if isinstance(task_results, dict):
                # Some tasks might have 'n-samples' or similar fields
                for key, value in task_results.items():
                    if 'sample' in key.lower() and isinstance(value, (int, float)):
                        sample_sizes.append(int(value))
                        break
    
    # Determine the actual sample size
    if sample_sizes:
        # Use the most common sample size, or the first one if all are the same
        from collections import Counter
        sample_counts = Counter(sample_sizes)
        actual_sample_size = sample_counts.most_common(1)[0][0]
        
        # Check if there's variation in sample sizes across tasks
        if len(set(sample_sizes)) > 1:
            min_samples = min(sample_sizes)
            max_samples = max(sample_sizes)
            sample_size_note = f"Sample sizes vary from {min_samples} to {max_samples} across tasks"
        else:
            sample_size_note = f"Consistent {actual_sample_size} samples per task"
    else:
        # Fallback: try to detect from common evaluation configurations
        actual_sample_size = "unknown"
        sample_size_note = "Sample size could not be determined from results data"
    
    # Extract model information
    config = results_data.get('config', {})
    model_info = extract_model_info(config)
    
    # Start building the report
    report = [
        f"# 🚀 LLM Evaluation Report",
        f"## {model_info['name']}",
        "",
        f"📅 **Generated:** {(datetime.now(CET) if CET else datetime.now()).strftime('%B %d, %Y at %H:%M:%S')}",
        f"🏷️ **Report ID:** {datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "",
        "---",
        ""
    ]
    
    # Add executive summary
    report.extend(generate_executive_summary(results_data))
    
    # Model Information Section
    report.extend([
        "## 🔧 Model Configuration",
        "",
        "| Specification | Details |",
        "| ------------- | ------- |",
        f"| **Model Name** | `{model_info['name']}` |",
        f"| **Parameters** | {model_info['parameters']} |",
        f"| **Architecture** | {model_info['architecture']} |",
        f"| **Backend** | {model_info['backend']} |",
        f"| **Quantization** | {model_info['quantization']} |",
        f"| **Device Setup** | {model_info['device_mapping']} |",
        ""
    ])
    
    # Add generation parameters if available
    if 'generation_args' in config:
        gen_args = config['generation_args']
        report.extend([
            "### ⚙️ Generation Parameters",
            "",
            "| Parameter | Value |",
            "| --------- | ----- |"
        ])
        
        for key, value in gen_args.items():
            if isinstance(value, (int, float, str, bool)):
                report.append(f"| {key} | `{value}` |")
        report.append("")
    
    # Performance Overview Section
    metrics = results_data.get('results', {})
    if metrics:
        report.extend([
            "## 📊 Performance Overview",
            ""
        ])
        
        # Create performance table
        performance_data = {}
        detailed_table = [
            "| Task | Metric | Score | Performance |",
            "| ---- | ------ | ----- | ----------- |"
        ]
        
        for task_name, task_metrics in metrics.items():
            for metric_name, value in task_metrics.items():
                if isinstance(value, (int, float)) and 'stderr' not in metric_name:
                    percentage = value * 100 if value <= 1.0 else value
                    performance_data[f"{task_name}_{metric_name}"] = percentage
                    
                    # Create progress bar and badge
                    progress_bar = create_progress_bar(percentage)
                    badge = create_performance_badge(percentage)
                    
                    detailed_table.append(f"| {task_name} | {metric_name} | {percentage:.1f}% | {badge} |")
        
        report.extend(detailed_table)
        report.append("")
        
        # Add visual performance chart if we have data
        if performance_data:
            # Group by task for cleaner visualization
            task_avg_scores = {}
            for key, score in performance_data.items():
                task = key.split('_')[0]
                if task not in task_avg_scores:
                    task_avg_scores[task] = []
                task_avg_scores[task].append(score)
            
            # Calculate average scores per task
            task_averages = {task: np.mean(scores) for task, scores in task_avg_scores.items()}
            
            if task_averages:
                chart = create_comparison_chart(task_averages, "Task Performance Comparison")
                report.append(chart)
        
        # ✅ NEW: Add detailed metrics table
        detailed_metrics_table = create_detailed_metrics_table(metrics)
        if detailed_metrics_table:
            # Add methodology explanation before the table
            methodology_lines = [
                "---",
                "",
                "### 🔬 **Evaluation Methodology Note**",
                "",
                "The following **Detailed Results** use the standard LM Evaluation Harness methodology:",
                "- **📊 Loglikelihood-based scoring** for multiple choice questions",
                "- **🎯 Limited sample evaluation** (same sample size as text output analysis)",
                "- **⚖️ Token probability comparisons** for answer selection",
                "- **📏 Standardized prompting** with task-specific few-shot examples",
                ""
            ]
            
            # Add sample size information dynamically
            if actual_sample_size != "unknown":
                methodology_lines.append(f"**📝 Sample Size**: {sample_size_note}")
            else:
                methodology_lines.append(f"**📝 Sample Size**: {sample_size_note}")
            
            methodology_lines.extend(["", ""])
            
            report.extend(methodology_lines)
            report.extend(detailed_metrics_table)
            report.append("")
    
    # ✅ NEW: Model Output Analysis section
    if 'samples' in results_data:
        report.extend([
            "## 🔍 Model Output Analysis",
            "",
            "### 📋 **Methodology Overview**",
            "",
            "This section analyzes **actual text generation performance** by examining decoded model outputs:",
            "",
            "**🎯 Approach**:",
            "- **Text Generation**: Model generates complete responses (not just probabilities)",  
            "- **String Matching**: Exact comparison between generated text and target answers",
            f"- **Sample Size**: {sample_size_note}",
            "- **Real-World Insight**: Shows how the model performs in actual text generation scenarios",
            "",
            "**⚖️ Comparison with Benchmark Metrics**:",
            "- **Benchmark scores** use loglikelihood comparison (optimal token probability)",
            "- **Text outputs** use actual generation + exact string matching",
            "- **Same sample limitations** ensure fair comparison between methodologies",
            "- **Performance gaps** indicate generation vs. reasoning capability differences",
            ""
        ])
        
        # Add configuration section
        config_section = create_evaluation_config_section(actual_sample_size, sample_size_note)
        report.extend(config_section)
        
        # Collect enhanced statistics about model outputs
        total_samples = 0
        samples_with_outputs = 0
        correct_outputs = 0
        incorrect_outputs = 0
        task_stats = {}
        
        for task_name, samples_list in results_data.get('samples', {}).items():
            task_correct = 0
            task_total = 0
            task_with_outputs = 0
            
            for sample in samples_list:
                if isinstance(sample, dict):
                    total_samples += 1
                    task_total += 1
                    
                    if 'model_output' in sample:
                        samples_with_outputs += 1
                        task_with_outputs += 1
                        
                        if 'output_matches_target' in sample:
                            if sample['output_matches_target']:
                                correct_outputs += 1
                                task_correct += 1
                            else:
                                incorrect_outputs += 1
            
            if task_total > 0:
                task_accuracy = (task_correct / task_with_outputs * 100) if task_with_outputs > 0 else 0
                task_stats[task_name] = {
                    'total': task_total,
                    'with_outputs': task_with_outputs,
                    'correct': task_correct,
                    'accuracy': task_accuracy
                }
        
        # Overall statistics with visual elements
        overall_accuracy = (correct_outputs / samples_with_outputs * 100) if samples_with_outputs > 0 else 0
        coverage = (samples_with_outputs / total_samples * 100) if total_samples > 0 else 0
        
        # Create enhanced summary table with progress bars
        report.extend([
            "### 📊 Text Output Summary",
            "",
            "| Metric | Value | Visual |",
            "| ------ | ----- | ------ |",
            f"| **Total Samples** | {total_samples} | 📝 |",
            f"| **With Text Outputs** | {samples_with_outputs} ({coverage:.1f}%) | {create_progress_bar(coverage)} |",
            f"| **Correct Responses** | {correct_outputs} | ✅ |",
            f"| **Incorrect Responses** | {incorrect_outputs} | ❌ |",
            f"| **Overall Accuracy** | {overall_accuracy:.1f}% | {create_progress_bar(overall_accuracy)} |",
            ""
        ])
        
        # Add performance badge for overall accuracy
        accuracy_badge = create_performance_badge(overall_accuracy)
        report.extend([
            f"🎯 **Text Output Performance:** {accuracy_badge}",
            ""
        ])
        
        # Add performance comparison if we have both benchmark and text output data
        if 'results' in results_data and len(task_stats) > 0:
            report.extend([
                "### ⚖️ **Methodology Comparison**",
                "",
                "Comparing **loglikelihood-based benchmark scores** vs **text generation performance**:",
                ""
            ])
            
            comparison_table = [
                "| Task | Benchmark Score | Text Generation | Gap | Analysis |",
                "| ---- | --------------- | --------------- | --- | -------- |"
            ]
            
            # Compare scores where both are available
            for task_name, text_stats in task_stats.items():
                if text_stats['total'] > 0:
                    text_accuracy = (text_stats['correct'] / text_stats['total']) * 100
                    
                    # Try to find corresponding benchmark score
                    benchmark_score = None
                    for bench_task, bench_metrics in results_data.get('results', {}).items():
                        if task_name.replace('leaderboard_', '') in bench_task or bench_task in task_name:
                            for metric_name, value in bench_metrics.items():
                                if isinstance(value, (int, float)) and 'stderr' not in metric_name:
                                    benchmark_score = value * 100 if value <= 1.0 else value
                                    break
                            if benchmark_score is not None:
                                break
                    
                    if benchmark_score is not None:
                        gap = benchmark_score - text_accuracy
                        
                        # Analyze the gap
                        if gap > 15:
                            analysis = "🔴 Large gap - generation challenges"
                        elif gap > 5:
                            analysis = "🟡 Moderate gap - formatting issues possible"
                        elif gap < -5:
                            analysis = "🟢 Text generation outperforms - possible chance"
                        else:
                            analysis = "✅ Consistent performance"
                        
                        # Shorten task name for display
                        display_name = task_name.replace('leaderboard_', '').replace('_', ' ').title()
                        if len(display_name) > 20:
                            display_name = display_name[:17] + "..."
                        
                        comparison_table.append(
                            f"| {display_name} | {benchmark_score:.1f}% | {text_accuracy:.1f}% | {gap:+.1f}% | {analysis} |"
                        )
            
            if len(comparison_table) > 2:  # We have actual comparisons
                report.extend(comparison_table)
                report.extend([
                    "",
                    "**🔍 Key Insights**:",
                    "- **Positive gaps**: Benchmark (loglikelihood) scores higher than text generation",
                    "- **Negative gaps**: Text generation surprisingly outperforms benchmark",
                    "- **Large gaps**: Indicate model struggles with consistent text formatting",
                    "- **Small gaps**: Show good alignment between reasoning and generation abilities",
                    ""
                ])
            else:
                report.append("*No matching benchmark tasks found for comparison.*")
                report.append("")

        # Per-task breakdown with enhanced visualization
        if len(task_stats) > 1:
            per_task_note = ""
            if isinstance(actual_sample_size, int):
                per_task_note = f"*Based on {actual_sample_size} samples per task - results may vary with larger sample sizes*"
            else:
                per_task_note = f"*Based on {sample_size_note.lower()} - statistical reliability may vary*"
                
            report.extend([
                "### 📋 Per-Task Text Output Performance",
                "",
                per_task_note,
                "",
                "| Task | Samples | Outputs | Correct | Accuracy | Performance |",
                "| ---- | ------- | ------- | ------- | -------- | ----------- |"
            ])
            
            for task_name, stats in task_stats.items():
                # Shorten task names for better readability
                display_name = task_name.replace('leaderboard_', '').replace('_', ' ').title()[:25]
                badge = create_performance_badge(stats['accuracy'])
                progress = create_progress_bar(stats['accuracy'])
                
                report.append(
                    f"| {display_name} | {stats['total']} | {stats['with_outputs']} | {stats['correct']} | {stats['accuracy']:.1f}% | {badge} |"
                )
            
            report.append("")
            
            # Create a visual chart for task accuracy
            task_accuracy_data = {
                task_name.replace('leaderboard_', '').replace('_', ' ')[:15]: stats['accuracy'] 
                for task_name, stats in task_stats.items() 
                if stats['with_outputs'] > 0
            }
            if task_accuracy_data:
                chart = create_comparison_chart(task_accuracy_data, "Text Output Accuracy by Task")
                report.append(chart)

    # Recommendations Section
    if metrics:
        report.extend([
            "## 💡 Recommendations",
            ""
        ])
        
        # Calculate overall average for recommendations
        all_scores = []
        for task_metrics in metrics.values():
            for metric_name, value in task_metrics.items():
                if isinstance(value, (int, float)) and 'stderr' not in metric_name:
                    percentage = value * 100 if value <= 1.0 else value
                    all_scores.append(percentage)
        
        if all_scores:
            avg_performance = np.mean(all_scores)
            
            # Add evaluation methodology recommendations
            report.extend([
                "",
                "### 🔬 **Evaluation Methodology Insights**",
                "",
                "**📊 Understanding Score Differences**:",
                "- **Loglikelihood scores** measure token probability optimization (what the model 'knows')",
                "- **Text generation scores** measure actual output quality (what the model 'produces')",
                f"- **Sample consistency** {sample_size_note.lower()} ensures fair comparison",
                "",
                "**🎯 Optimization Recommendations**:",
                ""
            ])
            
            if avg_performance < 50:
                report.extend([
                    "**🔴 Low Performance (< 50%)**:",
                    "- Consider fine-tuning on task-specific datasets",
                    "- Improve prompt engineering and few-shot examples",
                    "- Evaluate if model size/capability is sufficient for these tasks",
                    "- Check if quantization significantly impacts performance"
                ])
            elif avg_performance < 75:
                report.extend([
                    "**🟡 Moderate Performance (50-75%)**:",
                    "- Focus on prompt optimization and instruction clarity",
                    "- Consider task-specific fine-tuning for critical applications",
                    "- Analyze per-task performance to identify strengths and weaknesses",
                    "- Optimize generation parameters (temperature, top_p, etc.)"
                ])
            else:
                report.extend([
                    "**🟢 Good Performance (> 75%)**:",
                    "- Model shows strong capability across evaluation methods",
                    "- Fine-tune generation parameters for optimal deployment",
                    "- Consider this model suitable for production use in these domains",
                    "- Monitor performance consistency across different input distributions"
                ])
                
            # Add general methodology recommendations
            evaluation_recommendations = [
                "",
                "**📈 For More Reliable Evaluation**:",
            ]
            
            if isinstance(actual_sample_size, int):
                if actual_sample_size < 50:
                    evaluation_recommendations.append(f"- Increase sample size from {actual_sample_size} to 50+ per task for more stable estimates")
                elif actual_sample_size < 100:
                    evaluation_recommendations.append(f"- Consider increasing sample size from {actual_sample_size} to 100+ per task for production-grade estimates")
                else:
                    evaluation_recommendations.append(f"- Current sample size ({actual_sample_size}) provides good statistical reliability")
            else:
                evaluation_recommendations.append("- Verify and optimize sample sizes for more reliable evaluation")
            
            evaluation_recommendations.extend([
                "- Use multiple random seeds to assess variance across different sample sets",
                "- Compare both loglikelihood and generation approaches for comprehensive assessment",
                "- Consider domain-specific evaluation metrics beyond exact string matching"
            ])
            
            report.extend(evaluation_recommendations)
    
    # Sample Analysis Section
    if 'samples' in results_data:
        report.extend([
            "## 📖 Sample Analysis",
            "",
            "*Detailed examples showing model performance on specific questions.*",
            ""
        ])
        
        sample_count = 0
        max_samples_per_task = 2
        
        for task_name, samples_list in results_data['samples'].items():
            if sample_count >= 6:  # Limit total samples in report
                break
                
            report.append(f"### 📚 {task_name.title()}")
            report.append("")
            
            task_samples_shown = 0
            for sample in samples_list:
                if task_samples_shown >= max_samples_per_task or sample_count >= 6:
                    break
                
                if sample and isinstance(sample, dict):
                    formatted_sample = format_sample_display(sample, task_name, task_samples_shown + 1)
                    report.extend(formatted_sample)
                    task_samples_shown += 1
                    sample_count += 1
    
    # Footer
    report.extend([
        "---",
        "",
        "## 📋 Report Information",
        "",
        f"**Generated by:** LLM Evaluation Framework v2.0",
        f"**Timestamp:** {datetime.now().isoformat()}",
        f"**Framework:** Professional Report Generator",
        "",
        "*This report provides a comprehensive analysis of model performance across various evaluation tasks.*",
        "*For technical details, refer to the accompanying JSON results file.*"
    ])
    
    # Determine output path
    if not output_path:
        reports_dir = get_reports_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_name_clean = re.sub(r'[^\w\-_]', '_', model_info['name'].split('/')[-1])
        output_path = os.path.join(reports_dir, f"professional_report_{model_name_clean}_{timestamp}.md")
    
    # Write the report
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"✅ Professional report generated: {output_path}")
        
        # Generate task-specific reports only if we're in the organized evaluation structure
        # (i.e., the path contains "evaluations/" and ends with "report.md")
        base_output_dir = os.path.dirname(output_path)
        if "evaluations/" in output_path and output_path.endswith("report.md"):
            task_reports = generate_task_specific_reports(results_data, base_output_dir)
            
            if task_reports:
                print(f"✅ Generated {len(task_reports)} task-specific reports")
        
        return output_path
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return ""

def generate_professional_report_from_json(json_path: str, output_path: Optional[str] = None) -> str:
    """Generate a professional report from a JSON results file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            results_data = json.load(f)
        
        return generate_professional_report(results_data, output_path)
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return ""

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python professional_report_generator.py <json_results_file> [output_path]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = generate_professional_report_from_json(json_file, output_file)
    if result:
        print(f"Report generated successfully: {result}")
    else:
        print("Failed to generate report")
        sys.exit(1) 