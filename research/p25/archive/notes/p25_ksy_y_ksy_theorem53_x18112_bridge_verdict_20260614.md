# P25 KSY-y KSY Theorem 5.3 X1(8112) Bridge Verdict

Updated: 2026-06-14 13:07 PDT

## Purpose

The exact-product scout already killed Koo-Shin-Yoon Theorem 5.3 as a direct
75-atom p25 product theorem.  The newer question is narrower:

```text
Can Theorem 5.3 at N=8112 provide the same-j bridge to the active X_1(16)
DANGER3 extractor?
```

Verdict:

```text
positive as vocabulary / abstract torsion shape
not a p25 cross-level bridge theorem as stated
```

## Source Evidence

Equation `(3.4)` supplies normalized-y formula language:

```text
y(Q) = -g(2Q)/g(Q)^4
```

Theorem `5.3` supplies ray-class generation from torsion data.  For `N>=8`,
and especially when `4 | N`, the theorem gives a torsion-point generator shape
on one elliptic curve.

At `N=8112`, this is suggestive because:

```text
8112 = 16 * 507
```

but it still does not identify the recorded p25 odd target, the production
`X_1(16)` chart, a halving chain, or a verified DANGER3 triple.

## Local Verdict Rows

Actual KSY rows:

```text
Equation (3.4):
  decision = conditional_missing_exact_product
  missing  = exact product P with C=(47,28), D=(22,3), K=(57,0)

Theorem 5.3 family-level generation:
  decision = conditional_missing_exact_p25_specialization
  missing  = p25-specialized target, not a family-level possibility

Theorem 5.3 generation-only source claim:
  decision = reject_not_closure_theorem
  missing  = not an exact finite-field identity for P
```

Optimistic bridge calibration rows:

```text
N=8112 abstract R without odd target:
  decision = reject_generic_x16_not_ksy_bridge
  missing  = odd-level KSY/Yang/H90 value or divisor payload

N=8112 bridge after exact odd target:
  decision = cross_level_target_identified_specialization_missing
  missing  = specialized relation yielding X_1(16) y, A, xP16, or x0

N=8112 bridge plus X_1(16) surface:
  decision = cross_level_surface_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

DANGER3-framed surface:
  decision = x16_surface_reached_halving_or_vpp_missing
  missing  = valid halving chain from xP16 to concrete x0
```

## Consequence

Theorem `5.3` should not be retried as a direct p25 closer.

It remains useful only if a new clause or companion theorem supplies one of:

```text
exact p25 odd target projected from the N=8112 point
production X_1(16) y/model-root/A/xP16 specialization
checkable halving chain or direct x0
official vpp.py verified triple
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_ksy_theorem53_x18112_bridge_verdict_gate.py
```

Marker:

```text
ksy_y_ksy_theorem53_x18112_bridge_verdict_rows=1/1
```
