# Agent Embedded Tower Followup

Scope: embedded tower / `ell=677` / first odd degree-`157` child route.

## Conclusion

I did not find a concrete finite-field identity or class-field tower
construction that computes the `314` `ell=677` component sums, or the
degree-`157` child polynomials above the genus layer, without using the
embedded CM roots or an equivalent non-genus relative trace.

The sharpest positive statement remains conditional:

```text
L = <g^(2*157)>        index 314
K = <g^2>              index 2
K/L ~= Z/157Z

y_{aL} = sum_{l in L} j_{a l}
Z_{aK} = sum_{k in K} j_{a k}
F_157(Z_{aK},Y) = product_{u in K/L} (Y - y_{a u L})
```

The child polynomial is equivalently determined by the relative traces

```text
T_s(aK) = sum_{u in K/L} zeta_157^(s u) y_{a u L}
        = sum_{k in K} chi_s(k) j_{a k},       0 <= s < 157.
```

The root-of-unity extension is cheap.  The missing operation is computing the
embedded non-genus traces `T_s(aK)`.

## Ell-677 Equivalence

The split prime `ell=677` has

```text
order([677]) = 655670051 = 211 * 3107441
index([677]) = 314 = 2 * 157.
```

Thus its horizontal components are exactly the quotient `G/<g^314>`, i.e. the
genus layer followed by the first odd `157` refinement.  The component sums

```text
Z_r = sum_{k=0}^{655670050} j_{r + 314*k}
```

are the same embedded data as the degree-`314` quotient periods.  This is a
good fixed-p24 sub-sqrt success criterion, but not a different primitive from
the first odd tower layer.

The checked seedless routes still fail:

```text
universal Phi_ell cycle equations:
  contain the CM component sums but include extra non-CM cycles;

fixed trace + nonsplit conductor-2 gate:
  identifies the correct conductor branch, but naive enumeration scans A and
  does not compute component sums;

vertical conductor-2 transfer:
  preserves odd-prime components equivariantly, but changes the embedded sums;

genus projection:
  recovers only parity averages, not the 157 child values.
```

## Sharp Missing Relation

Let `alpha` be an abstract class-field quotient generator for the
`L`-fixed field, obtained for example from `bnrclassfield`.  A useful tower
construction needs an explicit embedded recovery relation

```text
R(A,X) in F_p[A,X]
```

such that, for each quotient root `alpha_r`,

```text
R(alpha_r, X) = product_{l in L} (X - j_{r l}).
```

For the `ell=677` layer this recovery degree is

```text
deg_X R(alpha_r,X) = |L| = 655670051.
```

The `314` component sum is then the negative `X^(|L|-1)` coefficient of this
specialization.  For the first odd child over a genus parent, the analogous
relation has recovery degree

```text
211 * 3107441
```

inside each of the `157` child branches.

Equivalently, one could supply a pairing relation directly between abstract
child roots and embedded child periods:

```text
S(Z,A,Y) = 0,
```

where `Z` is the genus parent, `A` is the abstract child root, and `Y` is the
embedded child period.  This is strictly the same missing phase data as the
relative traces above.

The existing toys show why an abstract quotient equation alone is not enough:

```text
D=-2239, q=2243, h=35, quotient degree 5:
  abstract quotient roots and embedded component sums both split;
  affine/Mobius maps between the two root sets: 0.

D=-5000, q=1259, h=30, quotient degree 6:
  the first rational selector y(j) appears at degree 15,
  exactly the generic interpolation threshold.
```

## Proposed Small Discriminating Toy Test

Use the non-genus degree-5 toy, preferably the genus-then-degree-5 analogue
`D=-711, q=727, h=20`, because it matches the p24 layer shape

```text
genus parent -> odd child.
```

For each genus parent:

1. Compute the abstract degree-5 child roots `alpha_i` from `bnrclassfield`.
2. Compute the embedded child periods `Y_j` from the known toy CM cycle.
3. Search for a low-bidegree graph relation

   ```text
   S(A,Y) = 0
   ```

   whose zeros on `{alpha_i} x {Y_j}` form a perfect matching: one zero in
   every row and every column, and no cross zeros.

Suggested first bidegrees:

```text
(deg_A, deg_Y) = (1,1), (1,2), (2,1)
```

The cross-zero condition is the discriminator.  A generic interpolation can
fit one chosen matching once the bidegree is large enough, but it will not
usually avoid all wrong pairs at very low bidegree.

Interpretation:

```text
success:
  evidence for a concrete relation shape S(A,Y), worth lifting to the
  p24 degree-157 layer;

failure:
  strengthens the pairing obstruction: abstract child roots and embedded
  child periods are split torsors with no simple finite-field relation.
```

## Follow-up Scan Result

The low-bidegree graph-relation test is now implemented in:

```text
p24/abstract_embedded_graph_relation_scan.py
```

For the established `D=-2239, q=2243` degree-5 non-genus toy it reports:

```text
degA=1 degY=1 variables=4 actual_success_matchings=0
degA=1 degY=2 variables=6 actual_success_matchings=120
degA=2 degY=1 variables=6 actual_success_matchings=120
degA=2 degY=2 variables=9 actual_success_matchings=120
```

The random controls behave the same:

```text
(1,1): 0/20 random controls have any graph relation
(1,2): 20/20 random controls have graph relations
(2,1): 20/20 random controls have graph relations
(2,2): 20/20 random controls have graph relations
```

So the first meaningful threshold is stricter than the proposed `(1,2)` or
`(2,1)` test.  Those bidegrees already have more coefficients than the five
matched points and therefore create generic graph equations.  A useful
embedded pairing theorem must supply either a relation below interpolation
threshold, a canonical coefficient restriction, or a modular construction of
the relation; plain low-bidegree existence is not enough.

This test is small because the child degree is only `5`; it checks exactly the
kind of relation the p24 route would need, without touching large p24 jobs.
