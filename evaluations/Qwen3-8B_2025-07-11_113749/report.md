# 🚀 LLM Evaluation Report
## Qwen/Qwen3-8B

📅 **Generated:** July 11, 2025 at 13:41:05
🏷️ **Report ID:** 20250711-114105

---

## 📋 Executive Summary

🎯 **Overall Performance:** 🔴 **NEEDS IMPROVEMENT**
📊 **Average Score:** 44.8%
📈 **Best Performance:** 100.0%
📉 **Lowest Performance:** 0.0%
📏 **Score Range:** 100.0 points

### 🔍 Key Insights
🔧 **Performance below expectations** - consider fine-tuning or model selection
📊 **High variance** in task performance - model shows task-specific strengths

## 🔧 Model Configuration

| Specification | Details |
| ------------- | ------- |
| **Model Name** | `Qwen/Qwen3-8B` |
| **Parameters** | Not specified |
| **Architecture** | Not specified |
| **Backend** | HF |
| **Quantization** | 4-bit |
| **Device Setup** | Single GPU |

## 📊 Performance Overview

| Task | Metric | Score | Performance |
| ---- | ------ | ----- | ----------- |
| leaderboard_bbh_boolean_expressions | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_causal_judgement | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_date_understanding | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_disambiguation_qa | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_formal_fallacies | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_geometric_shapes | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_hyperbaton | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_logical_deduction_five_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_logical_deduction_seven_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_logical_deduction_three_objects | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_movie_recommendation | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_navigate | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_object_counting | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_penguins_in_a_table | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_reasoning_about_colored_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_ruin_names | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_salient_translation_error_detection | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_snarks | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_sports_understanding | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_temporal_sequences | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_five_objects | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_seven_objects | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_three_objects | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_web_of_lies | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_gpqa_diamond | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_gpqa_extended | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_gpqa_main | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | prompt_level_strict_acc,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | inst_level_strict_acc,none | 33.3% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | prompt_level_loose_acc,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | inst_level_loose_acc,none | 33.3% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_algebra_hard | exact_match,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_math_counting_and_prob_hard | exact_match,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_math_geometry_hard | exact_match,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_math_intermediate_algebra_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_num_theory_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_prealgebra_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_precalculus_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_mmlu_pro | acc,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_musr_murder_mysteries | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_musr_object_placements | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_musr_team_allocation | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |

### 📊 Task Performance Comparison

```
Performance Distribution:

🟢 leaderboard     │████████████████████████████████████████ │ 44.4
```

---

### 🔬 **Evaluation Methodology Note**

The following **Detailed Results** use the standard LM Evaluation Harness methodology:
- **📊 Loglikelihood-based scoring** for multiple choice questions
- **🎯 Limited sample evaluation** (same sample size as text output analysis)
- **⚖️ Token probability comparisons** for answer selection
- **📏 Standardized prompting** with task-specific few-shot examples

**📝 Sample Size**: Consistent 1 samples per task


## 📊 Detailed Results

| Tasks | Version | Filter | n-shot | Metric | | Value | | Stderr |
| ----- | ------- | ------ | ------ | ------ |-| ----- |-| ------ |
| **BBH** | | | | | | | | |
| Bbh Boolean Expressions | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Causal Judgement | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Date Understanding | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Disambiguation Qa | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Formal Fallacies | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Geometric Shapes | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Hyperbaton | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Logical Deduction Five Objects | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Logical Deduction Seven Objects | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Logical Deduction Three Objects | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Movie Recommendation | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Navigate | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Object Counting | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Penguins In A Table | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Reasoning About Colored Objects | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Ruin Names | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Salient Translation Error Detection | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Snarks | 1.0 | none | 3 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Bbh Sports Understanding | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Temporal Sequences | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Tracking Shuffled Objects Five Ob... | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Tracking Shuffled Objects Seven O... | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Tracking Shuffled Objects Three O... | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Bbh Web Of Lies | 1.0 | none | 3 | acc_norm | ↑ | 0.0000 | ± | N/A |
| **GPQA** | | | | | | | | |
| Gpqa Diamond | 1.0 | none | 0 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Gpqa Extended | 1.0 | none | 0 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Gpqa Main | 1.0 | none | 0 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Mmlu Pro | 1.0 | none | 5 | acc | ↑ | 1.0000 | ± | N/A |
| **MUSR** | | | | | | | | |
| Musr Murder Mysteries | 1.0 | none | 0 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Musr Object Placements | 1.0 | none | 0 | acc_norm | ↑ | 0.0000 | ± | N/A |
| Musr Team Allocation | 1.0 | none | 0 | acc_norm | ↑ | 1.0000 | ± | N/A |
| Ifeval | 1.0 | none | 0 | prompt_level_strict_acc | ↑ | 0.0000 | ± | N/A |
|  | | | | inst_level_strict_acc | ↑ | 0.3333 | ± | N/A |
|  | | | | prompt_level_loose_acc | ↑ | 0.0000 | ± | N/A |
|  | | | | inst_level_loose_acc | ↑ | 0.3333 | ± | N/A |
| **Math** | | | | | | | | |
| Math Algebra Hard | 1.0 | none | 4 | exact_match | ↑ | 1.0000 | ± | N/A |
| Math Counting And Prob Hard | 1.0 | none | 4 | exact_match | ↑ | 1.0000 | ± | N/A |
| Math Geometry Hard | 1.0 | none | 4 | exact_match | ↑ | 1.0000 | ± | N/A |
| Math Intermediate Algebra Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | N/A |
| Math Num Theory Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | N/A |
| Math Prealgebra Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | N/A |
| Math Precalculus Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | N/A |

**Notes:**
- ↑ indicates higher values are better
- Version refers to the task format version
- Filter shows any applied filtering (none = no filtering)
- n-shot indicates the number of few-shot examples used
- Stderr shows standard error where available


## 🔍 Model Output Analysis

### 📋 **Methodology Overview**

This section analyzes **actual text generation performance** by examining decoded model outputs:

**🎯 Approach**:
- **Text Generation**: Model generates complete responses (not just probabilities)
- **String Matching**: Exact comparison between generated text and target answers
- **Sample Size**: Consistent 1 samples per task
- **Real-World Insight**: Shows how the model performs in actual text generation scenarios

**⚖️ Comparison with Benchmark Metrics**:
- **Benchmark scores** use loglikelihood comparison (optimal token probability)
- **Text outputs** use actual generation + exact string matching
- **Same sample limitations** ensure fair comparison between methodologies
- **Performance gaps** indicate generation vs. reasoning capability differences

### ⚙️ **Evaluation Configuration**

| Parameter | Value | Description |
| --------- | ----- | ----------- |
| **Text Output Sample Size** | 1 per task | Number of samples for generation analysis |
| **Sample Selection** | Random | Randomly selected from test sets |
| **Matching Method** | Exact String | Case-sensitive exact matching |

**📝 Notes**:
- **Sample size impact**: Current sample size provides statistical reliability
- **Confidence level**: 1 samples provide limited statistical confidence
- **Recommendation**: Consider 100+ samples for production evaluation

**📊 Detection Results**: Consistent 1 samples per task

### 📊 Text Output Summary

| Metric | Value | Visual |
| ------ | ----- | ------ |
| **Total Samples** | 39 | 📝 |
| **With Text Outputs** | 39 (100.0%) | 🟩 ████████████████████ 100.0% |
| **Correct Responses** | 11 | ✅ |
| **Incorrect Responses** | 28 | ❌ |
| **Overall Accuracy** | 28.2% | 🟥 █████░░░░░░░░░░░░░░░ 28.2% |

🎯 **Text Output Performance:** 🔴 **NEEDS IMPROVEMENT**

### ⚖️ **Methodology Comparison**

Comparing **loglikelihood-based benchmark scores** vs **text generation performance**:

| Task | Benchmark Score | Text Generation | Gap | Analysis |
| ---- | --------------- | --------------- | --- | -------- |
| Mmlu Pro | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Boolean Expre... | 100.0% | 100.0% | +0.0% | ✅ Consistent performance |
| Bbh Causal Judgement | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Bbh Date Understa... | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Disambiguatio... | 100.0% | 100.0% | +0.0% | ✅ Consistent performance |
| Bbh Formal Fallacies | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Bbh Geometric Shapes | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Hyperbaton | 0.0% | 100.0% | -100.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Logical Deduc... | 100.0% | 100.0% | +0.0% | ✅ Consistent performance |
| Bbh Logical Deduc... | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Logical Deduc... | 0.0% | 100.0% | -100.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Movie Recomme... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Bbh Navigate | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Object Counting | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Penguins In A... | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Reasoning Abo... | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Ruin Names | 0.0% | 100.0% | -100.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Salient Trans... | 0.0% | 100.0% | -100.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Snarks | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Bbh Sports Unders... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Bbh Temporal Sequ... | 0.0% | 100.0% | -100.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Tracking Shuf... | 0.0% | 100.0% | -100.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Tracking Shuf... | 0.0% | 100.0% | -100.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Tracking Shuf... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Bbh Web Of Lies | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Gpqa Diamond | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Gpqa Extended | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Gpqa Main | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Algebra Hard | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Math Counting And... | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Math Geometry Hard | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |
| Math Intermediate... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Num Theory Hard | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Prealgebra Hard | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Precalculus ... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Ifeval | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Musr Murder Myste... | 100.0% | 100.0% | +0.0% | ✅ Consistent performance |
| Musr Object Place... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Musr Team Allocation | 100.0% | 0.0% | +100.0% | 🔴 Large gap - generation challenges |

**🔍 Key Insights**:
- **Positive gaps**: Benchmark (loglikelihood) scores higher than text generation
- **Negative gaps**: Text generation surprisingly outperforms benchmark
- **Large gaps**: Indicate model struggles with consistent text formatting
- **Small gaps**: Show good alignment between reasoning and generation abilities

### 📋 Per-Task Text Output Performance

*Based on 1 samples per task - results may vary with larger sample sizes*

| Task | Samples | Outputs | Correct | Accuracy | Performance |
| ---- | ------- | ------- | ------- | -------- | ----------- |
| Mmlu Pro | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Boolean Expressions | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Causal Judgement | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Date Understanding | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Disambiguation Qa | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Formal Fallacies | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Geometric Shapes | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Hyperbaton | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Logical Deduction Fiv | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Logical Deduction Sev | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Logical Deduction Thr | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Movie Recommendation | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Navigate | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Object Counting | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Penguins In A Table | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Reasoning About Color | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Ruin Names | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Salient Translation E | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Snarks | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Sports Understanding | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Temporal Sequences | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Tracking Shuffled Obj | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Tracking Shuffled Obj | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Bbh Tracking Shuffled Obj | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Web Of Lies | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Gpqa Diamond | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Gpqa Extended | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Gpqa Main | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Algebra Hard | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Counting And Prob Ha | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Geometry Hard | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Intermediate Algebra | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Num Theory Hard | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Prealgebra Hard | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Precalculus Hard | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Ifeval | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Musr Murder Mysteries | 1 | 1 | 1 | 100.0% | 🟢 **EXCELLENT** |
| Musr Object Placements | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Musr Team Allocation | 1 | 1 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |

### 📊 Text Output Accuracy by Task

```
Performance Distribution:

🟢 bbh boolean exp │████████████████████████████████████████ │ 100.0
🟢 bbh disambiguat │████████████████████████████████████████ │ 100.0
🟢 bbh hyperbaton  │████████████████████████████████████████ │ 100.0
🟢 bbh logical ded │████████████████████████████████████████ │ 100.0
🟢 bbh ruin names  │████████████████████████████████████████ │ 100.0
🟢 bbh salient tra │████████████████████████████████████████ │ 100.0
🟢 bbh temporal se │████████████████████████████████████████ │ 100.0
🟢 musr murder mys │████████████████████████████████████████ │ 100.0
🔴 mmlu pro        │                                         │ 0.0
🔴 bbh causal judg │                                         │ 0.0
🔴 bbh date unders │                                         │ 0.0
🔴 bbh formal fall │                                         │ 0.0
🔴 bbh geometric s │                                         │ 0.0
🔴 bbh movie recom │                                         │ 0.0
🔴 bbh navigate    │                                         │ 0.0
🔴 bbh object coun │                                         │ 0.0
🔴 bbh penguins in │                                         │ 0.0
🔴 bbh reasoning a │                                         │ 0.0
🔴 bbh snarks      │                                         │ 0.0
🔴 bbh sports unde │                                         │ 0.0
🔴 bbh tracking sh │                                         │ 0.0
🔴 bbh web of lies │                                         │ 0.0
🔴 gpqa diamond    │                                         │ 0.0
🔴 gpqa extended   │                                         │ 0.0
🔴 gpqa main       │                                         │ 0.0
🔴 math algebra ha │                                         │ 0.0
🔴 math counting a │                                         │ 0.0
🔴 math geometry h │                                         │ 0.0
🔴 math intermedia │                                         │ 0.0
🔴 math num theory │                                         │ 0.0
🔴 math prealgebra │                                         │ 0.0
🔴 math precalculu │                                         │ 0.0
🔴 ifeval          │                                         │ 0.0
🔴 musr object pla │                                         │ 0.0
🔴 musr team alloc │                                         │ 0.0
```

## 💡 Recommendations


### 🔬 **Evaluation Methodology Insights**

**📊 Understanding Score Differences**:
- **Loglikelihood scores** measure token probability optimization (what the model 'knows')
- **Text generation scores** measure actual output quality (what the model 'produces')
- **Sample consistency** consistent 1 samples per task ensures fair comparison

**🎯 Optimization Recommendations**:

**🔴 Low Performance (< 50%)**:
- Consider fine-tuning on task-specific datasets
- Improve prompt engineering and few-shot examples
- Evaluate if model size/capability is sufficient for these tasks
- Check if quantization significantly impacts performance

**📈 For More Reliable Evaluation**:
- Increase sample size from 1 to 50+ per task for more stable estimates
- Use multiple random seeds to assess variance across different sample sets
- Compare both loglikelihood and generation approaches for comprehensive assessment
- Consider domain-specific evaluation metrics beyond exact string matching
## 📖 Sample Analysis

*Detailed examples showing model performance on specific questions.*

### 📚 Leaderboard_Mmlu_Pro

### 📝 Sample 1

#### ❓ Question
```text
Typical advertising regulatory bodies suggest, for example that adverts must not: encourage _________, cause unnecessary ________ or _____, and must not cause _______ offence.
```

#### 📋 Answer Choices
**A.** Safe practices, Fear, Jealousy, Trivial
**B.** Unsafe practices, Distress, Joy, Trivial
**C.** Safe practices, Wants, Jealousy, Trivial
**D.** Safe practices, Distress, Fear, Trivial
**E.** Unsafe practices, Wants, Jealousy, Serious
**F.** Safe practices, Distress, Jealousy, Serious
**G.** Safe practices, Wants, Fear, Serious
**H.** Unsafe practices, Wants, Fear, Trivial
**I.** Unsafe practices, Distress, Fear, Serious

#### ✅ Expected Answer
**I**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `A`

💬 **Analysis:** The model responded with `A` but the correct answer is `I`.

---

### 📚 Leaderboard_Bbh_Boolean_Expressions

### 📝 Sample 1

#### ❓ Question
```text
not ( True ) and ( True ) is
```

#### ✅ Expected Answer
**False**

#### 🤖 Model Output (✅ Correct)

**Response:** `False`

💬 **Analysis:** The model correctly identified the answer.

---

### 📚 Leaderboard_Bbh_Causal_Judgement

### 📝 Sample 1

#### ❓ Question
```text
How would a typical person answer each of the following questions about causation?
A machine is set up in such a way that it will short circuit if both the black wire and the red wire touch the battery at the same time. The machine will not short circuit if just one of these wires touches the battery. The black wire is designated as the one that is supposed to touch the battery, while the red wire is supposed to remain in some other part of the machine. One day, the black wire and the red wire both end up touching the battery at the same time. There is a short circuit. Did the black wire cause the short circuit?
Options:
- Yes
- No
```

#### ✅ Expected Answer
**No**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `Yes`

💬 **Analysis:** The model responded with `Yes` but the correct answer is `No`.

---

### 📚 Leaderboard_Bbh_Date_Understanding

### 📝 Sample 1

#### ❓ Question
```text
Today is Christmas Eve of 1937. What is the date tomorrow in MM/DD/YYYY?
Options:
(A) 12/11/1937
(B) 12/25/1937
(C) 01/04/1938
(D) 12/04/1937
(E) 12/25/2006
(F) 07/25/1937
```

#### ✅ Expected Answer
**(B)**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `(A)`

💬 **Analysis:** The model responded with `(A)` but the correct answer is `(B)`.

---

### 📚 Leaderboard_Bbh_Disambiguation_Qa

### 📝 Sample 1

#### ❓ Question
```text
In the following sentences, explain the antecedent of the pronoun (which thing the pronoun refers to), or state that it is ambiguous.
Sentence: The patient was referred to the specialist because he had a rare skin condition.
Options:
(A) The patient had a skin condition
(B) The specialist had a skin condition
(C) Ambiguous
```

#### ✅ Expected Answer
**(A)**

#### 🤖 Model Output (✅ Correct)

**Response:** `(A)`

💬 **Analysis:** The model correctly identified the answer.

---

### 📚 Leaderboard_Bbh_Formal_Fallacies

### 📝 Sample 1

#### ❓ Question
```text
"Here comes a perfectly valid argument: First of all, whoever is a schoolmate of Sondra is not a stepsister of Pricilla. In consequence, whoever is not a stepsister of Pricilla is a schoolmate of Sondra."
Is the argument, given the explicitly stated premises, deductively valid or invalid?
Options:
- valid 
- invalid
```

#### ✅ Expected Answer
**invalid**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `valid`

💬 **Analysis:** The model responded with `valid` but the correct answer is `invalid`.

---

---

## 📋 Report Information

**Generated by:** LLM Evaluation Framework v2.0
**Timestamp:** 2025-07-11T11:41:05.047433
**Framework:** Professional Report Generator

*This report provides a comprehensive analysis of model performance across various evaluation tasks.*
*For technical details, refer to the accompanying JSON results file.*