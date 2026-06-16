# Ell-677 Component Quotient Boundary

This note isolates the best split-prime intermediate target for the third
strict p24 trace.

## p24 data

For

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
```

the split prime

```text
ell = 677
```

has ideal-class order

```text
order([677]) = 655670051 = 211 * 3107441
index([677]) = 314 = 2 * 157.
```

Thus the horizontal `677`-isogeny graph on the embedded CM roots should split
into `314` cycles, each of length `655670051`.

## Why this is a real intermediate target

If the cycle-sum quotient

```text
Z_r = sum_{k=0}^{655670050} j_{r + 314*k},     0 <= r < 314
```

were constructible over `F_p` without enumerating the full CM class set, then
one could work with:

```text
quotient degree        = 314
recovery degree        = 655670051
Gamma0(677) proxy      = 678
seeded walk proxy      = 678 * 655670051
                         = 444544294578
seeded proxy / sqrt(p) = 0.444544
```

This is a genuine fixed-p24 sub-sqrt certificate shape.  It is stronger as a
certificate target than the direct `ell=2897` index-157 toy, whose seeded
proxy is `3.800264 * sqrt(p)`.

It is weaker than the final balanced composite target:

```text
balanced quotient degree   = 66254
balanced recovery degree   = 3107441
balanced seeded proxy      = 968924963328 = 0.968925 * sqrt(p)
```

The balanced target has a larger quotient but much smaller final recovery.

## Equivalence to the first odd tower layer

The `ell=677` cycles are not a new kind of object.  They are exactly the
degree-`314` quotient

```text
G / <g^314>
```

which is the genus layer followed by the degree-`157` odd refinement:

```text
G / <g^2>             degree 2
G / <g^(2*157)>       degree 314
```

So constructing the `677` cycle-sum polynomial is equivalent to constructing
the unordered child periods after the first odd non-genus layer.  In character
language, it requires quotient characters of order dividing `314`, including
the non-genus order-`157` characters in the principal genus.

The root-of-unity side is still cheap:

```text
p mod 157 = 21
ord_157(p) = 156
```

The missing part is the embedded class-character trace, not cyclotomic
arithmetic.

## Why natural seedless constructions fail

The split-cycle quotient toy

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/split_cycle_quotient_toy.py
```

uses `D=-5000`, `q=1259`, `h=30`, and `ell=11` with class order `3`.
It confirms that whole split-prime cycle sums have the expected quotient
degree, but edge values still have the full orbit:

```text
component_count=10
component_sizes=[3]
distinct_edge_sums=30
distinct_edge_products=30
cycle_sum_polynomial_degree=10
```

The seedless elimination toy

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/seedless_cycle_elimination_toy.py
```

recovers the degree-2 cycle-sum polynomial for `D=-87`, `h=6`, `ell=7`, but
only by using `H_D`:

```text
eliminated_cycle_sum_polynomial=(Y - 29)*(Y - 4)
elimination_uses_H_D_polynomial=1
p24_H_D_degree_is_205880396014=1
```

The matching unfiltered toy removes the `H_D` equations:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/unfiltered_phi_cycle_toy.py
```

For the same `D=-87`, `q=103`, `ell=7` calibration, the universal simple
3-cycles of `Phi_7` give:

```text
universal_simple_3cycles=10
universal_cycle_sums=[4, 9, 28, 29, 50, 55, 65, 76, 80, 88]
CM_cycle_sums=[4, 29]
CM_sums_subset_universal=True
```

So the closed-cycle equations include the target CM cycle sums, but do not
select the fixed CM order.  The missing filter is an embedded CM-order
relation, not the modular correspondence itself.

I generalized this check in:

```text
p24/universal_cycle_sum_filter_scan.py
```

Bounded run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/universal_cycle_sum_filter_scan.py \
  --max-cases 12 --min-h 4 --max-h 40 --max-abs-D 8000 \
  --q-stop 350 --max-ell 13 --max-component-size 4
```

Output summary:

```text
rows=12
all_cm_sums_subset_universal=1
rows_with_extra_universal_sums=12
```

Every tested CM component-sum set was contained in the universal
`Phi_ell` closed-cycle sum set, but every universal set had extra non-CM
cycle sums.  Thus this is not an accident of `D=-87`: seedless closed-cycle
equations systematically overselect unless a CM-order/fixed-trace filter is
added.

Adding a fixed-trace filter helps but still does not isolate the target
maximal-order component quotient.  I added:

```text
p24/fixed_trace_cycle_filter_toy.py
```

For the same `p=103`, `t=8`, `ell=7` toy, fixed trace gives the union of the
maximal order `D=-87` and conductor-2 order `D=-348`.  The run reports:

```text
universal_sums=10
maximal_sums=[4, 29]
fixed_trace_sums=[4, 29, 50, 88]
extra_fixed_trace_sums=[50, 88]
```

So fixed trace removes many universal cycles but still leaves extra conductor
layers.  In p24, the strict trace has the same conductor-2 shape, so a
fixed-trace filter still needs an order/volcano filter to select the desired
CM component quotient.

The Montgomery verifier changes the interpretation of those "extra" roots.  I
added:

```text
p24/fixed_trace_montgomery_verifier_toy.py
```

For the same `p=103`, `t=8` analogue, the official x-only verifier condition
selects the nonsplit conductor-2 Montgomery branch, not the split maximal-order
branch:

```text
valid_triples=96
good_trace_A_without_verifier_x=24
maximal_trace_A_count=24
maximal_trace_A_torsion_shape={'split': 24, 'nonsplit': 0}
maximal_valid_j=[]
maximal_valid_A_count=0
conductor2_trace_A_count=12
conductor2_trace_A_torsion_shape={'split': 0, 'nonsplit': 12}
conductor2_valid_j=[4, 44, 62, 63, 85, 86]
conductor2_valid_A_count=12
```

So the conductor-2 fixed-trace roots are not automatically noise.  In this
calibration they are precisely the roots that admit a cyclic x-only
`2^k` chain.  For p24, where the strict trace discriminants are also
`4*D_K` with `D_K == 1 mod 8`, the component-sum theorem should be phrased for
the Frobenius-order/conductor-2 branch, or should include an explicit
nonsplit-Montgomery gate after producing a fixed-trace root.  This does not
remove the non-genus class-selection problem: the conductor-2 class number is
the same as the maximal one in the p24 cases, so the target component quotient
still has the same class-group scale.

## Linear Atkin-Lehner Boundary

The finite-field zero lemma does not become available by passing to the
Atkin-Lehner quotient of `X0(677)`.  The note

```text
p24/ell677_linear_pole_boundary.md
```

shows that the optimistic quotient proxy `339` is not the pole degree of the
linear endpoint traces forced by content collapse.  The best
Atkin-Lehner-descended endpoint-linear function has pole degree `677`, still
larger than the required index `314`.

The moment route is also the same idempotent in disguise:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/period_moment_idempotent_toy.py
```

For a quotient-size-10 toy, direct power sums satisfy the convolution identity

```text
P_d = m^(1-d) * sum_{s_1+...+s_d=0 mod m} T_{s_1}...T_{s_d}.
```

Thus moments of the cycle sums still require the high-order quotient
characters.  Genus-only moments reconstruct a coarser repeated-average
polynomial, not the true period polynomial.

Finally, the standard modular-form trace route puts the non-genus character
at level/discriminant scale:

```text
dihedral weight-1 level proxy:       5.449371e22
half-integral trace level proxy:     4.904434e23
sqrt(p):                             1.000000e12
```

So known twisted-trace formulas do not make the `677` component polynomial
sub-sqrt.

## Current conclusion

The `ell=677` target is the sharpest first-odd-layer fixed-p24 certificate
target:

```text
construct the 314 component sums of the horizontal 677-isogeny graph without
enumerating the CM vertices.
```

If achieved, it would already give a sub-sqrt path to a p24 certificate.  But
it is not a different theorem from the degree-157 embedded tower target.  It
is the same missing non-genus phase, packaged as split-prime graph components
instead of relative child polynomials.

The complement-trace recovery audit now records the same tradeoff from the
subgroup side:

```text
p24/generated_subgroup_split_tradeoff.py
p24/complement_trace_recovery_relation.md
p24/conductor2_nonsplit_gate.md
p24/conductor2_component_transfer_boundary.md
```

There `ell=677` appears as the best generated-subgroup fallback:

```text
G / <677>   degree 314,
<677> / H   relative degree 211,
H           final recovery degree 3107441.
```

This is a clean tower shape, but still needs the embedded component sums and
relative child relation rather than just the abstract subgroup data.

The conductor-2/nonsplit refinement does not change this conclusion.  The
bounded transfer scan in `p24/conductor2_component_transfer_boundary.md` found
that the descending `2`-isogeny is equivariant on odd-prime components, but the
conductor-2 component-sum values are different embedded periods, not a
collapsed copy of the maximal-order sums:

```text
rows=20
all_equivariant=1
rows_with_same_sum_set=0
```

So the final p24 target should use the conductor-2/nonsplit branch, but the
same `314` embedded component-sum construction remains the missing primitive.
