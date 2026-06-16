# Centered Marginal Full-Origin Borcherds Gate

Date: 2026-06-06

This note records the centered analogue of the full-origin norm bridge.

## Why This Matters

The reduced centered target is:

```text
Pi_C,right = prod_{t mod 211} Delta_C(t),
```

where `Delta_C(t)` is the cyclic right-window centered Schubert determinant.

The origin-norm power theorem from

```text
p24/centered_marginal_origin_norm_power_theorem.md
```

shows that, for `h=m*n` and `right=211`, an origin shift

```text
shift = n*alpha + m*beta
```

changes the determinant only through `alpha mod 211` up to p-units.  In the
p24 centered case the left sign is trivial because `157` is odd prime.

Therefore:

```text
prod_{alpha mod m} Delta_origin(alpha,beta)
  = p-unit * Pi_C,right^(m/211),
```

and the full-origin product over all class origins satisfies:

```text
prod_{all origins} Delta_origin
  = p-unit * Pi_C,right^(n*m/211).
```

For p24:

```text
m = 66254,
n = 3107441,
m/211 = 314,
n*m/211 = 975736474.
```

So a closed p-unit formula for the full-origin centered Chow product would
prove the 211-factor right product is a p-unit.

The power relation was checked on small actual-CM rows in:

```text
p24/centered_marginal_origin_norm_power_audit.py
```

with beta cancellation and the predicted full-origin powers matching for
right factors `7`, `7`, and `13`.

## Lean Gate

The finite handoff is checked in:

```text
p24/lean/CenteredFullOriginBorcherdsGate.lean
```

It proves:

```text
zero local intersection for psiFull
  => psiFull is a p-unit

p-unit comparison:
  psiFull -> actual full-origin centered norm

full-origin norm detects right-product zero
right product detects centered Chow zeros
centered Chow zero detects plateau Schubert bad event
  => selected centered window is good.
```

Lean also records the p24 exponent:

```text
n*m/211 = 975736474.
```

The finite payload for a genuinely closed full-origin product is only:

```text
psiFull and psiFull^{-1}: 2 base-field elements.
```

## What It Does Not Allow

This bridge does not license enumerating the full class torsor.  The class
number is:

```text
h = 205880396014,
```

which is class-number scale even though it is below `sqrt(p)` for this fixed
instance.  The goal is an asymptotic speedup, so the full-origin product is
useful only if produced by a closed modular/class-field/Borcherds/Fitting
formula.

## Arithmetic Theorem Still Missing

A successful centered full-origin theorem must construct a phase-aware
section:

```text
Psi_C,full
```

such that:

```text
Psi_C,full(CM_p24)
  = p-unit * prod_{all origins} Chow_origin(W_C,B_origin),
```

and then prove:

```text
v_p(Psi_C,full(CM_p24)) = 0
```

at the selected ordinary prime above `p = 10^24 + 7`.

The p-integral determinant-line model is:

```text
p24/centered_marginal_chow_integral_model.md
```

The local p24 arithmetic is friendly and already pinned:

```text
p24/trace_gcd_p24_local_intersection_invariants.md
```

The missing bridge is still recognition of the centered Chow divisor as the
divisor of a closed phase-aware automorphic/class-field product.
