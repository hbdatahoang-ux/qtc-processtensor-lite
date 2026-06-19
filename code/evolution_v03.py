from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from positivity import (
    ProjectionAudit,
    repair_state,
    is_physical_state,
    hermitianize,
    trace_normalize,
)


@dataclass
class SimulationResultV03:
    """
    Complete V0.3 simulation result.

    Stores:
        - Final projected state
        - Raw trajectory
        - Projected trajectory
        - Projection audit information
    """

    rho_final: np.ndarray

    raw_traj: List[np.ndarray]

    proj_traj: List[np.ndarray]

    audit: ProjectionAudit

    steps: int

    mem_strength: float


    def summary(self) -> dict:

        return {

            "steps":
                self.steps,

            "trajectory_length":
                len(self.proj_traj),

            "mem_strength":
                self.mem_strength,

            "projection_calls":
                self.audit.projection_calls,

            "repair_count":
                self.audit.repair_count,

            "repair_rate":
                self.audit.repair_rate,

            "max_negative_eig":
                self.audit.max_negative_eig,

            "avg_negative_eig":
                self.audit.avg_negative_eig,

            "max_projection_shift":
                self.audit.max_projection_shift,

            "avg_projection_shift":
                self.audit.avg_projection_shift,
        }



def normalize_density_matrix(
    rho: np.ndarray,
    eps: float = 1e-12,
) -> np.ndarray:

    rho = hermitianize(rho)

    rho = trace_normalize(
        rho,
        eps=eps,
    )

    rho = hermitianize(rho)

    return rho



def unitary_step(
    rho: np.ndarray,
    U: np.ndarray,
) -> np.ndarray:

    return (
        U
        @ rho
        @ U.conj().T
    )



def trajectory_distance(
    raw_traj: List[np.ndarray],
    proj_traj: List[np.ndarray],
) -> dict:


    if len(raw_traj) != len(proj_traj):

        raise ValueError(
            "trajectory lengths differ"
        )


    shifts = []


    for raw, proj in zip(
        raw_traj,
        proj_traj,
    ):

        shifts.append(
            np.linalg.norm(
                raw - proj,
                ord="fro",
            )
        )


    shifts = np.asarray(
        shifts,
        dtype=float,
    )


    return {

        "mean_shift":
            float(np.mean(shifts)),

        "max_shift":
            float(np.max(shifts)),
    }



def raw_non_markov_step(
    rho_curr: np.ndarray,
    rho_prev: np.ndarray,
    U: np.ndarray,
    mem_strength: float,
) -> np.ndarray:


    rho_markov = (
        U
        @ rho_curr
        @ U.conj().T
    )


    rho_raw = (

        rho_markov

        +

        mem_strength
        *
        (
            rho_prev
            -
            rho_curr
        )
    )


    return rho_raw



def evolve_non_markov_projected(
    rho0: np.ndarray,
    steps: int,
    U: np.ndarray,
    mem_strength: float,
    eps: float = 1e-12,
) -> SimulationResultV03:


    if steps < 1:

        raise ValueError(
            "steps must be >= 1"
        )


    raw_traj: List[np.ndarray] = []

    proj_traj: List[np.ndarray] = []


    audit = ProjectionAudit()

    audit.steps = steps



    rho0 = normalize_density_matrix(
        rho0,
        eps,
    )


    raw_traj.append(rho0)

    proj_traj.append(rho0)



    rho_step = unitary_step(
        rho0,
        U,
    )


    rho_step = normalize_density_matrix(
        rho_step,
        eps,
    )


    raw_traj.append(rho_step)

    proj_traj.append(rho_step)



    for _ in range(1, steps):


        rho_curr = proj_traj[-1]

        rho_prev = proj_traj[-2]


        rho_raw = raw_non_markov_step(

            rho_curr=rho_curr,

            rho_prev=rho_prev,

            U=U,

            mem_strength=mem_strength,
        )


        raw_traj.append(
            rho_raw
        )


        rho_proj = repair_state(

            rho_raw,

            audit=audit,

            eps=eps,
        )


        proj_traj.append(
            rho_proj
        )



    return SimulationResultV03(

        rho_final=
            proj_traj[-1],

        raw_traj=
            raw_traj,

        proj_traj=
            proj_traj,

        audit=
            audit,

        steps=
            steps,

        mem_strength=
            mem_strength,
    )



def validate_result(
    result: SimulationResultV03,
) -> dict:

    return is_physical_state(
        result.rho_final
    )



if __name__ == "__main__":


    print(
        "\n=== EVOLUTION V0.3 SELF TEST ==="
    )


    theta = 0.20


    U = np.array(

        [

            [
                np.cos(theta),
                -np.sin(theta)
            ],

            [
                np.sin(theta),
                np.cos(theta)
            ],

        ],

        dtype=complex,
    )


    rho0 = np.array(

        [

            [
                1.0,
                0.0
            ],

            [
                0.0,
                0.0
            ],

        ],

        dtype=complex,
    )



    result = evolve_non_markov_projected(

        rho0=rho0,

        steps=50,

        U=U,

        mem_strength=0.30,
    )



    print("\nValidation: - evolution_v03.py:387")

    print(
        validate_result(result)
    )


    print("\nAudit: - evolution_v03.py:394")

    print(
        result.audit.summary()
    )


    print("\nTrajectory Distance: - evolution_v03.py:401")

    print(

        trajectory_distance(

            result.raw_traj,

            result.proj_traj,

        )

    )


    print("\nSummary: - evolution_v03.py:416")

    print(
        result.summary()
    )