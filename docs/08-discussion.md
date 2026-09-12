# Discussion

## 1. Evolution

The first six versions form the following progression:

```text
V1: Baseline
 ↓
V2: Extreme-value control
 ↓
V3: Heavy-tail compression
 ↓
V4: Attack-family evaluation
 ↓
V5: Feature-level separability diagnostic
 ↓
V6: Latent compression + threshold calibration
```

## 2. Preprocessing

V2 and V3 indicate that network-flow feature distributions require explicit numerical treatment.

The current preprocessing pipeline is:

- train-derived clipping;
- signed log1p;
- RobustScaler.

## 3. Feature Separability

V5 adds an important diagnostic layer.

If an attack family has weak separation from normal traffic in the selected feature representation, changing the Autoencoder may not solve the information limitation.

This makes feature-level analysis useful before increasing model complexity.

## 4. Bottleneck Compression

V6 reduces latent dimensions.

The hypothesis is that a tighter bottleneck may force the model to encode only the most characteristic structure of normal traffic.

However, excessive compression can also harm reconstruction of legitimate normal traffic.

## 5. Threshold Calibration

V1–V5 use a normal-only P99 threshold.

V6 uses a small labeled calibration set to optimize F1.

This provides a task-oriented operating point but changes the experimental setting.

The correct terminology is:

> Autoencoder anomaly detection with semi-supervised threshold calibration.

## 6. V6 Confounding

V6 changes both bottleneck size and threshold strategy.

Therefore a V6 performance change cannot be assigned to either factor alone.

A four-condition ablation would isolate the effects.

## 7. Calibration/Test Separation

V6 currently reuses calibration attack records during final evaluation.

This should be corrected in a later version by separating calibration and final attack-test subsets.

## 8. Practical Selection

Final model selection should consider more than F1:

- false-positive rate;
- attack recall;
- per-attack performance;
- ROC-AUC;
- threshold stability;
- computational cost.

## 9. Current Scientific Position

V1–V6 provide a traceable evolution of the pipeline. Final conclusions must wait for verified numerical results.
