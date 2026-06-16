# p25 Lane B: GK/HD Projection Legitimacy Scout

Updated: 2026-06-13 13:18 PDT

## Scout Result

The inspected Gross-Koblitz, Hasse-Davenport, Davenport-Hasse lifting,
Greene, and McCarthy sources did not justify the post-hoc operation

```text
R(q) -> R(q)^2029
```

as a standard theorem-level finite-field hypergeometric/Gauss-sum
normalization after the quotient already contains a `mu_2029` component.

The operation remains natural as a local multiplicative projection in the
auxiliary value field:

```text
fixes mu_2028, hence fixes mu_39
kills mu_2029
R(138) = zeta_39^5 * additive_root^1475
R(138)^2029 = zeta_39^5
```

But that is weaker than an admissible producer identity.  Hasse-Davenport
products/lifts, Gross-Koblitz gamma rewrites, and McCarthy/Greene
normalizations act through Gauss/Jacobi factors, character products, lifts, or
balanced quotient terms; the scout found no theorem that says to form the
already-dense quotient and then erase its `mu_2029` component by a nonadditive
residue-field power.

The normalization by `(zeta_39^5 - 1)^-1 = 636` is canonical after accepting
the powered unit

```text
U = 1 + (zeta_39^5 - 1) * e_138,
```

because it extracts `e_138`.  The scout did not find a GK/HD theorem that
forces that normalization before the powered unit exists.

## Updated Viability Read

McCarthy Theorem 1.7 remains the best theorem hook because its exceptional
delta is real and exactly selects `q=138`.

The moonshot is now conditional on one of these stronger outcomes:

```text
1. find a theorem-level quotient where the mu_2029 component cancels before
   q-power projection;
2. show the relevant arithmetic object naturally lives modulo the mu_2029
   component, so q-power projection is not arbitrary post-processing;
3. replace the powered-quotient step with a direct endpoint identity producing
   U or e_138.
```

Absent one of those, the powered McCarthy route is a strong diagnostic and
finite payload recipe, not yet a credible certificate producer.

## Recommended Probe

Run an auxiliary-prime invariance probe:

```text
for several primes ell = 1 mod 2029*2028*5:
  recompute the McCarthy quotient in F_ell
  decompose R(138) into mu_39 * mu_2029 * mu_5 components
  test whether only the ell-local map x -> x^2029 removes mu_2029
```

Kill condition: if no balanced Gauss/Jacobi quotient, HD product/lift, or
additive-character norm removes the `mu_2029` component uniformly, then the
projection is post-processing rather than theorem-level structure.
