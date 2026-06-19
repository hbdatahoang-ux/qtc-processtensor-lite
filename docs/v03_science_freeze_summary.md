# QTC ProcessTensor Lite V0.3
# Science Freeze Summary


Version:

v0.3-science-freeze


Date:

2026-06-19


Author:

Bui Dinh Hoang



---

# 1. Milestone Overview


This document records the science freeze milestone
of QTC ProcessTensor Lite V0.3.


V0.3 has completed:

- Engine stabilization
- Experimental validation
- Reproducibility setup
- Extended stress experiment framework



The project transitions from:

Engineering Phase

to

Scientific Exploration Phase



---

# 2. Frozen Software State


Repository:

QTC-ProcessTensor-Lite


Branch:

v0.3-dev


Science freeze tag:

v0.3-science-freeze


Engine validation tag:

v0.3-alpha-engine-stable


Validation tag:

v0.3-validation-pass



Latest freeze commit:

2b40b6b



---

# 3. Core Architecture Frozen


The following components are considered stable:


## Evolution Engine


code/evolution_v03.py



Provides:

- Dual trajectory evolution
- Raw dynamics tracking
- Projected physical dynamics
- Non-Markov memory evolution



## Positivity Layer


code/positivity.py



Provides:

- Hermitian correction
- Trace normalization
- PSD repair
- Projection audit



## Benchmark System


code/benchmark_v03.py



Provides:

- Standardized metrics
- Audit extraction
- Validation interface



## Experimental Runner


code/run_validation_v03.py



Provides:

- Full validation pipeline
- Artifact generation
- Reproducible sweep execution



---

# 4. Completed Experiments


## Experiment 1: Retention Validation


Range:

\[
\lambda = 0.0 \rightarrow 1.0
\]


Resolution:

0.05


Points:

17



Result:


Average retention:

100 %



Minimum retention:

≈100 %



Projection repairs:

0



Interpretation:


The PSD projection layer introduces
no measurable distortion in the tested stable regime.



---

# 5. Extended Experiments


The following reproducibility experiments
are now integrated:



experiments/

├── random_initial_states/

├── high_memory_lambda/

└── higher_dimension/




## Random Initial States


Purpose:

Test dependence on initial conditions.



## High Memory Lambda


Purpose:

Explore non-linear memory regime.



## Higher Dimension


Purpose:

Test scaling beyond minimal Hilbert space.



---

# 6. Validation Evidence


Generated artifacts:



results/v03/

├── retention.csv

├── retention.json

├── projection_audit.json

├── benchmark_summary.json

├── retention_plot.png

└── retention_report.txt




Evidence summary:



repair_count = 0

max_negative_eigenvalue = 0

projection_shift ≈ machine precision




---

# 7. Scientific Status


Current status:


ENGINE:

STABLE



VALIDATION:

PASSED



SCIENCE FREEZE:

ACHIEVED



The V0.3 architecture is frozen
for further scientific investigation.



---

# 8. Known Limitations


Not yet validated:


- Strongly non-positive raw trajectories
- Large memory instability regime
- High dimensional scaling limits
- Tensor compression effects
- Physical observable comparison



---

# 9. Next Research Phase


Recommended next milestone:


v0.4-exploration



Focus:


1. Strong memory dynamics

2. Larger Hilbert dimensions

3. Compression metrics

4. Observable-level validation

5. Comparison with reference models



---

# 10. Final Statement


QTC ProcessTensor Lite V0.3 has successfully completed
the transition from software construction
to reproducible experimental framework.


The engine is frozen.

The experiments are reproducible.

The next stage is scientific exploration.