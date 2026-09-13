# 07 — Results and Analysis

## 1. Purpose

This document records numerical results only after actual execution of the corresponding version.

No metric is fabricated here.

## 2. Required Comparison

The main comparison should include:

| Version | Shallow F1 | Shallow AUC | Deep F1 | Deep AUC |
|---|---:|---:|---:|---:|
| V1 | — | — | — | — |
| V2 | — | — | — | — |
| V3 | — | — | — | — |
| V4 | — | — | — | — |
| V5 | — | — | — | — |
| V6 | — | — | — | — |
| V7 | — | — | — | — |
| V8 | — | — | — | — |

## 3. Attack-Level Analysis

For V8, record:

| Attack | Recall | Precision | F1 | AUC | N |
|---|---:|---:|---:|---:|---:|
| Bruteforce | — | — | — | — | — |
| DoS | — | — | — | — | — |
| WebAttacks | — | — | — | — | — |
| Botnet | — | — | — | — | — |
| DDoS | — | — | — | — | — |
| Portscan | — | — | — | — | — |

## 4. Feature-Weight Analysis

V8 should additionally record:

- number of skewed features;
- threshold used for skewness;
- minimum feature weight;
- maximum feature weight;
- top weighted features;
- Cohen's d values used to construct weights.

## 5. Interpretation Rules

A higher Recall means fewer attacks are missed.

A higher Precision means fewer normal samples are incorrectly classified as attacks.

F1 summarizes Precision and Recall.

ROC-AUC evaluates ranking/separation based on reconstruction score and is independent of the chosen threshold.

## 6. Important Scientific Question

If V8 improves metrics, the documentation must determine whether the improvement is caused by:

- selective log transformation;
- feature weighting;
- threshold behavior;
- or a combination.

A single V8-vs-V7 comparison cannot isolate these causes.
