# Degree-157 Refinement Target

This note records the next positive proof obligation for the best p24
certificate route.

## Context

For the third strict trace,

```text
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
G = Cl(O_K) ~= C_h
```

The best balanced formal target uses the oriented class

```text
beta = 2 * 463 * 223^(-1)
```

with

```text
order(beta) = 3107441
index(beta) = 66254 = 2 * 157 * 211.
```

If the embedded quotient periods

```text
y_r = sum_{k=0}^{3107440} j_{r + 66254*k}
```

were known, the quotient degree would be `66254` and the recovery degree would
be `3107441`, both far below `sqrt(p)=10^12`.

## First odd layer

The top degree-2 layer is genus.  The first genuinely non-genus refinement is
the degree-`157` layer:

```text
G / <g^2>          degree 2
G / <g^(2*157)>    degree 314
relative degree    157
```

The stabilizers are:

```text
genus parent stabilizer size:
  h / 2 = 102940198007

after degree-157 refinement:
  h / (2*157) = 655670051 = 211 * 3107441
```

The root-of-unity side is cheap:

```text
p mod 157 = 21
ord_157(p) = 156
```

So the Fourier/Kummer field for the relative degree-157 traces is not the
obstruction.

## Desired theorem

For each genus parent value `Z`, construct an embedded relative child
polynomial

```text
F_157(Z, Y)
```

of degree `157` in `Y`, whose roots are the embedded child periods above that
parent:

```text
y_{a + 2*r},        0 <= r < 157
```

where each `y` is already the period over the deeper stabilizer

```text
<g^(2*157)>.
```

Equivalently, compute the nontrivial relative traces

```text
T_s(a <g^2>) =
  sum_{u in <g^2>/<g^(2*157)>} zeta_157^(s*u) y_{a u <g^(2*157)>},
  1 <= s < 157,
```

embedded relative to the `j`-torsor and paired to the parent value.

## Why this is the right next target

This target avoids the closed routes:

```text
not a bounded local identity:
  it intentionally pays degree 157;

not an abstract class-field tower:
  it requires embedded child periods paired to j;

not a canonical child selector:
  it asks for an unordered degree-157 child polynomial;

not genus or ray-kernel data:
  the layer lies in the unramified principal genus;

not the final recovery:
  it tests the first odd phase before attempting degree 3107441.
```

If this degree-157 embedded relation cannot be constructed without full class
enumeration, the whole third-trace quotient-tower route lacks its first
non-genus step.

If it can be constructed, the next obligation is the analogous degree-`211`
refinement from degree `314` to degree `66254`, followed by degree-`3107441`
recovery in `j`.

## Direct quotient comparison

There is a direct split-prime analogue of this first odd layer:

```text
ell = 2897
order([ell]) = 1311340102 = 2 * 211 * 3107441
index([ell]) = 157
Gamma0(2897) degree proxy = 2898
seeded proxy = 2898 * 1311340102 = 3800263615596
```

This is a cleaner theorem toy because its quotient degree is exactly `157`.
But it is not the best certificate route: the recovery degree is
`1311340102`, and the seeded proxy is `3.800264 * sqrt(p)`.  The balanced
oriented composite target still has the better final recovery degree
`3107441` and proxy `0.968925 * sqrt(p)`.

The direct route is therefore useful mainly as a minimal first-odd-layer
question:

```text
Can the 157 embedded component sums of the horizontal 2897-isogeny cycles be
computed without first enumerating the CM vertices?
```

The answer would still need the same kind of embedded non-genus phase data as
the tower route.  Details are recorded in:

```text
p24/direct_degree157_quotient_target.md
```
