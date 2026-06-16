# Trace-GCD p24 Local-Intersection Invariants

Date: 2026-06-06

This note records the exact p-local arithmetic facts that any
trace-GCD Borcherds/Fitting/local-intersection proof must use for the current
third-trace p24 target.

The audit script is:

```text
p24/trace_gcd_p24_local_invariants.py
```

## Target Data

```text
p = 1000000000000000000000007 = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
|D_K| = 599 * 1089874116562502921057
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441
right = 211
```

The trace discriminant identity is exact:

```text
t^2 - 4p = 4D_K.
```

Equivalently:

```text
Norm(t/2 + sqrt(D_K)) = p.
```

For this target:

```text
t/2 = -589207437308
(t/2)^2 - D_K = p.
```

## Prime Above p

The prime `p` is split and unramified in `K = Q(sqrt(D_K))`:

```text
Kronecker(D_K,p) = 1
p does not divide D_K.
```

The two residue embeddings are explicit:

```text
sqrt(D_K) =  t/2 mod p
sqrt(D_K) = -t/2 mod p.
```

Numerically:

```text
 t/2 mod p  = 999999999999410792562699
-t/2 mod p  = 589207437308
```

Both square to `D_K mod p`.

This is useful because a future p-adic or Borcherds proof should not leave the
prime above `p` as an abstract label.  The selected ordinary embedding can be
checked against one of these two square-root orientations.

## Prime-To-p Levels

All finite certificate levels are p-units:

```text
gcd(p,2) = 1
gcd(p,157) = 1
gcd(p,211) = 1
gcd(p,66254) = 1
gcd(p,3107441) = 1
gcd(p,205880396014) = 1
```

Thus denominator problems in a p-integral determinant-line model cannot be
blamed on these levels.  The missing theorem is genuine nonintersection or
p-unitness, not level ramification at `p`.

## Frobenius Orbits

The finite right-orbit data is:

```text
p mod 211 = 114
ord_211(p) = 35
right orbit lengths = 1 plus six orbits of length 35.
```

The other relevant orders are:

```text
ord_157(p) = 156
ord_3107441(p) = 388430
ord_157*211(p) = 5460
```

This matches the seven orbit-product payload and explains why a base-field
right polynomial is not available without a twisted/split algebra.

## Ray-Kernel Warning

For the odd quotient layers:

```text
Kronecker(D_K,157) = -1
Kronecker(D_K,211) = -1
```

and:

```text
|(O_K/157)^*| = 157^2 - 1 = 24648
|(O_K/211)^*| = 211^2 - 1 = 44520.
```

Neither has an `ell`-primary factor for its own `ell`.  The `157` and `211`
class factors are unramified Hilbert-class layers, not ray-kernel layers that
can be collapsed by ordinary distribution relations.

## Consequence For The Missing Theorem

The p-local side of a successful theorem should now look like:

```text
1. construct the actual phase-aware Chow/Fitting/Borcherds section;
2. compare its CM value to the trace-GCD determinant section up to p-units;
3. choose one of the two explicit square-root orientations above;
4. prove the pulled-back Chow divisor has zero local intersection with the
   p24 CM point at that ordinary prime above p;
5. conclude the relevant orbit/global/full-origin norm is a p-unit.
```

The local arithmetic is friendly: split ordinary, unramified, and prime to all
certificate levels.  What remains hard is recognizing the determinant divisor
itself.  These invariants make a proposed local-intersection proof checkable;
they do not supply the missing divisor.

The resulting ordinary Fitting criterion is stated in:

```text
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
```

The companion semilinear descent note is:

```text
p24/trace_gcd_semilinear_descent_frontier.md
```

It records why principal Hilbert Frobenius at `p` does not imply an ordinary
base-polynomial determinant: the unramified CM torsor is fixed, while the
`157/211` cyclotomic phase coordinates still have Frobenius orders `156` and
`35`.
