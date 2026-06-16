# Relative Fiber Recurrence Boundary

The augmentation determinant

```text
Res(Phi_n, J_u)
```

would become computationally tractable without enumerating the order-`n`
fiber if the sequence

```text
j_u, j_{u+m}, ..., j_{u+m(n-1)}
```

had a short linear recurrence.  This note records a toy-scale check that it
does not.

## Diagnostic

I added:

```text
p24/relative_fiber_complexity_scan.py
```

It measures Berlekamp-Massey complexity of relative fibers and records
primitive packet zeros on the same rows.

Small run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_fiber_complexity_scan.py \
  --max-cases 8 --min-h 12 --max-h 60 --max-abs-D 8000 \
  --max-prime-quotients 3 --max-composite-quotients 3 \
  --min-n 3 --max-n 60 --q-stop 80000 \
  --max-shifts 4 --summary-only
```

Output:

```text
fiber_rows=304
prime_fiber_rows=184
composite_fiber_rows=120
prime_full_or_near_full_bm=184
composite_full_or_near_full_bm=120
prime_low_bm=0
composite_low_bm=0
```

Moderate run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_fiber_complexity_scan.py \
  --max-cases 80 --min-h 12 --max-h 100 --max-abs-D 25000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 100 --q-stop 250000 \
  --max-shifts 4 --summary-only
```

Output:

```text
fiber_rows=2636
prime_fiber_rows=1464
composite_fiber_rows=1172
prime_full_or_near_full_bm=1464
composite_full_or_near_full_bm=1172
prime_low_bm=0
composite_low_bm=0
prime_primitive_zero_fibers=0
composite_primitive_zero_fibers=4
```

The `min_bm_over_n` values can be below `1` only because "near-full" for
small `n` means `bm=n-1`, e.g. `2/3` for `n=3`.  There is no actual short
recurrence signal in this window.

## Consequence

The augmentation determinant does not appear compressible by a bounded or
small linear recurrence of the relative fiber.  The surviving theorem target
remains p-adic/normality:

```text
prove selected-prime p-unitness of Res(Phi_3107441, J_u),
```

not compute the determinant by a hidden low-order recurrence.

The stronger packet-factor shape check in

```text
p24/relative_packet_factor_vanishing_shape.md
p24/relative_packet_factor_shape_scan.py
```

confirms the same boundary from the opposite direction.  Actual small-CM
coordinate-zero failures for composite `n` also have full/near-full
Berlekamp-Massey complexity and no proper period.  So even when
`J_u mod f = 0` occurs, it need not reveal a short recurrence that could be
recognized or excluded cheaply.
