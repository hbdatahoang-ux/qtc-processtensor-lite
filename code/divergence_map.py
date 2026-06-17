# ============================================================
# divergence_map.py
# QTC ProcessTensor Lite V0.2
# ============================================================

import numpy as np


class DivergenceLandscape:
    """
    BM1 vs BM2 divergence analysis engine.

    Compatible with SimulationResult.

    Output:
        surface[row, chi]
        = log10(BM2/BM1)
    """

    NUMERICAL_FLOOR = 1e-12

    def __init__(
        self,
        bm1_runner,
        bm2_runner
    ):
        self.bm1 = bm1_runner
        self.bm2 = bm2_runner

    @classmethod
    def safe_log_ratio(
        cls,
        numerator,
        denominator
    ):
        numerator = np.asarray(
            numerator,
            dtype=float
        )

        denominator = np.asarray(
            denominator,
            dtype=float
        )

        return np.log10(
            (numerator + cls.NUMERICAL_FLOOR)
            /
            (denominator + cls.NUMERICAL_FLOOR)
        )

    def run_surface(
        self,
        chi_list,
        lambda_grid
    ):
        """
        Parameters
        ----------
        chi_list : list[int]

        lambda_grid : list[dict]

        Returns
        -------
        ndarray
            shape = (len(lambda_grid), len(chi_list))
        """

        n_rows = len(lambda_grid)
        n_cols = len(chi_list)

        surface = np.zeros(
            (n_rows, n_cols),
            dtype=float
        )

        for row_idx, params in enumerate(lambda_grid):

            bm1_result = self.bm1(**params)
            bm2_result = self.bm2(**params)

            e1 = np.asarray(
                bm1_result.metrics,
                dtype=float
            )

            e2 = np.asarray(
                bm2_result.metrics,
                dtype=float
            )

            if e1.shape != e2.shape:
                raise ValueError(
                    "BM1/BM2 metric shape mismatch: "
                    f"{e1.shape} vs {e2.shape}"
                )

            surface[row_idx] = (
                self.safe_log_ratio(
                    e2,
                    e1
                )
            )

        return surface


# ============================================================
# DETECTOR A4
# ============================================================

def persistent_divergence(
    bm1_err,
    bm2_err,
    warmup=2,
    threshold=0.20
):
    """
    Persistent divergence detector.

    Ignore low-chi region and inspect
    convergence tail only.
    """

    bm1 = np.asarray(
        bm1_err,
        dtype=float
    )

    bm2 = np.asarray(
        bm2_err,
        dtype=float
    )

    delta = np.abs(
        np.log10(
            (bm2 + 1e-12)
            /
            (bm1 + 1e-12)
        )
    )

    tail = (
        delta[warmup:]
        if len(delta) > warmup
        else delta
    )

    score = float(np.mean(tail))

    return {
        "score": score,
        "persistent": score > threshold,
        "tail_values": tail.tolist(),
        "max_tail": float(np.max(tail)),
        "min_tail": float(np.min(tail))
    }


# ============================================================
# SUMMARY
# ============================================================

def summarize_surface(
    surface
):
    arr = np.asarray(
        surface,
        dtype=float
    )

    return {
        "shape": arr.shape,
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr))
    }