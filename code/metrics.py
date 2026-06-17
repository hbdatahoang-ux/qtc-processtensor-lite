# ============================================================
# metrics.py
# QTC ProcessTensor Lite V0.2
# ============================================================

import numpy as np
import scipy.linalg


# ============================================================
# BASIC HELPERS
# ============================================================

def hermitize(rho):
    """
    Return Hermitian part of rho.

    Useful when numerical noise creates
    tiny anti-Hermitian components.
    """
    return 0.5 * (
        rho +
        rho.conj().T
    )


# ============================================================
# TRACE DISTANCE
# ============================================================

def trace_distance(rho1, rho2):
    """
    Trace distance:

        D(rho1,rho2)
        = 0.5 ||rho1-rho2||_1

    where ||A||_1 is the trace norm
    (sum of singular values).

    Returns
    -------
    float
    """

    diff = rho1 - rho2

    return float(
        0.5 *
        np.linalg.norm(
            diff,
            ord="nuc"
        )
    )


# ============================================================
# FIDELITY
# ============================================================

def fidelity(rho1, rho2):
    """
    Uhlmann Fidelity

    F(rho1,rho2)
    =
    (Tr[sqrt(
        sqrt(rho1)
        rho2
        sqrt(rho1)
    )])^2

    Robust against small numerical
    negativity.
    """

    rho1_h = hermitize(rho1)
    rho2_h = hermitize(rho2)

    try:

        sqrt_rho1 = scipy.linalg.sqrtm(
            rho1_h
        )

        inner = (
            sqrt_rho1
            @ rho2_h
            @ sqrt_rho1
        )

        inner = hermitize(inner)

        fid = np.trace(
            scipy.linalg.sqrtm(inner)
        )

        value = float(
            np.real(fid) ** 2
        )

        return float(
            np.clip(
                value,
                0.0,
                1.0
            )
        )

    except Exception:
        return np.nan


# ============================================================
# VON NEUMANN ENTROPY
# ============================================================

def von_neumann_entropy(
    rho,
    cutoff=1e-12
):
    """
    Von Neumann entropy

        S(rho)
        =
        -Tr(rho log rho)

    Returns
    -------
    float
    """

    rho_h = hermitize(rho)

    evals = np.linalg.eigvalsh(
        rho_h
    )

    evals = np.clip(
        evals,
        0.0,
        None
    )

    evals = evals[
        evals > cutoff
    ]

    if len(evals) == 0:
        return 0.0

    return float(
        -np.sum(
            evals *
            np.log(evals)
        )
    )


# ============================================================
# PURITY
# ============================================================

def purity(rho):
    """
    Purity

        P = Tr(rho^2)

    Pure state:
        P = 1

    Maximally mixed:
        P = 1/d
    """

    rho_h = hermitize(rho)

    value = np.trace(
        rho_h @ rho_h
    )

    return float(
        np.real(value)
    )


# ============================================================
# MIN EIGENVALUE
# ============================================================

def min_eigenvalue(rho):
    """
    Minimum eigenvalue.

    Useful for positivity diagnostics.
    """

    rho_h = hermitize(rho)

    return float(
        np.min(
            np.linalg.eigvalsh(
                rho_h
            )
        )
    )


# ============================================================
# TRACE ERROR
# ============================================================

def trace_error(rho):
    """
    Absolute trace deviation
    from unity.

        |Tr(rho)-1|
    """

    return float(
        abs(
            np.trace(rho) - 1.0
        )
    )


# ============================================================
# PHYSICALITY CHECK
# ============================================================

def physicality_report(
    rho,
    eig_tol=1e-8,
    trace_tol=1e-8
):
    """
    Quick physicality report.

    Returns
    -------
    dict
    """

    rho_h = hermitize(rho)

    herm_err = np.linalg.norm(
        rho - rho.conj().T
    )

    tr_err = abs(
        np.trace(rho) - 1.0
    )

    min_eval = np.min(
        np.linalg.eigvalsh(
            rho_h
        )
    )

    return {
        "is_physical":
            (
                herm_err < trace_tol
                and
                tr_err < trace_tol
                and
                min_eval > -eig_tol
            ),

        "hermitian_error":
            float(herm_err),

        "trace_error":
            float(tr_err),

        "min_eigenvalue":
            float(min_eval),

        "purity":
            purity(rho_h),

        "entropy":
            von_neumann_entropy(rho_h)
    }


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    dim = 4

    psi = np.zeros(
        dim,
        dtype=complex
    )

    psi[0] = 1.0

    rho_pure = np.outer(
        psi,
        psi.conj()
    )

    rho_mixed = (
        np.eye(dim)
        / dim
    )

    print("Trace Distance - metrics.py:315")
    print(
        trace_distance(
            rho_pure,
            rho_mixed
        )
    )

    print("\nFidelity - metrics.py:323")
    print(
        fidelity(
            rho_pure,
            rho_mixed
        )
    )

    print("\nEntropy - metrics.py:331")
    print(
        von_neumann_entropy(
            rho_mixed
        )
    )

    print("\nPurity - metrics.py:338")
    print(
        purity(
            rho_mixed
        )
    )

    print("\nPhysicality - metrics.py:345")
    print(
        physicality_report(
            rho_mixed
        )
    )