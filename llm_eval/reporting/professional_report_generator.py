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
    
    if ground_truth:
        display.extend([
            "#### ✅ Correct Answer",
            f"**{ground_truth}**",
            ""
        ])
    
    # Extract and format model response
    response = None
    is_correct = False
    
    if 'filtered_resps' in sample and sample['filtered_resps']:
        response = sample['filtered_resps'][0]
    elif 'resps' in sample and sample['resps']:
        response = sample['resps'][0]
    
    # Check correctness
    if 'exact_match' in sample:
        is_correct = sample['exact_match'] == 1.0
    
    if response is not None:
        status_icon = "✅" if is_correct else "❌"
        status_text = "Correct" if is_correct else "Incorrect"
        
        display.extend([
            f"#### 🤖 Model Response ({status_icon} {status_text})",
            f"**{response}**",
            ""
        ])
    
    display.append("---")
    display.append("")
    
    return display

def generate_professional_report(results_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """Generate a professional, visually appealing evaluation report."""
    
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
            
            if avg_performance >= 80:
                report.extend([
                    "🎉 **Excellent Performance!**",
                    "- Model shows strong capabilities across evaluated tasks",
                    "- Consider deploying for production use cases",
                    "- Explore more challenging benchmarks for further validation",
                    ""
                ])
            elif avg_performance >= 60:
                report.extend([
                    "⚡ **Good Performance with Opportunities**",
                    "- Model performs well but has room for improvement",
                    "- Consider fine-tuning on specific domains if needed",
                    "- Monitor performance on real-world tasks",
                    ""
                ])
            else:
                report.extend([
                    "🔧 **Performance Enhancement Needed**",
                    "- Current performance below optimal levels",
                    "- Consider larger model variants or fine-tuning",
                    "- Evaluate prompt engineering strategies",
                    "- Test with different generation parameters",
                    ""
                ])
    
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