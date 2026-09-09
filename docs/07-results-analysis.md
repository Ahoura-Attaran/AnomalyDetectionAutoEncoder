# Results Analysis

## 1. Purpose

This document is reserved for quantitative analysis of the experiments.

Unlike the experiment-history document, which records implementation changes, this document will interpret the measured results.

## 2. Required Result Table

For every completed version, the following table should eventually be populated:

| Version | Model | Precision | Recall | F1 | ROC-AUC | Notes |
|---|---|---:|---:|---:|---:|---|
| V1 | Shallow | — | — | — | — | Baseline |
| V1 | Deep | — | — | — | — | Baseline |
| V2 | Shallow | — | — | — | — | Clipping + RobustScaler |
| V2 | Deep | — | — | — | — | Clipping + RobustScaler |
| V3 | Shallow | — | — | — | — | + Signed log1p |
| V3 | Deep | — | — | — | — | + Signed log1p |
| V4 | Shallow | — | — | — | — | Per-attack diagnostics |
| V4 | Deep | — | — | — | — | Per-attack diagnostics |

## 3. Per-Attack Results

From V4 onward, attack-specific results should be recorded separately:

| Version | Model | Attack | Recall | Precision | F1 | AUC |
|---|---|---|---:|---:|---:|---:|
| V4 | Shallow | BruteForce | — | — | — | — |
| V4 | Shallow | DoS | — | — | — | — |
| V4 | Shallow | WebAttacks | — | — | — | — |
| V4 | Shallow | Botnet | — | — | — | — |
| V4 | Shallow | DDoS | — | — | — | — |
| V4 | Shallow | PortScan | — | — | — | — |
| V4 | Deep | BruteForce | — | — | — | — |
| V4 | Deep | DoS | — | — | — | — |
| V4 | Deep | WebAttacks | — | — | — | — |
| V4 | Deep | Botnet | — | — | — | — |
| V4 | Deep | DDoS | — | — | — | — |
| V4 | Deep | PortScan | — | — | — | — |

## 4. Interpretation Framework

For each experiment, analysis should answer:

- Did the overall detection performance improve?
- Did false positives decrease?
- Did false negatives decrease?
- Did ROC-AUC improve?
- Which attack types improved?
- Which attack types became worse?
- Did the change solve the original problem?
- Did it introduce a new problem?

## 5. Important Rule

No numerical result should be entered into this document unless it comes from an actual experiment output, saved result, or execution log.

## 6. V1–V4 Current State

At this stage, the source files establish the methodology and implementation changes, but no execution-result dataset is available in the current documentation set.

Therefore quantitative conclusions are intentionally left open.
