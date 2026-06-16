#!/usr/bin/env python3
"""Random-subspace failure estimate for the p24 trace-frame target."""

from __future__ import annotations

import math

P = 10**24 + 7
E_DEGREE = 5460
AXIS_DIM = 368
TRACE_FRAME_DIM = 3 * 179


def main() -> None:
    codim_margin = TRACE_FRAME_DIM - AXIS_DIM + 1
    log10_q = E_DEGREE * math.log10(P)
    log10_failure_leading = -codim_margin * log10_q
    print("p24 trace-frame random-subspace estimate")
    print(f"p={P}")
    print(f"E_degree={E_DEGREE}")
    print(f"log10_Q={log10_q:.6f}")
    print(f"axis_dim={AXIS_DIM}")
    print(f"trace_frame_dim={TRACE_FRAME_DIM}")
    print(f"codim_margin=trace_frame_dim-axis_dim+1={codim_margin}")
    print()
    print("random_matrix_model")
    print("  failure_probability = 1 - product_{i=0}^{axis_dim-1}(1-Q^(i-trace_frame_dim))")
    print("  leading_term ~= Q^-(trace_frame_dim-axis_dim+1)")
    print(f"  log10_leading_failure_probability ~= {log10_failure_leading:.6e}")
    print()
    print("interpretation")
    print("  random_failure_probability_is_astronomically_small=1")
    print("  any_failure_would_signal_a_structured_CM_annihilator=1")
    print("  probability_is_evidence_not_a_certificate=1")
    print("conclusion=reported_tensor_factor_trace_frame_probability")


if __name__ == "__main__":
    main()
