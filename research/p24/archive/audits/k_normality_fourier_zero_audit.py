#!/usr/bin/env python3
"""Numeric audit for the K-normality Fourier-zero boundary."""

from __future__ import annotations

import math

P24 = 10**24 + 7
N = 3107441
ORD_N_P = 388430


def main() -> None:
    remaining_support = N - ORD_N_P
    uncertainty_lower = math.ceil(N / remaining_support)
    print("K-normality Fourier-zero audit")
    print(f"p={P24}")
    print(f"n={N}")
    print(f"packet_size=ord_n(p)={ORD_N_P}")
    print(f"packet_count={(N - 1) // ORD_N_P}")
    print(f"fourier_support_after_one_packet_zero_at_most={remaining_support}")
    print(f"cyclic_uncertainty_time_support_lower_bound={uncertainty_lower}")
    print()
    print("interpretation")
    print("  one_packet_zero_is_frequency_domain_vanishing=1")
    print("  support_lower_bound_two_is_not_enough_for_modular_zero_lemma=1")
    print("  k_normality_needs_moore_or_cm_arithmetic_input=1")
    print("conclusion=reported_k_normality_fourier_zero_audit")


if __name__ == "__main__":
    main()
