# P27 Quartic Hit Geometry Promotion Tool

Date: 2026-06-22

## Claim

The full quartic GPU suite now has an immediate promotion-side analyzer.

If the GPU reports a B-line or K-line quartic hit, use this tool to verify the
hit against the frozen target packet and classify the double cover
`z^2=f(X)` before spending time on downstream source claims.

## Artifact

Tool:

```text
research/p27/archive/gates/p27_quartic_hit_geometry.py
```

Smoke outputs:

```text
research/p27/archive/probe_outputs/p27_quartic_hit_geometry_smoke_k1471_20260622.txt
research/p27/archive/probe_outputs/p27_quartic_hit_geometry_smoke_b1607_20260622.txt
```

## Commands

For a K-line hit:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_quartic_hit_geometry.py \
  --coordinate K \
  --field <q> \
  --family <family> \
  --coeffs <a,b,c,d> \
  --polarity <1-or--1>
```

For a B-line hit:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_quartic_hit_geometry.py \
  --coordinate B \
  --field <q> \
  --family <family> \
  --coeffs <a,b,c,d> \
  --polarity <1-or--1>
```

## Output

The analyzer reports:

```text
verifier pass/fail against the frozen packet
row matches/mismatches/zeros
quartic discriminant mod q
repeated-factor degree
squarefree degree
normalization genus
factor-degree profile
finite-field point count
promotion status
```

The promotion status is intentionally conservative:

```text
not_a_verified_hit
low_genus_source_candidate
degenerate_or_rational_candidate
higher_genus_or_singular_candidate
```

## Smoke Tests

The smoke tests use the non-hit quartic `X^4+1`, so verifier failure is
expected.  They validate packet lookup, verifier wiring, geometry, and point
counting for both coordinates.

```text
K q1471 d3_on_K, coeffs=0,0,0,1:
  verifier_pass = 0
  squarefree_degree = 4
  normalization_genus = 1
  factor_degrees = [(2, 1), (2, 1)]

B q1607 d3_on_legalB, coeffs=0,0,0,1:
  verifier_pass = 0
  squarefree_degree = 4
  normalization_genus = 1
  factor_degrees = [(2, 1), (2, 1)]
```

## Interpretation

Promote a GPU quartic only after:

```text
1. local verifier passes with zero target-row zeros
2. normalization genus is <= 1, or a degenerate genus-0 case has a clear source interpretation
3. the same class is compared against the B/K bridge or a guard-field companion
```

If a verified hit is genus `1`, the next artifact should construct the elliptic
double cover `z^2=f(B)` or `z^2=f(K)`, compute its map/sourceability, and test
whether the class recurs or couples to the gate4/d4 target.

```text
p27_quartic_hit_geometry_promotion_tool_rows=1/1
```
