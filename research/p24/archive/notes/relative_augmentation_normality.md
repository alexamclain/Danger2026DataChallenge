# Relative Augmentation Normality

The prime-resultant theorem should not be phrased as full cyclic normality of
the length-`n` fiber.

## Full Circulant Is Too Strong

For a relative fiber

```text
x_k = j_{u+m*k},
J_u(X) = sum_k x_k X^k,
```

the full circulant determinant is

```text
det(circ(x)) = product_{a=0}^{n-1} J_u(zeta_n^a)
             = J_u(1) * Res(Phi_n, J_u)      when n is prime.
```

The p24 harmful packets only use nontrivial relative characters.  Therefore
the factor

```text
J_u(1)
```

is irrelevant.  It is the quotient-period coordinate, not a relative packet.

## Toy Evidence

The diagnostic

```text
p24/relative_circulant_rank_scan.py
```

checks full circulant rank defects and separates them into:

```text
trivial_zero          J_u(1)=0
primitive_zero_count  primitive cyclotomic packet zeros
```

Small run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_circulant_rank_scan.py \
  --max-cases 20 --min-h 12 --max-h 80 --max-abs-D 12000 \
  --max-prime-quotients 3 --max-composite-quotients 3 \
  --min-n 3 --max-n 80 --q-stop 120000 --summary-only
```

Output:

```text
fiber_rows=2663
prime_fiber_rows=1781
composite_fiber_rows=882
prime_rank_defects=12
prime_primitive_zero_fibers=0
prime_trivial_zero_fibers=12
composite_primitive_zero_fibers=0
```

So even for prime `n`, full circulant normality can fail through the trivial
character while the primitive/resultant target remains clean.

A concrete sample:

```text
D=-464 q=197 h=12 m=4 n=3
trivial_zero=1
primitive_zero_count=0
rank=2/3
```

Moderate run on the same shape as the selected-origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_circulant_rank_scan.py \
  --max-cases 80 --min-h 12 --max-h 100 --max-abs-D 25000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 100 --q-stop 250000 --summary-only
```

Output:

```text
fiber_rows=13114
prime_fiber_rows=7252
composite_fiber_rows=5862
prime_rank_defects=30
composite_rank_defects=16
prime_primitive_zero_fibers=0
composite_primitive_zero_fibers=16
prime_trivial_zero_fibers=30
composite_trivial_zero_fibers=0
```

In this window the rank defects split perfectly:

```text
prime n:     only irrelevant trivial-period failures;
composite n: primitive augmentation failures.
```

## Correct Form

The right theorem is reduced/augmentation normality:

```text
Res(Phi_n, J_u) != 0 mod p.
```

Equivalently, multiplication by the fiber element is invertible on the
augmentation quotient of the group algebra, after ignoring the trivial
character.  For prime p24 recovery length

```text
n = 3107441,
```

this covers every nontrivial relative character and is exactly aligned with
the harmful-packet certificate.

Thus the current theorem target is:

```text
selected-prime p-unitness of the augmentation determinant
Res(Phi_3107441, J_u), for every 0 <= u < 66254.
```

The companion recurrence check

```text
p24/relative_fiber_recurrence_boundary.md
p24/relative_fiber_complexity_scan.py
```

finds full or near-full Berlekamp-Massey complexity in the relative fibers.
So the determinant target is not currently supported by a hidden low-order
recurrence compression; it remains a p-adic normality theorem.
