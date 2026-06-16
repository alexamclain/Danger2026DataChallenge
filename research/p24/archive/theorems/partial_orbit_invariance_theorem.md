# Partial-Orbit Invariance Theorem

This note closes a small constructive temptation in the oriented-composite
route.  Maybe one does not need the full `H`-period

```text
sum_{h in H} j_{g h}
```

or full degree-`|H|` recovery polynomial.  Perhaps a shorter symmetric window
along the oriented composite cycle already collapses to the `G/H` quotient.

It cannot, unless the window is the whole `H`-orbit.

## Theorem

Let `H=<a>` be cyclic of order `n`, acting freely on a CM orbit.  Let

```text
S <= H
```

be a nonempty subset, and consider any unordered aggregate of

```text
{j_{g s} : s in S}
```

that is faithful to the subset as a multiset, for example its monic polynomial

```text
prod_{s in S} (X - j_{g s}).
```

If this aggregate is constant on the `H`-coset, i.e. unchanged when replacing
`g` by `g a`, then

```text
a S = S.
```

Since `a` generates `H`, this forces

```text
S = H.
```

Thus every exact subset-polynomial invariant of an `H`-coset uses either no
points or all `|H|` points.

## Proof

Changing `g` to `g a` sends the subset `S` to `aS`.  If the unordered
polynomial is unchanged and the CM roots are distinct, the underlying
multisets are equal:

```text
{j_{g s} : s in S} = {j_{g a s} : s in S}.
```

The class action is free, so this implies `S=aS`.  A nonempty subset invariant
under a transitive cyclic action is the whole orbit.

## Toy Check

I added:

```text
p24/partial_orbit_window_toy.py
```

using the calibrated `D=-5000` row.  The oriented composite move

```text
3 * 17^(-1)
```

has index `6` and orbit size `5`.  The toy computes partial window
polynomials along the oriented move.  The quotient collapse appears only at
full length:

```text
window_length=1 distinct_window_polys=30
window_length=2 distinct_window_polys=30
window_length=3 distinct_window_polys=30
window_length=4 distinct_window_polys=30
window_length=5 distinct_window_polys=6
```

## p24 Consequence

For the third trace, a short symmetric arc along

```text
2 * 463 * 223^(-1)
```

cannot be the missing quotient selector.  Any exact subset-polynomial
coordinate constant on the recovery subgroup must use all

```text
|H| = 3107441
```

CM roots in the recovery orbit.  This is the finite-set version of the
degree/support lower bound, specialized to the oriented-composite cycle.
