# P25 KSY-y Priority-1 Exact Divisor Lane

Updated: 2026-06-13 21:25 PDT

## Purpose

The post-scout reduction says the first moonshot lane is exact
Sprang/KSY theta2-or-`P` divisor/additive data.  This note states the current
conversion checkpoint: what would turn the existing finite payload into a real
theorem hit, and what should be killed immediately.

Target:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
y(Q) = -g(2Q)/g(Q)^4
```

Finite landing pad already verified:

```text
75 K-traced atoms
300-term theta2/theta2^-1 normalized-y footprint
31-cell compact factor budget
975-cell telescoping witness
support period = 156
```

## Conversion Clauses

The lane now has exactly two first-priority theorem-hit shapes:

```text
1. Sprang/Kronecker D=2 exact additive identity:
   an even-D Kronecker/differential theorem specializes to exact P or exact
   theta2/theta2^-1 divisor data with the mixed graph, equal weights, and
   orientation.

2. KSY normalized-y product/distribution identity:
   a KSY/Siegel-function theorem proves the full K-traced anti-invariant
   product, not merely the formula y(Q)=-g(2Q)/g(Q)^4 or ray-class generation.
```

Either clause routes through exact-product intake as
`closing_exact_product_identity`.

Sprang source split:

```text
arXiv:1801.05677 = Eisenstein-Kronecker / Kronecker-section source handle
arXiv:1802.04996 = algebraic de Rham polylogarithm / differential-form handle
marker = ksy_y_priority1_sprang_source_split_rows=1/1
```

Both Sprang handles remain conditional until specialized to the exact p25
product or theta2/theta2-inverse divisor data.  Ordinary Kato-Siegel `theta_D`
is still killed as a direct `D=2` proof.

KSY source split:

```text
Equation (3.4) = normalized-y/Siegel formula language
Theorem 5.3 = ray-class generation
Theorem 6.2 / Corollary 6.4 = single-y-value invariant output
marker = ksy_y_priority1_ksy_source_split_rows=1/1
```

Only an exact K-traced normalized-y product/distribution theorem for the full
p25 `P` closes the priority-1 KSY lane.

The exact snippet query packet is now:

```text
research/p25/p25_ksy_y_priority1_theorem_query_packet_20260613.md
marker = ksy_y_priority1_theorem_query_packet_rows=1/1
```

## Non-Closers

Keep but do not count as closure:

```text
compact KSY center/half/orientation payload
KSY Equation (3.4) formula language
Sprang distribution or dlog language without exact P specialization
```

Kill as direct closers:

```text
KSY single-y or ray-class generation
ordinary Kato-Siegel theta_D imported directly at D=2
nonuniform or partial atom weights
missing or collapsed K trace
truncated D, wrong D, or wrong T
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_exact_divisor_lane_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_theorem_query_packet_gate.py
```

## Completed Gate

```text
direct_source_closing_rows = 0
theorem_hit_hypotheticals  = 2
conditional_rows           = 2
rejected_rows              = 5
finite_only_rows           = 1
```

Marker:

```text
ksy_y_priority1_exact_divisor_lane_rows=1/1
```
