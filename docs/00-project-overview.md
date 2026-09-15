# 00 — Project Overview

## Purpose

The project develops an autoencoder-based network anomaly detector using CICIDS-2017 network-flow data. Autoencoders learn reconstruction behavior from normal traffic, and reconstruction error is used as the anomaly score.

## V1 → V9 pipeline

```text
V1 Baseline Autoencoders
        ↓
V2 Clipping + RobustScaler
        ↓
V3 Signed Log Transformation
        ↓
V4 Per-Attack Evaluation
        ↓
V5 Feature Separability Diagnostic
        ↓
V6 Bottleneck Changes + F1 Threshold
        ↓
V7 Deep Bottleneck Adjustment
        ↓
V8 Selective Log + Feature-Weighted Loss
        ↓
V9 Score-Level Ensemble
```

## Version map

### V1
Baseline:
- StandardScaler
- normal-validation P99 threshold
- Shallow bottleneck 16
- Deep bottleneck 8

### V2
Robust preprocessing:
- train-derived clipping
- RobustScaler

### V3
Distribution transformation:
- signed `log1p`

### V4
Evaluation improvement:
- per-attack-family metrics

### V5
Diagnostic improvement:
- Cohen's-d-style feature separability

### V6
Representation and threshold:
- Shallow 16 → 8
- Deep 8 → 4
- P99 → F1-calibrated threshold

### V7
Deep representation:
- Deep 4 → 12

### V8
Feature-aware learning:
- selective log based on skewness
- Cohen's-d-style feature weights
- weighted reconstruction loss
- weighted anomaly score

### V9
Score-level ensemble:
- Shallow score
- Deep score
- normalized fusion
- separate ensemble threshold

## Scientific characterization

V8/V9 should not be described as purely unsupervised because attack labels contribute to feature-weight construction and threshold calibration. The autoencoder itself is trained on normal traffic.

## Main validity issues

- V6 changes bottleneck and threshold simultaneously.
- V8 changes log policy and loss simultaneously.
- Calibration attack samples may overlap final evaluation.
- Normal splitting is randomized rather than chronological.
- A single seed is insufficient for strong variance claims.
