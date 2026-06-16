# Trace-GCD Chow-Norm Theorem Candidate

Date: 2026-06-06

This note gives the selected Schubert p-unit theorem its intrinsic
Grassmannian name.

## Grassmannian Object

For one nonzero right orbit, work after splitting the 35-dimensional orbit
algebra:

```text
B_O = direct sum_{u in O} character_line_u.
```

The trace-GCD construction gives:

```text
W in Gr(16, B_O)
```

and the selected tail projection gives a fixed complementary subspace:

```text
C = ker(P),        dim C = 19.
```

For each right translate `t`, put:

```text
C_t = V_t^{-1} C.
```

The bad event is:

```text
W cap C_t != {0}.
```

Since `dim W + dim C_t = 35`, this is a Schubert divisor on
`Gr(16,35)`.  In Plucker coordinates it is a single hyperplane:

```text
Chow_Ct(W) = 0.
```

In the trace-GCD notation:

```text
Chow_Ct(W) = unit(t) * Delta(t).
```

The unit depends only on basis/trivialization conventions.  This is the
intrinsic version of:

```text
Delta(t) = det(P V_t W).
```

## Orbit Norm

For a Frobenius orbit `O_right` on right translations, the certificate scalar is:

```text
Pi_O = prod_{t in O_right} Delta(t).
```

Equivalently:

```text
Pi_O = unit * Norm_{O_right}(Chow_Ct(W)).
```

Thus the theorem to prove can be written as:

```text
the p24 CM point W has p-unit Chow norm against the cyclic translate family
{C_t}_{t in O_right}.
```

This phrasing avoids basis-dependent kernel determinants and makes clear that
the determinant is a section of a determinant line:

```text
det(W)^vee tensor det(B_O/C_t)^vee
```

after choosing compatible volume forms.

## Why This Is Useful

The Chow form is the exact divisor needed by the local-intersection route:

```text
D_O = sum_{t in O_right} {W : W cap C_t != {0}}.
```

The p-unit theorem is:

```text
local_p_intersection(W_CM, D_O) = 0.
```

So a successful Borcherds or modular-product proof does not have to identify
the row-reduced tail determinant.  It only has to identify the pullback of
this Chow divisor along the CM period/trace-GCD map and show its CM value has
zero selected p-valuation.

The finite implication is now isolated in:

```text
p24/lean/TraceGcdChowNormGate.lean
```

It checks:

```text
Chow zero detects the Schubert bad event,
orbit Chow norms detect local Chow zeros,
orbit Chow norms are p-units
=> no bad event and all determinant values are nonzero.
```

The p-integral determinant-line model is separated in:

```text
p24/trace_gcd_chow_integral_model.md
```

It shows that the Chow values are p-integral and basis-independent up to
p-units.  Thus the remaining theorem is genuine p-unitness, not denominator
hygiene.

## What It Does Not Give For Free

The Chow name does not prove nonvanishing.  The orbit exterior toy

```text
p24/orbit_exterior_schubert_toy.py
```

shows that even when every fixed Schubert coefficient and every Plucker
coordinate is nonzero, the Chow evaluation can vanish by cancellation.

The spectral-support audit shows p24 has full right-frequency support:

```text
distinct_subset_sum_size_k16=211.
```

Therefore the Chow norm is not a sparse resultant or a one-frequency
determinant.  A proof still needs arithmetic input about the actual CM
Plucker vector.

## Bounded-Correspondence Boundary

The easy modular-correspondence zero-lemma route is already closed for the
balanced order-`3107441` class.  The relevant notes are:

```text
p24/correspondence_zero_lemma_window.md
p24/low_norm_order3107441_search.md
p24/finite_field_modular_zero_lemma.md
```

The zero-lemma window would need a correspondence degree proxy

```text
delta < m = 66254.
```

But the exhaustive split-prime-power audit found no representative of the
order-`3107441` class with norm at most `66254`, even after allowing the
ramified genus prime `599`.  The best balanced representative currently has:

```text
2 * 463 * 223^(-1),
X0 index proxy = 311808 = 4.706252 * 66254.
```

Thus a small split correspondence cannot prove the Chow p-unit by forcing too
many zeros for too small a pole divisor.  This does not rule out a new
automorphic section for the Chow divisor, and it does not rule out the
growing-degree embedded phase route.  It only removes the bounded/local
correspondence shortcut.

## Recognition Audit

A side synthesis pass compared nearby formalisms.  The conclusion was:

```text
strongest name:
  orbit Chow norm / Schubert-Fitting reduced norm.
```

Other recognitions are weaker:

```text
resultant:
  true but tautological; it packages prod_t Delta(t) and does not prove
  p-unitness.  Ordinary base-field residues are not honest for the actual
  nonconstant Frobenius orbit values.

Plucker coordinate norm:
  too narrow.  Delta(t) is a Chow hyperplane value, a large linear
  combination of Plucker coordinates.  Nonzero Plucker entries can still
  cancel.

Toeplitz or Jacobi-Trudi determinant:
  useful as a weighted-Fourier rewrite, but nonzero symbol/invertible
  circulant does not force selected minors.

Wronskian:
  no osculating or rational-normal/GRS flag has been identified.  The small
  arc-like audits look generic rather than Wronskian.

Borcherds/local intersection:
  promising only after constructing an automorphic or class-field section
  whose divisor is this exact pulled-back Chow divisor.
```

The small actual-CM plain-divisor diagnostic

```text
p24/trace_gcd_chow_plain_divisor_scan.py
p24/trace_gcd_chow_plain_divisor_boundary.md
```

tests the easiest version of that hope.  In the pinned `D=-13319`,
`q=13463`, `h=140`, `m=28`, `(left,right)=(4,7)` row, the determinant has
right-period structure (`7` distinct values) but as a function of the plain
CM root `j_i` it has random-sized interpolation:

```text
polynomial_degree=139
rational_degree=70
random_rational_degree_mean=70.000
```

No expression of bidegree at most `4` in the oriented edge `(j_i,j_{i+1})`
was found.  Thus the visible period structure is not a simple plain-`j` or
one-edge divisor.  A Borcherds/local-intersection proof must construct the
phase-aware Chow/Fitting divisor itself.

The phase-coordinate diagnostic

```text
p24/trace_gcd_chow_phase_coordinate_scan.py
p24/trace_gcd_chow_phase_coordinate_boundary.md
```

confirms that this is the right kind of extra structure in the pinned row:
the determinant descends exactly to `alpha mod right`, compressing `140`
origin values to a length-`7` right-phase sequence with one nonzero Frobenius
orbit of DFT support.  For p24, the exterior support calculation is full by
subset size `3`, so a one-orbit support theorem would require special
arithmetic cancellation.  The safe payload remains seven orbit Chow norms.

The first phase-aware unit-span scan

```text
p24/trace_gcd_chow_phase_divisor_span_scan.py
p24/trace_gcd_chow_phase_divisor_span_boundary.md
```

does not find a non-random product formula from bounded right-binomial
cyclotomic units and small Heegner-fiber units.  The odd log spans are already
full rank, and the only non-full-rank mod-`2` span misses the Chow targets.

The global scalar version was tested in:

```text
p24/trace_gcd_global_product_miner.py
p24/trace_gcd_global_product_mining_boundary.md
```

It finds low-weight formulas for the isolated full product `Pi_all` in the
pinned row, but no corresponding low-weight formulas for the phase vector.
This is a negative-control result: scalar recognition is too weak to serve as
a producer theorem unless it is accompanied by a divisor/local-intersection
comparison to the actual Chow section.

The tensor-factor/top-coefficient route is adjacent but not a free substitute:

```text
p24/trace_gcd_chow_tensor_bridge_boundary.md
```

It would imply the Chow norm theorem only after a new p-integral
determinant-line comparison identifying the selected Chow/Fitting section as
a p-unit Schur factor or image of the tensor exterior products.  Tensor rank
or top-coefficient injectivity alone does not force a chosen Chow minor to be
a p-unit.

## Candidate Theorem

The next theorem worth trying to prove is:

```text
For the p24 conductor-2 CM trace-GCD period map, the pullback of the
right-orbit Chow divisor D_O is the divisor of an explicit p-integral
class-field/Borcherds/Fitting section whose selected CM value is a p-unit.
```

Equivalently:

```text
the orbit Chow norm Pi_O is a p-unit for each of the seven right Frobenius
orbits.
```

This is the same finite certificate target as the seven orbit products, but
phrased in the language most likely to connect to divisor/local-intersection
machinery.

The sharpened phase-aware version, including the lemma stack and the next
small-data falsifier, is recorded in:

```text
p24/trace_gcd_phase_aware_chow_borcherds_target.md
p24/lean/TraceGcdChowBorcherdsPUnitGate.lean
```
