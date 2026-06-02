# CM Exact-Trace Audit

Date: 2026-06-01

Purpose: decide whether exact-trace CM construction can plausibly construct a curve over

```text
p = 100000000000000000000117
```

with one of the two p23 target traces.

## Target Traces

```text
t0 =  321963163766
t1 = -227792650122
```

For CM, the relevant discriminant equation is:

```text
t^2 - 4p = D * f^2
```

where `D` is a negative fundamental discriminant and `f` is the conductor.

Equivalently:

```text
4p - t^2 = |D| * f^2
```

## Factor Audit

Commands:

```bash
factor 296339721177787864697712 348110508550396093385584
openssl prime -checks 128 6173744191203913847869
openssl prime -checks 128 481741841427711973
```

Results:

```text
t = 321963163766:
  4p - t^2 = 296339721177787864697712
             = 2^4 * 3 * 6173744191203913847869

  6173744191203913847869 is prime

t = -227792650122:
  4p - t^2 = 348110508550396093385584
             = 2^4 * 19 * 2377 * 481741841427711973

  481741841427711973 is prime
```

Both odd parts are squarefree and congruent to `3 mod 4`:

```text
18521232573611741543607 mod 4 = 3
21756906784399755836599 mod 4 = 3
```

Therefore:

```text
t = 321963163766:
  fundamental discriminant D = -18521232573611741543607
  conductor f = 4

t = -227792650122:
  fundamental discriminant D = -21756906784399755836599
  conductor f = 4
```

There is no hidden large square factor. The only square conductor factor is `4^2 = 16`.

## Class-Number Scale

Square-root scale:

```text
sqrt(18521232573611741543607) ~= 1.36092735198e11
sqrt(21756906784399755836599) ~= 1.47502226371e11
```

The class number for an imaginary quadratic fundamental discriminant is on the order of

```text
sqrt(|D|) * L(1, chi_D) / pi
```

up to the usual analytic factor. The exact value is not needed for this decision: with `sqrt(|D|)` already around `1e11`, the class polynomial degree is far outside the practical range for this challenge.

## Decision

Exact-trace CM is a no-go for this p23 target.

Reason:

```text
The target traces force huge fundamental discriminants, not merely huge nonfundamental discriminants with a large conductor square.
```

This rules out:

```text
ordinary Hilbert class polynomial CM
CRT-CM as a practical workaround
small-CM j-invariant families
GLV/special-endomorphism families
```

CM should remain on the shortlist for future p values only when `4p - t^2` has a large square factor leaving a small fundamental discriminant.

Primary reference:

```text
Reinier Broker and Peter Stevenhagen,
"Constructing elliptic curves of prime order",
https://arxiv.org/abs/0712.2022
```
