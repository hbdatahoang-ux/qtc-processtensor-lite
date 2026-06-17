import os
import sys
from dataclasses import dataclass

import yaml
import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import expm

from divergence_map import DivergenceLandscape
from m25_filter import M25RobustnessFilter

from truncation import mpo_like_truncation
from metrics import trace_distance


# ============================================================
# CONFIG
# ============================================================

config_global = None


def load_config(path="configs/default.yaml"):
    if not os.path.exists(path):
        print(f"ERROR: Config file not found: {path} - main_unified.py:27")
        sys.exit(1)

    with open(path, "r", encoding="utf-8-sig") as f:
        return yaml.safe_load(f)


def setup_directories():
    os.makedirs("data", exist_ok=True)
    os.makedirs("figures", exist_ok=True)
    os.makedirs("logs", exist_ok=True)


# ============================================================
# RESULT OBJECT
# ============================================================

@dataclass
class SimulationResult:
    rho: np.ndarray
    metrics: np.ndarray
    worst_min_eig: float = 0.0
    worst_trace_err: float = 0.0


# ============================================================
# PHYSICS ENGINE
# ============================================================

def initialize_state(dim, seed):
    rng = np.random.default_rng(seed)

    psi = (
        rng.standard_normal(dim)
        + 1j * rng.standard_normal(dim)
    )

    psi /= np.linalg.norm(psi)

    return np.outer(psi, psi.conj())


def build_hamiltonian(dim, seed):
    rng = np.random.default_rng(seed)

    H_raw = (
        rng.standard_normal((dim, dim))
        + 1j * rng.standard_normal((dim, dim))
    )

    return 0.5 * (H_raw + H_raw.conj().T)


def evolve_markov(rho0, steps, U):

    traj = [rho0]

    for _ in range(steps):

        rho_next = (
            U
            @ traj[-1]
            @ U.conj().T
        )

        rho_next /= np.trace(rho_next)

        traj.append(rho_next)

    return traj


def evolve_non_markov(
    rho0,
    steps,
    U,
    mem_strength
):

    traj = [rho0]

    worst_min_eig = 0.0
    worst_trace_err = 0.0

    rho1 = U @ rho0 @ U.conj().T
    rho1 /= np.trace(rho1)

    traj.append(rho1)

    for _ in range(1, steps):

        rho_curr = traj[-1]
        rho_prev = traj[-2]

        rho_markov = (
            U
            @ rho_curr
            @ U.conj().T
        )

        memory_term = (
            mem_strength
            * (rho_prev - rho_curr)
        )

        rho_raw = rho_markov + memory_term

        trace_err = abs(
            np.trace(rho_raw) - 1.0
        )

        worst_trace_err = max(
            worst_trace_err,
            float(trace_err)
        )

        tr = np.trace(rho_raw)

        if abs(tr) < 1e-14:
            break

        rho_next = rho_raw / tr

        rho_h = 0.5 * (
            rho_next +
            rho_next.conj().T
        )

        min_eig = np.min(
            np.linalg.eigvalsh(rho_h)
        )

        worst_min_eig = min(
            worst_min_eig,
            float(min_eig)
        )

        traj.append(rho_next)

    return (
        traj,
        worst_min_eig,
        worst_trace_err
    )


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(
    rho,
    chi_list
):

    errors = []

    for chi in chi_list:

        rho_trunc = mpo_like_truncation(
            rho,
            chi
        )

        err = trace_distance(
            rho,
            rho_trunc
        )

        errors.append(float(err))

    return np.asarray(errors)


# ============================================================
# WRAPPERS
# ============================================================

def bm1_wrapper(
    dt,
    seed,
    eps,
    mem_strength
):

    dim = 16

    rho0 = initialize_state(
        dim,
        seed
    )

    H = build_hamiltonian(
        dim,
        seed
    )

    U = expm(
        -1j * H * dt
    )

    traj = evolve_markov(
        rho0,
        steps=20,
        U=U
    )

    rho_final = traj[-1]

    metrics = calculate_metrics(
        rho_final,
        config_global["chi_list"]
    )

    return SimulationResult(
        rho=rho_final,
        metrics=metrics
    )


def bm2_wrapper(
    dt,
    seed,
    eps,
    mem_strength
):

    dim = 16

    rho0 = initialize_state(
        dim,
        seed
    )

    H = build_hamiltonian(
        dim,
        seed
    )

    U = expm(
        -1j * H * dt
    )

    (
        traj,
        worst_min_eig,
        worst_trace_err
    ) = evolve_non_markov(
        rho0,
        steps=20,
        U=U,
        mem_strength=mem_strength
    )

    rho_final = traj[-1]

    metrics = calculate_metrics(
        rho_final,
        config_global["chi_list"]
    )

    return SimulationResult(
        rho=rho_final,
        metrics=metrics,
        worst_min_eig=worst_min_eig,
        worst_trace_err=worst_trace_err
    )


# ============================================================
# VALIDATION
# ============================================================

def run_v02_validation():

    print("\n=== V0.2 VALIDATION === - main_unified.py:302")

    params = {
        "dt": config_global["dt"],
        "seed": config_global["seed"],
        "eps": config_global["eps"],
        "mem_strength": 0.0
    }

    bm1 = bm1_wrapper(**params)
    bm2 = bm2_wrapper(**params)

    diff = np.linalg.norm(
        bm1.metrics - bm2.metrics
    )

    print(
        f"Markov Limit : "
        f"{'PASS' if diff < 1e-12 else 'FAIL'} "
        f"({diff:.3e})"
    )

    a = bm2_wrapper(
        dt=config_global["dt"],
        seed=config_global["seed"],
        eps=config_global["eps"],
        mem_strength=0.10
    )

    b = bm2_wrapper(
        dt=config_global["dt"],
        seed=config_global["seed"],
        eps=config_global["eps"],
        mem_strength=0.10
    )

    det_diff = np.linalg.norm(
        a.rho - b.rho
    )

    print(
        f"Determinism  : "
        f"{'PASS' if det_diff < 1e-12 else 'FAIL'} "
        f"({det_diff:.3e})"
    )


def run_memory_sweep():

    print("\n=== MEMORY SWEEP === - main_unified.py:351")

    base = bm1_wrapper(
        dt=config_global["dt"],
        seed=config_global["seed"],
        eps=config_global["eps"],
        mem_strength=0.0
    )

    print(
        f"\n{'Memory':<10} | "
        f"{'Divergence':<15} | "
        f"{'WorstMinEig':<15} | "
        f"{'WorstTraceErr':<15}"
    )

    print("" * 70)

    for mem in [
        0.00,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30
    ]:

        res = bm2_wrapper(
            dt=config_global["dt"],
            seed=config_global["seed"],
            eps=config_global["eps"],
            mem_strength=mem
        )

        div = np.linalg.norm(
            base.metrics - res.metrics
        )

        print(
            f"{mem:<10.2f} | "
            f"{div:<15.6e} | "
            f"{res.worst_min_eig:<15.6e} | "
            f"{res.worst_trace_err:<15.6e}"
        )


# ============================================================
# AUDIT
# ============================================================

def audit_runner(
    dt,
    seed,
    eps
):

    dim = 16

    rho0 = initialize_state(
        dim,
        seed
    )

    H = build_hamiltonian(
        dim,
        seed
    )

    U = expm(
        -1j * H * dt
    )

    return evolve_markov(
        rho0,
        steps=20,
        U=U
    )


# ============================================================
# PLOT
# ============================================================

def plot_surface(
    surface,
    chi_list
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        chi_list,
        surface.flatten(),
        marker="o"
    )

    plt.axhline(
        y=0,
        linestyle="--"
    )

    plt.xlabel("Chi")
    plt.ylabel("log10(BM2/BM1)")
    plt.title("QTC Divergence Landscape")

    plt.grid(True)
    plt.tight_layout()

    output_path = (
        "figures/divergence_landscape.png"
    )

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"[INFO] Plot saved: {output_path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    global config_global

    setup_directories()

    config_global = load_config()

    print("= - main_unified.py:488" * 80)
    print("QTC ProcessTensor Lite V0.2 - main_unified.py:489")
    print("= - main_unified.py:490" * 80)

    m25 = M25RobustnessFilter(
        runner_func=audit_runner
    )

    audit_result = m25.run_all_tests(
        {
            "dt_list": [config_global["dt"]],
            "seeds": [config_global["seed"]],
            "eps_list": [config_global["eps"]]
        }
    )

    print("\nM2.5 AUDIT - main_unified.py:504")
    print(audit_result)

    run_v02_validation()

    run_memory_sweep()

    params = {
        "dt": config_global["dt"],
        "seed": config_global["seed"],
        "eps": config_global["eps"],
        "mem_strength": config_global["memory_strength"]
    }

    bm1 = bm1_wrapper(**params)
    bm2 = bm2_wrapper(**params)

    print("\nBM1 Errors - main_unified.py:521")
    print(bm1.metrics)

    print("\nBM2 Errors - main_unified.py:524")
    print(bm2.metrics)

    print(
        f"\nWorstMinEig   : "
        f"{bm2.worst_min_eig:.3e}"
    )

    print(
        f"WorstTraceErr : "
        f"{bm2.worst_trace_err:.3e}"
    )

    engine = DivergenceLandscape(
        bm1_wrapper,
        bm2_wrapper
    )

    surface = engine.run_surface(
        config_global["chi_list"],
        [params]
    )

    np.save(
        "data/result.npy",
        surface
    )

    plot_surface(
        surface,
        config_global["chi_list"]
    )

    print("\nSimulation Finished. - main_unified.py:557")


if __name__ == "__main__":
    main()

