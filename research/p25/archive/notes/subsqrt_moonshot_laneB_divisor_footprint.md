# Subsqrt Moonshot Lane B Divisor Footprint

Date: 2026-06-12

## Result

The p25 Lane B local pullback has a concrete divisor-footprint profile.  The
raw Jacobi-carry packet is not degree-zero: it contains a nonzero scalar
character component.  After subtracting exactly that scalar component, the
packet becomes degree-zero and row-balanced, but the remaining local part is
still genuinely coupled across `C_3 x C_c`.  It is not a sum of a right-axis
unit and a C-axis unit.

This sharpens the next arithmetic embedding target:

```text
embedded producer = global scalar/polar normalization + coupled local divisor
```

For the first target, that coupled local divisor is the `151 x 677` pullback
realizing `C_3 x C_13`.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_divisor_footprint_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_divisor_footprint_gate.py
```

Observed:

```text
tiny_C3xC13:
  pairs_checked = 264/264 exhaustive
  raw_degree_nonzero = 264/264
  raw_equal_row_sums = 264/264
  raw_no_forbidden_fourier = 264/264
  raw_nonseparable = 264/264
  raw_mixed_rank_positive = 264/264
  norm_degree_zero = 264/264
  norm_zero_row_sums = 264/264
  norm_nonseparable = 264/264
  norm_mixed_rank_positive = 264/264

prime_axis_C3xC53:
  representative_pairs_checked = 4
  all corresponding raw and scalar-normalized checks pass

divisor_footprint_rows = 2/2
conclusion=reported_p25_laneB_divisor_footprint_gate
```

## Canonical Profiles

For `C_3 x C_13`, the canonical carry `theta_{3,1}` over the split field
`F_79` has:

```text
raw degree = 70
raw row sums = [76, 76, 76]
raw Fourier support = scalar + 12 pure-C + 24 mixed slots
raw pure-right Fourier slots = 0
scalar component removed = 18
normalized degree = 0
normalized row sums = [0, 0, 0]
normalized Fourier support = 12 pure-C + 24 mixed slots
mixed difference rank = 2
```

For `C_3 x C_53`, the canonical carry `theta_{3,1}` over `F_3181` has:

```text
raw degree = 2859
raw row sums = [953, 953, 953]
raw Fourier support = scalar + 52 pure-C + 104 mixed slots
raw pure-right Fourier slots = 0
scalar component removed = 78
normalized degree = 0
normalized row sums = [0, 0, 0]
normalized Fourier support = 52 pure-C + 104 mixed slots
mixed difference rank = 2
```

## Consequence

The first falsifier for an actual arithmetic producer is now precise:

```text
Can a p25 negative-trace CM/Lang or modular-unit specialization supply the
needed scalar/polar normalization while realizing the normalized mixed
151 x 677 carry footprint?
```

If the object can only produce independent local units on the `151` and `677`
sources, this Lane B path dies.  If it can produce the coupled footprint with
the scalar component accounted for, the remaining work is to lift the finite
packet into the actual p25 producer and then into a verifier payload.

The next finite product-formula checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_punctured_hd_anchor.md
```

It shows that the p24 punctured Hasse-Davenport / single-anchor correction
ports to the p25 `C_3 x C_13` and `C_3 x C_53` rows.  The obstruction is now
specifically the CM-Artin pullback plus single-anchor Kummer descent, not the
finite Jacobi product formula itself.
