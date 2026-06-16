# Low-Norm Order-3107441 Search

This note records a sharper test of the correspondence zero-lemma route.

## Question

For the third p24 target, the useful recovery subgroup has

```text
n = 3107441,
m = h/n = 66254.
```

The finite-field zero lemma would certify a relative packet if we could
represent an order-`n` class by a correspondence of degree

```text
delta < m.
```

For an ideal of rational norm `N > 1`, the `X0(N)` degree is larger than `N`.
Therefore a necessary condition is an ideal representative of the desired
class index

```text
gcd(h, log(class)) = 66254
```

with rational norm at most `66254`.

## Exhaustive split-prime-power audit

I ran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/composite_split_cycle_audit.py \
  --prime-bound 66254 --max-factors 1 --max-norm 1 \
  --exhaustive-norm 66254 --show 12
```

This computes class logs for all split rational primes up to `66254`, then
enumerates signed split-prime-power products of norm at most `66254`.

Result:

```text
split_prime_logs=3270
exhaustive_signed_prime_power_products_norm_le_66254
  index_314:   hits exist
  index_422:   hits exist
  index_66254: none
```

So no split-prime-power ideal word under the required norm threshold has the
desired order `3107441`.

## Ramified-prime check

The small ramified prime in `D_K` is

```text
599.
```

I also checked it explicitly.  Its class log relative to the norm-23
generator is

```text
log(599) = 102940198007
index = 102940198007
order = 2.
```

Adding this ramified class to the exhaustive norm-`<=66254` search still gives

```text
index_66254_hits_with_599 = 0.
```

## Consequence

The current p24 order-`3107441` class representative

```text
2 * 463 * 223^(-1)
```

has norm

```text
206498
```

and `X0` index

```text
311808 = 4.706252 * 66254.
```

The low-norm audit shows this miss is not just because the earlier search was
restricted to squarefree products.  There is no split-prime-power
representative, even with the ramified genus class allowed, below the
necessary norm threshold for the zero-lemma inequality.

Thus the bounded-correspondence zero-lemma route is closed for the order
`3107441` recovery class unless one finds a correspondence whose pole degree
is substantially smaller than its `X0(N)` norm/index proxy.

## Follow-Up: Gap Below The Known Representative

I later closed the remaining visible split-prime-power gap up to the known
norm `206498`:

```text
p24/composite_split_cycle_norm_gap_206498.md
p24/composite_split_cycle_ramified_norm_gap_206498.md
```

That run computed `9265` split-prime logs below `206498` and exhaustively
enumerated signed split-prime-power products of norm at most `206497`.
It again found:

```text
index_66254: none
```

So the known representative `2 * 463 * 223^(-1)` is the first visible
order-`3107441` recovery representative in this split-prime-power model.
The ramified follow-up adds the ramified prime `599` in the widened window and
still finds no order-`3107441` representative below norm `206498`.
