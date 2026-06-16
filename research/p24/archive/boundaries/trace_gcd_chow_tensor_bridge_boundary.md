# Trace-GCD Chow vs Tensor-Factor Bridge Boundary

Date: 2026-06-06

This note checks whether the tensor-factor/top-coefficient machinery can be
lifted directly into the current trace-GCD Chow norm theorem.

## Two Nearby Objects

The tensor-factor route works after adjoining

```text
E = F_p(mu_m),     m = 2*157*211,
```

and splitting an `H`-packet for

```text
n = 3107441.
```

For p24, one tensor factor has degree

```text
5549 = 31 * 179
```

over `E`.  The refined theorem is a top-coefficient / trace-frame
anti-annihilator:

```text
W_axis(B) cap span_C{1,theta,theta^2}^perp = {0},
C = F_{E^179}.
```

Equivalently, three exterior products of CRT-marginal top-coefficient vectors
are p-units.

The trace-GCD Chow route has already compressed to the right `211` component:

```text
Delta(t) = det(P V_t A),
Pi_O = prod_{t in O} Delta(t).
```

For a nonzero right orbit, this is a Chow hyperplane evaluation of a
16-plane `W` against translated 19-planes in a 35-dimensional orbit algebra.

## Candidate Bridge

A direct import would need a theorem of the following form.

```text
Trace-GCD Chow/Tensor Bridge.

After choosing the same embedded conductor-2 CM torsor and the same
157/211 relative phase data, the orbit Chow section

  Delta_O(t)

is the image, under a p-integral determinant-line morphism, of one of the
tensor-factor exterior products

  Omega_1, Omega_211, Omega_3

or of a canonical Schur/Fitting factor of their direct-sum map.

The morphism has p-unit determinant on the selected local model.
Therefore p-unitness of the relevant tensor exterior product implies
p-unitness of the Chow orbit norm Pi_O.
```

This would be powerful: the tensor theorem supplies a structured
anti-annihilator statement with a `3 x 179` trace-frame surface, while the
trace-GCD verifier needs only seven orbit Chow norms and seven inverses.

## Why This Is Not Automatic

The existing tensor theorem is a rank statement for axis-frequency resolvents
inside one degree-5549 `H`-packet tensor factor.  The trace-GCD Chow
determinant is a selected Schubert minor after:

```text
1. taking the mixed 157 x 211 phase data;
2. deleting one right orbit;
3. cutting a four-orbit prefix kernel;
4. testing sixteen selected tail coordinates in a different right orbit.
```

The tensor exterior products prove that a large axis map is injective.  They
do not identify a particular selected Schubert coordinate of the kernel after
row reduction.  A nonzero exterior vector can have zero in a chosen Plucker
coordinate, and the orbit exterior toy already shows cancellation in selected
Chow evaluations even when the visible pieces are nonzero.

So the tensor route can imply the Chow route only after an additional
p-integral Schur/Fitting comparison:

```text
top-coefficient exterior p-unit
  => selected prefix kernel is p-integral of dimension 16
  => selected tail Chow determinant is a p-unit.
```

The first implication is not a formal consequence of rank; it is exactly a
selected-minor p-unit theorem in another basis.

## Useful Experiment

The small actual-CM test to run next, if pursuing this bridge, is:

```text
for rows where both objects are computable,
  compute the tensor top-coefficient exterior rank/minor package;
  compute the trace-GCD Chow determinant sequence for matching 157/211 data;
  test whether Chow zeros are always detected by a named tensor Schur factor,
  and whether nonzero tensor rank ever coexists with zero selected Chow minor.
```

A single coexistence example

```text
tensor exterior nonzero but selected Chow determinant zero
```

would show that tensor rank alone is too weak.  If no such example appears,
the bridge theorem should be sharpened to a concrete Schur complement identity
between the two determinant-line sections.

## Current Assessment

The bridge is plausible only as a **new determinant-line comparison theorem**,
not as a free import from tensor rank.  The two routes are therefore adjacent
but still separate:

```text
tensor route:
  prove a structured top-coefficient anti-annihilator p-unit;

trace-GCD Chow route:
  prove selected Schubert/Fitting orbit Chow norms are p-units.
```

The trace-GCD route remains the smaller certificate surface.  The tensor route
remains the more structured high-dimensional anti-annihilator surface.  A real
unification would have to construct a p-unit Schur/Fitting morphism between
their exterior determinant lines.
