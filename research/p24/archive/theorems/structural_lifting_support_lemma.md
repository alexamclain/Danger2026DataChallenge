# Structural support lemma for embedded selectors

This records the clean theorem that survives the lifting audits.  It is not
yet a certificate theorem, because it assumes exactly the equivariance and
finite-field faithfulness that a p-specific selector might evade.

## Lemma

Let `G = Cl(O)` act simply transitively on the embedded ordinary CM torsor

```text
J = {j_a : a in G}
```

over a field `k` of characteristic `p`.  Let `H <= G`.  Suppose a proposed
selector formula satisfies:

```text
1. It is an additive k-linear combination of oriented horizontal modular
   correspondences.
2. Its levels are prime to p and to the conductor/bad discriminant set.
3. It has a p-integral model and no denominator or pole collapses on the
   reduced CM torsor.
4. After orientations are chosen, each correspondence restricts on CM points
   to finitely many class translates.
5. The identity is equivariant on the whole torsor:

      L(j_a) = sum_{h in H} j_{h*a}          for all a in G.

6. The reduced CM element is normal/faithful:

      k[G] -> span_k(G*j),    A -> A*j

   is injective.
```

Then the formula restricts to a group-algebra element

```text
L = sum_s c_s [s] in k[G],
```

and the identity forces

```text
L = e_H = sum_{h in H} [h].
```

Up to a translate or scalar normalization, the same conclusion holds for a
translated/scaled period.  Therefore the collected support of the formula is
at least `|H|`.

## Proof

Hypotheses 1-4 say that the reduced formula acts on the CM torsor as a
well-defined element of `k[G]`: oriented horizontal correspondences are class
translations, and additive combinations remain group-algebra operators.

Hypothesis 5 says this operator and the subgroup projector `e_H` have the same
effect on every translate of `j`.  Thus

```text
(L - e_H) * (g*j) = 0        for all g in G.
```

Equivalently, `(L-e_H)` is in the kernel of the representation map
`k[G] -> span_k(G*j)`.  Hypothesis 6 makes that map injective, so `L=e_H`.
Since `e_H` has exactly `|H|` nonzero coefficients, any exact sparse local
operator has support at least `|H|`.

## p24 consequences

For the live targets:

```text
first trace order-19:
  |H| = 14670196166

third trace composite 2 * 463 * 223^(-1):
  |H| = 3107441
```

The characteristic-zero singular modulus is normal for the p24 CM torsors by
the dominant-conjugate estimate in:

```text
p24/singular_moduli_normality_bound.py
```

But the finite-field reduced-normality/lifting condition is not proved.  The
naive norm-height proof fails by many orders of magnitude:

```text
p24/finite_field_lifting_height_audit.py
p24/class_invariant_lifting_height_audit.py
```

So the theorem boundary is now:

```text
local/equivariant/additive selectors require projector-sized support;
p-specific non-lifted or nonlinear selectors are not excluded by this lemma.
```

## Failure modes not covered

The lemma does not rule out:

```text
1. a one-prime congruence that works modulo p but not in characteristic zero;
2. a formula that selects only one origin/root and is not equivariant;
3. an unoriented, vertical, ramified, Atkin-Lehner-quotiented, or order-changing
   correspondence;
4. a denominator or pole collapse after reduction modulo p;
5. nonlinear constructions such as resultants, products, norms, or root
   selection where support in k[G] is not the right complexity measure;
6. an abstract quotient root not paired with the embedded j-cycle period;
7. finite-field reduced normality failure even though characteristic-zero
   normality holds.
```

In the `D=-5000`, `q=1259` toy, reduced normality holds (`gcd_degree=0`) and
the support conclusion is exact; see:

```text
p24/normal_basis_support_toy.py
```
