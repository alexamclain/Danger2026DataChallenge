# P25 KSY-y Cross-Level Bridge Source-Route Packet

Updated: 2026-06-14 13:02 PDT

## Purpose

The conductor-39 route can produce an odd-level value/divisor theorem.  DANGER3
still needs the active `X_1(16)` Montgomery surface and a halving chain.  This
packet names the theorem shapes that actually bridge those worlds.

## Projection Arithmetic

```text
16 * 507 = 8112
gcd(16,507) = 1

507^-1 mod 16 = 3
16^-1 mod 507 = 412

P16  = [1521]R = [3*507]R
Q507 = [6592]R = [412*16]R
1521 + 6592 = 1 mod 8112
```

So a useful bridge can be stated either as:

```text
same-curve exact P16 and Q507
```

or:

```text
exact order-8112 point R with normalized projections to P16 and Q507
```

## Route Rows

### Same-Curve P16 And Q507

Accepted source families:

```text
X_1(16) x_j X_1(507) fiber-product theorem
modular correspondence preserving the same j-invariant
explicit elliptic curve carrying both exact torsion components
```

First falsifier:

```text
independent level-16 and level-507 data, or no same-j proof
```

Expected local decision:

```text
cross_level_target_identified_specialization_missing
```

### Order-8112 Generator R

Accepted source families:

```text
single X_1(8112) point theorem
same-curve torsion gluing theorem with R=P16+Q507
explicit normalized projections [1521]R=P16 and [6592]R=Q507
```

First falsifier:

```text
R does not have exact order 8112 or does not project to the recorded odd target
```

Expected local decision:

```text
cross_level_target_identified_specialization_missing
```

### X1(16) Y/Model Surface

Accepted source families:

```text
X_1(8112) theorem specialized to the production X_1(16) chart
explicit y and model root x satisfying the recorded quadratic
direct A,xP16 payload derived from the same odd target
```

First falsifier:

```text
abstract P16 torsion without y-chart or direct A,xP16 data
```

Expected local decision:

```text
cross_level_surface_policy_or_framing_missing
```

### Active X1(16) Surface With Policy

Accepted source families:

```text
finite-field/non-CM accepted bridge plus production X_1(16) surface
direct A,xP16 output with same-j odd-level provenance
optional d-gate surface only if it also preserves the active A,xP16 payload
```

First falsifier:

```text
surface lacks challenge framing or only emits optional first-half data
```

Expected local decision:

```text
x16_surface_reached_halving_or_vpp_missing
```

### Checkable Halving Chain

Accepted source families:

```text
explicit x-coordinate halving certificate
sqrt-witness chain for active branch provenance
direct x0 plus A verified by official vpp.py
```

First falsifier:

```text
branch word without actual x-values or sqrt witnesses
```

Expected local decision:

```text
checkable_x_chain_vpp_missing
```

### Direct Verified Triple

Accepted source families:

```text
official vpp.py verified triple
Lean certificate generated from the verified triple
archived command/log/environment bundle
```

First falsifier:

```text
official vpp.py rejects the triple
```

Expected local decision:

```text
closing_vpp_verified_submission
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_cross_level_bridge_source_route_packet_gate.py
```

Marker:

```text
ksy_y_cross_level_bridge_source_route_packet_rows=1/1
```
