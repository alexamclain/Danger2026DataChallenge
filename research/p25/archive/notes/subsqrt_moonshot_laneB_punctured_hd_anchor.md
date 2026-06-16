# Subsqrt Moonshot Lane B Punctured HD Anchor

Date: 2026-06-12

## Result

The p24 punctured Hasse-Davenport / single-anchor mechanism ports cleanly to
the p25 Lane B targets `C_3 x C_13` and `C_3 x C_53`.

For actual finite-field Jacobi sums

```text
U(r,k) = J(chi^(u*t(r,k)), chi^(v*t(r,k)))
```

on `C_3 x C_c`, every admissible right-mixed pair has the same pattern:

```text
raw packet:
  off-C pair-products are already constant
  full two-level pair-products fail
  selected row-product ratios fail

corrected packet:
  replace only J(1,1)=q-2 by 1
  pair-products pass
  selected row-product ratios pass
  full product formula passes
```

So the finite product-formula side is not the current obstruction.  The
producer-facing obstruction is now:

```text
construct a p25 negative-trace CM-Artin / modular-unit pullback of this reduced
Jacobi packet, and supply the single-anchor Kummer/sign descent.
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_punctured_hd_anchor_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_punctured_hd_anchor_gate.py
```

Observed:

```text
tiny_C3xC13:
  pairs_checked = 264/264
  base_field_q = 79
  value_field_l = 157
  q_minus_2 = 77
  raw_off_pair_hits = 264/264
  raw_two_level_pair_hits = 0/264
  raw_row_ratio_hits = 0/264
  corrected_pair_product_hits = 264/264
  corrected_row_ratio_hits = 264/264
  corrected_product_formula_hits = 264/264
  anchor_scale_formula_hits = 264/264
  anchor_has_13th_root = 0
  -anchor_has_13th_root = 0

prime_axis_C3xC53:
  pairs_checked = 5304/5304
  base_field_q = 3181
  value_field_l = 3499
  q_minus_2 = 3179
  raw_off_pair_hits = 5304/5304
  raw_two_level_pair_hits = 0/5304
  raw_row_ratio_hits = 0/5304
  corrected_pair_product_hits = 5304/5304
  corrected_row_ratio_hits = 5304/5304
  corrected_product_formula_hits = 5304/5304
  anchor_scale_formula_hits = 5304/5304
  anchor_has_53rd_root = 0
  -anchor_has_53rd_root = 0

punctured_hd_anchor_rows = 2/2
conclusion=reported_p25_laneB_punctured_hd_anchor_gate
```

## Cyclotomic Shadow

Plain cyclotomic Frobenius does not realize the full p25 quotient:

```text
C_3 x C_13:
  p mod 13 = 10
  ord_13(p) = 6
  ord_39(p) = 6
  quotient size = 39

C_3 x C_53:
  p mod 53 = 29
  ord_53(p) = 26
  ord_159(p) = 26
  quotient size = 159
```

This keeps the route honest: the producer cannot be the plain cyclotomic
Frobenius action.  It must be a CM-Artin pullback of the reduced Jacobi packet.

The positive news is that the real-cyclotomic residual is tiny:

```text
C_13 residual:
  real cyclotomic degree = 6
  splits over F_p into 2 components of degree 3

C_53 residual:
  real cyclotomic degree = 26
  splits over F_p into 2 components of degree 13
```

Thus, after a producer supplies the selected coordinate, the post-producer
residual check should be two small real-cyclotomic resultants rather than a
degree-`c` root-of-unity enumeration.

The explicit residual/resultant checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_real_cyclotomic_residual.md
```

The explicit Kummer/sign checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_kummer_sign_descent.md
```

It records that sign choice does not change the anchor class and that both
`q-2` and `-(q-2)` require a full degree-`c` Kummer extension.

## Consequence

Lane B now has a clean finite ladder:

```text
local quotient contract
=> literal Jacobi-carry packet
=> actual local-source pullback
=> scalar-normalized coupled divisor footprint
=> punctured Hasse-Davenport single-anchor product formula
```

The next falsifier is arithmetic, not finite linear algebra:

```text
Can the negative-trace class-field / modular-unit object realize the reduced
Jacobi packet on the 151 x 677 local source, including the single degenerate
anchor normalization and Kummer descent?
```

If it cannot produce the single-anchor correction, the Lane B moonshot dies.
If it can, the remaining verifier payload becomes unusually small for p25:
the `C_3 x C_13` lab needs only two degree-3 real-cyclotomic residual checks
after the selected producer is supplied.
