# Subsqrt Moonshot Lane B Packet Contract

Date: 2026-06-12

## Result

The p25 fixed-frequency/Jacobi lane now has a verified finite target for the
negative trace.  This is not a certificate producer, but it converts the next
moonshot step into a precise packet-construction problem.

Verified scripts:

- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_quotient_smoke.py`
- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_packet_contract.py`
- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_selected_defect_value_gate.py`
- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_producer_side_gates.py`

Commands:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_quotient_smoke.py
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_packet_contract.py
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_selected_defect_value_gate.py
```

All listed scripts return `PASS` / successful exit.

The producer-side continuation is recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_producer_side.md
```

## Exact Packet Contract

The negative-trace skeleton supplies a cyclic raw coordinate `Y[e]` indexed by
powers of `rho`.  The post-`B` trace packet is:

```text
g(r,c) = sum_{j=0}^{B-1} Y[c_axis*r + right*c + right*c_axis*j mod raw_order]
f(r,c) = g(r,c) - g(r,0)
```

The first falsifier is:

```text
tiny_C3xC13:
  n = 2453448
  rho = p^2
  raw_order = 12675 = 3 * 5^2 * 13^2
  right = 3
  c_axis = 13
  B = 325
  quotient_size = 39
  value_equations = 21
  admissible_dimension = 18
  axis decomposition: rho = (rho^13)^1 * (rho^3)^9 mod B
  g(r,c)=sum_{j=0}^324 Y[13*r + 3*c + 39*j mod 12675]
```

Cleaner follow-up:

```text
prime_axis_C3xC53:
  n = 11536098
  rho = p^16
  raw_order = 3975 = 3 * 5^2 * 53
  right = 3
  c_axis = 53
  B = 25
  quotient_size = 159
  value_equations = 81
  admissible_dimension = 78
  axis decomposition: rho = (rho^53)^2 * (rho^3)^18 mod B
  g(r,c)=sum_{j=0}^24 Y[53*r + 3*c + 159*j mod 3975]
```

Larger square-axis sanity row:

```text
square_axis_C3xC169:
  n = 2453448
  rho = p^2
  raw_order = 12675 = 3 * 5^2 * 13^2
  right = 3
  c_axis = 169
  B = 25
  quotient_size = 507
  value_equations = 255
  admissible_dimension = 252
  axis decomposition: rho = (rho^169)^1 * (rho^3)^113 mod B
  g(r,c)=sum_{j=0}^24 Y[169*r + 3*c + 507*j mod 12675]
```

Each contract partitions the raw cyclic coordinate into disjoint `B`-trace
blocks.

## Selected-Defect Gate

For `right=3`, the p24 selected-defect producer theorem specializes cleanly to
the p25 candidate axes:

```text
c=13:  value_condition_rank=21,  dimension=18
c=53:  value_condition_rank=81,  dimension=78
c=169: value_condition_rank=255, dimension=252
```

For all three rows, random equivalence and controls pass:

```text
selected_defect_producer_equivalence=3/3
forced_raw_producer_hits=3/3
selected_defect_only_controls=3/3
inversion_only_controls=3/3
affine_only_controls=3/3
```

Thus the actual p25 producer should target raw packet identities:

```text
g(r,0) + g(-r,0) = A0
g(r,c) + g(-r,-c) = A1, for c != 0
sum_c g(r,c) - c_axis*g(r,0) is independent of r
```

Equivalently, the selected defect `f(r,c)=g(r,c)-g(r,0)` must satisfy:

```text
f(r,0) = 0
sum_c f(r,c) is independent of r
f(r,c) + f(-r,-c) is constant for c != 0
```

## What Is Still Missing

The missing object is not another quotient count.  It is a p25-specific,
non-enumerative construction of the raw selected weighted packet `Y[e]` on the
negative trace, compatible with the `rho` cycle above.

Full class-set enumeration is not the intended path: the relevant p25 order
class number is about `10^12`, while this checkpoint only needs a selected
packet on a quotient of size `39` for the first falsifier.

## Continue / Kill Rule

Continue Lane B only if the next step produces one of:

- a concrete p25 formula for `Y[e]` on the `tiny_C3xC13` raw cycle;
- a proof that a CM/Lang/Jacobi ratio supplies the three raw identities above;
- a small analogue that uses this exact contract and explains how to lift the
  selected weighted packet without class-set enumeration.

Kill Lane B if the first actual `Y[e]` packet is materialized and its selected
defect fails the `C3xC13` value identities.

The production `x16halvenonsplit` fleet should continue unchanged.
