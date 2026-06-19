from __future__ import annotations

import json
import os
from datetime import datetime

import numpy as np

from benchmark_v03 import bm2_projected_wrapper
from retention_study import (
    run_retention_study,
    export_all,
)


# ============================================================
# PATHS
# ============================================================

RESULT_DIR = "results/v03"

SUMMARY_JSON = os.path.join(
    RESULT_DIR,
    "benchmark_summary.json",
)


# ============================================================
# CONFIG
# ============================================================

CONFIG = {

    "dt": 0.20,

    "seed": 42,

    "eps": 1e-12,

    "steps": 50,

    "memory_grid": [
        0.00,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.70,
        0.80,
        0.90,
        1.00,
    ],
}


# ============================================================
# RUNNERS
# ============================================================

def bm1_runner(
    dt,
    seed,
    eps,
    mem_strength,
):

    return bm2_projected_wrapper(
        dt=dt,
        seed=seed,
        mem_strength=0.0,
    )


def bm2_runner(
    dt,
    seed,
    eps,
    mem_strength,
):

    return bm2_projected_wrapper(
        dt=dt,
        seed=seed,
        mem_strength=mem_strength,
    )


def bm2_projected_runner(
    dt,
    seed,
    eps,
    mem_strength,
):

    return bm2_projected_wrapper(
        dt=dt,
        seed=seed,
        mem_strength=mem_strength,
    )


# ============================================================
# BENCHMARK SUMMARY EXPORT
# ============================================================

def export_benchmark_summary(
    rows
):

    os.makedirs(
        RESULT_DIR,
        exist_ok=True,
    )


    retention_values = [
        r["retention"]
        for r in rows
    ]


    total_repairs = sum(
        r["repair_count"]
        for r in rows
    )


    max_negative_eig = min(
        r["max_negative_eig"]
        for r in rows
    )


    avg_projection_shift = float(
        np.mean(
            [
                r["avg_projection_shift"]
                for r in rows
            ]
        )
    )


    summary = {

        "experiment_id":
            "sweep_0_to_1.0",

        "version":
            "v0.3-alpha-engine-stable",

        "timestamp":
            datetime.utcnow()
            .isoformat(),

        "configuration":
        {
            "dt":
                CONFIG["dt"],

            "steps":
                CONFIG["steps"],

            "memory_points":
                len(
                    CONFIG["memory_grid"]
                ),
        },


        "stats":
        {

            "avg_retention":
                float(
                    np.mean(
                        retention_values
                    )
                ),

            "min_retention":
                float(
                    np.min(
                        retention_values
                    )
                ),

            "max_retention":
                float(
                    np.max(
                        retention_values
                    )
                ),

            "total_memory_steps":
                len(
                    CONFIG["memory_grid"]
                ),

            "total_repairs":
                int(
                    total_repairs
                ),

            "global_max_negative_eig":
                float(
                    max_negative_eig
                ),

            "avg_projection_shift":
                avg_projection_shift,
        }
    }


    with open(
        SUMMARY_JSON,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            summary,
            f,
            indent=4,
        )


    print(
        f"[INFO] Saved {SUMMARY_JSON}"
    )


    return summary


# ============================================================
# MAIN VALIDATION PIPELINE
# ============================================================

def main():

    print(
        "\n=== QTC PROCESS TENSOR LITE V0.3 VALIDATION ==="
    )


    rows = run_retention_study(

        bm1_runner,

        bm2_runner,

        bm2_projected_runner,

        CONFIG,
    )


    export_all(
        rows
    )


    summary = export_benchmark_summary(
        rows
    )


    print(
        "\n=== VALIDATION SUMMARY ==="
    )


    print(
        json.dumps(
            summary,
            indent=4,
        )
    )


if __name__ == "__main__":

    main()