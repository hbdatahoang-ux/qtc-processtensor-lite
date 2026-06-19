# ============================================================
# benchmark_v03.py
# QTC ProcessTensor Lite V0.3-dev
#
# Benchmark Wrapper Layer
#
# Responsibilities:
#     - Build benchmark configuration
#     - Run projected evolution
#     - Compute metrics
#     - Return structured result
#
# No plotting
# No file IO
# No retention logic
# ============================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from evolution_v03 import (
    evolve_non_markov_projected,
    SimulationResultV03,
)

# ============================================================
# CONFIG
# ============================================================

DEFAULT_CHI_LIST = [
    1,
    2,
    4,
    6,
    8,
    12,
]

DEFAULT_STEPS = 50


# ============================================================
# RESULT
# ============================================================

@dataclass
class BenchmarkResultV03:

    simulation: SimulationResultV03

    metrics: np.ndarray

    chi_list: List[int]

    mem_strength: float

    def summary(self):

        return {

            "mem_strength":
                self.mem_strength,

            "repair_count":
                self.simulation.audit.repair_count,

            "max_negative_eig":
                self.simulation.audit.max_negative_eig,

            "avg_negative_eig":
                self.simulation.audit.avg_negative_eig,

            "max_projection_shift":
                self.simulation.audit.max_projection_shift,

            "avg_projection_shift":
                self.simulation.audit.avg_projection_shift,
        }


# ============================================================
# STATE HELPERS
# ============================================================

def initialize_state(
    seed: int = 42
) -> np.ndarray:
    """
    Standard benchmark initial state.

    |0><0|
    """

    return np.array(
        [
            [1.0, 0.0],
            [0.0, 0.0],
        ],
        dtype=complex,
    )


def build_unitary(
    dt: float
) -> np.ndarray:
    """
    Simple rotation benchmark.
    """

    theta = dt

    return np.array(
        [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)],
        ],
        dtype=complex,
    )


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(
    rho: np.ndarray,
    chi_list: List[int]
) -> np.ndarray:
    """
    Placeholder metric layer.

    Replace later with
    QTC compression metrics.
    """

    purity = np.real(
        np.trace(
            rho @ rho
        )
    )

    metrics = []

    for chi in chi_list:

        metrics.append(
            purity / np.sqrt(chi)
        )

    return np.asarray(metrics)


# ============================================================
# WRAPPER
# ============================================================

def bm2_projected_wrapper(
    dt: float,
    seed: int,
    mem_strength: float,
    chi_list: List[int] | None = None,
    steps: int = DEFAULT_STEPS,
):
    """
    Main V0.3 benchmark wrapper.
    """

    if chi_list is None:

        chi_list = DEFAULT_CHI_LIST

    rho0 = initialize_state(
        seed
    )

    U = build_unitary(
        dt
    )

    simulation = (
        evolve_non_markov_projected(
            rho0=rho0,
            steps=steps,
            U=U,
            mem_strength=mem_strength,
        )
    )

    metrics = calculate_metrics(
        simulation.rho_final,
        chi_list,
    )

    return BenchmarkResultV03(
        simulation=simulation,
        metrics=metrics,
        chi_list=chi_list,
        mem_strength=mem_strength,
    )


# ============================================================
# SWEEP
# ============================================================

def memory_sweep_v03(
    dt: float,
    seed: int,
    memory_values,
    chi_list=None,
):
    """
    Convenience sweep utility.
    """

    results = []

    for mem in memory_values:

        res = bm2_projected_wrapper(
            dt=dt,
            seed=seed,
            mem_strength=mem,
            chi_list=chi_list,
        )

        results.append(res)

    return results


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n=== BENCHMARK V0.3 SELF TEST ==="
    )

    result = bm2_projected_wrapper(
        dt=0.2,
        seed=42,
        mem_strength=0.30,
    )

    print(
        "\nMetrics:"
    )

    print(
        result.metrics
    )

    print(
        "\nSummary:"
    )

    print(
        result.summary()
    )

    print(
        "\nAudit:"
    )

    print(
        result.simulation.audit.summary()
    )