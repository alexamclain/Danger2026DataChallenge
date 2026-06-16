# Subsqrt Moonshot Lane B Real-Cyclotomic Residual

Date: 2026-06-12

## Result

The p25 reduced-anchor residual has a small post-producer certificate surface.
For prime `c`, the denominator-cleared residual is:

```text
D_c = sum_{k != 0} [zeta_c^k] - (c - 1)[1]
```

This is the diamond norm of the one-point divisor:

```text
[zeta_c] - [1]
```

The p25 `C_3 x C_13` and `C_3 x C_53` rows both pass this residual gate.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_real_cyclotomic_residual_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_real_cyclotomic_residual_gate.py
```

Observed:

```text
tiny_C3xC13:
  diamond_orbit_size = 12
  divisor_norm_ok = 1
  degree_zero_ok = 1
  Fourier profile = 36 nonzero slots
    pure right / C-zero slots = 0
    pure C slots = 12
    mixed slots = 24
  p mod 13 = 10
  ord_13(p) = 6
  ord_39(p) = 6
  mu_13 in F_p = 0
  real cyclotomic degree = 6
  real Frobenius orbit lengths = [3, 3]

prime_axis_C3xC53:
  diamond_orbit_size = 52
  divisor_norm_ok = 1
  degree_zero_ok = 1
  Fourier profile = 156 nonzero slots
    pure right / C-zero slots = 0
    pure C slots = 52
    mixed slots = 104
  p mod 53 = 29
  ord_53(p) = 26
  ord_159(p) = 26
  mu_53 in F_p = 0
  real cyclotomic degree = 26
  real Frobenius orbit lengths = [13, 13]

real_cyclotomic_residual_rows = 2/2
conclusion=reported_p25_laneB_real_cyclotomic_residual_gate
```

## Consequence

Plain cyclotomic Frobenius does not produce the full `C_3 x C_c` Lane B
quotient.  The missing producer still has to be a CM-Artin / modular-unit
pullback.

But if such a producer supplies the selected coordinate, the residual p-unit
check is small:

```text
C_3 x C_13 lab:
  two real-cyclotomic resultants of degree 3

C_3 x C_53 lab:
  two real-cyclotomic resultants of degree 13
```

So the current moonshot target is:

```text
construct the selected CM-Artin pullback of the reduced Jacobi packet;
then certify the single-anchor residual with two small real-cyclotomic
resultants and the Kummer/sign descent.
```

This is not a producer theorem.  It is the exact post-producer finite surface
we should use if the arithmetic object is found.

The next source-arithmetic checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_cm_artin_sources.md
```

It records that the first `C_3 x C_13` lab couples an inert `151` right source
to a split `677` C-axis source.  This rules out split-prime-only producer
searches as the next useful falsifier.
