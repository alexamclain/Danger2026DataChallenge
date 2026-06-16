# P25 Lane B: Robert KSY/Hilbert-90 Minimal Producer Spine

Updated: 2026-06-13 15:31 PDT

## Purpose

The Hilbert-90 lane, KSY/theta2 lane, and quotient-factor harness now describe
the same finite bridge payload in several increasingly compact interfaces. This
gate records the verified equivalence chain so future theorem or literature
hits can target one unambiguous object instead of drifting between coordinate
systems.

## Verified Spine

```text
Hilbert-90 signs
  -> source quotient packet
  -> quotient factor classes
  -> source factor tuple
  -> compact KSY theta2
  -> support-period/telescoping bridge recovery
```

Equivalent finite interfaces:

```text
Hilbert-90 signs: eps, branch in four active pairs
source quotient packet: 6 signed cells on C3 x C169
quotient factor classes: base=(1,25), D=(1,3), T=(2,113), primitive K
source factor tuple: base*K_trace*D_segment*(1-T)
compact KSY theta2: center_base/half_shift plus orientation
telescoping certificate: theta2=(4-[2])B and [2]^156 B=B
```

## Budgets

```text
source packet support        = 6
quotient factor input cells  = 3
factor support budget        = 31
telescoping compact budget   = 975
support resolvent term budget = 46800
```

The `46800`-term support-period resolvent and the `975`-cell telescoping check
remain verifier/certificate artifacts. The factor-level period proof explains
the active period `156` through the `K_trace` absorption law.

## Falsifiers

The spine gate rejects the main coordinate and factor mistakes:

```text
q-cycle coordinate packet accepted as source packet = false
nonprimitive K multiplier accepted                  = false
wrong quotient D class accepted                     = false
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate.py
```

Expected marker:

```text
robert_ksy_theta2_minimal_producer_spine_rows=1/1
```

## Interpretation

This is a spine ledger, not a new arithmetic producer. It compresses the
moonshot target to one missing object:

```text
challenge-legal arithmetic producer for the quotient packet /
Hilbert-90 signs / KSY theta2 object
```

That producer may arrive as Hilbert-90 signs, a six-cell source quotient
packet, quotient factor classes, source factor data, or compact KSY theta2
data. The current harnesses prove those interfaces are equivalent finite
targets and reject the known nearby false conventions.
