# CICIDS2017 Network Anomaly Detection Using Autoencoders

## 1. Project Overview

This project investigates network anomaly detection on CICIDS2017-derived flow data using Autoencoder-based models.

The main objective is to learn the representation of **normal network traffic** and identify anomalous traffic through reconstruction error.

The project has evolved incrementally from a baseline Autoencoder (V1) to a feature-aware, semi-supervised-threshold-calibrated approach (V8).

## 2. Experimental Data

The implementation uses processed Parquet files grouped into:

- Benign-Monday-no-metadata.parquet
- Bruteforce-Tuesday-no-metadata.parquet
- DoS-Wednesday-no-metadata.parquet
- WebAttacks-Thursday-no-metadata.parquet
- Botnet-Friday-no-metadata.parquet
- DDoS-Friday-no-metadata.parquet
- Portscan-Friday-no-metadata.parquet

The project treats the Benign dataset as the source of normal traffic for Autoencoder training, validation, and normal testing. Attack datasets are used for anomaly evaluation and, from V6 onward, for threshold calibration.

## 3. Main Pipeline

1. Load Parquet datasets.
2. Remove/align invalid observations.
3. Remove constant features.
4. Split normal data into train/validation/test.
5. Compute training-only outlier clipping bounds.
6. Transform skewed features.
7. Fit RobustScaler on training data.
8. Perform feature-separation analysis using Cohen's d.
9. Train Shallow and Deep Autoencoders.
10. Calculate reconstruction error.
11. Select an anomaly threshold.
12. Evaluate globally and separately for each attack family.
13. Compare model behavior.

## 4. Model Families

Two Autoencoders are evaluated:

- Shallow Autoencoder
- Deep Autoencoder

The architecture and bottleneck size were changed experimentally across versions.

## 5. Evolution

| Version | Main change |
|---|---|
| V1 | Baseline AE, StandardScaler, normal-only P99 threshold |
| V2 | Train-only clipping + RobustScaler |
| V3 | Signed log1p transformation |
| V4 | Per-attack-type evaluation |
| V5 | Feature-separation diagnostic using Cohen's d |
| V6 | Bottleneck compression + F1-based semi-supervised threshold calibration |
| V7 | Deep bottleneck changed from 4 to 12 |
| V8 | Selective log transform + Cohen's-d-based feature-weighted MSE |

## 6. Scientific Characterization

The model is trained primarily in an unsupervised manner using normal traffic. From V6 onward, labeled attack samples are used only for threshold calibration, not for updating Autoencoder weights.

V8 additionally uses attack/normal feature-separation information to construct feature weights for the reconstruction loss. Therefore V8 should be described carefully as an Autoencoder with **feature-aware supervised information in the training objective**, rather than as a purely unsupervised Autoencoder.

## 7. Reproducibility

The code uses:

```python
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
```

Experimental outputs and metrics should be recorded without inventing values when an execution result is unavailable.
