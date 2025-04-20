# LLM Evaluation Framework

**A Comprehensive and Modular Framework for Evaluating Large Language Models**

This framework provides a robust and extensible platform for evaluating the performance of various Large Language Models (LLMs) across a wide range of benchmarks and tasks. Built with a modular architecture, it facilitates easy integration, customization, and maintenance.

## Key Features

*   **Modular Design**: Based on a microservice-inspired architecture for clear separation of concerns and extensibility.
*   **Multiple Model Backends**: Supports Hugging Face (`hf`) and `vLLM` for flexible model loading and inference.
*   **Quantization Support**: Evaluate quantized models (e.g., 4-bit, 8-bit with `hf`, AWQ with `vLLM`) to assess performance under resource constraints.
*   **Comprehensive Benchmarks**: Includes support for standard benchmarks like MMLU, GSM8K, BBH, and more.
*   **Leaderboard Replication**: Easily run evaluations mimicking the Open LLM Leaderboard setup with standardized few-shot settings.
*   **Flexible Configuration**: Customize evaluations via CLI arguments or programmatic usage.
*   **Detailed Reporting**: Generates JSON results and Markdown reports for easy analysis.
*   **Parallelism**: Leverages `vLLM` for efficient inference, including tensor parallelism across multiple GPUs.

## Architecture Overview

The framework employs a service-oriented approach to manage different aspects of the evaluation process:

*   **Models Service**: Handles model loading, configuration, and backend selection (`hf`, `vllm`).
*   **Tasks Service**: Manages task definitions, configurations, and data loading.
*   **Evaluation Service**: Orchestrates the evaluation loop, running models on specified tasks.
*   **Normalization Service**: Processes raw scores and applies appropriate normalization based on the benchmark.
*   **Reporting Service**: Generates comprehensive JSON results and user-friendly Markdown summaries.
*   **Utils Service**: Contains shared utilities used across different services.

This structure promotes maintainability and allows developers to easily extend specific components, such as adding new model backends or custom tasks.

## Directory Structure

```
./                              # evaluation directory root
├── llm_eval/                   # Main Python package for the framework
│   ├── models/                 # Model loading and configuration logic
│   ├── tasks/                  # Task definitions and benchmark configurations
│   ├── evaluation/             # Core evaluation execution logic
│   ├── normalization/          # Score calculation and normalization
│   ├── reporting/              # Report generation (JSON, Markdown)
│   └── utils/                  # Shared helper functions and constants
├── llm_eval_cli.py             # Command-line interface script
├── reports/                    # Default output directory for Markdown reports
├── results/                    # Default output directory for JSON results
├── lm-evaluation-harness/      # Required dependency (EleutherAI's library)
└── README.md                   # This file
```

## Installation

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   Git
*   (Optional but Recommended) NVIDIA GPU with CUDA Toolkit installed for GPU acceleration.

### Steps

1.  **Clone the necessary repositories**:
    ```bash
    # Clone this framework repository (if you haven't already)
    # git clone <your-repository-url>
    # cd <repository-directory>

    # Clone the required lm-evaluation-harness library
    git clone https://github.com/EleutherAI/lm-evaluation-harness.git
    ```

2.  **Set up a virtual environment (Recommended)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    # Install lm-evaluation-harness in editable mode
    pip install -e lm-evaluation-harness

    # Install core dependencies for this framework
    # (Assuming requirements.txt exists or list packages explicitly)
    # pip install -r requirements.txt
    # Or, install common packages needed:
    pip install torch numpy tqdm transformers accelerate bitsandbytes sentencepiece

    # Install vLLM if you plan to use the vLLM backend
    pip install vllm
    ```
    *Note: Ensure your `torch` installation matches your CUDA version if using GPU.*

## Quick Start

Run a simple evaluation using a small model on a standard task:

```bash
python llm_eval_cli.py \
  --model hf \
  --model_name google/gemma-2b \
  --tasks hellaswag \
  --num_fewshot 0 \
  --device cuda  # Use 'cpu' if you don't have a GPU
```

This command will download the `gemma-2b` model (if not cached), run it on the Hellaswag benchmark with 0 few-shot examples, and save the results in the `results/` and `reports/` directories.

## Detailed Usage

### Command-Line Interface (`llm_eval_cli.py`)

The CLI provides extensive options for configuring your evaluation runs.

**Common Options:**

*   `--model`: Specify the model backend (`hf` or `vllm`). (Required)
*   `--model_name`: The identifier of the model (e.g., `meta-llama/Llama-2-7b-chat-hf` or a local path). (Required)
*   `--tasks`: Comma-separated list of tasks or task groups (e.g., `mmlu,gsm8k`, `LEADERBOARD`, `leaderboard_bbh`). (Required)
*   `--num_fewshot`: Number of few-shot examples to provide in the prompt (default: 0). Specific benchmarks (like in `LEADERBOARD`) may override this.
*   `--device`: The device to run inference on (`cuda`, `cpu`, `cuda:0`, etc.).
*   `--batch_size`: Evaluation batch size. Set to `"auto"` for automatic batch size detection (HF only).
*   `--output_path`: Specify a custom directory path to save results and reports.
*   `--num_samples`: Limit the number of samples evaluated per task (e.g., `10` for quick testing). Default is all samples.
*   `--list_tasks`: List all available tasks and exit.

**Hugging Face (`hf`) Specific Options:**

*   `--quantize`: Enable quantization (e.g., load in 4-bit or 8-bit).
*   `--quantization_method`: Specify the quantization type (`4bit`, `8bit`). Requires `bitsandbytes`.

**vLLM Specific Options:**

*   `--dtype`: Data type for model weights (`float16`, `bfloat16`, `float32`). Default often `auto`.
*   `--gpu_memory_utilization`: Proportion of GPU memory to use (0.0 to 1.0).
*   `--tensor_parallel_size`: Number of GPUs for tensor parallelism.
*   `--vllm_quantization`: Use quantized model formats supported by vLLM (e.g., `awq`, `gptq`).

**Usage Examples:**

1.  **Basic HF Evaluation:**
    ```bash
    python llm_eval_cli.py \
      --model hf \
      --model_name google/gemma-7b \
      --tasks mmlu,gsm8k \
      --num_fewshot 0 \
      --device cuda
    ```

2.  **4-bit Quantized HF Evaluation:**
    ```bash
    python llm_eval_cli.py \
      --model hf \
      --model_name meta-llama/Llama-2-13b \
      --tasks bbh,ifeval \
      --quantize \
      --quantization_method 4bit \
      --device cuda
    ```

3.  **Fast Inference with vLLM:**
    ```bash
    python llm_eval_cli.py \
      --model vllm \
      --model_name meta-llama/Llama-2-70b \
      --tasks mmlu,truthfulqa_mc \
      --dtype float16 \
      --gpu_memory_utilization 0.9 \
      --device cuda
    ```

4.  **Multi-GPU with vLLM:**
    ```bash
    python llm_eval_cli.py \
      --model vllm \
      --model_name mistralai/Mixtral-8x7B-Instruct-v0.1 \
      --tasks arc_challenge,hellaswag \
      --tensor_parallel_size 4 \
      --device cuda
    ```

5.  **AWQ Quantized Model with vLLM:**
    ```bash
    python llm_eval_cli.py \
      --model vllm \
      --model_name TheBloke/Llama-2-13B-chat-AWQ \
      --tasks mmlu,gsm8k \
      --vllm_quantization awq \
      --dtype float16 \
      --device cuda
    ```

### Leaderboard Evaluation

This framework includes configurations to replicate the setup used by the Hugging Face Open LLM Leaderboard. This is useful for standardized comparisons.

**Run the Full Leaderboard Suite:**

```bash
# Using the dedicated flag (recommended)
python llm_eval_cli.py \
  --model vllm \
  --model_name your-model-repo/your-model-name \
  --leaderboard \
  --device cuda \
  --gpu_memory_utilization 0.9 # Adjust as needed

# Or by specifying the task group
python llm_eval_cli.py \
  --model vllm \
  --model_name your-model-repo/your-model-name \
  --tasks LEADERBOARD \
  --device cuda \
  --gpu_memory_utilization 0.9 # Adjust as needed
```

**Key Aspects:**

*   Automatically uses the **correct few-shot settings** for each sub-benchmark, overriding the global `--num_fewshot` parameter:
    *   BBH: 3-shot
    *   GPQA: 0-shot
    *   MMLU-Pro: 5-shot
    *   MUSR: 0-shot
    *   IFEval: 0-shot (generative)
    *   Math-lvl-5: 4-shot (generative)
*   Includes the following benchmark sets: BBH, GPQA, MMLU-Pro, MUSR, IFEval, Math-lvl-5.
*   You can also run individual leaderboard components by specifying their task names (e.g., `--tasks leaderboard_bbh`, `--tasks leaderboard_mmlu_pro`). See the full list in the code or by inspecting task configurations.

### Using as a Library

Integrate the evaluation logic directly into your Python scripts.

```python
from llm_eval import evaluate_model
import os

# Define evaluation parameters
eval_config = {
    "model_type": "hf",
    "model_name": "google/gemma-2b-it",
    "tasks": ["mmlu", "gsm8k"],
    "num_fewshot": 0,
    "device": "cuda",
    "quantize": True,
    "quantization_method": "4bit",
    "batch_size": "auto",
    "output_dir": "./custom_results" # Optional: Specify output location
}

# Run the evaluation
try:
    results_summary, results_file_path = evaluate_model(**eval_config)

    print("Evaluation completed successfully!")
    print(f"Results summary: {results_summary}")
    print(f"Detailed JSON results saved to: {results_file_path}")

    # Construct the expected report path
    base_name = os.path.splitext(os.path.basename(results_file_path))[0]
    report_file_path = os.path.join(os.path.dirname(results_file_path).replace('results', 'reports'), f"{base_name}_report.md")

    if os.path.exists(report_file_path):
        print(f"Markdown report saved to: {report_file_path}")
    else:
        print("Markdown report not found at expected location.")

except Exception as e:
    print(f"An error occurred during evaluation: {e}")

```

## Results and Reporting

*   **JSON Results**: Detailed results for each task, including individual sample predictions (if applicable), metrics, and configuration details, are saved in the `results/` directory (or the custom path specified by `--output_path`).
*   **Markdown Reports**: A summary report aggregating scores across tasks is generated in the `reports/` directory (or the corresponding subdirectory if using `--output_path`). This provides a quick overview of the model's performance.

## Extending the Framework

The modular design makes it easier to add new functionalities:

1.  **Adding New Tasks/Benchmarks**:
    *   Define the task configuration in `llm_eval/tasks/task_registry.py` or a similar configuration file.
    *   Ensure the task is compatible with the `lm-evaluation-harness` structure or adapt it.
2.  **Supporting New Model Backends**:
    *   Create a new model handler class in `llm_eval/models/` inheriting from a base model class (if applicable).
    *   Implement the required methods for loading, inference, etc.
    *   Register the new backend type.
3.  **Customizing Reporting**:
    *   Modify the report generation logic in `llm_eval/reporting/` to change the format or content of the Markdown/JSON outputs.

## Contributing

Contributions are welcome! Please follow standard practices:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix (`git checkout -b feature/my-new-feature`).
3.  Make your changes and commit them (`git commit -am 'Add some feature'`).
4.  Push to the branch (`git push origin feature/my-new-feature`).
5.  Create a new Pull Request.

Please ensure your code adheres to the project's style guidelines and includes tests where appropriate.

## License

(Specify your license here, e.g., MIT, Apache 2.0, or leave as placeholder if undecided)

```
Placeholder for License Information.
```

## Support

For questions or issues, please open an issue on the GitHub repository.
