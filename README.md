# LLM Evaluation Framework

A comprehensive framework for evaluating Large Language Models (LLMs) using the `lm-evaluation-harness` library with enhanced features for multi-GPU support, professional reporting, and streamlined workflows.

## Features

- **Multi-GPU Support**: Automatic device mapping for large models across multiple GPUs
- **Professional Reports**: Enhanced visual reports with performance insights and recommendations
- **Multiple Backends**: Support for HuggingFace Transformers and vLLM
- **Quantization Support**: 4-bit and 8-bit quantization for memory efficiency
- **Comprehensive Task Coverage**: Support for leaderboard tasks and custom evaluations
- **Automated Workflows**: Streamlined evaluation pipelines with intelligent defaults

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd llm-evaluation

# Install dependencies
pip install -r requirements.txt

# Set up HuggingFace cache (recommended)
source setup_hf_cache.sh
```

## Quick Start

### Basic Evaluation
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name microsoft/DialoGPT-medium \
  --tasks arc_easy \
  --num_samples 10 \
  --batch_size 4
```

### Multi-GPU HF Evaluation (Auto Device Mapping)
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name mistralai/Mistral-7B-v0.1 \
  --tasks leaderboard_mmlu_pro,arc_easy \
  --additional_model_args "device_map=auto" \
  --device cuda \
  --batch_size 2
```

### Leaderboard Evaluation
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name mistralai/Mistral-7B-v0.1 \
  --leaderboard \
  --additional_model_args "device_map=auto" \
  --batch_size 2
```

## Professional Reports

The framework now includes **professional report generation** with enhanced visual design and comprehensive analysis:

### Report Features

- **📋 Executive Summary**: Overall performance assessment with key insights
- **🔧 Model Configuration**: Detailed technical specifications
- **📊 Performance Overview**: Visual performance indicators and progress bars
- **💡 Recommendations**: Actionable insights based on performance
- **📖 Sample Analysis**: Detailed examples with formatted questions and responses
- **🎯 Performance Badges**: Color-coded performance indicators (🟢 Excellent, 🟡 Good, 🔴 Needs Improvement)

### Report Format Options

Choose between two report formats:

#### Professional Format (Default)
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name microsoft/DialoGPT-medium \
  --tasks arc_easy \
  --report_format professional
```

Features:
- Modern visual design with emojis and progress bars
- Executive summary with performance insights
- Comprehensive model configuration details
- Visual performance charts and comparisons
- Actionable recommendations
- Enhanced sample formatting

#### Standard Format
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name microsoft/DialoGPT-medium \
  --tasks arc_easy \
  --report_format standard
```

Features:
- Traditional markdown format
- Basic performance tables
- Simple sample displays
- Lightweight and fast generation

### Report Generation

Reports are automatically generated in the `reports/` directory with timestamps:

- **Professional reports**: `professional_report_<model>_<timestamp>.md`
- **Standard reports**: `results_<model>_<timestamp>_report.md`

## Command Line Options

### Core Options
- `--model`: Model backend (`hf` or `vllm`)
- `--model_name`: Model identifier (e.g., `mistralai/Mistral-7B-v0.1`)
- `--tasks`: Tasks to evaluate (space or comma-separated)
- `--leaderboard`: Run full leaderboard evaluation suite
- `--report_format`: Report format (`professional` or `standard`)

### Model Configuration
- `--additional_model_args`: Additional model arguments (e.g., `"device_map=auto"`)
- `--quantize`: Enable quantization for HF models
- `--quantization_method`: Quantization method (`4bit`, `8bit`, etc.)
- `--dtype`: Data type for vLLM (`float16`, `bfloat16`, `float32`)

### Evaluation Settings
- `--num_samples`: Number of samples per task (`all` or number)
- `--batch_size`: Batch size (`auto` or number)
- `--num_fewshot`: Few-shot examples (0 for zero-shot)
- `--device`: Device specification (`cuda`, `cpu`, `cuda:0`)

### Multi-GPU Options
- `--tensor_parallel_size`: GPUs for vLLM tensor parallelism
- `--gpu_memory_utilization`: GPU memory usage (0.0-1.0)

## Multi-GPU Setup

### Automatic Device Mapping (HuggingFace)
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name mistralai/Mistral-7B-v0.1 \
  --additional_model_args "device_map=auto" \
  --tasks arc_easy
```

### Tensor Parallelism (vLLM)
```bash
python llm_eval_cli.py \
  --model vllm \
  --model_name mistralai/Mistral-7B-v0.1 \
  --tensor_parallel_size 2 \
  --tasks arc_easy
```

## Available Tasks

### Task Groups
- `LEADERBOARD`: Full leaderboard evaluation suite
- `BBH`: Big-Bench Hard tasks
- `GPQA`: Graduate-level science questions
- `MMLU_PRO`: Advanced MMLU tasks
- `MATH`: Mathematical reasoning
- `IFEVAL`: Instruction following

### Individual Tasks
Use `--list_tasks` to see all available tasks:
```bash
python llm_eval_cli.py --list_tasks
```

## Output Files

### Results
- **JSON Results**: `results/results_<model>_<timestamp>.json`
- **Normalized Scores**: Included in JSON with leaderboard-compatible scoring

### Reports
- **Professional Reports**: `reports/professional_report_<model>_<timestamp>.md`
- **Standard Reports**: `reports/results_<model>_<timestamp>_report.md`

## Performance Optimization

### Memory Management
- Use `device_map=auto` for automatic GPU distribution
- Enable quantization for large models: `--quantize --quantization_method 4bit`
- Adjust batch size based on available memory

### Speed Optimization
- Use vLLM backend for faster inference: `--model vllm`
- Increase batch size for better throughput: `--batch_size auto`
- Use tensor parallelism for multi-GPU setups

## Examples

### Quick Model Comparison
```bash
# Test a small model
python llm_eval_cli.py \
  --model hf \
  --model_name microsoft/DialoGPT-medium \
  --tasks arc_easy \
  --num_samples 10

# Test a larger model with multi-GPU
python llm_eval_cli.py \
  --model hf \
  --model_name mistralai/Mistral-7B-v0.1 \
  --additional_model_args "device_map=auto" \
  --tasks arc_easy \
  --num_samples 10
```

### Full Leaderboard Evaluation
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name mistralai/Mistral-7B-v0.1 \
  --leaderboard \
  --additional_model_args "device_map=auto" \
  --report_format professional
```

### Quantized Model Evaluation
```bash
python llm_eval_cli.py \
  --model hf \
  --model_name mistralai/Mistral-7B-v0.1 \
  --tasks arc_easy,hellaswag \
  --quantize \
  --quantization_method 4bit \
  --batch_size 4
```

## Troubleshooting

### Common Issues

1. **CUDA Memory Errors**: Reduce batch size or enable quantization
2. **Model Loading Errors**: Check model name and ensure sufficient memory
3. **Multi-GPU Issues**: Verify GPU availability and compatibility

### GPU Memory Management
```bash
# Check GPU status
nvidia-smi

# Clear GPU memory if needed
python -c "import torch; torch.cuda.empty_cache()"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
