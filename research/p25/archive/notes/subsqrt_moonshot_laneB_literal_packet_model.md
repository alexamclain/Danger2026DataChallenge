# Subsqrt Moonshot Lane B Literal Packet Model

Date: 2026-06-12

## Result

The exact p25 Lane B raw packet contract admits a literal Jacobi-carry divisor
model.  This is still not the embedded p25 CM packet, but it is the first
working `Y[e]` model that flows through the p25 contract and lands in the
selected-defect value identities.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_literal_jacobi_packet_model.py
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_local_pullback_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_literal_jacobi_packet_model.py
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_local_pullback_gate.py
```

Observed:

```text
tiny_C3xC13:
  pairs_checked = 264, exhaustive = 1
  raw_trace_roundtrips = 264/264
  carry_value_identity_hits = 264/264
  reduced_anchor_value_identity_hits = 0/264

prime_axis_C3xC53:
  pairs_checked = 5304, exhaustive = 1
  raw_trace_roundtrips = 5304/5304
  carry_value_identity_hits = 5304/5304
  reduced_anchor_value_identity_hits = 0/5304

square_axis_C3xC169:
  pairs_checked = 4, exhaustive = 0
  raw_trace_roundtrips = 4/4
  carry_value_identity_hits = 4/4
  reduced_anchor_value_identity_hits = 0/4

conclusion=reported_p25_laneB_literal_jacobi_packet_model
conclusion=reported_p25_laneB_local_pullback_gate
```

## Model

For `N = 3*c`, use an admissible Jacobi carry

```text
theta_{u,v}(t) = [u*t]_N + [v*t]_N - [(u+v)*t]_N
```

where:

```text
u = 3*s, s != 0 mod c
v is right-mixed
v is C-nontrivial
u+v is C-nontrivial
u+v != 0 mod N
```

Inflate it into the exact p25 raw cycle by distributing the post-`B` trace
uniformly over the `B` entries of each block:

```text
Y[c*r + 3*k + 3*c*j] = B^(-1) * theta_{u,v}(r,k)
g(r,k) = sum_j Y[c*r + 3*k + 3*c*j] = theta_{u,v}(r,k)
f(r,k) = g(r,k) - g(r,0)
```

The selected defect `f` satisfies:

```text
f(r,0)=0
sum_k f(r,k) is independent of r
f(r,k)+f(-r,-k) is constant for k != 0
```

exhaustively for the first two practical p25 axes `c=13` and `c=53`.

## Important Negative Control

Naively adding the single-anchor correction `-e_(0,0)` to this additive carry
breaks the value identities:

```text
reduced_anchor_profiles = {(c_zero=1, row_sums=0, inversion=0, all=0)}
```

This reconciles two earlier facts:

- The multiplicative literal Jacobi packet needs a degenerate-anchor
  normalization to repair product formulas.
- The additive/divisor carry model already has the value-side selected-defect
  identities; the anchor is not an extra additive row to be blindly added to
  the carry.

Therefore the embedded p25 `Y[e]` should model the reduced product-formula
divisor as a whole, not "carry plus anchor" as two independent additive
patches.

## Consequence

Lane B has a concrete mathematical packet shape now:

```text
Y[e] should be an embedded p25 specialization of an admissible C-axis
Jacobi-carry divisor on the 151 x 677 source coupling for C_3 x C_13.
```

The local pullback artifact:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_local_pullback.md
```

checks that this `Y[e]` factors through the actual local source coordinates.
For the first target:

```text
right_visible = log_151(rho^e) mod 3
r = right_visible
k = 9 * (log_677(rho^e) mod 13) mod 13
Y[e] = B^(-1) * theta_{u,v}(r,k)
```

The next hard step is no longer finite quotient algebra.  It is the arithmetic
embedding:

```text
map the p25 negative-trace CM/Lang or modular-unit object onto this carry
divisor without enumerating the full class set.
```

First falsifier remains: if an actual embedded `Y[e]` for the `151 x 677`
coupling is produced and its selected defect fails the `C_3 x C_13` value
identities, kill Lane B.
