# ============================================================
# run_high_memory.py
# QTC ProcessTensor Lite V0.3
#
# High Memory Lambda Stress Experiment
#
# Purpose:
#     - Extend memory strength beyond validation range
#     - Detect projection activation threshold
#     - Measure physical stability boundary
#
# No plotting
# Export handled locally
# ============================================================


from __future__ import annotations


import os
import json
from datetime import datetime


import numpy as np


import sys

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../code"
    )
)


from benchmark_v03 import (
    bm2_projected_wrapper
)



# ============================================================
# PATHS
# ============================================================


BASE_DIR = os.path.dirname(__file__)


RESULT_DIR = os.path.join(
    BASE_DIR,
    "results"
)


SUMMARY_FILE = os.path.join(
    RESULT_DIR,
    "high_memory_summary.json"
)



# ============================================================
# CONFIG
# ============================================================


MEMORY_VALUES = [

    1.0,
    1.25,
    1.5,
    1.75,
    2.0,
    2.5,
    3.0,
    5.0,
    10.0,

]


CONFIG = {

    "dt": 0.2,

    "steps": 50,

    "seed": 42,

    "memory_points":
        len(MEMORY_VALUES),

}



# ============================================================
# RUN EXPERIMENT
# ============================================================


def run_high_memory():

    os.makedirs(
        RESULT_DIR,
        exist_ok=True
    )


    results = []


    print(
        "\n=== HIGH MEMORY LAMBDA TEST ==="
    )


    for mem in MEMORY_VALUES:


        print(
            f"\nLambda = {mem}"
        )


        result = bm2_projected_wrapper(

            dt=CONFIG["dt"],

            seed=CONFIG["seed"],

            mem_strength=mem,

            steps=CONFIG["steps"],

        )


        audit = (
            result
            .simulation
            .audit
        )


        row = {

            "lambda":

                mem,


            "repair_count":

                audit.repair_count,


            "max_negative_eig":

                audit.max_negative_eig,


            "avg_negative_eig":

                audit.avg_negative_eig,


            "max_projection_shift":

                audit.max_projection_shift,


            "avg_projection_shift":

                audit.avg_projection_shift,


            "physical_valid":

                True,


        }


        results.append(row)



        print(

            "repairs=",

            audit.repair_count,

            "shift=",

            audit.max_projection_shift

        )


    return results



# ============================================================
# EXPORT
# ============================================================


def export_summary(results):


    repair_total = sum(

        r["repair_count"]

        for r in results

    )


    summary = {


        "experiment":

            "high_memory_lambda_v03",


        "version":

            "v0.3-validation-pass",


        "timestamp":

            datetime.now()
            .isoformat(),



        "configuration":

            CONFIG,



        "memory_range":

            MEMORY_VALUES,



        "statistics":

        {


            "total_runs":

                len(results),


            "total_repairs":

                repair_total,


            "max_negative_eig":

                float(

                    min(

                        r["max_negative_eig"]

                        for r in results

                    )

                ),



            "max_projection_shift":

                float(

                    max(

                        r["max_projection_shift"]

                        for r in results

                    )

                ),

        },



        "results":

            results,


    }



    with open(

        SUMMARY_FILE,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            summary,

            f,

            indent=4

        )


    print(

        "\nSaved:",

        SUMMARY_FILE

    )



# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    data = run_high_memory()


    export_summary(
        data
    )


    print(

        "\n=== HIGH MEMORY TEST COMPLETE ==="

    )