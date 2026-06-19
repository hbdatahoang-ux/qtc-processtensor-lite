# Experiment: Random Initial States

## QTC ProcessTensor Lite V0.3

Experiment ID:

random_initial_states_v03


## Objective

Evaluate the stability of the V0.3 evolution engine
under random physical density matrix initialization.


The validation question:

Does the PSD projection layer preserve physical evolution
for arbitrary valid initial states?


---

## Motivation

The first V0.3 validation used:

|0><0|

as the initial state.

This experiment extends the test space to:

- mixed states
- random pure states
- random density matrices


---

## Experimental Setup


Engine:

v0.3-alpha-engine-stable


Branch:

v0.3-dev


Parameters:


dt = 0.2

steps = 50


Memory sweep:


lambda = 0.0 -> 1.0


Resolution:

0.05



---

## Initial State Generation


Generate random density matrices:

1. Create random complex matrix A.

2. Construct:

rho = A A†


3. Normalize:

Tr(rho)=1



Constraints:


Hermitian:

PASS


Trace:

PASS


Positive semidefinite:

PASS



---

## Metrics


For each initial state:


### Physical Validation

- Hermiticity
- Trace preservation
- Positivity


### Projection Metrics

- repair_count
- max_negative_eig
- projection_shift


### Information Retention

- div_raw
- div_proj
- retention %



---

## Expected Result


Stable regime:

retention ≈ 100%


Projection:

inactive or near machine precision


---

## Output


Results will be stored:


results/v03/random_initial_states/


Expected files:


random_states_summary.json

random_states_audit.json

random_states_report.txt



---

## Scientific Purpose


This experiment tests whether
V0.3 stability is a property of the engine,
not a consequence of a special initial condition.


Status:

PLANNED