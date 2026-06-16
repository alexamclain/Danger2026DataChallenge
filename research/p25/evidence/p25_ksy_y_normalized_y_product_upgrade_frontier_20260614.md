# P25 KSY-y Normalized-y Product-Upgrade Frontier

Updated: 2026-06-14 08:28 PDT

## Purpose

The active KL/KSY lane now needs an exact product theorem, not another broad
KSY source pass.  This checkpoint records the exact boundary in
Koo-Shin-Yoon arXiv:1007.2307 between useful normalized-y formula language and
the p25 product payload.

## Source Rows

```text
KSY Equation (3.4)
window = /tmp/p25_lit_scout/1007.2307/source.tex:420-466
output = atom formula y(Q)=-g(2Q)/g(Q)^4
verdict = conditional atom formula, not a product theorem
missing = product/distribution theorem over the exact 75 p25 atoms

KSY Theorem 5.3
window = /tmp/p25_lit_scout/1007.2307/source.tex:1000-1080
output = ray-class generation from one torsion point coordinate pair
verdict = reject as direct p25 closer
missing = exact divisor/additive identity for P

KSY Theorem 6.2
window = /tmp/p25_lit_scout/1007.2307/source.tex:1160-1235
output = single Siegel-Ramachandra ratio generates a ray class field
verdict = reject as direct p25 closer
missing = mixed C3 x C169 K-traced row graph and orientation

KSY Corollary 6.4
window = /tmp/p25_lit_scout/1007.2307/source.tex:1235-1280
output = single y(0,1/N)^4 generator under odd-N Schertz hypotheses
verdict = conditional single-y value, not a product theorem
missing = exact P and full 75-atom distribution
```

## P25 Upgrade Contract

The live KSY upgrade must emit:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
75 normalized-y atoms
300-term theta2/theta2-inverse footprint
support period 156 if the theorem is value-level
orientation and challenge-legal finite-field framing
```

Here `75 normalized-y atoms` means the fixed factors
`Q=C+jD+kK` with `j=-1,0,1` and `k=0..24` inside the target product.  It is
not a 75-candidate search space.  The search/theorem problem is to find an
arithmetic identity that selects this whole 75-factor product with the right
orientation and framing.

The inspected KSY clauses do not contain that theorem.  KSY remains live only
as atom formula vocabulary or as a future exact product/distribution hit.

## Gate

This gate is intentionally lightweight: it scans the local TeX source and does
not re-run the heavy theta2/value-root harness.

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_normalized_y_product_upgrade_frontier_gate.py
```

Marker:

```text
ksy_y_normalized_y_product_upgrade_frontier_rows=1/1
```
