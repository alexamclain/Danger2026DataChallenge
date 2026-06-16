# Decomposed Certificate Handoff

Date: 2026-06-05

This note fixes the naming around the two dual decomposed CM handoffs for the
third p24 trace.

## Shared Data

```text
p = 10^24 + 7
t = -1178414874616
h = 205880396014
m = 66254 = 2*157*211
n = 3107441
sqrt(p) = 1000000000000
```

The post-root tail is now explicit:

```text
j root -> Montgomery A -> x0
```

via:

```text
p24/post_j_root_to_triple_boundary.md
p24/post_cm_root_projection_boundary.md
```

So the decomposed handoff only needs to produce an embedded conductor-2
`j`-root on the strict branch.

## H-Period Handoff

Let:

```text
H = <g^m>,      |H| = n = 3107441.
```

The H-period quotient values are:

```text
y_r = sum_{k=0}^{n-1} j_{r + m*k},      0 <= r < m.
```

Finite handoff:

```text
V_H(Y) = prod_{r=0}^{m-1} (Y - y_r),        degree 66254
R_r(J) = prod_{k=0}^{n-1} (J - j_{r+m*k}), degree 3107441.
```

This is the usual quotient/recovery language:

```text
quotient degree = 66254
recovery degree = 3107441
```

It matches the oriented composite class target in:

```text
p24/all_trace_period_frontier.md
p24/embedded_selector_theorem_attempt.md
```

The missing producer is the embedded H-period phase, equivalently the
non-genus relative character traces for the `157` and `211` quotient layers.

## Complement-Trace Handoff

Let:

```text
K = <g^n>,      |K| = m = 66254.
```

The complement trace values are:

```text
Y_k = sum_{r=0}^{m-1} j_{n*r + m*k},      0 <= k < n.
```

Finite handoff:

```text
F_K(Y) = prod_{k=0}^{n-1} (Y - Y_k),        degree 3107441
U_k(J) = prod_{r=0}^{m-1} (J - j_{n*r+m*k}), degree 66254.
```

This is the dual finite algebra in:

```text
p24/complement_trace_recovery_relation.md
p24/complement_trace_recovery_toy.py
```

It has the same largest degree but a different producer problem:

```text
construct the degree-3107441 complement trace polynomial
and the degree-66254 recovery map without a dense h-sized relation.
```

Small CM data says the naive bivariate relation is dense with about `h`
coefficients, so this variant still needs a tower/class-field formula.

## What Counts As Progress

Either handoff would beat sqrt scaling if produced without class-set
enumeration:

```text
max(66254, 3107441) / sqrt(p) = 3.107441e-6.
```

A valid p24 certificate-producing theorem may therefore supply either:

```text
1. H-period quotient plus degree-n recovery polynomial; or
2. complement-trace quotient plus degree-m recovery polynomial;
```

provided the supplied quotient root is embedded/paired with the recovery
factor in `j`.

The phase-lifted version of the H-period handoff is now explicit in:

```text
p24/phase_lifted_tower_certificate_spec.md
p24/phase_lifted_tower_certificate_toy.py
```

It replaces the single degree-66254 quotient polynomial by the tower:

```text
degree 2 top polynomial,
degree 157 relative relation,
degree 211 relative relation,
one selected degree-3107441 recovery polynomial.
```

The p24 coefficient count is:

```text
2 + 2*157 + 314*211 + 3107441 = 3174011,
```

still only `3.174011e-6 * sqrt(p)`.  The key restriction is that the recovery
object must be the selected degree-`n` polynomial, not the dense full
quotient/recovery relation of size `h`.

If the producer theorem directly supplies one phase-selected tower chain, the
full parent-relative relations are not logically required.  The smaller
selected-chain surface is:

```text
2 + 157 + 211 + 3107441 = 3107811,
```

or `3.107811e-6 * sqrt(p)`.  This is the form captured by the finite Lean
gate `p24/lean/PhaseLiftedTowerGate.lean`.

## First-Trace Order-19 Comparison

The first strict trace gives a much simpler theorem experiment, though a
larger finite payload:

```text
t = 1020608380936
h = 278733727154 = 2 * 19 * 7335098083
ell = 19
index = 19
recovery degree = 14670196166
payload coefficients = 14670196185
payload/sqrt(p) = 0.014670196185
```

This route is recorded in:

```text
p24/first_trace_order19_certificate_spec.md
p24/lean/QuotientRecoveryCertificateGate.lean
```

It is not as balanced as the third-trace decomposed handoff, but it strips the
missing arithmetic input down to one non-genus quotient phase and one selected
recovery fiber.  That makes it the cleanest small-data theorem laboratory for
the embedded quotient/recovery producer.

What is not enough:

```text
abstract quotient field roots,
unpaired tower equations,
dense h-sized interpolation tables,
genus/ray labels for only the top layer.
```

The remaining theorem is still the same:

```text
produce the embedded non-genus phase for the odd 157 and 211 class layers,
or an equivalent finite-field p-unit/directness identity that certifies one
of the two handoffs.
```
