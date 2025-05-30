# Evaluation Report: mistralai/Mistral-7B-v0.1
Generated on 2025-05-30 15:06:56

## Model Configuration

| Parameter | Value |
| --------- | ----- |
| Model | pretrained=mistralai/Mistral-7B-v0.1 |

## Task Category Performance Summary


**OVERALL SCORE: 16.67**

| Category | Task | Score |
| -------- | ---- | ----- |
| **LEADERBOARD** | | |
| leaderboard | mmlu_pro | 16.67 |
| **OVERALL** | **Average** | **16.67** |

## Detailed Metrics

| Task | Metric | Value |
| ---- | ------ | ----- |
| leaderboard_mmlu_pro | acc,none | 0.2500 |

## Normalized Scores

| Benchmark | Score |
| --------- | ----- |
| normalized_leaderboard_mmlu_pro | 16.67 |
| normalized_overall_average | 16.67 |

# Task Samples

## leaderboard_mmlu_pro

### Sample 1

**Question:**

Typical advertising regulatory bodies suggest, for example that adverts must not: encourage _________, cause unnecessary ________ or _____, and must not cause _______ offence.

**Choices:**

```
Safe practices, Fear, Jealousy, Trivial
Unsafe practices, Distress, Joy, Trivial
Safe practices, Wants, Jealousy, Trivial
Safe practices, Distress, Fear, Trivial
Unsafe practices, Wants, Jealousy, Serious
Safe practices, Distress, Jealousy, Serious
Safe practices, Wants, Fear, Serious
Unsafe practices, Wants, Fear, Trivial
Unsafe practices, Distress, Fear, Serious
```

**Model Response [none]:**

```
[-2.859375, False]
```

---

### Sample 2

**Question:**

Managers are entrusted to run the company in the best interest of ________. Specifically, they have a duty to act for the benefit of the company, as well as a duty of ________ and of _______.

**Choices:**

```
Shareholders, Diligence, Self-interest
Shareholders, Self-interest, Care and Skill
Stakeholders, Care and skill, Self-interest
Stakeholders, Diligence, Care and Skill
Customers, Care and Skill, Diligence
Shareholders, Care and Skill, Diligence
Shareholders, Self-interest, Diligence
Employees, Care and Skill, Diligence
Stakeholders, Self-interest, Diligence
Stakeholder, Care and Skill, Diligence
```

**Model Response [none]:**

```
[-3.390625, False]
```

---
