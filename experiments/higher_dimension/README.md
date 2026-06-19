# QTC ProcessTensor Lite V0.3

# Higher Dimension Validation Experiment


Version:

v0.3-validation-pass


Experiment:

higher_dimension_v03



---

# 1. Objective


This experiment extends the V0.3 evolution engine
from the minimal 2-dimensional Hilbert space
to higher-dimensional density matrices.


Purpose:


- Test scalability of PSD projection layer.
- Verify physical state preservation.
- Measure computational behavior with increasing dimension.
- Validate independence from qubit-only dynamics.



---

# 2. Experimental Scope


Hilbert dimensions:



d = 2

d = 4

d = 8

d = 16



For each dimension:


- Generate valid density matrices.
- Apply non-Markovian evolution.
- Apply PSD projection.
- Record audit metrics.



---

# 3. Initial State Generation


Random density matrices are generated using:


\[
\rho =
\frac{AA^\dagger}
{\mathrm{Tr}(AA^\dagger)}
\]


where:


- A is a random complex matrix.
- rho is guaranteed Hermitian.
- rho has unit trace.



---

# 4. Simulation Parameters


Default:



dt = 0.2

steps = 50

memory_strength = 0.5

samples = 100




---

# 5. Metrics


The following quantities are recorded:


## Physical Validation


- Hermitian condition
- Trace normalization
- Positive semidefinite condition


## Projection Audit


- projection_calls
- repair_count
- max_negative_eig
- avg_negative_eig
- max_projection_shift
- avg_projection_shift


## Performance


- runtime
- dimension scaling



---

# 6. Expected Observation


For increasing dimension:


Expected:



d=2

stable baseline

d=4

small increase in projection activity

d=8

higher numerical sensitivity

d=16

stress regime




The goal is not maximum speed,
but preservation of physical correctness.



---

# 7. Output Structure


Generated results:



results/

├── dimension_sweep.json

└── dimension_report.md




---

# 8. Scientific Question


Main question:


Does the V0.3 PSD projection framework
remain physically stable when the Hilbert space
dimension increases?



---

# 9. Status


Experiment:

PENDING



Next step:

Implement:

run_higher_dimension.py