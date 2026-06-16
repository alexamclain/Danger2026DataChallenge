# P25 Lane B: Robert/Kato-Siegel Primitive C169 Scout

Updated: 2026-06-13 13:45 PDT

## Verdict

Continue the Robert/Siegel lane only through a normalized odd `y/wp'` or
Kato-Siegel `dlog` translated finite-difference route at level `169`.  Kill
pure `x`, pure character tags, literal subgroup divisors, and split
`C_13 x C_13` replacements.

## Sources And Files

Local files inspected by the scout:

- `subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_corner_sign_candidate.md`
- `subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source.md`
- `subsqrt_moonshot_laneB_robert_sparse_source_candidate_harness.md`
- section C of `p25_moonshot_targeted_lit_search_results_20260613.md`
- nearby Robert edge/orientation, `C_169` nonsplit, and odd-quotient notes

Primary/near-primary sources:

- Koo-Shin-Yoon, normalized torsion coordinates:
  https://arxiv.org/pdf/1007.2307
- Sprang, Kato-Siegel `Dtheta` and logarithmic derivatives:
  https://arxiv.org/pdf/1802.04996
- Schertz, Klein-form elliptic-unit quotients:
  https://www.numdam.org/item/JTNB_1997__9_2_383_0.pdf
- Kubert-Lang Siegel-function generator backbone:
  https://eudml.org/doc/162977

## Candidate Shape

The best primitive `C_169` source candidate is Koo-Shin-Yoon's normalized odd
coordinate

```text
y(r1,r2) = -g(2r1,2r2) / g(r1,r2)^4
```

or the Kato-Siegel logarithmic-derivative avatar.  This is attractive because
it is a genuine ray-class/torsion generator at level `13^2`, not a split
`C_13 x C_13` adapter.

Finite shadow target:

```text
base * K_trace * D_segment * (1 - T)

base = (25,25)
K    = (57,0), length 25
D    = (22,3), length 3
T    = (38,113), quotient edge (2,113)
```

Analytic route:

```text
Phi(P) = y(P+T)/y(P-T)
```

or

```text
dlog Dtheta(P+T) - dlog Dtheta(P-T)
```

then apply the primitive `C_169` torsion/source coordinate, the 25-point `K`
trace, and the three-term non-subgroup `D` finite difference before the
Hilbert-90 bridge symmetrization.

## First Probe

Canonical finite probe:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate_harness.py \
  --point 0 0 0 -1 \
  --point 1 3 0 -1 \
  --point 2 1 11 -1
```

If a theorem emits signs first:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness.py \
  --eps 1 --branch -1
```

If a theorem emits sparse triples directly:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py \
  --sparse-source PATH
```

## Recommendation

Continue only normalized `y/wp'` or Kato-Siegel `dlog` translated finite
differences that can emit the two signs, the row-labeled primitive `C_169`
triangle, or the exact sparse-source triples.  Kill candidates that collapse to
literal finite-subgroup divisors, x-only even functions, plain `C_169`
characters, `12N` symmetrized pure Siegel/Klein quotients, or split
`C_13 x C_13` source models.
