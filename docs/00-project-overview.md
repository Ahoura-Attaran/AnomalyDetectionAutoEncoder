# CICIDS2017 Network Anomaly Detection Using Autoencoders

## 1. Project Overview

This project investigates network anomaly detection using Autoencoders trained on benign network traffic. The objective is to learn the reconstruction pattern of normal traffic and identify anomalous traffic through reconstruction error.

The implementation is developed as an iterative experimental pipeline so that preprocessing, model architecture, thresholding, and evaluation decisions remain traceable.

## 2. Problem Definition

The detection task is formulated as binary anomaly detection:

- `0` = Normal
- `1` = Attack

The Autoencoder is trained on normal traffic. Individual attack families are mainly used for evaluation. From V6, a small labeled sample of each attack family is additionally used only for threshold calibration.

## 3. Experimental Dataset

The implementation loads:

| Group | File |
|---|---|
| Normal | `Benign-Monday-no-metadata.parquet` |
| Brute Force | `Bruteforce-Tuesday-no-metadata.parquet` |
| DoS | `DoS-Wednesday-no-metadata.parquet` |
| Web Attacks | `WebAttacks-Thursday-no-metadata.parquet` |
| Botnet | `Botnet-Friday-no-metadata.parquet` |
| DDoS | `DDoS-Friday-no-metadata.parquet` |
| PortScan | `Portscan-Friday-no-metadata.parquet` |

## 4. Pipeline Through V6

```text
Data loading
   ↓
Cleaning
   ↓
Constant-feature removal
   ↓
Normal Train / Validation / Test split
   ↓
Train-derived percentile clipping
   ↓
Signed log1p transformation
   ↓
RobustScaler
   ↓
Autoencoder trained on normal data
   ↓
Reconstruction error
   ↓
Threshold calibration
   ↓
Global + per-attack evaluation
```

## 5. Model Families

Two Autoencoders are maintained:

- Shallow Autoencoder
- Deep Autoencoder

The initial bottlenecks were 16 and 8 dimensions. V6 reduces them to 8 and 4 dimensions.

## 6. Experimental Evolution

| Version | Main contribution |
|---|---|
| V1 | StandardScaler baseline |
| V2 | Train-based clipping + RobustScaler |
| V3 | Signed log1p transformation |
| V4 | Per-attack-type evaluation |
| V5 | Model-independent feature-separation diagnostic |
| V6 | Semi-supervised threshold calibration + tighter bottlenecks |
| V7 | Pending |
| V8 | Pending |
| V9 | Pending |

## 7. Reproducibility

```python
SEED = 42
```

NumPy and TensorFlow seeds are initialized.

## 8. Scientific Status

V1–V6 define an increasingly refined methodology. Numerical superiority between versions must be established from actual execution results, not inferred from source code.
