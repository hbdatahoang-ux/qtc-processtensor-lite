# ============================================================
# run_random_states.py
# QTC ProcessTensor Lite V0.3
#
# Experiment:
# Random Initial States Stability Test
#
# Responsibilities:
#     - Generate random physical density matrices
#     - Run V0.3 evolution engine
#     - Measure projection stability
#     - Export experiment summary
#
# No modification to core engine
# ============================================================


from __future__ import annotations


import os
import json
from datetime import datetime


import numpy as np


import sys

sys.path.append(
    "../../code"
)


from evolution_v03 import (
    evolve_non_markov_projected,
    validate_result,
)



# ============================================================
# CONFIG
# ============================================================


RESULT_DIR = (
    "../../results/v03/random_initial_states"
)


STEPS = 50

DT = 0.2


MEMORY_GRID = np.arange(
    0.0,
    1.01,
    0.05
)


NUM_STATES = 100


SEED = 42



# ============================================================
# HELPERS
# ============================================================


def ensure_output():

    os.makedirs(
        RESULT_DIR,
        exist_ok=True
    )



def random_density_matrix(
    dim=2,
    rng=None
):

    if rng is None:

        rng = np.random.default_rng()


    A = (
        rng.normal(
            size=(dim, dim)
        )
        +
        1j
        *
        rng.normal(
            size=(dim, dim)
        )
    )


    rho = (
        A
        @
        A.conj().T
    )


    rho /= np.trace(
        rho
    )


    return rho



def build_unitary(
    dt
):

    theta = dt


    return np.array(

        [
            [
                np.cos(theta),
                -np.sin(theta)
            ],

            [
                np.sin(theta),
                np.cos(theta)
            ]
        ],

        dtype=complex
    )



# ============================================================
# EXPERIMENT
# ============================================================


def run():

    ensure_output()


    rng = np.random.default_rng(
        SEED
    )


    U = build_unitary(
        DT
    )


    records = []


    total_repairs = 0

    max_negative = 0.0

    max_shift = 0.0



    for state_id in range(
        NUM_STATES
    ):


        rho0 = random_density_matrix(
            dim=2,
            rng=rng
        )



        for mem in MEMORY_GRID:


            result = evolve_non_markov_projected(

                rho0=rho0,

                steps=STEPS,

                U=U,

                mem_strength=float(mem),

            )


            validation = validate_result(
                result
            )


            audit = result.audit



            total_repairs += (
                audit.repair_count
            )


            max_negative = min(
                max_negative,
                audit.max_negative_eig
            )


            max_shift = max(
                max_shift,
                audit.max_projection_shift
            )



            records.append(

                {

                    "state_id":
                        state_id,


                    "memory":
                        float(mem),


                    "valid":
                        bool(
                            validation["valid"]
                        ),


                    "repair_count":
                        audit.repair_count,


                    "max_negative_eig":
                        audit.max_negative_eig,


                    "max_projection_shift":
                        audit.max_projection_shift,

                }

            )



    summary = {


        "experiment":

            "random_initial_states_v03",


        "timestamp":

            datetime.now().isoformat(),


        "configuration":

            {

                "states":
                    NUM_STATES,


                "steps":
                    STEPS,


                "memory_points":
                    len(MEMORY_GRID),

            },


        "results":

            {


                "total_runs":

                    len(records),


                "total_repairs":

                    total_repairs,


                "global_max_negative_eig":

                    max_negative,


                "global_max_projection_shift":

                    max_shift,


            }

    }



    with open(

        os.path.join(
            RESULT_DIR,
            "random_states_summary.json"
        ),

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(
            summary,
            f,
            indent=4
        )



    with open(

        os.path.join(
            RESULT_DIR,
            "random_states_raw.json"
        ),

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(
            records,
            f,
            indent=4
        )



    print(
        "\n=== RANDOM INITIAL STATES TEST ==="
    )


    print(
        json.dumps(
            summary,
            indent=4
        )
    )



# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":

    run()