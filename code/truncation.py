# ============================================================
# truncation.py
# QTC ProcessTensor Lite V0.2
# ============================================================

import numpy as np


def mpo_like_truncation(
    rho,
    chi,
    eps=1e-12
):
    """
    MPO-like compression using SVD truncation.

    Parameters
    ----------
    rho : ndarray

    chi : int
        Effective bond dimension.

    Returns
    -------
    ndarray
        Truncated density matrix.
    """

    rho = np.asarray(
        rho,
        dtype=complex
    )

    dim = rho.shape[0]

    # --------------------------------------------------------
    # No truncation needed
    # --------------------------------------------------------

    if chi >= dim:
        return rho.copy()

    if chi <= 0:
        return np.eye(dim) / dim

    # --------------------------------------------------------
    # SVD
    # --------------------------------------------------------

    U, s, Vh = np.linalg.svd(
        rho,
        full_matrices=False
    )

    # --------------------------------------------------------
    # Truncate
    # --------------------------------------------------------

    U = U[:, :chi]
    s = s[:chi]
    Vh = Vh[:chi, :]

    rho_trunc = (
        U
        @ np.diag(s)
        @ Vh
    )

    # --------------------------------------------------------
    # Hermitize
    # --------------------------------------------------------

    rho_trunc = 0.5 * (
        rho_trunc +
        rho_trunc.conj().T
    )

    # --------------------------------------------------------
    # Normalize trace
    # --------------------------------------------------------

    tr = np.trace(
        rho_trunc
    )

    if abs(tr) < eps:

        return (
            np.eye(
                dim,
                dtype=complex
            )
            / dim
        )

    rho_trunc = rho_trunc / tr

    return rho_trunc


# ============================================================
# TRUNCATION ERROR
# ============================================================

def truncation_error(
    singular_values,
    chi
):
    """
    Frobenius tail estimate.

    Useful diagnostic metric.
    """

    s = np.asarray(
        singular_values,
        dtype=float
    )

    if chi >= len(s):
        return 0.0

    return float(
        np.sqrt(
            np.sum(
                s[chi:] ** 2
            )
        )
    )


# ============================================================
# SPECTRUM ANALYSIS
# ============================================================

def singular_spectrum(
    rho
):
    """
    Return singular value spectrum.
    """

    _, s, _ = np.linalg.svd(
        rho,
        full_matrices=False
    )

    return s


# ============================================================
# COMPRESSION REPORT
# ============================================================

def compression_report(
    rho,
    chi
):
    """
    Diagnostic helper.
    """

    _, s, _ = np.linalg.svd(
        rho,
        full_matrices=False
    )

    rho_trunc = mpo_like_truncation(
        rho,
        chi
    )

    return {
        "chi": int(chi),
        "rank_original":
            int(np.linalg.matrix_rank(rho)),
        "rank_truncated":
            int(np.linalg.matrix_rank(rho_trunc)),
        "largest_sv":
            float(np.max(s)),
        "smallest_sv":
            float(np.min(s)),
        "tail_error":
            truncation_error(
                s,
                chi
            ),
        "trace":
            float(
                np.real(
                    np.trace(
                        rho_trunc
                    )
                )
            )
    }


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    dim = 16

    rng = np.random.default_rng(42)

    A = (
        rng.standard_normal((dim, dim))
        +
        1j * rng.standard_normal((dim, dim))
    )

    rho = A @ A.conj().T
    rho /= np.trace(rho)

    for chi in [1, 2, 4, 8, 16]:

        rep = compression_report(
            rho,
            chi
        )

        print(rep)