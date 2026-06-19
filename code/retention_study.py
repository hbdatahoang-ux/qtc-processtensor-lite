# ============================================================
# retention_study.py
# QTC ProcessTensor Lite V0.3-dev
#
# V0.2 vs V0.3 Retention Benchmark
# ============================================================

from __future__ import annotations

import os
import json
import csv

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PATHS
# ============================================================

RESULT_DIR = "results/v03"

RETENTION_CSV = os.path.join(
    RESULT_DIR,
    "retention.csv"
)

RETENTION_JSON = os.path.join(
    RESULT_DIR,
    "retention.json"
)

AUDIT_JSON = os.path.join(
    RESULT_DIR,
    "projection_audit.json"
)

RETENTION_PLOT = os.path.join(
    RESULT_DIR,
    "retention_plot.png"
)

RETENTION_REPORT = os.path.join(
    RESULT_DIR,
    "retention_report.txt"
)


# ============================================================
# UTILITIES
# ============================================================

def ensure_output_dir():
    os.makedirs(
        RESULT_DIR,
        exist_ok=True
    )


def divergence(a, b):
    return float(
        np.linalg.norm(
            np.asarray(a)
            -
            np.asarray(b)
        )
    )


def retention_ratio(
    div_raw,
    div_proj
):
    if abs(div_raw) < 1e-14:

        if abs(div_proj) < 1e-14:
            return 100.0

        return 0.0

    return float(
        100.0
        *
        div_proj
        /
        div_raw
    )


# ============================================================
# CORE STUDY
# ============================================================

def run_retention_study(
    bm1_runner,
    bm2_runner,
    bm2_projected_runner,
    config
):

    ensure_output_dir()

    print("\n=== RETENTION STUDY === - retention_study.py:104")

    baseline = bm1_runner(
        dt=config["dt"],
        seed=config["seed"],
        eps=config["eps"],
        mem_strength=0.0
    )

    memory_grid = config.get(
        "memory_grid",
        [0.00, 0.05, 0.10,
         0.15, 0.20, 0.25,
         0.30]
    )

    rows = []

    print()
    print(
        f"{'Memory':<8}"
        f"{'DivRaw':>14}"
        f"{'DivProj':>14}"
        f"{'Retention%':>14}"
        f"{'SignalLoss':>16}"
        f"{'Repairs':>12}"
    )

    print("" * 80)

    for mem in memory_grid:

        raw = bm2_runner(
            dt=config["dt"],
            seed=config["seed"],
            eps=config["eps"],
            mem_strength=mem
        )

        proj = bm2_projected_runner(
            dt=config["dt"],
            seed=config["seed"],
            eps=config["eps"],
            mem_strength=mem
        )

        div_raw = divergence(
            baseline.metrics,
            raw.metrics
        )

        div_proj = divergence(
            baseline.metrics,
            proj.metrics
        )

        retention = retention_ratio(
            div_raw,
            div_proj
        )

        signal_loss = abs(
            div_raw
            -
            div_proj
        )

        audit = proj.audit

        row = {
            "memory": mem,
            "div_raw": div_raw,
            "div_proj": div_proj,
            "retention": retention,
            "signal_loss": signal_loss,
            "repair_count":
                audit.repair_count,
            "max_negative_eig":
                audit.max_negative_eig,
            "avg_negative_eig":
                audit.avg_negative_eig,
            "max_projection_shift":
                audit.max_projection_shift,
            "avg_projection_shift":
                audit.avg_projection_shift
        }

        rows.append(row)

        print(
            f"{mem:<8.2f}"
            f"{div_raw:>14.6e}"
            f"{div_proj:>14.6e}"
            f"{retention:>14.2f}"
            f"{signal_loss:>16.6e}"
            f"{audit.repair_count:>12d}"
        )

    return rows


# ============================================================
# EXPORTS
# ============================================================

def save_retention_csv(rows):

    with open(
        RETENTION_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"[INFO] Saved: {RETENTION_CSV}"
    )


def save_retention_json(rows):

    with open(
        RETENTION_JSON,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            rows,
            f,
            indent=4
        )

    print(
        f"[INFO] Saved: {RETENTION_JSON}"
    )


def save_projection_audit(rows):

    audit = {
        "total_repairs":
            int(
                sum(
                    r["repair_count"]
                    for r in rows
                )
            ),

        "worst_negative_eig":
            float(
                min(
                    r["max_negative_eig"]
                    for r in rows
                )
            ),

        "worst_projection_shift":
            float(
                max(
                    r["max_projection_shift"]
                    for r in rows
                )
            )
    }

    with open(
        AUDIT_JSON,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            audit,
            f,
            indent=4
        )

    print(
        f"[INFO] Saved: {AUDIT_JSON}"
    )


# ============================================================
# REPORT
# ============================================================

def build_summary(rows):

    retentions = [
        r["retention"]
        for r in rows
    ]

    signal_losses = [
        r["signal_loss"]
        for r in rows
    ]

    return {
        "avg_retention":
            float(np.mean(retentions)),
        "min_retention":
            float(np.min(retentions)),
        "max_retention":
            float(np.max(retentions)),
        "avg_signal_loss":
            float(np.mean(signal_losses)),
        "total_repairs":
            int(
                sum(
                    r["repair_count"]
                    for r in rows
                )
            )
    }


def save_report(rows):

    summary = build_summary(rows)

    lines = []

    lines.append(
        "QTC ProcessTensor Lite V0.3\n"
    )

    lines.append(
        "=" * 60 + "\n"
    )

    for k, v in summary.items():
        lines.append(
            f"{k}: {v}\n"
        )

    with open(
        RETENTION_REPORT,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(lines)

    print(
        f"[INFO] Saved: {RETENTION_REPORT}"
    )


# ============================================================
# PLOT
# ============================================================

def save_plot(rows):

    mem = [
        r["memory"]
        for r in rows
    ]

    retention = [
        r["retention"]
        for r in rows
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        mem,
        retention,
        marker="o"
    )

    plt.xlabel(
        "Memory Strength"
    )

    plt.ylabel(
        "Retention (%)"
    )

    plt.title(
        "V0.3 Retention Study"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        RETENTION_PLOT,
        dpi=300
    )

    plt.close()

    print(
        f"[INFO] Saved: {RETENTION_PLOT}"
    )


# ============================================================
# PIPELINE
# ============================================================

def export_all(rows):

    save_retention_csv(rows)

    save_retention_json(rows)

    save_projection_audit(rows)

    save_plot(rows)

    save_report(rows)


# ============================================================
# STANDALONE
# ============================================================

if __name__ == "__main__":

    print(
        "\nRetention study module loaded.\n"
        "Run via benchmark_v03.py "
        "or main_unified.py"
    )