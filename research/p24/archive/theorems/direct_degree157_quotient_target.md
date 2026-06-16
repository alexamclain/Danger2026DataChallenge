# Direct Degree-157 Quotient Target

This note compares two ways to isolate the first odd non-genus layer in the
third strict p24 target.

## Shared p24 data

For the best third trace,

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
sqrt(p) = 1000000000000
```

The final balanced target remains the oriented composite class

```text
beta = 2 * 463 * 223^(-1)
order(beta) = 3107441
index(beta) = 66254 = 2 * 157 * 211
norm proxy = 206498
Gamma0 index proxy = 311808
seeded proxy = 311808 * 3107441 = 968924963328
```

This is just below `sqrt(p)`, but it is not a seedless construction.  It still
needs an embedded quotient/relative-period theorem.

## Tower-first degree 157

The tower route first uses the genus layer and then asks for the first odd
refinement:

```text
G / <g^2>             degree 2
G / <g^(2*157)>       degree 314
relative degree       157
recovery subgroup     h / (2*157) = 655670051 = 211 * 3107441
```

The desired object is an embedded relative child polynomial

```text
F_157(Z,Y)
```

over each genus parent value `Z`, with degree `157` in `Y`.  Its roots are the
periods over `<g^(2*157)>` lying above that parent.  Equivalently, one must
compute the nontrivial relative character traces on
`<g^2>/<g^(2*157)>`.

The root-of-unity side is harmless:

```text
p mod 157 = 21
ord_157(p) = 156
```

The hard part is not adjoining `mu_157`; it is pairing the relative
non-genus child periods with the embedded `j`-torsor.

## Direct split-prime degree 157

There is also a cleaner direct odd-layer target.  The split prime

```text
ell = 2897
```

has ideal-class order

```text
order([ell]) = 1311340102 = 2 * 211 * 3107441
index([ell]) = 157
```

So its horizontal `ell`-isogeny cycles give, in principle, `157` embedded
components.  This is a useful first non-genus theorem toy because the quotient
degree is exactly the first odd factor.

It is not the best certificate route:

```text
direct quotient degree        = 157
direct recovery degree        = 1311340102
Gamma0(2897) degree proxy     = 2898
seeded walk proxy             = 2898 * 1311340102
                              = 3800263615596
seeded proxy / sqrt(p)        = 3.800264
```

By contrast, the balanced composite target has recovery degree `3107441` and
seeded proxy `0.968925 * sqrt(p)`.

## Seedless obstruction

The direct split-prime graph becomes cheap only after embedded CM vertices are
already available.  A seedless closed-cycle equation is enormous.

For the direct `ell=2897` subgroup cycle, the natural `X0(ell^r)` closed-cycle
degree proxy has

```text
r = 1311340102
log10 psi(2897^r) = 4.539792e9
```

Even a hypothetical subgroup generator of order `3107441` has the lower bound

```text
log10(degree) >= 3107441 * log10(2) = 9.354330e5
```

before it selects a CM root.

Thus the small quotient is not obtained by a seedless modular-polynomial
fixed-point condition.  It is obtained only after an embedded CM root set,
cycle, or equivalent quotient-period identity exists.

## Normalizer quotient does not supply the odd layer

Atkin-Lehner and Fricke quotients can reduce an `X0(N)` map by at most the
normalizer symmetries.  For the relevant prime levels this is only a factor
of `2`:

```text
level 2897: Gamma0 index 2898, full AL lower proxy 1449
level 677:  Gamma0 index 678,  full AL lower proxy 339
level 7349: Gamma0 index 7350, full AL lower proxy 3675
```

These quotients change constants but do not create the class-field
stabilizers `157`, `211`, `3107441`, or `66254`.

## Small analogue

The toy

```text
D = -5000
q = 1259
h = 30 = 2 * 3 * 5
G >= <g^2> >= <g^6>
```

is the p24 tower shape with `3` in place of `157`.

Running

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_phase_refinement_toy.py
```

constructs a bivariate child relation from the embedded cycle:

```text
top_periods=[1126, 532]
parent=0 child polynomial=[563, 777, 133, 1]
parent=1 child polynomial=[648, 958, 727, 1]
wrong_parent_cross_zeros=0
```

The companion Fourier toy

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_tower_character_toy.py
```

shows the equivalence:

```text
relative child polynomial
  <=> relative class-character traces on <g^2>/<g^6>.
```

But both scripts build the relation from the embedded `j`-cycle.  The abstract
tower degrees alone do not supply those traces.

The non-genus abstract pairing toy

```text
D = -2239, q = 2243, h = 35, quotient size = 5
```

shows the sharper negative control: both the abstract degree-5 quotient and
the embedded period quotient split over the same finite field, but there is no
affine or Mobius set map between their root sets.

A second odd-child analogue found by the sidecar has `5` in place of `157`:

```text
D = -711
q = 727
h = 20 = 2 * 5 * 2
ell = 2
```

It gives a genus parent followed by a degree-5 child refinement:

```text
top_periods=[635, 334]
parent 0 child polynomial=[372, 709, 415, 16, 92, 1]
parent 1 child polynomial=[338, 93, 520, 109, 393, 1]
wrong_parent_cross_zeros=0
```

But comparing PARI's abstract degree-5 quotient roots with the embedded child
sets again finds no affine or Mobius pairing:

```text
affine_maps=0
mobius_maps=0
```

This strengthens the boundary: the tower child polynomial is a real object,
but abstract quotient roots are still unpaired without embedded non-genus
relative traces.

## Current conclusion

The direct `ell=2897` quotient should be treated as a clean first-odd-layer
theorem toy:

```text
Can one build the 157 embedded component sums of the horizontal 2897-isogeny
cycles without enumerating the CM root set?
```

The p24 certificate route should not switch to it as the main target.  Its
recovery degree and seeded walk proxy are worse than the balanced composite
period.  The useful proof obligation remains the tower/composite form:

```text
construct embedded non-genus relative traces for the 157 layer,
then for the 211 layer,
then recover j in degree 3107441.
```

Equivalently, prove the exact relative content or Hermitian packet
nonvanishing theorem for the balanced quotient.
