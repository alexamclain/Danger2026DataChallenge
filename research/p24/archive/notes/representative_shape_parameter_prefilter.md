# Representative Shape Parameter Prefilter

Date: 2026-06-05

This note records a cheap orbit-arithmetic prefilter for small analogues of
the p24 representative determinant.

## p24 Shape

For the live p24 representative row:

```text
p = 10^24 + 7
p mod 157 = 21
p mod 211 = 114
ord_157(p) = 156
ord_211(p) = 35
(211-1)/35 = 6 right orbits
156 = 4*35 + 16
```

Thus the one-punit determinant keeps:

```text
4 full right packets + 16 tail coordinates.
```

## Prefilter

Added:

```text
p24/representative_shape_parameter_prefilter.py
```

It searches small prime bases `q` and prime moduli `(left,right)` for the
same delete-one geometry:

```text
right_orbit_count = 6,
floor(ord_left(q)/ord_right(q)) = 4,
ord_left(q) mod ord_right(q) > 0,
gcd(ord_left(q), ord_right(q)) = 1.
```

This is intentionally arithmetic-only.  It avoids class polynomial and CM
packet extraction until the orbit dimensions are promising.

## Output

Command:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_shape_parameter_prefilter.py \
  --max-q 31 --max-modulus 400 --limit 40
```

reported `76` hits.  The first and most important one is:

```text
q=5 left=157 L=156 right=211 R=35 right_orbits=6
shape=4*R+16 exact_p24_moduli=1
```

Filtering for the exact p24 tail length:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_shape_parameter_prefilter.py \
  --max-q 31 --max-modulus 400 --tail 16 --limit 20
```

reported:

```text
q=5  left=157 L=156 right=211 R=35 shape=4*R+16
q=13 left=313 L=156 right=211 R=35 shape=4*R+16
q=31 left=197 L=196 right=271 R=45 shape=4*R+16
```

So `q=5` gives the exact same `157/211` orbit dimensions and the exact same
`4*35+16` leading-erasure geometry as p24.

## Random Control At Same Dimensions

The random linear control at `q=5` and p24 dimensions:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_kernel_cs_boundary_audit.py \
  --q 5 --right-degree 35 --tail-dim 16 --trials 8 --max-enumerate 1000
```

reported:

```text
prefix_full=8/8
determinant_full=7/8
prefix_full_tail_fail=1/8
kernel_dim_hist={16:8}
shift_stable_counts={1:0, 2:0, 4:0}
```

This is just a random baseline.  It says the p24-shaped determinant is
generically nonzero over a modest field, but still not formal.

## Consequence For Theorem Search

This prefilter gives a useful discipline:

```text
Any proposed proof using only the 157/211 orbit geometry should have a
q=5 same-shape analogue.
```

If an identity is supposed to be universal in the cyclotomic/orbit data, it
should be testable or at least well-defined in this `q=5` model.  If the proof
uses the actual p24 CM class-field embedding or selected-prime p-unit
arithmetic, that dependence must be explicit.

The prefilter does not replace the missing theorem.  It narrows the next
search:

```text
look for a class-field norm/resultant formula for L_rep whose nonvanishing is
not merely generic orbit arithmetic, but a selected p24 p-unit statement.
```
