# X1(16) Split/Nonsplit Pullback Proof

Date: 2026-06-01

Purpose: record the exact mathematical transfer from the short-certificate
repo's Montgomery discriminant feature

```text
Legendre(A^2 - 4, p)
```

to the p23 `X1(16)` sampler's `y`-level nonsplit filter.

## Source Signal

The sibling repo

```text
../danger3-short-certificate-experiments
```

finds that short low-product DANGER3 certificates are enriched when

```text
Legendre(A^2 - 4, p) = 1.
```

On a Montgomery curve

```text
E_A: B*v^2 = u*(u^2 + A*u + 1),
```

the quadratic `u^2 + A*u + 1` splits over `Fp` exactly when
`A^2 - 4` is a square. Thus:

```text
split    iff chi(A^2 - 4) =  1
nonsplit iff chi(A^2 - 4) = -1
```

where `chi` is the quadratic character modulo `p`.

## X1(16) Relation

The local sampler accepts `y` values for which the quadratic

```text
(y^2 - 2y)*x^2 + (2y^2 - y^3)*x + (1 - y) = 0
```

has roots in `Fp`. Its discriminant is

```text
D16(y) = y*(y - 2)*(y^2 - 2)*(y^2 - 2y + 2).
```

The root-to-Montgomery conversion in `pomerance.c` computes `A` from such a
root `(x,y)`.

## Pullback Identity

Reducing the local `A` formula modulo the `X1(16)` quadratic relation gives:

```text
A^2 - 4 =
  ( y^2*(y - 2)^2*(y^2 - 2y + 2) / (4*(y - 1)^4) )^2
  * (y^2 - 2)*(y^2 - 4y + 2).
```

Away from the degeneracies already rejected by the sampler, the prefactor is a
nonzero square. Therefore the square class is exactly:

```text
chi(A^2 - 4) = chi((y^2 - 2)*(y^2 - 4y + 2)).
```

So the p23 sampler can classify split/nonsplit before constructing `A`:

```text
split    iff chi((y^2 - 2)*(y^2 - 4y + 2)) =  1
nonsplit iff chi((y^2 - 2)*(y^2 - 4y + 2)) = -1
```

This is implemented by `x16_y_predicts_nonsplit128` in `pomerance.c`, and the
guarded fallback binary `pomerance_nonsplit_yfilter` applies this test before
the quadratic solve for `A`.

## p23 Sign Choice

The external short-certificate frontier prefers the split side because it is
optimizing short current-verifier payloads in a low-product region.

The p23 `X1(16)` high-depth search prefers the nonsplit side. For

```text
p = 100000000000000000000117
k = 39
```

the only compatible group orders in the Hasse interval are:

```text
N40 =  99999999999678036836352, v2(N40) = 40
N39 = 100000000000227792650240, v2(N39) = 39
```

A split curve has rational 2-Sylow rank at least two, so an exact `v2 = 39`
group order cannot expose a point of order `2^39`. Split curves can only help
through the `v2 = 40` order in the skewed case `C_{2^39} x C_2`.

Nonsplit curves have cyclic rational 2-Sylow, so the deep order-`2^39` tail
naturally lives there. This explains the p23 sign reversal:

```text
external short-frontier heuristic: split
p23 X1(16) deep-halving heuristic: nonsplit
```

## Reproducible Checks

Numeric concordance check:

```bash
./scripts/audit_short_certificate_transfer.py --samples 512
```

Latest result:

```text
accepted_y = 512
roots_checked = 1024
mismatches = 0
status = PASS
```

Symbolic scratch check used for this note:

```text
reduce((A^2 - 4) / ((y^2 - 2)*(y^2 - 4y + 2))) modulo the X1(16) relation
= y^4*(y - 2)^4*(y^2 - 2y + 2)^2 / (16*(y - 1)^8),
```

which is the square of

```text
y^2*(y - 2)^2*(y^2 - 2y + 2) / (4*(y - 1)^4).
```
