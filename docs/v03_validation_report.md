# QTC ProcessTensor Lite V0.3
# Validation Report


Version:

v0.3-validation-pass


Date:

2026-06-19


Author:

Bui Dinh Hoang



---

# 1. Overview


This document records the first experimental validation
of the QTC ProcessTensor Lite V0.3 engine.


V0.3 introduces:


- Dual trajectory evolution
- PSD projection layer
- Projection audit system
- Benchmark wrapper
- Retention study pipeline


The purpose of this validation is:


1. Verify physical state preservation.
2. Quantify projection-induced distortion.
3. Measure information retention under memory evolution.



---

# 2. Software Configuration


Repository:

QTC-ProcessTensor-Lite


Branch:

v0.3-dev


Validated tag:

v0.3-validation-pass


Engine tag:

v0.3-alpha-engine-stable



Main modules:


```text
code/

├── evolution_v03.py

├── benchmark_v03.py

├── retention_study.py

└── run_validation_v03.py
3. Experimental Setup
Evolution Model

The engine evolves density matrices using:

ρ
raw
	​

(t+1)=Uρ(t)U
†
+λ(ρ(t−1)−ρ(t))

where:

U is the unitary evolution operator.
λ is the memory strength parameter.

Tested memory range:

λ=0.0→1.0

Sweep resolution:

0.05

Total tested points:

17

Simulation parameters:

dt = 0.2

steps = 50

initial state:

|0><0|
4. Validation Pipeline

Execution:

python code/run_validation_v03.py

Generated artifacts:

results/v03/

├── retention.csv

├── retention.json

├── projection_audit.json

├── benchmark_summary.json

├── retention_plot.png

└── retention_report.txt
5. Retention Results

Experimental output:

Parameter	Result
Average retention	100 %
Minimum retention	~100 %
Maximum retention	~100 %
Signal loss	0
Total repairs	0

Observation:

The projected trajectory follows the raw trajectory
without measurable distortion.

The PSD projection layer remains inactive because
the tested evolution stays inside the physical state manifold.

6. Positivity Audit

Projection audit:

repair_count = 0

projection_calls = 49

max_negative_eigenvalue = 0

avg_negative_eigenvalue = 0

Projection displacement:

max_projection_shift

≈ 2.36 × 10^-16


avg_projection_shift

≈ 1.8 × 10^-15

Interpretation:

The numerical correction is at machine precision level.

No physical repair intervention was required.

7. Physical Validation

Final state validation:

Hermitian:
PASS


Trace normalization:
PASS


Positive semidefinite:
PASS

Example:

min_eig =

0.4203794145

The final density matrix satisfies
physical state constraints.

8. Scientific Interpretation

The first V0.3 experiment demonstrates:

1. Stability

The dual trajectory framework preserves
physical evolution over the tested memory range.

2. Projection Transparency

The PSD projection layer does not introduce
observable distortion in the stable regime.

3. Benchmark Integrity

The benchmark pipeline successfully separates:

Raw dynamics

        |

        v

Projected physical dynamics

        |

        v

Retention measurement
9. Limitations

This validation does not yet explore:

Strongly non-positive raw trajectories.
Higher dimensional Hilbert spaces.
Larger memory kernels.
Tensor compression effects.

Future experiments should include:

lambda > 1

random initial states

higher dimensional density matrices

QTC compression metrics
10. Conclusion

QTC ProcessTensor Lite V0.3 successfully passes
the first validation stage.

Status:

ENGINE:

STABLE


VALIDATION:

PASSED


READY FOR:

extended physical stress testing

Recommended next milestone:

v0.3-science-freeze