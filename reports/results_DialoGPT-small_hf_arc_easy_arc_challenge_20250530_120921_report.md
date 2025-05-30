# Evaluation Report: microsoft/DialoGPT-small
Generated on 2025-05-30 14:09:34

## Model Configuration

| Parameter | Value |
| --------- | ----- |
| Model | pretrained=microsoft/DialoGPT-small |

## Task Category Performance Summary

| Category | Task | Score |
| -------- | ---- | ----- |

## Detailed Metrics

| Task | Metric | Value |
| ---- | ------ | ----- |
| arc_challenge | acc,none | 0.1333 |
| arc_challenge | acc_norm,none | 0.1333 |
| arc_easy | acc,none | 0.4000 |
| arc_easy | acc_norm,none | 0.2000 |

## Normalized Scores

| Benchmark | Score |
| --------- | ----- |
| *No normalized scores found* | - |

# Task Samples

## arc_challenge

### Sample 1

**Question:**

An astronomer observes that a planet rotates faster after a meteorite impact. Which is the most likely effect of this increase in rotation?

**Choices:**

```
{'text': ['Planetary density will decrease.', 'Planetary years will become longer.', 'Planetary days will become shorter.', 'Planetary gravity will become stronger.'], 'label': ['A', 'B', 'C', 'D']}
```

**Model Response [none]:**

```
[-36.09375, False]
```

---

### Sample 2

**Question:**

A group of engineers wanted to know how different building designs would respond during an earthquake. They made several models of buildings and tested each for its ability to withstand earthquake conditions. Which will most likely result from testing different building designs?

**Choices:**

```
{'text': ['buildings will be built faster', 'buildings will be made safer', 'building designs will look nicer', 'building materials will be cheaper'], 'label': ['A', 'B', 'C', 'D']}
```

**Model Response [none]:**

```
[-20.8125, False]
```

---

## arc_easy

### Sample 1

**Question:**

Which statement best explains why photosynthesis is the foundation of most food webs?

**Choices:**

```
{'text': ['Sunlight is the source of energy for nearly all ecosystems.', 'Most ecosystems are found on land instead of in water.', 'Carbon dioxide is more available than other gases.', 'The producers in all ecosystems are plants.'], 'label': ['A', 'B', 'C', 'D']}
```

**Model Response [none]:**

```
[-51.0, False]
```

---

### Sample 2

**Question:**

Which piece of safety equipment is used to keep mold spores from entering the respiratory system?

**Choices:**

```
{'text': ['safety goggles', 'breathing mask', 'rubber gloves', 'lead apron'], 'label': ['A', 'B', 'C', 'D']}
```

**Model Response [none]:**

```
[-14.7421875, False]
```

---
