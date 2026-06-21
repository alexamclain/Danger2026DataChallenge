# P27 Reverse-Doubling Source Screen

Date: 2026-06-21

## Claim

Reverse doubling gives the correct source-cover equation for the next
all-plus `u+2` / x-square gate, but the first finite-field screen shows no
cheap density advantage by itself.

This is a source-equation checkpoint, not a production filter:

```text
confirmed = exact reverse-doubling source equations
not found = obvious p27 density lift or small-field component anomaly
next = Sage/Magma genus, components, and quotient analysis
```

## Source Equation

For a Montgomery curve parameter `A`, if `q=x_next`, then x-coordinate doubling
gives:

```text
x_prev = (q^2 - 1)^2 / (4*q*(q^2 + A*q + 1)).
```

To source the next x-square gate, write:

```text
q = z^2
x_prev = (z^4 - 1)^2 / (4*z^2*(z^4 + A*z^2 + 1)).
```

For a legal rational half, the proposed half point must also lie on the
Montgomery curve:

```text
Y^2 = z^4 + A*z^2 + 1.
```

So the actual d3 all-plus source is the intersection of:

```text
label-2 compactD=-1 source
x5 = (z^4 - 1)^2 / (4*z^2*(z^4 + A*z^2 + 1))
Y^2 = z^4 + A*z^2 + 1
```

where `A` and `x5` are the label-2 candidate functions on the compactD source.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_reverse_doubling_source_probe.py \
  --target 5000 \
  --max-draws 1000000 \
  --small-primes 487,599,607,719,727,751,823,839,863,887,911,967,991 \
  | tee research/p27/archive/probe_outputs/p27_reverse_doubling_source_probe_20260621.txt
```

Replication:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_reverse_doubling_source_probe.py \
  --target 5000 \
  --seed 20260622 \
  --max-draws 1000000 \
  --small-primes 607,719,863,991 \
  | tee research/p27/archive/probe_outputs/p27_reverse_doubling_source_probe_seed20260622_20260621.txt
```

The probe checks:

```text
xDBL_A(x6) = x5
chi(x6) = chi(x6^2 + A*x6 + 1)
z-root and Y-root multiplicities for the source cover
small-prime q == 7 mod 8 enumerations of the same label-2/compactD equations
```

## Symbolic / Magma Handoff Check

The first symbolic handoff artifact exposed one convention issue: the selected
`x5` can come from either sign of the previous halving square root.  The
correct affine handoff therefore includes a branch parameter:

```text
eta^2 = 1
eta = selected first-half square-root sign
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_reverse_source_symbolic_artifact.py \
  --target 200 \
  --max-draws 200000 \
  | tee research/p27/archive/probe_outputs/p27_reverse_source_symbolic_artifact_20260621.txt
```

P27 verification:

```text
B_branch_minus = 200
B_branch_plus = 200
verified_oriented_candidates = 400
verified_source_points = 384
B_mismatch = 0
```

The tiny independent Magma check uses the online calculator only as the t24
workflow allows: a small finite-field probe, not a throughput tool.  The input
is `research/p27/archive/fixtures/p27_reverse_source_q607_magma.m`, and the
saved result is:

```text
RESULT p27_reverse_q607 ok 512 256 0 0 1024 2048
```

This matches the local Python enumeration for `q=607`:

```text
oriented_candidates = 512
d3_plus_candidates = 256
reverse_mismatch = 0
point_mismatch = 0
reverse_z_points = 1024
reverse_zy_points = 2048
```

Conclusion: the reverse-source formulas and the `eta` two-component convention
survive an independent small Magma validation.  This validates the source
equation handoff; it does not change the density conclusion.

## P27 Result

Seed `20260621`, 5,000 compactD pairs:

```text
oriented_candidates = 20000
unique_A_x5 = 5000
d3_plus_candidates = 9864
oriented_d3_plus_rate = 0.493200000
branch_square_rate = 0.493200000
reverse_z_points_per_oriented = 1.972800000
reverse_zy_points_per_oriented = 3.945600000
reverse_mismatch = 0
point_mismatch = 0
```

Seed `20260622`, 5,000 compactD pairs:

```text
oriented_candidates = 20000
unique_A_x5 = 5000
d3_plus_candidates = 10088
oriented_d3_plus_rate = 0.504400000
branch_square_rate = 0.504400000
reverse_z_points_per_oriented = 2.017600000
reverse_zy_points_per_oriented = 4.035200000
reverse_mismatch = 0
point_mismatch = 0
```

The random-half expectation is:

```text
d3_plus_rate ~= 1/2
reverse_z_points_per_oriented ~= 2
reverse_zy_points_per_oriented ~= 4
```

The p27 samples match that expectation.

## Small-Prime Screen

The small-prime enumeration is a component/anomaly screen, not p27 density
evidence.  On `q == 7 mod 8` primes, the reverse identity and rational-point
condition had zero mismatches.  Some small fields are extreme because the
source has few points, but larger examples include exact half splits:

```text
q=607: d3_plus_rate = 0.500000000, reverse_z/oriented = 2.000000000
q=863: d3_plus_rate = 0.500000000, reverse_z/oriented = 2.000000000
q=991: d3_plus_rate = 0.500000000, reverse_z/oriented = 2.000000000
```

Other small fields fluctuate high or low; no stable extra component or density
lift appears from point counting alone.

## Interpretation

Positive:

```text
The reverse-doubling equations are exact and source precisely the smaller
continuation scope defined by the next x-square gate.
```

Negative:

```text
Naively adjoining z and Y behaves like the expected generic quadratic source
cover over p27: it does not remove the 1/2 loss by density alone.
```

This does not kill the source-cover route.  It kills only the easy hope:

```text
set x_next=z^2 and immediately get a cheap p27 sampler.
```

## Concrete Next Tests

1. Sage/Magma genus and components:

```text
Build the curve defined by label-2 compactD=-1 plus
  x5 = (z^4 - 1)^2 / (4*z^2*(z^4 + A*z^2 + 1))
  Y^2 = z^4 + A*z^2 + 1.
Compute components, genus, quotient maps, and whether any component is
elliptic/rational or dominated by the residual E.
```

2. Projection test:

```text
Ask whether the reverse source factors through the order-4 compactD quotient
D/<alpha> or through the residual elliptic curve E: W^2=X^3-X.
```

3. GPU rule:

```text
Do not implement a reverse-doubling sampler until a quotient/source map is
named.  The p27 density screen alone says it is another generic half cover.
```

## Continue / Kill

```text
continue = Sage/Magma component/genus/quotient analysis of the reverse source
continue = derive whether the reverse source factors through D/<alpha> or E
continue = use the equations as the exact expert ask for a source-cover review

kill = expecting reverse doubling alone to beat the random 1/2 loss
kill = GPU sampler from z without a named quotient/source map
kill = using small-prime density fluctuations as promotion evidence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_reverse_doubling_source_probe.py`
- Symbolic handoff: `research/p27/archive/gates/p27_reverse_source_symbolic_artifact.py`
- Online Magma input: `research/p27/archive/fixtures/p27_reverse_source_q607_magma.m`
- Output: `research/p27/archive/probe_outputs/p27_reverse_doubling_source_probe_20260621.txt`
- Replication output: `research/p27/archive/probe_outputs/p27_reverse_doubling_source_probe_seed20260622_20260621.txt`
- Symbolic handoff output: `research/p27/archive/probe_outputs/p27_reverse_source_symbolic_artifact_20260621.txt`
- Online Magma output: `research/p27/archive/probe_outputs/p27_reverse_source_q607_magma_20260621.txt`
- Online Magma raw XML: `research/p27/archive/probe_outputs/p27_reverse_source_q607_magma_20260621.xml`
- Related: [P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md)
- Related: [P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md)
- Related: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Related: [P27 Label-2 Second-Gate Cover](p27_label2_second_gate_cover_20260621.md)

```text
p27_reverse_doubling_source_screen_rows=1/1
```
