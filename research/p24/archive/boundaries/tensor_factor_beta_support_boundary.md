# Tensor Factor Beta-Support Boundary

This note checks whether the marginal beta-product can be compressed by small
character support.

## Spectral Support

In one p24 tensor factor over `E=F_p(mu_m)`, multiplication by `theta` has
E-eigencharacters indexed by the orbit

```text
O = <a> mod n,       a = p^ord_m(p) mod n.
```

For p24:

```text
n = 3107441,
ord_m(p) = 5460,
a = 209035,
|O| = 5549.
```

A beta-shifted Plucker coordinate of a marginal exterior product has the form:

```text
beta |-> P(Top_k(theta^(-beta) * marginal vectors)).
```

After diagonalizing multiplication by `theta`, this is an exponential
polynomial in beta.  Its possible characters lie in exterior sumsets of `O`.
Thus small sumsets of `O` would give a route to recurrence/resultant
compression of the beta product.

## p24 Audit

The audit script is:

```text
p24/tensor_factor_beta_support_audit.py
```

Run with the bundled NumPy runtime:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/tensor_factor_beta_support_audit.py
```

It reports:

```text
fold=2 covered=3090793 missing=16648
       min_positive=2 max_count=24
       zero_covered=0
       cosets_covered=557 cosets_missing=3 partial_cosets=0

fold=3 covered=3107441 missing=0
       min_positive=33294 max_count=56901
       zero_covered=1
       cosets_covered=560 cosets_missing=0 partial_cosets=0

fold=4 covered=3107441 missing=0
       min_positive=304785298 max_count=314961240
       zero_covered=1
       cosets_covered=560 cosets_missing=0 partial_cosets=0
```

So `O+O` already covers `557` of the `560` nonzero `E`-Frobenius orbit
factors of `T^n-1`, and `O+O+O` covers all of them plus the zero character.

## Consequence

The p24 exterior ranks are:

```text
Omega_1:    rank 158 in C,
Omega_211:  rank 210 in C^2,
Omega_3:    rank 368 in C^3.
```

For ranks this large, the exterior beta characters have full support
available.  Therefore the beta-product p-unit route is not likely to be
compressed by a small-support or low-recurrence theorem.  A proof must use
arithmetic cancellation avoidance, a Plucker-content p-unit identity, or a
class-field tower formula for the actual CM marginal vectors.

This refines the origin-product route: the product is origin-stable and
certificate-shaped, but not low-order in the beta phase for generic exterior
coordinates.

In recurrence language, a generic `Omega_3` Plucker coordinate may require all
`560` nontrivial degree-`5549` spectral factors.  That is a valid resultant
certificate surface, but not the desired asymptotic speedup.
