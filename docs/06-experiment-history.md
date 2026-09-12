# Experiment History

The project is documented as an experimental sequence:

```text
Version → Problem → Change → Result → Decision
```

Results are added only from actual execution output.

## V1 — Baseline

### Change
Initial Autoencoder pipeline using `StandardScaler`.

### Configuration
- 70/15/15 normal split
- Shallow bottleneck 16
- Deep bottleneck 8
- Normal-validation P99 threshold
- Global Normal vs Attack evaluation

### Problem Identified
Extreme values could distort scaling and reconstruction loss.

---

## V2 — Clipping + RobustScaler

### Problem
Extreme finite values could strongly influence feature scaling.

### Change
- Train-derived 0.001/0.999 percentile clipping
- `RobustScaler`

### Controlled Components
Model architecture, optimizer, loss, callbacks, split, and threshold method remained unchanged.

### Classification
Preprocessing experiment.

---

## V3 — Signed Log1p

### Problem
Highly skewed and zero-inflated rate features could retain a large dynamic range even after robust scaling and clipping.

### Change
Added:

\[
x'=sign(x)\log(1+|x|)
\]

before RobustScaler.

### Controlled Components
Autoencoder architecture and threshold strategy remained unchanged.

### Classification
Preprocessing refinement.

---

## V4 — Per-Attack-Type Evaluation

### Problem
A single aggregate attack metric could hide differences between attack families.

### Change
Added per-attack evaluation for:

- BruteForce
- DoS
- WebAttacks
- Botnet
- DDoS
- PortScan

with Recall, Precision, F1, AUC, and sample count.

### Classification
Evaluation refinement.

---

## V5 — Model-Independent Feature-Separation Diagnostic

### Problem
A weak attack-detection result could originate from the model, threshold, or insufficient information in the selected features.

### Change
Added:

```python
analyze_feature_separation(...)
```

The function operates before model training and compares transformed normal and attack feature means using a standardized difference equivalent to a Cohen's-d-style effect size.

### Purpose
Determine whether an attack family has strong feature-level separation from normal traffic before changing model architecture.

### Controlled Components
The V3 preprocessing, model architectures, P99 threshold, and evaluation strategy remained unchanged.

### Classification
Data-level diagnostic experiment.

---

## V6 — Tighter Bottlenecks + Semi-Supervised Threshold Calibration

### Problems
V6 addresses two separate concerns:

1. The normal-only P99 threshold may not provide the desired precision/recall operating point.
2. A larger bottleneck may reconstruct patterns that should ideally receive higher anomaly errors.

### Change A — Threshold
A small labeled sample from each attack family is used only for threshold calibration.

Up to 2,000 samples per attack family are used.

The threshold maximizing F1 on the calibration set is selected.

The previous normal-only P99 threshold is also calculated as a reference.

### Change B — Bottleneck
| Model | Previous | V6 |
|---|---:|---:|
| Shallow | 16 | 8 |
| Deep | 8 | 4 |

### What Stayed Fixed
- cleaning
- train/validation/test split
- clipping
- signed log1p
- RobustScaler
- optimizer
- loss
- callbacks
- global evaluation
- per-attack evaluation

### Scientific Interpretation
V6 is a combined **model-capacity + decision-threshold experiment**.

Because two important variables changed simultaneously, a performance difference cannot be causally attributed to only the bottleneck or only the threshold.

A future ablation should test:

```text
A: Old bottleneck + P99
B: New bottleneck + P99
C: Old bottleneck + F1 threshold
D: New bottleneck + F1 threshold
```

### Limitation
Calibration attack samples are not removed from the final evaluation datasets in V6. This creates calibration/test overlap for threshold-dependent metrics.

---

## Version Comparison

| Version | Main Change | Category | Shallow Bottleneck | Deep Bottleneck | Threshold |
|---|---|---|---:|---:|---|
| V1 | StandardScaler | Preprocessing | 16 | 8 | Normal P99 |
| V2 | Clipping + RobustScaler | Preprocessing | 16 | 8 | Normal P99 |
| V3 | Signed log1p | Preprocessing | 16 | 8 | Normal P99 |
| V4 | Per-attack evaluation | Evaluation | 16 | 8 | Normal P99 |
| V5 | Feature-separation diagnostic | Data diagnostic | 16 | 8 | Normal P99 |
| V6 | Bottleneck reduction + F1 calibration | Model + Threshold | 8 | 4 | Semi-supervised F1 |
| V7 | Pending | Pending | — | — | — |
| V8 | Pending | Pending | — | — | — |
| V9 | Pending | Pending | — | — | — |

## Experimental-Control Note

V1–V5 each have a dominant experimental change.

V6 changes two major variables simultaneously. This is acceptable as an iterative engineering step, but the limitation should be explicitly acknowledged in the research methodology.
