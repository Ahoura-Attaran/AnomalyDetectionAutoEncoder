# CICIDS2017 Network Anomaly Detection Using Autoencoders

**Project Documentation — Stage 1: Project Overview**

---

## 1. Project Overview

This project investigates the use of **Autoencoder-based anomaly detection** for identifying malicious network traffic in the CICIDS2017 intrusion detection dataset.

The main idea is to train an Autoencoder primarily on **benign network traffic** and learn a compact representation of normal network behavior. After training, the model reconstructs previously unseen network flows. The reconstruction error is then used as an anomaly score:

* Low reconstruction error → behavior similar to normal traffic
* High reconstruction error → behavior potentially associated with an attack

The project does not rely only on a single Autoencoder configuration. Multiple model architectures and preprocessing strategies have been investigated through a sequence of experimental versions. The purpose of this iterative process is to determine which combination of preprocessing, architecture, threshold selection, and evaluation strategy provides the most reliable anomaly detection performance.

The project therefore has two complementary goals:

1. Develop an effective Autoencoder-based anomaly detection pipeline.
2. Document and analyze the evolution of the methodology from the initial implementation to the final version.

---

## 2. Problem Statement

Traditional supervised intrusion detection systems require labeled examples of attacks during model training.

This can create a limitation in practical environments because:

* New attack types may not be available in the training dataset.
* The number of possible attack patterns is potentially very large.
* A model trained specifically for known attack classes may have difficulty detecting previously unseen behavior.

An alternative approach is to model **normal network behavior** and identify observations that significantly deviate from this learned representation.

In this project, an Autoencoder is used for this purpose.

The model is trained using benign traffic and learns to reconstruct the input features. The reconstruction error is subsequently used as an anomaly score.

Formally, for an input vector

$$
x \in \mathbb{R}^{d}
$$

the Autoencoder consists of an encoder and decoder:

$$
z = f_{\theta}(x)
$$

$$
\hat{x} = g_{\phi}(z)
$$

where:

* \(x\) is the original network-flow feature vector,
* \(z\) is the latent representation,
* \(\hat{x}\) is the reconstructed feature vector,
* \(f_{\theta}\) represents the encoder,
* \(g_{\phi}\) represents the decoder.

The reconstruction error is calculated as:

$$
E(x)=\frac{1}{d}\sum_{i=1}^{d}(x_i-\hat{x}_i)^2
$$

A threshold \(T\) is then used to determine whether a flow is considered anomalous:

$$
\text{Prediction}(x)=
\begin{cases}
Normal & E(x)\leq T\\
Attack & E(x)>T
\end{cases}
$$

---

## 3. Research Motivation

The main motivation of this project is to investigate whether a model trained primarily on normal network behavior can effectively identify different categories of malicious traffic through reconstruction error.

The project specifically investigates several challenges that arise in practical Autoencoder-based anomaly detection:

* Highly skewed network-flow features
* Extreme numerical values and outliers
* Different scales between network-flow features
* Feature redundancy and constant features
* Selection of an appropriate latent representation
* Selection of the Autoencoder architecture
* Selection of an anomaly threshold
* Differences in detection performance between attack categories
* Generalization from normal training traffic to unseen attack traffic

The preprocessing pipeline was therefore progressively improved during the project.

In the later versions, outlier clipping is calculated using the training data and subsequently applied consistently to validation, normal test, and attack data. A signed logarithmic transformation is also applied before scaling, followed by `RobustScaler`.

---

## 4. Dataset

### 4.1 Dataset Source

The project is based on the **CICIDS2017** intrusion detection dataset.

The dataset used as the external source for this project is available through Hugging Face:

**Dataset:** `bvk/CICIDS-2017`

The dataset repository contains five daily CSV files:

* `monday.csv`
* `tuesday.csv`
* `wednesday.csv`
* `thursday.csv`
* `friday.csv`

The repository describes the data as network-flow records generated from traffic collected during a five-day period from Monday through Friday. The flow records contain network characteristics such as packet counts, packet lengths, flow duration, inter-arrival times, protocol-related information, and other statistical features.

The Dataset Viewer currently exposes approximately **2.1 million rows** and includes a `Label` field containing multiple traffic classes.

### 4.2 Dataset Structure

The dataset contains network-flow-level features generated from network traffic.

Examples of the available features include:

* Source IP
* Destination IP
* Source Port
* Destination Port
* Protocol
* Flow Duration
* Forward/Backward packet counts
* Forward/Backward packet lengths
* Flow Bytes/s
* Flow Packets/s
* Inter-arrival time statistics
* TCP flag information
* Packet length statistics
* Active/Idle statistics
* TCP flow time
* Label

The Dataset Viewer indicates that the dataset contains approximately 80 network-flow-related features together with the traffic label.

---

## 5. Experimental Dataset Used in This Project

Although the external dataset is organized by day, the experimental pipeline used in this project works with a processed Parquet representation in which benign and attack traffic are separated.

The current pipeline defines the following experimental groups:

| Group       | Experimental File                         |
| ----------- | ----------------------------------------- |
| Normal      | `Benign-Monday-no-metadata.parquet`       |
| Brute Force | `Bruteforce-Tuesday-no-metadata.parquet`  |
| DoS         | `DoS-Wednesday-no-metadata.parquet`       |
| Web Attacks | `WebAttacks-Thursday-no-metadata.parquet` |
| Botnet      | `Botnet-Friday-no-metadata.parquet`       |
| DDoS        | `DDoS-Friday-no-metadata.parquet`         |
| Port Scan   | `Portscan-Friday-no-metadata.parquet`     |

This mapping is explicitly defined in the project implementation.

**Important:** The exact relationship between the original five daily files and these processed Parquet files will be documented in the dataset/preprocessing stage. We will not assume that the processed files are identical to the raw Hugging Face files without verifying the transformation process.

---

## 6. Detection Strategy

The project follows an anomaly-detection approach rather than training a conventional multi-class classifier.

The general workflow is:

```text
CICIDS2017
      │
      ▼
Data Loading
      │
      ▼
Data Cleaning
      │
      ▼
Feature Selection / Constant Feature Removal
      │
      ▼
Normal Traffic
      │
      ├──────────────► Train
      │
      ├──────────────► Validation
      │
      └──────────────► Normal Test
      │
      ▼
Outlier Clipping
      │
      ▼
Signed Log Transformation
      │
      ▼
Robust Scaling
      │
      ▼
Autoencoder Training
      │
      ▼
Reconstruction Error
      │
      ▼
Threshold Calibration
      │
      ▼
Normal vs Attack
      │
      ├──────────────► Overall Evaluation
      │
      └──────────────► Per-Attack Evaluation
```

The preprocessing and model pipeline implemented in the current version follows this general sequence.

---

## 7. Autoencoder Models

Two Autoencoder architectures are currently investigated:

### 7.1 Shallow Autoencoder

The shallow model uses a relatively compact architecture with an 8-dimensional bottleneck.

Its main structure is:

```text
Input
  │
  ▼
Dense(64)
  │
Batch Normalization
  │
Dropout
  │
Dense(32)
  │
Batch Normalization
  │
Dropout
  │
Dense(8)  ← Bottleneck
  │
Dense(32)
  │
Dense(64)
  │
Output
```

### 7.2 Deep Autoencoder

The deep model uses a larger encoder and decoder with a 4-dimensional bottleneck.

```text
Input
  │
  ▼
Dense(128)
  │
Batch Normalization
  │
Dropout
  │
Dense(64)
  │
Batch Normalization
  │
Dropout
  │
Dense(32)
  │
Batch Normalization
  │
Dropout
  │
Dense(4)  ← Bottleneck
  │
Dense(32)
  │
Batch Normalization
  │
Dropout
  │
Dense(64)
  │
Batch Normalization
  │
Dropout
  │
Dense(128)
  │
Output
```

Both architectures use Mean Squared Error as the reconstruction loss.

---

## 8. Thresholding Strategy

A central component of the anomaly detection system is the selection of the reconstruction-error threshold.

The current implementation does not simply select an arbitrary threshold.

Instead, a small labeled sample of attack traffic is used together with normal validation errors to calibrate the threshold.

The implementation samples up to 2,000 observations from each attack type and evaluates candidate thresholds between the 50th and 99.9th percentiles of the resulting reconstruction-error distribution.

The threshold producing the highest F1-score is selected.

Therefore, the current methodology can be characterized as:

> **Normal-data Autoencoder training with semi-supervised threshold calibration.**

This distinction is important for the final research paper and will be explicitly discussed in the methodology section.

---

## 9. Evaluation Strategy

The evaluation is performed at two levels.

### 9.1 Overall Binary Anomaly Detection

The first evaluation considers two classes:

```text
Normal
Attack
```

The current implementation reports:

* Precision
* Recall
* F1-score
* Confusion Matrix
* ROC-AUC

The ROC curve is generated using reconstruction error as the anomaly score.

---

### 9.2 Per-Attack-Type Evaluation

The second evaluation investigates how effectively the model detects individual attack categories.

The current implementation calculates, for each attack type:

* Recall
* Precision
* F1-score
* ROC-AUC
* Number of samples

This allows the project to determine whether the Autoencoder performs consistently across different attack families.

The two Autoencoder architectures are subsequently compared on a per-attack basis, with the current implementation selecting the better architecture based on Recall.

---

## 10. Experimental Evolution

This project was developed iteratively rather than as a single final implementation.

The development history consists of multiple versions:

```text
V1
 │
 ├── Problem
 ▼
V2
 │
 ├── Problem
 ▼
V3
 │
 ├── Problem
 ▼
...
 │
 ▼
V9
 │
 ▼
Final Methodology
```

Each version represents an experimental modification intended to solve a specific limitation observed in the previous version.

The evolution will be documented separately in:

```text
docs/06-experiment-history.md
```

For every version, the following information will be recorded:

| Field                 | Description                           |
| --------------------- | ------------------------------------- |
| Version               | Version identifier                    |
| Modification          | What changed                          |
| Motivation            | Why the change was introduced         |
| Observed Problem      | Problem in the previous version       |
| Experimental Result   | Effect of the modification            |
| Decision              | Whether the change was retained       |
| Research Significance | Why the change matters scientifically |

This section is particularly important because the objective is not merely to present the final model, but to explain how the final methodology was reached.

---

## 11. Reproducibility

The project uses a fixed random seed:

```python
SEED = 42
```

and initializes both NumPy and TensorFlow random generators using this seed.

The project also stores important preprocessing artifacts, including:

* Constant feature list
* Feature-column list
* Outlier clipping bounds
* RobustScaler

These artifacts allow the same preprocessing configuration to be reused during evaluation and future inference.

---

## 12. Current Research Questions

The project is designed to investigate the following questions.

### RQ1 — Can an Autoencoder trained primarily on benign network traffic detect malicious flows?

### RQ2 — How strongly does preprocessing affect Autoencoder-based anomaly detection?

### RQ3 — Does a deeper Autoencoder provide better anomaly detection performance than a shallow architecture?

### RQ4 — Do different attack categories produce substantially different detection performance?

### RQ5 — How does threshold-selection methodology affect the final detection results?

### RQ6 — Can the final methodology provide a reliable balance between detecting attacks and avoiding false positives?

These questions will be refined after completing the analysis of all nine experimental versions.

---

## 13. Project Structure

The planned documentation structure is:

```text
project/
│
├── data/
│
├── models/
│
├── Cols/
│
├── experiments/
│   └── EXPERIMENT_LOG.md
│
├── docs/
│   ├── 00-project-overview.md
│   ├── 01-dataset.md
│   ├── 02-preprocessing.md
│   ├── 03-model.md
│   ├── 04-threshold.md
│   ├── 05-evaluation.md
│   ├── 06-experiment-history.md
│   └── 07-paper-outline.md
│
└── README.md
```

---

## 14. Document Status

**Current Stage:** Stage 1 — Project Overview

**Dataset:** CICIDS2017

**External Dataset Source:** Hugging Face `bvk/CICIDS-2017`

**Detection Method:** Autoencoder-based anomaly detection

**Primary Training Data:** Benign network traffic

**Anomaly Score:** Reconstruction Error

**Thresholding:** Semi-supervised threshold calibration

**Models:** Shallow Autoencoder / Deep Autoencoder

**Evaluation:** Overall binary detection + per-attack analysis

**Experimental Versions:** V1–V9

---

## 15. Items Requiring Verification

The following information will be verified during the next documentation stages rather than being assumed:

* Exact number of features used after preprocessing
* Exact number of samples in each experimental file
* Exact mapping between the Hugging Face daily files and processed Parquet files
* Exact attack-label distribution
* Features removed as constant
* Features removed for other reasons
* Exact train/validation/test sample counts
* Exact results obtained by each experimental version
* Whether any attack samples used for threshold calibration overlap with the final evaluation set
* Final comparison between Shallow and Deep Autoencoders

These values will be extracted directly from the project files and experimental outputs.

---

## 16. Reference

Primary dataset source:

`bvk/CICIDS-2017` — Hugging Face Dataset Repository.

The dataset documentation states that CICIDS2017 contains network-flow records collected over five days and includes benign traffic as well as multiple attack categories.

The original CICIDS2017 work should also be cited in the final academic paper:

> I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization," Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP), 2018.

The Hugging Face dataset documentation also references subsequent work concerning corrections and troubleshooting of CICIDS2017.
