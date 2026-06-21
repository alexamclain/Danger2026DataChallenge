# P27 Transfer Plan: P26 Trace/Norm Structure

Date: 2026-06-21

## Purpose

Use the p26 certificate search and post-hit structure as amortized prior art for
p27 without assuming that the same squareclass signs survive unchanged.

## P26 Input

The latest p26 work isolated a trace/norm descent on the F-square slice:

```text
F = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
E_K: w^2 = -(y^2 - 2)(y^2 - 4y + 2)
t = y - 1
E_K: w^2 = -t^4 + 6t^2 - 1
g(t,w) = (-1/t, w/t^2)
a = t - 1/t
b = w(t^2 + 1)/t^2
b^2 = 16 - a^4
```

For p26, the normalized sign `D_norm = D * chi(y)` descended under the
involution, and a line-normalized variant removed the b-flip cocycle:

```text
D(gP) / D(P) = chi((y - 1)y(y - 2)) = chi(g(y) / y)
T = D_norm
T(a, -b) / T(a, b) = chi(a)
T_line = T if chi(a) = +1 else T * chi(b)
```

The p26 domain also descended to the same line through:

```text
F = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
```

Tiny degree-1 and degree-2 line families were flat on p26; that falsifies the
smallest visible family, not the existence of a higher-structure source.

## P27 Transfer Caveat

p27 changes the squareclass of `2`:

```text
p26 mod 8 = 3 -> chi(2) = -1
p27 mod 8 = 7 -> chi(2) = +1
```

Therefore the p26 formulas should be ported as exactness tests, not promoted as
accepted filters. Recheck every identity involving constants `2`, `4`, `16`,
the reciprocal involution, branch orientation, and any `sqrt(2)`-adjacent
normalization.

## Concrete Tests

### Test A: Orbit Identity Smoke

Port the p26 quotient automorphism gate to p27 and measure:

```text
D(gP) / D(P)
chi((y - 1)y(y - 2))
chi(g(y) / y)
```

Status: passed.  See
[P27 Trace/Norm Transfer Gate](p27_trace_norm_transfer_gate_20260621.md).
On `32,780` compare rows, the neg-inv ratio matched both
`chi((y - 1)y(y - 2))` and `chi(g(y)/y)` exactly.

Kill condition: the identity fails after correcting only obvious p27 branch
normalizations.

### Test B: T-Line Descent Smoke

After Test A, test whether the same `T_line` normalization is consistent on
the quotient `a = t - 1/t`.

Status: passed.  The p26 `T_line` normalization had `16,390` line rows and
`0` inconsistencies on the medium p27 sample.

Kill condition: line inconsistency remains after sign/branch repairs.

### Test C: Domain-Line Collapse

Test whether the p26 F-square domain still descends cleanly to the p27 `a`
line.

Status: passed.  The domain line had `32,974` rows and `0` inconsistencies.

Kill condition: p27 splits the domain in a way that cannot be expressed in the
existing quotient coordinate.

### Test D: Non-Flat Payload Search

Only after Tests A-C pass, run bounded line-family screens and GPU same-stream
telemetry.

Status: partially negative.  Degree-1 and degree-2 tiny line families had no
exact survivors for either the domain line or the target line.  The next test
should be a named branch-divisor/theta identity or same-stream GPU telemetry,
not more blind tiny fitting.

Kill condition: only low-degree flatness or post-branch filtering that loses
more throughput than it gains.

## GPU Boundary

Do not spend a large GPU production run on this structure until the CPU gates
show exact p27 consistency. The first GPU ask should be a paired telemetry
experiment, not a certificate hunt:

```text
baseline same seeds vs p27 candidate source/filter same seeds
report raw candidate rate, accepted candidate rate, survivor distribution,
and effective lift per GPU-second
```

The exact telemetry bits to emit are now:

```text
a = (y - 1) - 1/(y - 1)
domain_line = chi((y - 1)(y^2 - 2)(y^2 - 2y + 2))
T_line = D*chi(y) if chi(a)=+1 else D*chi(y)*chi(b)
b = w((y - 1)^2 + 1)/(y - 1)^2
```
