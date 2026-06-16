# Lane B Quotient Checkpoint

Date: 2026-06-12

## Purpose

Promote the Lane B fixed-frequency/Jacobi idea from a note into a repeatable
p25 arithmetic gate.  This checkpoint validates only the formal Frobenius
quotient skeletons on the negative trace; it does not construct a selected
packet and is not a certificate producer.

## Files Added

- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_quotient_smoke.py`

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_quotient_smoke.py
```

## Output

```text
p25 Lane B quotient smoke
p=10000000000000000000000013
tiny_C3xC13: n=2453448 rho=p^2 ord=12675=3 * 5^2 * 13^2 quotient=C_3xC_13 size=39 equations=21 dimension=18 cover=yes
prime_axis_C3xC53: n=11536098 rho=p^16 ord=3975=3 * 5^2 * 53 quotient=C_3xC_53 size=159 equations=81 dimension=78 cover=yes
verdict=PASS
```

## Interpretation

The p25 negative-trace quotient arithmetic is real:

- Tiny falsifier target: `C_3 x C_13`, quotient size `39`, `21` value-side
  equations, dimension `18`.
- Cleaner prime-axis target: `C_3 x C_53`, quotient size `159`, `81`
  value-side equations, dimension `78`.

Both quotient products cover the intended Frobenius quotient after modding out
the trace subgroup.  This justifies one more narrow Lane B step.

## Next Gate

This gate has been promoted in:

```text
research/p25/subsqrt_moonshot_laneB_packet_contract.md
research/p25/p25_laneB_packet_contract.py
research/p25/p25_selected_defect_value_gate.py
```

The next missing object is a raw selected weighted packet `Y[e]` on the
negative trace.  Its first post-`B` packet is:

```text
g(r,c)=sum_{j=0}^324 Y[13*r + 3*c + 39*j mod 12675]
f(r,c)=g(r,c)-g(r,0)
```

Reject Lane B immediately if the first materialized `f` fails any value-side
identity:

```text
f(r,0) = 0
row sums are independent of r
f(r,c) + f(-r,-c) is constant for c != 0
```

If `C_3 x C_13` passes but looks too small to authenticate the mechanism,
repeat the same gate on `C_3 x C_53`.

## Discard Condition

Kill the Lane B moonshot route if no selected packet builder can be produced
for the negative trace, or if the first materialized packet fails the three
value-side identities.  The production `x16halvenonsplit` fleet should continue
unchanged either way.
