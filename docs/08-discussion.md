# 08 — Discussion

## 1. Evolution of the Approach

The project evolved from a conventional reconstruction-based anomaly detector toward a more feature-aware system.

The major progression is:

```text
Baseline
  ↓
Robust preprocessing
  ↓
Magnitude transformation
  ↓
Attack-specific diagnostics
  ↓
Feature separability analysis
  ↓
Threshold calibration
  ↓
Bottleneck revision
  ↓
Feature-aware loss
```

## 2. V7 Interpretation

V7 revisits the latent representation capacity of the Deep Autoencoder.

The Deep bottleneck changes from 4 to 12.

This tests the hypothesis that the V6 bottleneck was too restrictive.

## 3. V8 Interpretation

V8 addresses a different question:

> Should every feature contribute equally to the reconstruction objective?

The answer tested experimentally is no: features with stronger measured normal-vs-attack separation receive greater weights.

This is a hypothesis-driven change rather than an arbitrary architecture modification.

## 4. Selective Log Transformation

V8 also challenges the assumption that every feature benefits from log transformation.

Only features with absolute training skewness above 1.0 are transformed.

This attempts to preserve information in features whose distributions do not require strong compression.

## 5. Main Methodological Risk

The feature weights are calculated using attack data.

Consequently, V8 is no longer a purely unsupervised training procedure.

This must be stated explicitly in any paper or presentation.

## 6. Calibration Leakage Risk

V6–V8 reuse attack samples involved in threshold calibration during final evaluation.

For rigorous publication results, calibration and evaluation attack samples should be disjoint.

## 7. Ablation Study

The recommended next experiment is:

| Experiment | Log | Weighted Loss | Threshold |
|---|---|---|---|
| A | All-feature log | No | F1 |
| B | Selective log | No | F1 |
| C | Selective log | Yes | F1 |

A second useful control is:

```text
Selective log + weighted loss + P99 threshold
```

This separates the contribution of the loss from the threshold strategy.

## 8. Final Model Selection

The best model should not be selected using Recall alone.

The decision should consider:

- Recall
- Precision
- F1
- ROC-AUC
- attack-family consistency
- false-positive behavior
- calibration protocol
- computational cost
- methodological validity

## 9. Practical Conclusion

The central contribution of the iterative work is not merely changing Autoencoder depth. It is progressively identifying where the anomaly-detection pipeline loses information:

- preprocessing;
- representation compression;
- threshold selection;
- feature separability;
- feature contribution to reconstruction error.
