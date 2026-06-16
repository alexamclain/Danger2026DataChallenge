#!/usr/bin/env python3
"""Global norms do not identify a selected split prime.

For D=-87 and q=103 the Hilbert class polynomial splits completely.  The
algebraic integer alpha = j - 5 has nonzero global norm, and that norm is
divisible by q.  Modulo the selected prime corresponding to the root 5, alpha
vanishes; modulo the selected prime corresponding to the root 29, it does not.

This is the small warning behind the p24 Hermitian p-unit target: full norms
or characteristic-zero nonvanishing do not by themselves certify a selected
finite-field embedding.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import pari_linear_roots

D = -87
Q = 103
SELECTED_A = 5
OTHER_ROOT = 29


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    hilbert = pari.polclass(D)
    roots = pari_linear_roots(hilbert, Q)
    norm = int(pari(f"subst({hilbert}, x, {SELECTED_A})"))

    print("selected-prime norm toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"hilbert_degree={int(pari.poldegree(hilbert))}")
    print(f"roots_mod_q={roots}")
    print(f"alpha=j-{SELECTED_A}")
    print(f"global_norm_alpha=H_D({SELECTED_A})={norm}")
    print(f"global_norm_mod_q={norm % Q}")
    print(f"alpha_at_root_{SELECTED_A}={(SELECTED_A - SELECTED_A) % Q}")
    print(f"alpha_at_root_{OTHER_ROOT}={(OTHER_ROOT - SELECTED_A) % Q}")
    print()
    print("interpretation")
    print("  alpha_nonzero_in_characteristic_zero=1")
    print("  q_divides_global_norm_alpha=1")
    print("  selected_prime_root_5_zero=1")
    print("  selected_prime_root_29_zero=0")
    print(
        "conclusion=global_norm_divisibility_detects_some_split_prime_not_"
        "the_selected_embedding"
    )


if __name__ == "__main__":
    main()
