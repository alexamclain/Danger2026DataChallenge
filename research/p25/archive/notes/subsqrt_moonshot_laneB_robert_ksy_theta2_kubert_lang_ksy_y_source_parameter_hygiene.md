# P25 Lane B: KSY-y Source-Parameter Hygiene

Updated: 2026-06-13 20:05 PDT

## Purpose

The exact p25 product target now has a theorem-shaped boundary, but several
source families reuse the same letters with different meanings.  This note
adds an executable guardrail so future theorem or literature scouts do not
silently move statements across incompatible parameter regimes.

## Target

The live product remains

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK) / y(-C-jD-kK)
C = (47,28)
D = (22,3), quotient D = (1,3)
K = (57,0)
y(Q) = -g(2Q)/g(Q)^4
```

## Hygiene Rows

```text
safe:
  KSY [2] in y(Q)=-g(2Q)/g(Q)^4
    meaning: multiplication-by-2 inside the normalized-y formula
    not: ordinary Kato-Siegel Dtheta parameter

  raw D=(22,3), quotient D=(1,3)
    meaning: finite p25 source direction in C_75 x C_169
    not: integer parameter satisfying a source theorem hypothesis

conditional:
  Sprang/Kronecker D=2
    live only as an explicit even-D differential/additive clause emitting exact P
    not imported from the ordinary Kato-Siegel Dtheta theorem

  Kubert-Lang C169 screen
    useful as a prime-power C-axis congruence screen
    not enough for the mixed C_3 x C_169 row graph

  Kubert-Lang mixed levels 507/12675
    carries the actual row graph and K trace
    needs an exact mixed-level product theorem or reduction to accepted finite identity

rejected:
  ordinary Kato-Siegel Dtheta with D=2
    killed by the prime-to-6 hypothesis in the ordinary Dtheta statement
```

## Completed Gate

```text
safe_notational_rows      = 2
conditional_source_rows   = 3
rejected_misread_rows     = 1
C169 prime-power screen   = live
mixed 507/12675 levels    = need extra source clause
ordinary Kato Dtheta D=2  = rejected
KSY doubling [2]          = live
raw D step                = finite geometry only
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate.py
```

Marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_rows=1/1
```

## Consequence

The moonshot remains narrowly viable, but the source ask is sharper:

- A KSY hit may use the `[2]` normalized-y formula, but it must prove the exact
  K-traced product `P`.
- A Sprang/Kronecker hit must explicitly supply an even-`D` differential or
  additive identity for exact `P`; ordinary Kato-Siegel `Dtheta` at `D=2` does
  not provide it.
- A Kubert-Lang hit must preserve the mixed `C_3 x C_169` row graph and row
  anchor.  C-axis `169` congruence hygiene is only a screen, and mixed levels
  `507/12675` need a stronger source clause or a reduction to a finite-field
  identity that DANGER3 accepts.
