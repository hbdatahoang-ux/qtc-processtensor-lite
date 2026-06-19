# QTC ProcessTensor Lite V0.3

# High Memory Lambda Stability Report


Version:

v0.3-validation-pass


Experiment:

high_memory_lambda_v03


Date:

2026-06-19


Author:

Bui Dinh Hoang



---

# 1. Objective


This report summarizes the high memory strength
stress test of the QTC ProcessTensor Lite V0.3
non-Markovian evolution engine.


The experiment investigates:

- Stability boundary of memory evolution.
- Activation of PSD projection layer.
- Physical state preservation under strong memory coupling.



---

# 2. Experimental Configuration


Engine:

v0.3-alpha-engine-stable


Simulation:

dt = 0.2

steps = 50

Hilbert dimension = 2

initial state = |0><0|



Memory sweep:


\[
\lambda = 1.0 \rightarrow 10.0
\]


Test points:



1.0
1.25
1.5
1.75
2.0
2.5
3.0
5.0
10.0




---

# 3. Metrics


The following quantities were recorded:


## Physical stability

- Hermiticity
- Trace normalization
- Positive semidefinite condition


## Projection behavior

- repair_count
- negative eigenvalue magnitude
- projection displacement


## Memory response

- stability region
- transition region
- stress boundary



---

# 4. Results Summary


| Lambda | Projection | Physical State |
|---|---|---|
| 1.0 | inactive | stable |
| 1.5 | inactive | stable |
| 2.0 | activated | stable |
| 3.0 | active | stable |
| 5.0 | strong correction | stable |
| 10.0 | extreme correction | stable |



---

# 5. Stability Analysis


## Low Memory Region


\[
\lambda \leq 1.5
\]


Observation:


The raw trajectory remains inside the
physical density manifold.


Projection layer:


repair_count ≈ 0



Interpretation:

The evolution is naturally physical.



---

# 6. Transition Region


\[
\lambda \approx 2.0 - 3.0
\]


Observation:


The non-Markov memory contribution begins
to generate small non-positive components.


Projection layer activates.


Detected signals:


- increasing repair count
- increasing projection shift
- negative eigenvalue appearance



Interpretation:


The PSD projection layer acts as a
physical constraint regulator.



---

# 7. Strong Memory Region


\[
\lambda > 5
\]


Observation:


Large memory feedback produces stronger
deviation from the physical manifold.


The projection mechanism prevents
physical failure.


Final states remain:



Hermitian PASS

Trace PASS

Positive PASS




---

# 8. Scientific Interpretation


The V0.3 engine demonstrates:


## 1. Physical Robustness


The PSD projection layer maintains
valid density matrices even when the
raw evolution becomes unstable.



## 2. Controlled Correction


Projection distortion increases smoothly
with memory strength.


No catastrophic instability observed.



## 3. Stability Boundary


A transition appears around:


\[
\lambda \approx 2
\]


where projection changes from passive
validation to active stabilization.



---

# 9. Limitations


This experiment uses:


- 2-dimensional Hilbert space
- fixed unitary evolution
- single memory kernel


Future tests:


- higher dimensions
- random initial states
- tensor compression
- adaptive memory kernels



---

# 10. Conclusion


The high-memory stress experiment confirms:


STATUS:


V0.3 ENGINE:
ROBUST



The PSD projection layer provides a stable
physical envelope for strong non-Markovian
memory evolution.


Recommended next milestone:



v0.3-science-freeze




Experiment completed.