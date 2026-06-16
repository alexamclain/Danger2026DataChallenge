# p25 Lane B: McCarthy Auxiliary-Prime Invariance Probe

Updated: 2026-06-13 13:23 PDT

## Result

The McCarthy exceptional delta remains stable at the target twist, but the
post-hoc q-power projection is not stable across auxiliary value primes.

For primes

```text
ell = 1 mod 2029*2028*5
```

the probe recomputed the target quotient

```text
R(138) = LHS(138) / main_sum(138)
```

using the same McCarthy Theorem 1.7 setup.

## Observed Profiles

```text
ell = 20574061, multiplier = 1, primitive_root = 2
  LHS-main = 2028
  ord(R(138)) = 79131
  ord(R(138)^2029) = 39
  R(138)^2029 in mu_39 = true
  mu_39 exponent = 5
  quotient additive exponent = 1475
  mu_5 exponent = 0

ell = 82296241, multiplier = 4, primitive_root = 38
  LHS-main = 2028
  ord(R(138)) = 10287030
  ord(R(138)^2029) = 5070
  R(138)^2029 in mu_39 = false
  mu_5 exponent = 2

ell = 144018421, multiplier = 7, primitive_root = 11
  LHS-main = 2028
  ord(R(138)) = 48006140
  ord(R(138)^2029) = 23660
  R(138)^2029 in mu_39 = false
```

## Interpretation

The stable part is the theorem hook: the exceptional McCarthy delta still
gives the same target transformed difference at `q=138`.

The unstable part is the powered quotient: `x -> x^2029` removes the additive
root component cleanly only in the minimal auxiliary field `F_20574061`.  In
larger auxiliary prime fields it leaves extra components.  That makes the
post-hoc projection look representation-specific unless a theorem supplies:

```text
1. quotient-level cancellation before projection;
2. a natural quotient modulo the extra auxiliary root components;
3. a direct endpoint identity producing U or e_138.
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_aux_prime_invariance_probe.py
```

Observed:

```text
square_axis_mccarthy_aux_prime_invariance_rows=1/1
```
