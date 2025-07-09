# 🚀 LLM Evaluation Report
## mistralai/Ministral-8B-Instruct-2410

📅 **Generated:** July 09, 2025 at 09:57:51
🏷️ **Report ID:** 20250709-075751

---

## 📋 Executive Summary

🎯 **Overall Performance:** 🔴 **NEEDS IMPROVEMENT**
📊 **Average Score:** 49.5%
📈 **Best Performance:** 100.0%
📉 **Lowest Performance:** 0.0%
📏 **Score Range:** 100.0 points

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
| leaderboard_bbh_boolean_expressions | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_causal_judgement | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_date_understanding | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_disambiguation_qa | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_formal_fallacies | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_geometric_shapes | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_hyperbaton | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_logical_deduction_five_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_logical_deduction_seven_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_logical_deduction_three_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_movie_recommendation | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_navigate | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_object_counting | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_penguins_in_a_table | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_reasoning_about_colored_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_ruin_names | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_salient_translation_error_detection | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_snarks | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_sports_understanding | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_temporal_sequences | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_tracking_shuffled_objects_five_objects | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_seven_objects | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_bbh_tracking_shuffled_objects_three_objects | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_bbh_web_of_lies | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_gpqa_diamond | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_gpqa_extended | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_gpqa_main | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_ifeval | prompt_level_strict_acc,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | inst_level_strict_acc,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | prompt_level_loose_acc,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_ifeval | inst_level_loose_acc,none | 33.3% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_algebra_hard | exact_match,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_math_counting_and_prob_hard | exact_match,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_math_geometry_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_intermediate_algebra_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_num_theory_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_prealgebra_hard | exact_match,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_math_precalculus_hard | exact_match,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_mmlu_pro | acc,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |
| leaderboard_musr_murder_mysteries | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_musr_object_placements | acc_norm,none | 100.0% | 🟢 **EXCELLENT** |
| leaderboard_musr_team_allocation | acc_norm,none | 0.0% | 🔴 **NEEDS IMPROVEMENT** |

### 📊 Task Performance Comparison

```
Performance Distribution:

🟢 leaderboard     │████████████████████████████████████████ │ 48.4
```

## 💡 Recommendations

🔧 **Performance Enhancement Needed**
- Current performance below optimal levels
- Consider larger model variants or fine-tuning
- Evaluate prompt engineering strategies
- Test with different generation parameters

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

#### ✅ Correct Answer
**I**

#### 🤖 Model Response (❌ Incorrect)
**[-2.53125, False]**

---

### 📚 Leaderboard_Bbh_Boolean_Expressions

### 📝 Sample 1

#### ❓ Question
```text
not ( True ) and ( True ) is
```

#### ✅ Correct Answer
**False**

#### 🤖 Model Response (❌ Incorrect)
**[-0.212890625, True]**

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

#### ✅ Correct Answer
**No**

#### 🤖 Model Response (❌ Incorrect)
**[-0.64453125, True]**

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

#### ✅ Correct Answer
**(B)**

#### 🤖 Model Response (❌ Incorrect)
**[-3.46875, False]**

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

#### ✅ Correct Answer
**(A)**

#### 🤖 Model Response (❌ Incorrect)
**[-2.78125, False]**

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

#### ✅ Correct Answer
**invalid**

#### 🤖 Model Response (❌ Incorrect)
**[-0.54296875, True]**

---

---

## 📋 Report Information

**Generated by:** LLM Evaluation Framework v2.0
**Timestamp:** 2025-07-09T07:57:51.336259
**Framework:** Professional Report Generator

*This report provides a comprehensive analysis of model performance across various evaluation tasks.*
*For technical details, refer to the accompanying JSON results file.*