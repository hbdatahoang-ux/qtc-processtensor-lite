# QTC ProcessTensor Lite

Experimental benchmark framework for studying memory-induced divergence in compressed quantum process tensors.

---

## Status

### Frozen Release

**Version:** v0.2

**Git Tag:** v0.2

**State:** Gold Standard Baseline

Validated Features:

* Markov benchmark (BM1)
* Non-Markov benchmark (BM2)
* MPO-like compression
* Trace-distance divergence metrics
* M2.5 robustness audit
* Deterministic execution
* Memory sweep validation

---

## Current Development Branch

**Branch:** v0.3-dev

**Goal:** Physical-State Projection Layer

**Main Objective:**

Maintain observable memory-induced divergence while enforcing:

* Hermiticity
* Positive Semi-Definiteness (PSD)
* Trace Preservation

---

# Repository Structure

```text
project_root/

├── code/
│   ├── main_unified.py
│   ├── divergence_map.py
│   ├── truncation.py
│   ├── metrics.py
│   ├── m25_filter.py
│   ├── positivity.py
│   └── retention_study.py
│
├── configs/
│   └── default.yaml
│
├── data/
│
├── figures/
│
├── logs/
│
├── results/
│   ├── v02/
│   └── v03/
│       ├── retention.csv
│       ├── retention.json
│       ├── projection_audit.json
│       ├── retention_plot.png
│       └── retention_report.txt
│
├── requirements.txt
│
└── README.md
```

---

# Scientific Motivation

Many quantum simulations produce mathematically meaningful dynamics that may slightly violate physical constraints due to truncation, approximation, or memory kernels.

The central question addressed by this repository is:

> Can memory-induced divergence remain observable after enforcing physical quantum-state constraints?

---

# V0.2 Baseline Program

The frozen V0.2 release serves as the reference benchmark for all future developments.

## Benchmark 1 (BM1)

Pure Markovian evolution:

```math
\rho_{t+1}
=
U \rho_t U^\dagger
```

---

## Benchmark 2 (BM2)

Memory-enhanced evolution:

```math
\rho_{t+1}
=
U \rho_t U^\dagger
+
\lambda (\rho_{t-1}-\rho_t)
```

where

* λ = memory strength
* λ = 0 recovers the Markov limit

---

## Core Observation

Increasing memory strength produces increasing compression divergence.

```text
Memory ↑
⇒
Divergence ↑
```

---

# V0.2 Validation Results

The frozen benchmark passed:

### Markov Limit Test

```text
PASS
```

BM2 with λ = 0 reproduces BM1.

### Determinism Test

```text
PASS
```

Repeated runs with identical seeds produce identical results.

### M2.5 Robustness Audit

```text
PASS
```

Checks:

* NaN detection
* Inf detection
* Hermiticity
* Trace preservation

---

# V0.3 Physical Projection Program

V0.3 introduces a Physical-State Projection Layer.

The objective is not to alter the observed signal but to enforce physical density-matrix constraints during evolution.

---

## Projection Pipeline

```text
Raw State
    │
    ▼
Hermitianization
    │
    ▼
PSD Projection
    │
    ▼
Trace Normalization
    │
    ▼
Physical State
```

Implemented in:

```text
code/positivity.py
```

---

# Physical-State Projection

The projection operator maps an arbitrary matrix into the density-matrix manifold.

```math
\rho
\rightarrow
\Pi_{PSD}(\rho)
```

Projection steps:

1. Hermitian symmetrization
2. Eigenvalue decomposition
3. Negative eigenvalue clipping
4. Reconstruction
5. Trace normalization

---

# Projection Audit Metrics

The projection layer continuously records repair statistics.

## Repair Count

Number of positivity repairs applied.

```text
repair_count
```

---

## Maximum Negative Eigenvalue

Worst positivity violation observed before repair.

```text
max_negative_eig
```

---

## Average Negative Eigenvalue

Mean negativity magnitude across repairs.

```text
avg_negative_eig
```

---

## Projection Shift

Frobenius distance between raw and projected states.

```math
||\rho_{raw}-\rho_{proj}||_F
```

Reported as:

```text
max_projection_shift
avg_projection_shift
```

---

# Retention Study

The retention study compares:

* V0.2 Raw Dynamics
* V0.3 Projected Dynamics

against the frozen BM1 baseline.

Implemented in:

```text
code/retention_study.py
```

---

## Divergence Metrics

### Raw Divergence

```math
Div_{Raw}
=
||M_{BM1}-M_{Raw}||
```

### Projected Divergence

```math
Div_{Proj}
=
||M_{BM1}-M_{Proj}||
```

---

## Retention

Measures how much of the original memory signal survives projection.

```math
Retention(\%)
=
100
\times
\frac{Div_{Proj}}
     {Div_{Raw}}
```

---

## Signal Loss

```math
SignalLoss
=
|Div_{Raw}-Div_{Proj}|
```

Lower values indicate that projection minimally alters dynamics.

---

# Validation Targets for V0.3

## Identity Test

Memory:

```text
λ = 0
```

Expected:

```text
RepairCount = 0
Retention = 100%
```

---

## Positivity Test

Memory:

```text
λ > 0
```

Expected:

```text
MinEig(Projected) ≥ 0
```

---

## Signal Integrity Test

Expected:

```text
Retention > 95%
```

---

# Output Files

Running V0.3 retention analysis generates:

```text
results/v03/

retention.csv
retention.json
projection_audit.json
retention_plot.png
retention_report.txt
```

---

# Usage

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run V0.2 Benchmark

```bash
python code/main_unified.py
```

Generated outputs:

```text
data/result.npy
figures/divergence_landscape.png
```

---

## Run V0.3 Retention Study

```bash
python code/retention_study.py
```

Generated outputs:

```text
results/v03/
```

---

# Development Roadmap

## Completed

* V0.1 Alpha
* V0.2 Frozen Baseline

## Current

* V0.3 Physical Projection Layer

## Planned

* V0.4 Process-Tensor Kernel Extraction
* V0.5 Information-Theoretic Analysis
* V1.0 Research Release

---

# Author

**Bui Dinh Hoang**

Phu Tho, Viet Nam

---

# License

This repository is intended for research, benchmarking, and educational purposes.

Please cite the repository if used in derivative research projects.
