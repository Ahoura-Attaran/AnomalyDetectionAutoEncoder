# 08 — Discussion

## Overall evolution

The project moves from a basic reconstruction detector to a feature-aware score ensemble.

- V1 establishes the baseline.
- V2 improves numerical robustness.
- V3 addresses skew/extreme magnitudes.
- V4 exposes family-specific performance.
- V5 studies feature separability.
- V6 changes representation compression and threshold strategy.
- V7 tests a larger Deep representation.
- V8 introduces feature-aware preprocessing and reconstruction.
- V9 combines complementary anomaly scores.

## Feature weighting

Feature weights emphasize dimensions with stronger attack/normal separation.

This may align reconstruction with informative dimensions, but it uses attack labels and therefore changes the method's scientific characterization.

## Threshold calibration

F1 calibration directly optimizes a classification objective and may improve the practical decision boundary compared with fixed P99.

The trade-off is dependence on labeled attack examples.

## Ensemble

V9 performs score-level fusion after independent model inference. It does not merge latent representations.

## Threats to validity

- calibration/test overlap
- V6 confounding
- V8 confounding
- random rather than chronological splitting
- single-seed evaluation
- metric-selection bias

## Recommended final protocol

1. Fit preprocessing using training data.
2. Train autoencoders on normal training traffic.
3. Separate calibration data.
4. Keep final test data untouched.
5. Calibrate thresholds only on calibration data.
6. Repeat with multiple seeds.
7. Add chronological evaluation.
8. Report ROC-AUC, PR-AUC, Precision, Recall, F1 and FPR.
9. Report every attack family.
10. Preserve V1→V9 as the experimental history.
