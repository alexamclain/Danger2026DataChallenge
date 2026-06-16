# Class-character period reframing

The split-cycle quotient can be rephrased exactly as a class-character period
problem.  This is the closest analogue so far to Gaussian periods in
cyclotomic fields.

## Fourier identity

Let `G=Cl(O)=<g>` be cyclic of order `h`, and let `H=<g^m>` have size `n`, so
`h=mn`.  Write the CM conjugates as

```text
j_i = j(g^i * a_0).
```

The subgroup periods are

```text
y_r = sum_{k=0}^{n-1} j_{r + mk},        0 <= r < m.
```

For a primitive `m`-th root of unity `zeta_m`, define twisted traces

```text
T_s = sum_{i=0}^{h-1} zeta_m^{s*i} j_i,  0 <= s < m.
```

Then

```text
y_r = (1/m) * sum_{s=0}^{m-1} zeta_m^{-sr} T_s.
```

So the embedded quotient polynomial

```text
V(Y) = product_r (Y - y_r)
```

is cheap once all quotient-character twisted traces `T_s` are known.

## Toy verification

I added:

```text
p24/character_period_transform_toy.py
```

For `D=-5000`, `h=30`, subgroup size `3`, quotient size `10`, and split prime
`q=3851` with `q == 1 mod 10`, the script computes the DFT exactly in `F_q`:

```text
inverse_dft_recovers_period_sums=1
period_polynomial_degree=10
```

This verifies the identity over a finite field.  In the toy script the
twisted traces are still computed by summing the embedded vertices; the point
is to isolate the missing primitive.

## p24 requirements

I added:

```text
p24/class_character_period_route_audit.py
```

For the original smooth third-trace candidates:

```text
ell=7349:
  quotient_size = 422
  subgroup_size = 487868237
  root_of_unity_extension_degree_over_Fp = 35

ell=677:
  quotient_size = 314
  subgroup_size = 655670051
  root_of_unity_extension_degree_over_Fp = 156

composite ideal 2 * 463 * 223^(-1):
  quotient_size = 66254
  subgroup_size = 3107441
  root_of_unity_extension_degree_over_Fp = 5460
```

Thus the Fourier/inverse-Fourier layer is not the obstruction.  The missing
object is a sublinear way to compute high-order, non-genus twisted traces

```text
T_chi = sum_{a in Cl(O)} chi(a) j(a)
```

for characters of order involving `157` or `211`.

The all-target audit later found an even cleaner instance on the first strict
trace:

```text
t = 1020608380936
D_K = -739589633190799177940983
h = 2 * 19 * 7335098083

ell=19:
  quotient_size = 19
  subgroup_size = 14670196166
  root_of_unity_extension_degree_over_Fp = 2
  seeded_walk_proxy = 0.293404 * sqrt(p)
```

So the smallest current theorem experiment is an embedded order-19 twisted
trace formula.  For an actual certificate route, however, the third trace's
balanced composite ideal remains better because its recovery degree is only
`3107441`, versus `14670196166` for the first-trace `ell=19` cycle.

Known Zagier/Borcherds/Bruinier-Funke trace formulas give global traces and
some twisted traces, especially genus-character style traces.  They do not
currently provide the high-order odd class-character traces needed here
without summing over CM classes or using an equivalent embedded class object.

## Seedless elimination toy

I also added:

```text
p24/seedless_cycle_elimination_toy.py
```

For the tiny model

```text
D=-87, h=6, ell=7, class_order(ell)=3, q=103,
```

eliminating `x0,x1,x2` from

```text
H_D(x_i)=0
Phi_7(x0,x1)=Phi_7(x1,x2)=Phi_7(x2,x0)=0
Y=x0+x1+x2
```

over `F_103` yields

```text
(Y - 29) * (Y - 4).
```

These are exactly the two 3-cycle sums.  This is a positive check that the
cycle quotient is algebraic and seedless once `H_D` is supplied.

For p24, however, supplying `H_D` means a degree-`205880396014` class
polynomial.  The elimination identity therefore does not by itself beat the
class-set barrier; it shows what a non-enumerative twisted-trace theorem would
need to replace.

## Current theorem target

The missing theorem has the cleanest form now:

```text
Compute the non-genus class-character twisted traces T_chi for one of the
small quotient targets, especially order `19` for the first strict trace, in
o(sqrt(p)) work without first constructing H_D or enumerating CM classes.
```

Fourier inversion, cycle-sum quotient construction, and recovery to a cycle
are then structurally clear.  The hard gap is exactly the high-order twisted
trace computation.

## Non-genus modular-form level audit

I added:

```text
p24/non_genus_twisted_trace_level_audit.py
p24/genus_projection_period_toy.py
```

The standard modular-form route has the wrong level scale.  A non-genus class
group character of `K` is an unramified Hecke/class character.  Its associated
dihedral theta series over `Q` has natural level `|D_K|` (up to the usual small
half-integral-weight factors), not level `314` or `422`.

For the third p24 target:

```text
|D_K| = 652834595820939249713143 = 599 * 1089874116562502921057

weight-1 dihedral level |D_K|:
  Gamma0 index ~= 6.539e23
  k/12 index proxy ~= 5.449e22 = 5.449e10 * sqrt(p)

half-integral trace level 4|D_K|:
  k/12 index proxy ~= 4.904e23 = 4.904e11 * sqrt(p)
```

This does not prove a lower bound, but it rules out the naive plan "use the
known twisted-trace modular form and compute in a small space".

The genus projection toy shows the information loss directly.  In the
`D=-5000`, quotient-size-10 period toy, retaining only the trivial and
quadratic/genus traces recovers only two parity averages:

```text
projection_distinct_values=[3153, 3570]
```

For p24, genus traces would similarly average over `157` periods for the
`ell=677` quotient, over `211` periods for the `ell=7349` quotient, and over
`33127` periods for the balanced `66254` quotient.  The order-`157` and
order-`211` class characters are genuinely needed.

Relevant source anchors:

```text
Zagier traces and Choi/Bruinier-Funke extensions:
  https://arxiv.org/abs/1105.1223
  https://arxiv.org/abs/1108.3961

Dihedral theta-series level shape:
  https://www.sciencedirect.com/science/article/pii/S0019357711000243
```

## Moment and norm escape hatches

I added:

```text
p24/period_moment_idempotent_toy.py
p24/period_correlation_idempotent_toy.py
p24/relative_norm_phase_toy.py
p24/abstract_vs_embedded_quotient_toy.py
p24/period_selector_theorem_status.md
```

The quotient-polynomial-by-moments idea does not remove the high-order
character data.  In the D=-5000 quotient-size-10 toy, the power sums satisfy
the exact idempotent convolution identity

```text
P_d = sum_r y_r^d
    = m^(1-d) * sum_{s_1+...+s_d=0 mod m} T_{s_1}...T_{s_d}.
```

The script verifies:

```text
convolution_formula_matches=1
newton_reconstructs_true_period_polynomial=1
genus_polynomial_equals_true=0
```

Thus moments are useful only if a theorem already supplies the high-order
subgroup idempotent.  Trivial/genus moments reconstruct a repeated-average
polynomial, not the true quotient.

The correlation/Hecke-trace variant is the same obstruction in another basis.

## Multiplication-table boundary

I also checked the most direct Gaussian-period analogy in:

```text
p24/period_multiplication_table_scan.py
p24/period_multiplication_table_boundary.md
```

For a quotient-period vector `y`, use its cyclic shifts as a normal basis of
the split quotient algebra and solve

```text
shift_i(y) * shift_j(y) = sum_k c_{i,j,k} shift_k(y).
```

In the `D=-5000` and `D=-2239` toys, every multiplication table was dense and
matched random controls:

```text
D=-5000 quotient=10: avg_support=10.000, random_avg=9.985
D=-2239 quotient=7: avg_support=7.000, random_avg=6.986
```

The number of distinct product rows was the commutative maximum `m(m+1)/2`.
So there is no visible sparse cyclotomic-number-style multiplication table.
Access to this table is essentially access to the embedded period algebra
itself, not a new small primitive for computing the child polynomial.
The script

```text
p24/period_correlation_idempotent_toy.py
```

checks the exact `D=-5000`, quotient-size-10 calibration.  If

```text
C(d) = sum_i j_i j_{i+d},
```

then

```text
sum_r y_r^2 = sum_{d in H} C(d).
```

The toy output verifies:

```text
square_sum_equals_projected_autocorrelation=1
autocorrelation_spectrum_matches_trace_products=1
nonzero_spectral_components=10
```

The autocorrelation diagonalizes to `T_s*T_{-s}`, where the `T_s` are the same
quotient-character traces.  Thus a Hecke-trace/correlation formula would still
need a cheap way to project onto the high-order subgroup `H`; without that it
only reformulates the relative-period problem.

The norm/product analogue has the same shape.  Coset products

```text
z_r = prod_{k=0}^{n-1} j_{r+mk}
```

are valid quotient coordinates, but global norms only give `prod_r z_r` and
erase the quotient phase.  In the toy:

```text
distinct_period_products=10
global_norms_match=1
```

So Gross-Zagier/Borcherds-style global product formulas do not select a cycle;
a useful theorem would need a relative norm formula retaining the full
degree-314 or degree-422 quotient polynomial.

Finally, the abstract-vs-embedded toy makes the `bnrclassfield` limitation
explicit.  For `D=-87`, PARI gives an abstract quotient `x^2+3`, with roots
`[10,93]` over `F_103`, while the embedded `Phi_7` cycle-sum quotient has roots
`[4,29]`.  The roots are unpaired until a relation to `j` is supplied.  This
is exactly the missing relation in the p24 degree-314/422 quotient.
