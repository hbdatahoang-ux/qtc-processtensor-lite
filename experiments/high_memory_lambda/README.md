# QTC ProcessTensor Lite V0.3

# High Memory Lambda Experiment


Version:

v0.3-validation-pass


Experiment:

high_memory_lambda_v03



---

# 1. Objective


This experiment studies the behavior of the
QTC ProcessTensor Lite V0.3 engine under
strong memory coupling regimes.


The purpose is to determine:

1. Stability limit of the memory kernel.
2. Activation behavior of PSD projection.
3. Physical state preservation under extreme lambda.



---

# 2. Motivation


The first V0.3 validation tested:


\[
\lambda = 0.0 \rightarrow 1.0
\]


with physical initial states.


In this experiment the memory parameter is
extended beyond the standard range to probe
non-linear and unstable regimes.



---

# 3. Experiment Scope


Memory strength:


\[
\lambda > 1
\]


Suggested sweep:


```text
1.0
1.25
1.5
1.75
2.0
2.5
3.0
5.0
10.0