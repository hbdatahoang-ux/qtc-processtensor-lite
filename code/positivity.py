# ============================================================
# positivity.py
# QTC ProcessTensor Lite V0.3-dev
#
# Physical-State Projection Layer
#
# Responsibilities:
#   - Density-matrix validation
#   - PSD projection
#   - Repair auditing
#   - Projection diagnostics
#
# Independent from:
#   - compression layer
#   - benchmark layer
#   - visualization layer
# ============================================================

from dataclasses import dataclass, asdict

import numpy as np


# ============================================================
# AUDIT OBJECT
# ============================================================

@dataclass
class ProjectionAudit:
    """
    Collect projection statistics during
    non-Markovian evolution.

    Negative eigenvalues are stored with
    their original sign.
    """

    repair_count: int = 0

    projection_calls: int = 0

    max_negative_eig: float = 0.0
    total_negative_eig: float = 0.0

    max_projection_shift: float = 0.0
    total_projection_shift: float = 0.0

    steps: int = 0

    @property
    def avg_negative_eig(self) -> float:

        if self.repair_count == 0:
            return 0.0

        return (
            self.total_negative_eig
            / self.repair_count
        )

    @property
    def avg_projection_shift(self) -> float:

        if self.projection_calls == 0:
            return 0.0

        return (
            self.total_projection_shift
            / self.projection_calls
        )

    @property
    def repair_rate(self) -> float:

        if self.steps == 0:
            return 0.0

        return (
            self.repair_count
            / self.steps
        )

    def summary(self):

        data = asdict(self)

        data.update(
            {
                "avg_negative_eig":
                    self.avg_negative_eig,

                "avg_projection_shift":
                    self.avg_projection_shift,

                "repair_rate":
                    self.repair_rate,
            }
        )

        return data


# ============================================================
# BASIC UTILITIES
# ============================================================

def hermitianize(rho):
    """
    Force Hermitian symmetry.

    rho -> (rho + rho†)/2
    """

    rho = np.asarray(
        rho,
        dtype=complex
    )

    return 0.5 * (
        rho +
        rho.conj().T
    )


def trace_normalize(
    rho,
    eps=1e-12
):
    """
    Normalize density matrix
    to unit trace.
    """

    dim = rho.shape[0]

    tr = float(
        np.real(
            np.trace(rho)
        )
    )

    if abs(tr) < eps:

        return (
            np.eye(
                dim,
                dtype=complex
            )
            / dim
        )

    return rho / tr


def minimum_eigenvalue(rho):
    """
    Minimum eigenvalue of Hermitian part.
    """

    rho_h = hermitianize(rho)

    return float(
        np.min(
            np.linalg.eigvalsh(rho_h)
        )
    )


def state_frobenius_norm(rho):
    """
    Frobenius norm.
    """

    return float(
        np.linalg.norm(
            rho,
            ord="fro"
        )
    )


# ============================================================
# PHYSICALITY VALIDATION
# ============================================================

def is_physical_state(
    rho,
    atol=1e-10
):
    """
    Validate density matrix.

    Conditions:
        Hermitian
        PSD
        Trace = 1
    """

    rho_h = hermitianize(rho)

    hermitian_ok = np.allclose(
        rho_h,
        rho_h.conj().T,
        atol=atol
    )

    trace_ok = np.isclose(
        np.real(np.trace(rho_h)),
        1.0,
        atol=atol
    )

    min_eig = minimum_eigenvalue(
        rho_h
    )

    positivity_ok = (
        min_eig >= -atol
    )

    return {
        "valid":
            (
                hermitian_ok
                and trace_ok
                and positivity_ok
            ),

        "hermitian":
            hermitian_ok,

        "trace":
            trace_ok,

        "positivity":
            positivity_ok,

        "min_eig":
            min_eig,
    }


# ============================================================
# PSD PROJECTION
# ============================================================

def project_to_physical_state(
    rho,
    eps=1e-12
):
    """
    Project matrix onto physical
    density-matrix manifold.

    Steps
    -----
    1. Hermitianization
    2. Spectral decomposition
    3. Eigenvalue clipping
    4. Reconstruction
    5. Trace normalization
    """

    dim = rho.shape[0]

    rho_h = hermitianize(
        rho
    )

    evals, evecs = np.linalg.eigh(
        rho_h
    )

    evals_clipped = np.maximum(
        evals,
        eps
    )

    rho_proj = (
        evecs
        @ np.diag(evals_clipped)
        @ evecs.conj().T
    )

    rho_proj = hermitianize(
        rho_proj
    )

    rho_proj = trace_normalize(
        rho_proj,
        eps=eps
    )

    rho_proj = hermitianize(
        rho_proj
    )

    return rho_proj


# ============================================================
# REPAIR METRICS
# ============================================================

def projection_shift(
    rho_raw,
    rho_projected
):
    """
    Frobenius shift induced
    by projection.
    """

    return float(
        np.linalg.norm(
            rho_raw -
            rho_projected,
            ord="fro"
        )
    )


def relative_projection_shift(
    rho_raw,
    rho_projected,
    eps=1e-12
):
    """
    Relative repair impact.

    shift / ||rho_raw||
    """

    denom = max(
        state_frobenius_norm(
            rho_raw
        ),
        eps
    )

    return (
        projection_shift(
            rho_raw,
            rho_projected
        )
        / denom
    )


# ============================================================
# AUDITED REPAIR
# ============================================================

def repair_state(
    rho,
    audit=None,
    eps=1e-12
):
    """
    Repair state and update audit.
    """

    min_eig = minimum_eigenvalue(
        rho
    )

    rho_proj = project_to_physical_state(
        rho,
        eps=eps
    )

    shift = projection_shift(
        rho,
        rho_proj
    )

    if audit is not None:

        audit.projection_calls += 1

        audit.total_projection_shift += (
            shift
        )

        audit.max_projection_shift = max(
            audit.max_projection_shift,
            shift
        )

        if min_eig < 0.0:

            audit.repair_count += 1

            audit.total_negative_eig += (
                min_eig
            )

            audit.max_negative_eig = min(
                audit.max_negative_eig,
                min_eig
            )

    return rho_proj


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    rng = np.random.default_rng(42)

    A = (
        rng.standard_normal((4, 4))
        +
        1j * rng.standard_normal((4, 4))
    )

    rho_bad = (
        A +
        A.conj().T
    )

    rho_bad = trace_normalize(
        rho_bad
    )

    audit = ProjectionAudit()

    rho_fixed = repair_state(
        rho_bad,
        audit
    )

    print(
        "\n=== POSITIVITY SELF TEST ==="
    )

    print(
        "\nValidation:"
    )

    print(
        is_physical_state(
            rho_fixed
        )
    )

    print(
        "\nAudit:"
    )

    print(
        audit.summary()
    )

    print(
        "\nMinEig After:"
    )

    print(
        minimum_eigenvalue(
            rho_fixed
        )
    )