# ============================================================
# m25_filter.py
# QTC ProcessTensor Lite V0.2
# M2.5 Robustness Audit Layer
# ============================================================

import numpy as np


class M25RobustnessFilter:
    """
    M2.5 Robustness Filter

    Audit numerical stability and physical consistency
    of generated density matrices.

    Checks:
        - NaN / Inf
        - Hermiticity
        - Trace Preservation
        - Positivity

    Designed to never crash the benchmark pipeline.
    """

    def __init__(
        self,
        runner_func,
        herm_tol=1e-8,
        trace_tol=1e-5,
        eig_tol=-1e-8
    ):
        self.runner = runner_func

        self.herm_tol = herm_tol
        self.trace_tol = trace_tol
        self.eig_tol = eig_tol

    # ========================================================
    # Internal Checks
    # ========================================================

    def _check_nan_inf(self, rho):

        if np.isnan(rho).any():
            return False, "NaN detected"

        if np.isinf(rho).any():
            return False, "Inf detected"

        return True, "OK"

    def _check_hermitian(self, rho):

        herm_err = np.linalg.norm(
            rho - rho.conj().T
        )

        if herm_err > self.herm_tol:
            return (
                False,
                f"Non-Hermitian (err={herm_err:.3e})"
            )

        return True, "OK"

    def _check_trace(self, rho):

        tr = np.trace(rho)

        trace_err = abs(tr - 1.0)

        if trace_err > self.trace_tol:

            return (
                False,
                f"Trace violation ({trace_err:.3e})"
            )

        return True, "OK"

    def _check_positivity(self, rho):

        rho_h = 0.5 * (
            rho +
            rho.conj().T
        )

        eigvals = np.linalg.eigvalsh(rho_h)

        min_eig = float(np.min(eigvals))

        if min_eig < self.eig_tol:

            return (
                False,
                f"Negative eigenvalue ({min_eig:.3e})"
            )

        return True, "OK"

    # ========================================================
    # Matrix Audit
    # ========================================================

    def check_stability(
        self,
        rho
    ):
        """
        Audit single density matrix.
        """

        rho = np.asarray(rho)

        diagnostics = {
            "trace": float(np.real(np.trace(rho))),
            "min_eig": None,
            "herm_error": None
        }

        # ----------------------------
        # NaN / Inf
        # ----------------------------

        status, msg = self._check_nan_inf(rho)

        if not status:
            return False, msg, diagnostics

        # ----------------------------
        # Hermiticity
        # ----------------------------

        herm_error = np.linalg.norm(
            rho - rho.conj().T
        )

        diagnostics["herm_error"] = float(
            herm_error
        )

        status, msg = self._check_hermitian(rho)

        if not status:
            return False, msg, diagnostics

        # ----------------------------
        # Trace
        # ----------------------------

        status, msg = self._check_trace(rho)

        if not status:
            return False, msg, diagnostics

        # ----------------------------
        # Positivity
        # ----------------------------

        rho_h = 0.5 * (
            rho +
            rho.conj().T
        )

        eigvals = np.linalg.eigvalsh(rho_h)

        diagnostics["min_eig"] = float(
            np.min(eigvals)
        )

        status, msg = self._check_positivity(rho)

        if not status:
            return False, msg, diagnostics

        return True, "PASSED", diagnostics

    # ========================================================
    # Full Audit
    # ========================================================

    def run_all_tests(
        self,
        test_config
    ):
        """
        test_config = {
            "dt_list": [...],
            "seeds": [...],
            "eps_list": [...]
        }
        """

        logs = []

        total_cases = 0
        passed_cases = 0

        worst_min_eig = np.inf
        worst_trace_error = 0.0

        try:

            for dt in test_config["dt_list"]:

                for seed in test_config["seeds"]:

                    for eps in test_config["eps_list"]:

                        total_cases += 1

                        result = self.runner(
                            dt=dt,
                            seed=seed,
                            eps=eps
                        )

                        if not isinstance(
                            result,
                            (list, tuple)
                        ):
                            result = [result]

                        case_ok = True

                        for rho in result:

                            status, msg, diag = (
                                self.check_stability(rho)
                            )

                            if diag["min_eig"] is not None:

                                worst_min_eig = min(
                                    worst_min_eig,
                                    diag["min_eig"]
                                )

                            trace_err = abs(
                                diag["trace"] - 1.0
                            )

                            worst_trace_error = max(
                                worst_trace_error,
                                trace_err
                            )

                            if not status:

                                case_ok = False

                                logs.append(
                                    (
                                        f"[FAIL] "
                                        f"dt={dt}, "
                                        f"seed={seed}, "
                                        f"eps={eps} -> "
                                        f"{msg}"
                                    )
                                )

                        if case_ok:
                            passed_cases += 1

        except Exception as exc:

            logs.append(
                f"[CRITICAL CRASH] {exc}"
            )

            return {
                "M2_5_ALL_PASSED": False,
                "total_cases": total_cases,
                "passed_cases": passed_cases,
                "worst_min_eig": None,
                "worst_trace_error": None,
                "logs": logs
            }

        return {
            "M2_5_ALL_PASSED":
                passed_cases == total_cases,

            "total_cases":
                total_cases,

            "passed_cases":
                passed_cases,

            "worst_min_eig":
                float(worst_min_eig)
                if np.isfinite(worst_min_eig)
                else None,

            "worst_trace_error":
                float(worst_trace_error),

            "logs":
                logs
        }