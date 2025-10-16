# 🚀 LLM Evaluation Report
## mistralai/Ministral-8B-Instruct-2410

📅 **Generated:** October 09, 2025 at 17:33:29
🏷️ **Report ID:** 20251009-153329

---

## 📋 Executive Summary

🎯 **Overall Performance:** 🔴 **NEEDS IMPROVEMENT**
📊 **Average Score:** 40.6%
📈 **Best Performance:** 80.0%
📉 **Lowest Performance:** 10.0%
📏 **Score Range:** 70.0 points

### 🔍 Key Insights
🔧 **Performance below expectations** - consider fine-tuning or model selection
📊 **High variance** in task performance - model shows task-specific strengths

## 🔧 Model Configuration

| Specification | Details |
| ------------- | ------- |
| **Model Name** | `mistralai/Ministral-8B-Instruct-2410` |
| **Parameters** | Not specified |
| **Architecture** | Mistral (Transformer) |
| **Backend** | HF |
| **Quantization** | 4-bit |
| **Device Setup** | Single GPU |

## 📊 Performance Overview

| Task | Metric | Score | Performance |
| ---- | ------ | ----- | ----------- |
| leaderboard_bbh_boolean_expressions | acc_norm,none | 80.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_causal_judgement | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_date_understanding | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_disambiguation_qa | acc_norm,none | 60.0% | 🟡 **GOOD** |
| leaderboard_bbh_formal_fallacies | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_geometric_shapes | acc_norm,none | 50.0% | 🟡 **GOOD** |
| leaderboard_bbh_hyperbaton | acc_norm,none | 60.0% | 🟡 **GOOD** |
| leaderboard_bbh_logical_deduction_five_objects | acc_norm,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_logical_deduction_seven_objects | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_logical_deduction_three_objects | acc_norm,none | 60.0% | 🟡 **GOOD** |
| leaderboard_bbh_movie_recommendation | acc_norm,none | 50.0% | 🟡 **GOOD** |
| leaderboard_bbh_navigate | acc_norm,none | 70.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_object_counting | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_penguins_in_a_table | acc_norm,none | 50.0% | 🟡 **GOOD** |
| leaderboard_bbh_reasoning_about_colored_objects | acc_norm,none | 50.0% | 🟡 **GOOD** |
| leaderboard_bbh_ruin_names | acc_norm,none | 70.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_salient_translation_error_detection | acc_norm,none | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_snarks | acc_norm,none | 70.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_sports_understanding | acc_norm,none | 50.0% | 🟡 **GOOD** |
| leaderboard_bbh_temporal_sequences | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_five_objects | acc_norm,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_seven_objects | acc_norm,none | 10.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_three_objects | acc_norm,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_web_of_lies | acc_norm,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_gpqa_diamond | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_gpqa_extended | acc_norm,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_gpqa_main | acc_norm,none | 50.0% | 🟡 **GOOD** |
| leaderboard_ifeval | prompt_level_strict_acc,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | inst_level_strict_acc,none | 27.8% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | prompt_level_loose_acc,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | inst_level_loose_acc,none | 33.3% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_algebra_hard | exact_match,none | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_algebra_hard | exact_match_original,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_counting_and_prob_hard | exact_match,none | 10.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_counting_and_prob_hard | exact_match_original,none | 10.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_geometry_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_geometry_hard | exact_match_original,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_intermediate_algebra_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_intermediate_algebra_hard | exact_match_original,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_num_theory_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_num_theory_hard | exact_match_original,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_prealgebra_hard | exact_match,none | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_prealgebra_hard | exact_match_original,none | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_precalculus_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_precalculus_hard | exact_match_original,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_mmlu_pro | acc,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_musr_murder_mysteries | acc_norm,none | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_musr_object_placements | acc_norm,none | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_musr_team_allocation | acc_norm,none | 30.0% | 🔴 **NEEDS IMPROVEMENT** |

### 📊 Task Performance Comparison

```
Performance Distribution:

🟢 leaderboard     │████████████████████████████████████████ │ 31.7
```

---

### 🔬 **Evaluation Methodology Note**

The following **Detailed Results** use the standard LM Evaluation Harness methodology:
- **📊 Loglikelihood-based scoring** for multiple choice questions
- **🎯 Limited sample evaluation** (same sample size as text output analysis)
- **⚖️ Token probability comparisons** for answer selection
- **📏 Standardized prompting** with task-specific few-shot examples

**📝 Sample Size**: Consistent 10 samples per task


## 📊 Detailed Results

| Tasks | Version | Filter | n-shot | Metric | | Value | | Stderr |
| ----- | ------- | ------ | ------ | ------ |-| ----- |-| ------ |
| **BBH** | | | | | | | | |
| Bbh Boolean Expressions | 1.0 | none | 3 | acc_norm | ↑ | 0.8000 | ± | 0.1333 |
| Bbh Causal Judgement | 1.0 | none | 3 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Bbh Date Understanding | 1.0 | none | 3 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Bbh Disambiguation Qa | 1.0 | none | 3 | acc_norm | ↑ | 0.6000 | ± | 0.1633 |
| Bbh Formal Fallacies | 1.0 | none | 3 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Bbh Geometric Shapes | 1.0 | none | 3 | acc_norm | ↑ | 0.5000 | ± | 0.1667 |
| Bbh Hyperbaton | 1.0 | none | 3 | acc_norm | ↑ | 0.6000 | ± | 0.1633 |
| Bbh Logical Deduction Five Objects | 1.0 | none | 3 | acc_norm | ↑ | 0.2000 | ± | 0.1333 |
| Bbh Logical Deduction Seven Objects | 1.0 | none | 3 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Bbh Logical Deduction Three Objects | 1.0 | none | 3 | acc_norm | ↑ | 0.6000 | ± | 0.1633 |
| Bbh Movie Recommendation | 1.0 | none | 3 | acc_norm | ↑ | 0.5000 | ± | 0.1667 |
| Bbh Navigate | 1.0 | none | 3 | acc_norm | ↑ | 0.7000 | ± | 0.1528 |
| Bbh Object Counting | 1.0 | none | 3 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Bbh Penguins In A Table | 1.0 | none | 3 | acc_norm | ↑ | 0.5000 | ± | 0.1667 |
| Bbh Reasoning About Colored Objects | 1.0 | none | 3 | acc_norm | ↑ | 0.5000 | ± | 0.1667 |
| Bbh Ruin Names | 1.0 | none | 3 | acc_norm | ↑ | 0.7000 | ± | 0.1528 |
| Bbh Salient Translation Error Detection | 1.0 | none | 3 | acc_norm | ↑ | 0.3000 | ± | 0.1528 |
| Bbh Snarks | 1.0 | none | 3 | acc_norm | ↑ | 0.7000 | ± | 0.1528 |
| Bbh Sports Understanding | 1.0 | none | 3 | acc_norm | ↑ | 0.5000 | ± | 0.1667 |
| Bbh Temporal Sequences | 1.0 | none | 3 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Bbh Tracking Shuffled Objects Five Ob... | 1.0 | none | 3 | acc_norm | ↑ | 0.2000 | ± | 0.1333 |
| Bbh Tracking Shuffled Objects Seven O... | 1.0 | none | 3 | acc_norm | ↑ | 0.1000 | ± | 0.1000 |
| Bbh Tracking Shuffled Objects Three O... | 1.0 | none | 3 | acc_norm | ↑ | 0.2000 | ± | 0.1333 |
| Bbh Web Of Lies | 1.0 | none | 3 | acc_norm | ↑ | 0.2000 | ± | 0.1333 |
| **GPQA** | | | | | | | | |
| Gpqa Diamond | 1.0 | none | 0 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Gpqa Extended | 1.0 | none | 0 | acc_norm | ↑ | 0.2000 | ± | 0.1333 |
| Gpqa Main | 1.0 | none | 0 | acc_norm | ↑ | 0.5000 | ± | 0.1667 |
| Mmlu Pro | 1.0 | none | 5 | acc | ↑ | 0.4000 | ± | 0.1633 |
| **MUSR** | | | | | | | | |
| Musr Murder Mysteries | 1.0 | none | 0 | acc_norm | ↑ | 0.4000 | ± | 0.1633 |
| Musr Object Placements | 1.0 | none | 0 | acc_norm | ↑ | 0.2000 | ± | 0.1333 |
| Musr Team Allocation | 1.0 | none | 0 | acc_norm | ↑ | 0.3000 | ± | 0.1528 |
| Ifeval | 1.0 | none | 0 | prompt_level_strict_acc | ↑ | 0.2000 | ± | 0.1333 |
|  | | | | inst_level_strict_acc | ↑ | 0.2778 | ± | N/A |
|  | | | | prompt_level_loose_acc | ↑ | 0.2000 | ± | 0.1333 |
|  | | | | inst_level_loose_acc | ↑ | 0.3333 | ± | N/A |
| **Math** | | | | | | | | |
| Math Algebra Hard | 1.0 | none | 4 | exact_match | ↑ | 0.3000 | ± | 0.1528 |
|  | | | | exact_match_original | ↑ | 0.2000 | ± | 0.1333 |
| Math Counting And Prob Hard | 1.0 | none | 4 | exact_match | ↑ | 0.1000 | ± | 0.1000 |
|  | | | | exact_match_original | ↑ | 0.1000 | ± | 0.1000 |
| Math Geometry Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | 0.0000 |
|  | | | | exact_match_original | ↑ | 0.0000 | ± | 0.0000 |
| Math Intermediate Algebra Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | 0.0000 |
|  | | | | exact_match_original | ↑ | 0.0000 | ± | 0.0000 |
| Math Num Theory Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | 0.0000 |
|  | | | | exact_match_original | ↑ | 0.0000 | ± | 0.0000 |
| Math Prealgebra Hard | 1.0 | none | 4 | exact_match | ↑ | 0.3000 | ± | 0.1528 |
|  | | | | exact_match_original | ↑ | 0.3000 | ± | 0.1528 |
| Math Precalculus Hard | 1.0 | none | 4 | exact_match | ↑ | 0.0000 | ± | 0.0000 |
|  | | | | exact_match_original | ↑ | 0.0000 | ± | 0.0000 |

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
- **Sample Size**: Consistent 10 samples per task
- **Real-World Insight**: Shows how the model performs in actual text generation scenarios

**⚖️ Comparison with Benchmark Metrics**:
- **Benchmark scores** use loglikelihood comparison (optimal token probability)
- **Text outputs** use actual generation + exact string matching
- **Same sample limitations** ensure fair comparison between methodologies
- **Performance gaps** indicate generation vs. reasoning capability differences

### ⚙️ **Evaluation Configuration**

| Parameter | Value | Description |
| --------- | ----- | ----------- |
| **Text Output Sample Size** | 10 per task | Number of samples for generation analysis |
| **Sample Selection** | Random | Randomly selected from test sets |
| **Matching Method** | Exact String | Case-sensitive exact matching |

**📝 Notes**:
- **Sample size impact**: Current sample size provides statistical reliability
- **Confidence level**: 10 samples provide limited statistical confidence
- **Recommendation**: Consider 100+ samples for production evaluation

**📊 Detection Results**: Consistent 10 samples per task

### 📊 Text Output Summary

| Metric | Value | Visual |
| ------ | ----- | ------ |
| **Total Samples** | 390 | 📝 |
| **With Text Outputs** | 390 (100.0%) | 🟩 ████████████████████ 100.0% |
| **Correct Responses** | 86 | ✅ |
| **Incorrect Responses** | 304 | ❌ |
| **Overall Accuracy** | 22.1% | 🟥 ████░░░░░░░░░░░░░░░░ 22.1% |

🎯 **Text Output Performance:** 🔴 **NEEDS IMPROVEMENT**

### ⚖️ **Methodology Comparison**

Comparing **loglikelihood-based benchmark scores** vs **text generation performance**:

| Task | Benchmark Score | Text Generation | Gap | Analysis |
| ---- | --------------- | --------------- | --- | -------- |
| Math Precalculus ... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Prealgebra Hard | 30.0% | 0.0% | +30.0% | 🔴 Large gap - generation challenges |
| Math Num Theory Hard | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Intermediate... | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Geometry Hard | 0.0% | 0.0% | +0.0% | ✅ Consistent performance |
| Math Counting And... | 10.0% | 0.0% | +10.0% | 🟡 Moderate gap - formatting issues possible |
| Math Algebra Hard | 30.0% | 0.0% | +30.0% | 🔴 Large gap - generation challenges |
| Ifeval | 20.0% | 0.0% | +20.0% | 🔴 Large gap - generation challenges |
| Musr Team Allocation | 30.0% | 20.0% | +10.0% | 🟡 Moderate gap - formatting issues possible |
| Musr Object Place... | 20.0% | 40.0% | -20.0% | 🟢 Text generation outperforms - possible chance |
| Musr Murder Myste... | 40.0% | 50.0% | -10.0% | 🟢 Text generation outperforms - possible chance |
| Mmlu Pro | 40.0% | 10.0% | +30.0% | 🔴 Large gap - generation challenges |
| Gpqa Extended | 20.0% | 10.0% | +10.0% | 🟡 Moderate gap - formatting issues possible |
| Gpqa Diamond | 40.0% | 30.0% | +10.0% | 🟡 Moderate gap - formatting issues possible |
| Gpqa Main | 50.0% | 20.0% | +30.0% | 🔴 Large gap - generation challenges |
| Bbh Web Of Lies | 20.0% | 20.0% | +0.0% | ✅ Consistent performance |
| Bbh Tracking Shuf... | 20.0% | 50.0% | -30.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Tracking Shuf... | 10.0% | 20.0% | -10.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Tracking Shuf... | 20.0% | 20.0% | +0.0% | ✅ Consistent performance |
| Bbh Temporal Sequ... | 40.0% | 30.0% | +10.0% | 🟡 Moderate gap - formatting issues possible |
| Bbh Sports Unders... | 50.0% | 50.0% | +0.0% | ✅ Consistent performance |
| Bbh Snarks | 70.0% | 60.0% | +10.0% | 🟡 Moderate gap - formatting issues possible |
| Bbh Salient Trans... | 30.0% | 30.0% | +0.0% | ✅ Consistent performance |
| Bbh Ruin Names | 70.0% | 20.0% | +50.0% | 🔴 Large gap - generation challenges |
| Bbh Reasoning Abo... | 50.0% | 0.0% | +50.0% | 🔴 Large gap - generation challenges |
| Bbh Penguins In A... | 50.0% | 30.0% | +20.0% | 🔴 Large gap - generation challenges |
| Bbh Object Counting | 40.0% | 0.0% | +40.0% | 🔴 Large gap - generation challenges |
| Bbh Navigate | 70.0% | 40.0% | +30.0% | 🔴 Large gap - generation challenges |
| Bbh Movie Recomme... | 50.0% | 0.0% | +50.0% | 🔴 Large gap - generation challenges |
| Bbh Logical Deduc... | 60.0% | 40.0% | +20.0% | 🔴 Large gap - generation challenges |
| Bbh Logical Deduc... | 40.0% | 20.0% | +20.0% | 🔴 Large gap - generation challenges |
| Bbh Logical Deduc... | 20.0% | 10.0% | +10.0% | 🟡 Moderate gap - formatting issues possible |
| Bbh Hyperbaton | 60.0% | 60.0% | +0.0% | ✅ Consistent performance |
| Bbh Geometric Shapes | 50.0% | 0.0% | +50.0% | 🔴 Large gap - generation challenges |
| Bbh Formal Fallacies | 40.0% | 40.0% | +0.0% | ✅ Consistent performance |
| Bbh Disambiguatio... | 60.0% | 10.0% | +50.0% | 🔴 Large gap - generation challenges |
| Bbh Date Understa... | 40.0% | 20.0% | +20.0% | 🔴 Large gap - generation challenges |
| Bbh Causal Judgement | 40.0% | 60.0% | -20.0% | 🟢 Text generation outperforms - possible chance |
| Bbh Boolean Expre... | 80.0% | 50.0% | +30.0% | 🔴 Large gap - generation challenges |

**🔍 Key Insights**:
- **Positive gaps**: Benchmark (loglikelihood) scores higher than text generation
- **Negative gaps**: Text generation surprisingly outperforms benchmark
- **Large gaps**: Indicate model struggles with consistent text formatting
- **Small gaps**: Show good alignment between reasoning and generation abilities

### 📋 Per-Task Text Output Performance

*Based on 10 samples per task - results may vary with larger sample sizes*

| Task | Samples | Outputs | Correct | Accuracy | Performance |
| ---- | ------- | ------- | ------- | -------- | ----------- |
| Math Precalculus Hard | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Prealgebra Hard | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Num Theory Hard | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Intermediate Algebra | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Geometry Hard | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Counting And Prob Ha | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Math Algebra Hard | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Ifeval | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Musr Team Allocation | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Musr Object Placements | 10 | 10 | 4 | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| Musr Murder Mysteries | 10 | 10 | 5 | 50.0% | 🟡 **GOOD** |
| Mmlu Pro | 10 | 10 | 1 | 10.0% | 🔴 **NEEDS IMPROVEMENT** |
| Gpqa Extended | 10 | 10 | 1 | 10.0% | 🔴 **NEEDS IMPROVEMENT** |
| Gpqa Diamond | 10 | 10 | 3 | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| Gpqa Main | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Web Of Lies | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Tracking Shuffled Obj | 10 | 10 | 5 | 50.0% | 🟡 **GOOD** |
| Bbh Tracking Shuffled Obj | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Tracking Shuffled Obj | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Temporal Sequences | 10 | 10 | 3 | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Sports Understanding | 10 | 10 | 5 | 50.0% | 🟡 **GOOD** |
| Bbh Snarks | 10 | 10 | 6 | 60.0% | 🟡 **GOOD** |
| Bbh Salient Translation E | 10 | 10 | 3 | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Ruin Names | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Reasoning About Color | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Penguins In A Table | 10 | 10 | 3 | 30.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Object Counting | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Navigate | 10 | 10 | 4 | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Movie Recommendation | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Logical Deduction Thr | 10 | 10 | 4 | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Logical Deduction Sev | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Logical Deduction Fiv | 10 | 10 | 1 | 10.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Hyperbaton | 10 | 10 | 6 | 60.0% | 🟡 **GOOD** |
| Bbh Geometric Shapes | 10 | 10 | 0 | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Formal Fallacies | 10 | 10 | 4 | 40.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Disambiguation Qa | 10 | 10 | 1 | 10.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Date Understanding | 10 | 10 | 2 | 20.0% | 🔴 **NEEDS IMPROVEMENT** |
| Bbh Causal Judgement | 10 | 10 | 6 | 60.0% | 🟡 **GOOD** |
| Bbh Boolean Expressions | 10 | 10 | 5 | 50.0% | 🟡 **GOOD** |

### 📊 Text Output Accuracy by Task

```
Performance Distribution:

🟢 bbh snarks      │████████████████████████████████████████ │ 60.0
🟢 bbh hyperbaton  │████████████████████████████████████████ │ 60.0
🟢 bbh causal judg │████████████████████████████████████████ │ 60.0
🟢 musr murder mys │█████████████████████████████████        │ 50.0
🟢 bbh sports unde │█████████████████████████████████        │ 50.0
🟢 bbh boolean exp │█████████████████████████████████        │ 50.0
🟡 musr object pla │██████████████████████████               │ 40.0
🟡 bbh navigate    │██████████████████████████               │ 40.0
🟡 bbh formal fall │██████████████████████████               │ 40.0
🔴 gpqa diamond    │████████████████████                     │ 30.0
🔴 bbh temporal se │████████████████████                     │ 30.0
🔴 bbh salient tra │████████████████████                     │ 30.0
🔴 bbh penguins in │████████████████████                     │ 30.0
🔴 musr team alloc │█████████████                            │ 20.0
🔴 gpqa main       │█████████████                            │ 20.0
🔴 bbh web of lies │█████████████                            │ 20.0
🔴 bbh tracking sh │█████████████                            │ 20.0
🔴 bbh ruin names  │█████████████                            │ 20.0
🔴 bbh date unders │█████████████                            │ 20.0
🔴 mmlu pro        │██████                                   │ 10.0
🔴 gpqa extended   │██████                                   │ 10.0
🔴 bbh logical ded │██████                                   │ 10.0
🔴 bbh disambiguat │██████                                   │ 10.0
🔴 math precalculu │                                         │ 0.0
🔴 math prealgebra │                                         │ 0.0
🔴 math num theory │                                         │ 0.0
🔴 math intermedia │                                         │ 0.0
🔴 math geometry h │                                         │ 0.0
🔴 math counting a │                                         │ 0.0
🔴 math algebra ha │                                         │ 0.0
🔴 ifeval          │                                         │ 0.0
🔴 bbh reasoning a │                                         │ 0.0
🔴 bbh object coun │                                         │ 0.0
🔴 bbh movie recom │                                         │ 0.0
🔴 bbh geometric s │                                         │ 0.0
```

## 💡 Recommendations


### 🔬 **Evaluation Methodology Insights**

**📊 Understanding Score Differences**:
- **Loglikelihood scores** measure token probability optimization (what the model 'knows')
- **Text generation scores** measure actual output quality (what the model 'produces')
- **Sample consistency** consistent 10 samples per task ensures fair comparison

**🎯 Optimization Recommendations**:

**🔴 Low Performance (< 50%)**:
- Consider fine-tuning on task-specific datasets
- Improve prompt engineering and few-shot examples
- Evaluate if model size/capability is sufficient for these tasks
- Check if quantization significantly impacts performance

**📈 For More Reliable Evaluation**:
- Increase sample size from 10 to 50+ per task for more stable estimates
- Use multiple random seeds to assess variance across different sample sets
- Compare both loglikelihood and generation approaches for comprehensive assessment
- Consider domain-specific evaluation metrics beyond exact string matching
## 📖 Sample Analysis

*Detailed examples showing model performance on specific questions.*

### 📚 Leaderboard_Math_Precalculus_Hard

### 📝 Sample 1

#### ❓ Question
```text
Let $\mathbf{u}$ and $\mathbf{v}$ be vectors such that $\|\mathbf{u}\| = \|\mathbf{v}\| = 2$ and $\mathbf{u} \cdot \mathbf{v} = -1.$  If $\theta$ is the angle between the vectors $\mathbf{u} + \mathbf{v}$ and $2 \mathbf{u} - \mathbf{v},$ then find $\cos \theta.$
```

#### ✅ Expected Answer
**\frac{1}{4}**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `[ERROR: Could not decode response]`

💬 **Analysis:** The model responded with `[ERROR: Could not decode response]` but the correct answer is `\frac{1}{4}`.

---

### 📝 Sample 2

#### ❓ Question
```text
Let $M_n$ be the $n \times n$ matrix with entries as follows: for $1 \le i \le n$, $m_{i,i} = 10$; for $1 \le i \le n - 1$, $m_{i+1,i} = m_{i,i+1} = 3$; all other entries in $M_n$ are zero. Let $D_n$ be the determinant of matrix $M_n$. Find
\[\sum_{n=1}^{\infty} \frac{1}{8D_n+1}.\]Note: The determinant of the $1 \times 1$ matrix $[a]$ is $a$, and the determinant of the $2 \times 2$ matrix $\left[ {\begin{array}{cc}
a & b \\
c & d \\
\end{array} } \right] = ad - bc$; for $n \ge 2$, the determinant of an $n \times n$ matrix with first row or first column $a_1$ $a_2$ $a_3$ $\dots$ $a_n$ is equal to $a_1C_1 - a_2C_2 + a_3C_3 - \dots + (-1)^{n+1}a_nC_n$, where $C_i$ is the determinant of the $(n - 1) \times (n - 1)$ matrix formed by eliminating the row and column containing $a_i$.
```

#### ✅ Expected Answer
**\frac{1}{72}**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `[ERROR: Could not decode response]`

💬 **Analysis:** The model responded with `[ERROR: Could not decode response]` but the correct answer is `\frac{1}{72}`.

---

### 📚 Leaderboard_Math_Prealgebra_Hard

### 📝 Sample 1

#### ❓ Question
```text
John and Gary are playing a game. John spins a spinner numbered with integers from 1 to 20. Gary then writes a list of all of the positive factors of the number spun except for the number itself. Gary then creates a new spinner with all of the numbers on his list. John then spins this spinner, and the process continues. The game is over when the spinner has no numbers on it. If John spins a 20 on his first spin, what is the maximum number of total spins (including the one he already made) that John can make before the game is over?
```

#### ✅ Expected Answer
**4**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `[ERROR: Could not decode response]`

💬 **Analysis:** The model responded with `[ERROR: Could not decode response]` but the correct answer is `4`.

---

### 📝 Sample 2

#### ❓ Question
```text
A square and a regular heptagon  are coplanar and share a common side $\overline{AD}$, as shown. What is the degree measure of angle $BAC$?  Express your answer as a common fraction.

[asy]
for(int i=0; i <=7; ++i) {
draw(dir(360*i/7+90)--dir(360*(i+1)/7+90));
}
pair A = dir(360*3/7+90);
pair F = dir(360*4/7+90);
pair C = A+dir(90)*(F-A);
pair D = C+F-A;
pair B = dir(360*2/7+90);

draw(A--C--D--F);

label("$A$",A,S);
label("$B$",B,W);
label("$C$",C,SE);
label("$D$",F,S);

[/asy]
```

#### ✅ Expected Answer
**\frac{270}7\text{ degrees}**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `[ERROR: Could not decode response]`

💬 **Analysis:** The model responded with `[ERROR: Could not decode response]` but the correct answer is `\frac{270}7\text{ degrees}`.

---

### 📚 Leaderboard_Math_Num_Theory_Hard

### 📝 Sample 1

#### ❓ Question
```text
Compute $17^{-1}\pmod{83}$. Express your answer as a residue from $0$ to $82$, inclusive.

(You may find it helpful to consider the fact that $17\cdot 5=85$.)
```

#### ✅ Expected Answer
**44**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `[ERROR: Could not decode response]`

💬 **Analysis:** The model responded with `[ERROR: Could not decode response]` but the correct answer is `44`.

---

### 📝 Sample 2

#### ❓ Question
```text
What is the largest integer less than $2010$ that has a remainder of $5$ when divided by $7,$ a remainder of $10$ when divided by $11,$ and a remainder of $10$ when divided by $13$?
```

#### ✅ Expected Answer
**1440**

#### 🤖 Model Output (❌ Incorrect)

**Response:** `[ERROR: Could not decode response]`

💬 **Analysis:** The model responded with `[ERROR: Could not decode response]` but the correct answer is `1440`.

---

---

## 📋 Report Information

**Generated by:** LLM Evaluation Framework v2.0
**Timestamp:** 2025-10-09T15:33:29.004659
**Framework:** Professional Report Generator

*This report provides a comprehensive analysis of model performance across various evaluation tasks.*
*For technical details, refer to the accompanying JSON results file.*