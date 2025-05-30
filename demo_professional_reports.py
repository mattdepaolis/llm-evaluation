#!/usr/bin/env python3
"""
Demonstration script for Professional Report Generation
Shows how to use the enhanced reporting features of the LLM Evaluation Framework.
"""

import os
import sys
from llm_eval.reporting.professional_report_generator import generate_professional_report_from_json

def demo_professional_reports():
    """Demonstrate the professional report generation features."""
    
    print("🚀 LLM Evaluation Framework - Professional Reports Demo")
    print("=" * 60)
    
    # Check for existing results files
    results_dir = "results"
    if not os.path.exists(results_dir):
        print("❌ No results directory found. Please run an evaluation first.")
        print("\nExample command:")
        print("python llm_eval_cli.py --model hf --model_name microsoft/DialoGPT-medium --tasks arc_easy --num_samples 5")
        return
    
    # Find JSON results files
    json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    
    if not json_files:
        print("❌ No JSON results files found. Please run an evaluation first.")
        print("\nExample command:")
        print("python llm_eval_cli.py --model hf --model_name microsoft/DialoGPT-medium --tasks arc_easy --num_samples 5")
        return
    
    print(f"📁 Found {len(json_files)} results file(s)")
    
    # Use the most recent file
    latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(results_dir, x)))
    json_path = os.path.join(results_dir, latest_file)
    
    print(f"📊 Processing: {latest_file}")
    print()
    
    # Generate professional report
    print("🎨 Generating Professional Report...")
    try:
        report_path = generate_professional_report_from_json(json_path)
        
        if report_path:
            print(f"✅ Professional report generated successfully!")
            print(f"📄 Report location: {report_path}")
            print()
            
            # Show report features
            print("🌟 Professional Report Features:")
            print("  📋 Executive Summary with performance insights")
            print("  🔧 Detailed model configuration")
            print("  📊 Visual performance indicators and progress bars")
            print("  💡 Actionable recommendations")
            print("  📖 Enhanced sample analysis")
            print("  🎯 Color-coded performance badges")
            print()
            
            # Show how to view the report
            print("👀 To view the report:")
            print(f"  cat '{report_path}'")
            print("  # or open in your favorite markdown viewer")
            print()
            
            # Show comparison with standard reports
            print("🔄 Report Format Comparison:")
            print("  Professional Format (Default):")
            print("    ✨ Modern visual design with emojis")
            print("    📈 Performance charts and progress bars")
            print("    🎯 Executive summary and insights")
            print("    💡 Actionable recommendations")
            print()
            print("  Standard Format:")
            print("    📝 Traditional markdown tables")
            print("    🔢 Basic metrics display")
            print("    ⚡ Lightweight and fast")
            print()
            
            # Show CLI usage examples
            print("🚀 CLI Usage Examples:")
            print()
            print("  # Professional format (default)")
            print("  python llm_eval_cli.py \\")
            print("    --model hf \\")
            print("    --model_name mistralai/Mistral-7B-v0.1 \\")
            print("    --tasks arc_easy \\")
            print("    --report_format professional")
            print()
            print("  # Standard format")
            print("  python llm_eval_cli.py \\")
            print("    --model hf \\")
            print("    --model_name mistralai/Mistral-7B-v0.1 \\")
            print("    --tasks arc_easy \\")
            print("    --report_format standard")
            print()
            
        else:
            print("❌ Failed to generate professional report")
            
    except Exception as e:
        print(f"❌ Error generating professional report: {e}")

def show_report_features():
    """Show the key features of professional reports."""
    
    print("🎨 Professional Report Features Overview")
    print("=" * 50)
    print()
    
    features = [
        ("📋 Executive Summary", "Overall performance assessment with key insights and recommendations"),
        ("🔧 Model Configuration", "Comprehensive technical specifications including architecture and setup"),
        ("📊 Performance Overview", "Visual performance indicators with color-coded badges and progress bars"),
        ("💡 Smart Recommendations", "Actionable insights based on performance analysis"),
        ("📖 Enhanced Sample Analysis", "Beautifully formatted questions, choices, and model responses"),
        ("🎯 Performance Badges", "🟢 Excellent (70%+), 🟡 Good (50-70%), 🔴 Needs Improvement (<50%)"),
        ("📈 Visual Charts", "ASCII-based performance comparison charts"),
        ("🏷️ Professional Formatting", "Modern design with emojis, sections, and clear hierarchy")
    ]
    
    for feature, description in features:
        print(f"{feature}")
        print(f"  {description}")
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--features":
        show_report_features()
    else:
        demo_professional_reports() 