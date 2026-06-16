# L1 Interpolation-Shape Boundary

This note records a cheap diagnostic for the remaining embedded finite-field
identity route for

```text
L1 = M0 + P2 + P157 + P211.
```

The question is whether the selected-origin packet norm of `L1` looks like a
low-degree rational function of the selected CM root `j_i`.  A strong positive
signal would be a rational degree well below the generic finite-set
interpolation threshold `floor(h/2)`, stable across packets or split primes.

## Diagnostic

I added:

```text
p24/l1_interpolation_shape_scan.py
```

For a small split CM cycle, quotient `h=m*n`, and packet factor
`f | Phi_n`, it rotates the selected origin and computes

```text
N_i = Res(f, L1_f(origin=i)) mod q.
```

It then measures:

```text
polynomial degree of j_i -> N_i,
bounded rational degree below floor(h/2),
whether the packet norm is H-periodic,
random controls preserving H-periodicity when present.
```

The generic threshold matters.  A rational relation first appearing at degree
`floor(h/2)` is just interpolation on `h` points, not a theorem primitive.

## Pinned M0 Failure

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_interpolation_shape_scan.py \
  --only-D -899 --min-h 12 --max-h 20 \
  --q-start 281 --q-stop 282 --include-linear \
  --max-prime-quotients 3 --max-composite-quotients 3 \
  --min-n 3 --max-n 10 --max-rational-degree 4 \
  --random-trials 4 --random-combos 4 --max-rows 20
```

The known `M0` failure appears as a constant-zero packet norm:

```text
scalar=M0
zero_norms=14
distinct_norms=1
poly_degree=0
first_low_rational=0
```

For the same row, `L1` shows no low-degree structure:

```text
scalar=L1
zero_norms=0
distinct_norms=14
poly_degree=13
random_poly_range=[13,13]
rational_threshold=7
first_low_rational=None
```

So `L1` rescues the structural `M0` cancellation, but it does not do so by
becoming a simple low-degree function of `j`.

## Composite-m Stress Window

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_interpolation_shape_scan.py \
  --max-cases 6 --min-h 12 --max-h 70 --max-abs-D 16000 \
  --max-prime-quotients 0 --max-composite-quotients 3 \
  --min-n 3 --max-n 60 --q-stop 90000 \
  --max-splitting-primes 1 --include-linear --require-composite-m \
  --max-rational-degree 5 --random-trials 4 --random-combos 4 \
  --max-rows 12
```

All six displayed rows had

```text
h=60, m=15, n=4, deg(f)=2, components=[3,5].
```

The `M0` packet norm was constant:

```text
distinct_norms=1
poly_degree=0
first_low_rational=0
```

The `L1` packet norm was `H`-periodic, as expected for a nonlinear packet
norm, but otherwise generic:

```text
H_period_ok=1
distinct_norms=15
poly_degree=59
random_poly_range=[59,59]
rational_threshold=30
search_limit=5
first_low_rational=None
random_low_hits=0/4
```

Summary:

```text
rows=12
m0_rows=6
l1_rows=6
rows_with_low_rational_degree=6
l1_rows_with_low_rational_degree=0
l1_rows_with_H_period_ok=6
l1_zero_norms=0
max_l1_poly_degree=59
```

## Interpretation

The finite-field identity route is not killed, but it cannot currently be a
simple one-variable rational identity in the selected `j` root.

The data separates the scalars:

```text
M0:
  quotient-field/global phase erasure is visible as constant packet norms,
  but M0 has structural zero failures;

L1:
  selected-origin failures were not found,
  but the origin dependence looks generic after the known H-periodicity.
```

Thus a successful `L1` theorem still has to prove selected-origin p-unitness
or construct a higher-dimensional/phase-aware embedded identity.  The new
diagnostic gives no support for a cheap plain-`j` selector.
