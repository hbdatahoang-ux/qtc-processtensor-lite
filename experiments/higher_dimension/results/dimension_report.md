# QTC ProcessTensor Lite V0.3
# Higher Dimension Scaling Report


Version:

v0.3-validation-pass


Experiment:

higher_dimension_scaling


Date:

2026-06-19


Author:

Bui Dinh Hoang



---

# 1. Objective


This experiment evaluates the stability of the
QTC ProcessTensor Lite V0.3 engine when scaling
the Hilbert space dimension.


The objectives are:


1. Verify physical state preservation.

2. Measure PSD projection behavior.

3. Evaluate numerical stability with increasing dimension.

4. Estimate computational scaling.



---

# 2. Configuration


Experiment directory:



experiments/higher_dimension/



Configuration source:



config.json



Tested dimensions:


\[
d = 2,4,8,16
\]


Simulation parameters:



dt = 0.2

steps = 50

memory_strength = 0.5

samples_per_dimension = 10




---

# 3. Validation Pipeline


Execution:


```bash
python experiments/higher_dimension/run_dimension_test.py

Generated output:

results/

└── dimension_scaling.json

Pipeline:

Random Density Matrix

        |

        v

Non-Markov Evolution

        |

        v

PSD Projection Layer

        |

        v

Physical State Audit

        |

        v

Scaling Metrics
4. Results Summary
Dimension	Samples	Physical Pass	Avg Repairs	Projection Shift
2	10	100%	0	~1e-15
4	10	100%	0	~1e-15
8	10	100%	0	~1e-15
16	10	100%	0	~1e-14
5. Positivity Validation

Observed:

physical_validity_preserved = True

The projected density matrices satisfy:

Hermiticity
Trace normalization
Positive semidefinite condition

No physical repair intervention was required
within the tested range.

6. Projection Analysis

The PSD projection layer remained transparent.

Maximum observed correction:

∣∣ρ
raw
	​

−ρ
proj
	​

∣∣≈10
−14

Interpretation:

The deviation remains at numerical precision scale.

The projection operator does not introduce
measurable distortion in the tested dimensions.

7. Scaling Behavior

Observed trend:

dimension ↑

runtime ↑

projection stability unchanged

The engine maintains stable behavior up to:

d=16

with no degradation in physical validity.

8. Scientific Interpretation

This experiment demonstrates:

1. Dimension Robustness

The V0.3 dual trajectory framework remains
stable when increasing Hilbert space size.

2. Projection Transparency

The PSD correction layer acts as a numerical
safety mechanism rather than a dynamical distortion.

3. Architecture Scalability

The separation between:

Evolution Engine

        +

Projection Layer

        +

Audit System

allows independent scaling analysis.

9. Limitations

This experiment does not yet include:

very high dimensions (d > 16)
tensor-network compression
adaptive bond dimension
large memory kernels
GPU acceleration

Future tests:

dimension = 32,64,128

compression metrics

large-scale ProcessTensor benchmark
10. Conclusion

QTC ProcessTensor Lite V0.3 successfully passes
the higher dimension stability validation.

Status:

DIMENSION SCALING:
PASSED


PHYSICAL VALIDITY:
STABLE


READY FOR:
compression benchmark stage

Recommended next milestone:

v0.3-science-freeze