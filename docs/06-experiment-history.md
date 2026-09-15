# 06 — Experiment History

This is the central explanation of what changed, why it changed, and what should be tested next.

## V1 — Baseline Autoencoders

### What changed
Initial Shallow and Deep autoencoders.

### Configuration
- StandardScaler
- normal-only P99 threshold
- Shallow bottleneck 16
- Deep bottleneck 8

### Why V2
Extreme values can distort scaling.

---

## V2 — Robust Preprocessing

### What changed
- train-derived clipping
- RobustScaler

### Why
Reduce sensitivity to extreme values and heavy tails.

---

## V3 — Signed Log Transformation

### What changed
Signed `log1p`.

### Why
Compress large magnitudes and reduce skew.

---

## V4 — Per-Attack Evaluation

### What changed
Metrics are calculated for individual attack families.

### Why
Aggregate metrics can hide family-specific failures.

---

## V5 — Feature Separability Diagnostic

### What changed
Cohen's-d-style comparison between normal and each attack family.

### Why
Determine whether weak detection is related to weak feature information.

Diagnostic only; it does not modify training.

---

## V6 — Bottleneck + F1 Threshold

### What changed
- Shallow 16 → 8
- Deep 8 → 4
- P99 → F1-calibrated threshold

### Problem
Two variables changed simultaneously, so a direct causal claim is not valid.

### Required 2×2 ablation

| Experiment | Bottleneck | Threshold |
|---|---|---|
| A | Old | P99 |
| B | New | P99 |
| C | Old | F1 |
| D | New | F1 |

---

## V7 — Deep Bottleneck Adjustment

### What changed
Deep bottleneck 4 → 12.

### Why
Test whether the V6 representation was over-compressed.

---

## V8 — Feature-Aware Reconstruction

### What changed
1. Selective log transformation based on skewness.
2. Cohen's-d-style feature weights.
3. Weighted reconstruction loss.
4. Weighted anomaly score.

### Problem
Log policy and loss objective changed together.

### Required 2×2 ablation

| Experiment | Log Policy | Loss |
|---|---|---|
| A | All-log | MSE |
| B | Selective-log | MSE |
| C | All-log | Weighted MSE |
| D | Selective-log | Weighted MSE |

---

## V9 — Score-Level Ensemble

### What changed
Shallow and Deep scores are normalized and averaged.

```text
Ensemble =
0.5*(ShallowScore/ShallowThreshold)
+
0.5*(DeepScore/DeepThreshold)
```

The ensemble gets its own F1-calibrated threshold.

### Why
Exploit complementary model behavior without merging latent representations.

## Final evolution

```text
V1 Baseline
 ↓
V2 Robust preprocessing
 ↓
V3 Log compression
 ↓
V4 Family-level evaluation
 ↓
V5 Feature separability
 ↓
V6 Bottleneck + threshold
 ↓
V7 Deep bottleneck
 ↓
V8 Feature-aware loss
 ↓
V9 Score ensemble
```
