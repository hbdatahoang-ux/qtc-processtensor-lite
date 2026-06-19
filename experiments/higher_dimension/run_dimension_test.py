# ============================================================
# run_dimension_test.py
# QTC ProcessTensor Lite V0.3
#
# Higher Dimension Validation Experiment
#
# Purpose:
#   - Test PSD projection scalability
#   - Validate higher dimensional density matrices
#   - Measure physical stability
#
# No plotting
# No engine modification
# ============================================================


from __future__ import annotations


import os
import json
import time


import numpy as np


import sys

sys.path.append(
    os.path.abspath(
        "../../code"
    )
)


from evolution_v03 import (
    evolve_non_markov_projected,
    validate_result,
)



# ============================================================
# CONFIG
# ============================================================


RESULT_DIR = "results"


OUTPUT_JSON = os.path.join(
    RESULT_DIR,
    "dimension_sweep.json"
)


OUTPUT_REPORT = os.path.join(
    RESULT_DIR,
    "dimension_report.md"
)



DIMENSIONS = [
    2,
    4,
    8,
    16,
]


STEPS = 50


DT = 0.2


MEM_STRENGTH = 0.5


SAMPLES = 10


SEED = 42



# ============================================================
# UTILITIES
# ============================================================


def random_density_matrix(
    dim: int,
    rng: np.random.Generator,
):

    """
    Generate random PSD density matrix.

    rho = A A† / Tr(A A†)
    """

    A = (
        rng.normal(
            size=(dim, dim)
        )
        +
        1j *
        rng.normal(
            size=(dim, dim)
        )
    )


    rho = (
        A
        @
        A.conj().T
    )


    rho /= np.trace(rho)


    return rho



def random_unitary(
    dim: int,
    rng: np.random.Generator,
):

    """
    Generate random unitary matrix.
    """

    A = (
        rng.normal(
            size=(dim, dim)
        )
        +
        1j *
        rng.normal(
            size=(dim, dim)
        )
    )


    Q, R = np.linalg.qr(
        A
    )


    phases = np.diag(
        R
    )

    phases /= np.abs(
        phases
    )


    return Q @ np.diag(phases)



# ============================================================
# EXPERIMENT
# ============================================================


def run_dimension_test():


    os.makedirs(
        RESULT_DIR,
        exist_ok=True
    )


    rng = np.random.default_rng(
        SEED
    )


    results = []


    print(
        "\n=== HIGHER DIMENSION TEST ==="
    )



    for dim in DIMENSIONS:


        print(
            f"\nDimension: {dim}"
        )


        repairs = []

        max_negative = []

        shifts = []

        valid_count = 0


        start = time.time()



        for _ in range(SAMPLES):


            rho0 = random_density_matrix(
                dim,
                rng,
            )


            U = random_unitary(
                dim,
                rng,
            )


            result = evolve_non_markov_projected(

                rho0=rho0,

                steps=STEPS,

                U=U,

                mem_strength=MEM_STRENGTH,
            )



            validation = validate_result(
                result
            )


            if validation["valid"]:

                valid_count += 1



            audit = result.audit


            repairs.append(
                audit.repair_count
            )


            max_negative.append(
                audit.max_negative_eig
            )


            shifts.append(
                audit.max_projection_shift
            )



        elapsed = time.time() - start



        row = {

            "dimension":
                dim,


            "samples":
                SAMPLES,


            "valid_states":
                valid_count,


            "valid_rate":
                valid_count / SAMPLES,


            "avg_repairs":
                float(
                    np.mean(
                        repairs
                    )
                ),


            "max_negative_eig":
                float(
                    min(
                        max_negative
                    )
                ),


            "max_projection_shift":
                float(
                    max(
                        shifts
                    )
                ),


            "runtime_seconds":
                elapsed,
        }



        results.append(
            row
        )


        print(
            row
        )



    return results



# ============================================================
# EXPORT
# ============================================================


def save_results(
    results
):


    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            results,
            f,
            indent=4
        )



    with open(
        OUTPUT_REPORT,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "# QTC ProcessTensor Lite V0.3\n"
        )

        f.write(
            "# Higher Dimension Validation Report\n\n"
        )


        for row in results:

            f.write(
                f"""
## Dimension {row['dimension']}

Valid rate:

{row['valid_rate']}

Average repairs:

{row['avg_repairs']}

Maximum projection shift:

{row['max_projection_shift']}

Runtime:

{row['runtime_seconds']} seconds


---
"""
            )



    print(
        f"[INFO] Saved {OUTPUT_JSON}"
    )

    print(
        f"[INFO] Saved {OUTPUT_REPORT}"
    )



# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    results = run_dimension_test()


    save_results(
        results
    )