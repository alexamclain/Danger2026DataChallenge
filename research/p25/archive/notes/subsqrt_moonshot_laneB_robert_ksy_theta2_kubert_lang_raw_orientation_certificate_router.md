# P25 Lane B: Robert KSY Kubert-Lang Raw Orientation Certificate Router

Updated: 2026-06-13 18:13 PDT

## Purpose

The raw reflection-orientation contract says a theorem source may emit one of
four oriented anti-invariant product branches.  This router verifies that each
accepted branch feeds the existing theta2 candidate harness and finite
certificate path with the correct sign.

## Routes

```text
C=(47,28),  y(A)/y(-A)  -> theta2 inverse -> resolvent recovers -bridge
C=(47,28),  y(-A)/y(A)  -> theta2         -> resolvent recovers  bridge
-C=(28,141), y(A)/y(-A) -> theta2         -> resolvent recovers  bridge
-C=(28,141), y(-A)/y(A) -> theta2 inverse -> resolvent recovers -bridge
```

For all four routes:

```text
theta2 candidate harness      = pass
normalized bridge contract    = pass
support-resolvent term budget = 46800
support-resolvent union       = 11700
```

Controls:

```text
wrong center     -> emits neither theta2 nor theta2 inverse
wrong D          -> emits neither theta2 nor theta2 inverse
nonprimitive K   -> emits neither theta2 nor theta2 inverse
```

## Candidate Intake

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate.py \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 \
  --k-multiplier 1
```

Reverse orientation:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate.py \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 \
  --k-multiplier 1 --reverse
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_rows=1/1
```

## Interpretation

This is the current executable handoff from a theorem/literature hit to the
finite certificate chain:

```text
raw oriented product -> theta2/theta2-inverse classification
                     -> support-period finite resolvent
                     -> normalized bridge contract
```

The missing moonshot step remains the arithmetic legality of the product.  The
finite verifier path from such a product is now fully routed.
