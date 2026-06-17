# P25 v2 H90 Support Lower Bound

Updated: 2026-06-16

## Purpose

Promote the exact support lower bound behind the conductor-39 Hilbert-90
selector.  The minimal-preimage classifier enumerates the support-12 rows; this
page records the orbitwise reason no smaller H90 selector can exist for the
current boundary word `W`.

This is still not the missing arithmetic value/divisor theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`
- `evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_h90_support_lower_bound_gate.py
```

The gate returned `p25_v2_h90_support_lower_bound_rows=1/1`.

## Orbit Calculation

The boundary word `W` has four Frobenius orbits, each of length six:

```text
(1, 23, 22, 38, 16, 17)
(2, 7, 5, 37, 32, 34)
(4, 14, 10, 35, 25, 29)
(8, 28, 20, 31, 11, 19)
```

On every orbit, the local boundary pattern is:

```text
(-6, 6, -6, 6, -6, 6)
```

Writing the orbit equation as `x_i - x_{i-1} = y_i`, with indices cyclic, the
solutions are partial sums plus one constant.  With `x_0 = 0`, the partial sums
are:

```text
(0, 6, 0, 6, 0, 6)
```

The best constant can kill only one of the two displayed values, and each value
appears three times.  Therefore every local solution has support at least
three.  The constants `0` and `-6` attain that bound, giving exactly two local
support-three primitives on each orbit.

## Consequences

The four orbits are independent, so:

```text
local lower bound per orbit = 3
global support lower bound = 4 * 3 = 12
global support-12 minimizers = 2^4 = 16
```

The existing classifier then splits those sixteen support-12 minimizers as:

```text
mixed_legal_minimizers = 4
boundary_controls = 12
```

## Routing Rule

Future source answers cannot improve the current target by finding a smaller
H90 selector for this `W`.  A source-stage closer must land on one of the four
legal support-12 mixed minimizers, then add the missing arithmetic
divisor/additive theorem or period-156 value theorem.

Claims with support below twelve are impossible for the current `W`; claims
with support twelve still need the mixed-axis legality screen and finite
theorem content.

## Verdict

```text
orbit_count = 4
local_support_lower_bound = 3
global_support_lower_bound = 12
support_12_minimizers = 16
legal_mixed_minimizers = 4
current_source_theorems = 0
submission_ready = 0
next = arithmetic value/divisor theorem for one legal support-12 minimizer
```
