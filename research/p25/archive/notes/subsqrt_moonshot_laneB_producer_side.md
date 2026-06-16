# Subsqrt Moonshot Lane B Producer-Side Gates

Date: 2026-06-12

## Result

The p24 producer-side scaffolding ports cleanly to the p25 negative-trace
right-3 quotient targets.  This checkpoint still does not construct the
selected weighted packet `Y[e]`; it proves that if arithmetic supplies such a
packet through a multiplicative product formula and unramified quotient
selector, the finite gates are compatible with the p25 packet contract.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_producer_side_gates.py
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_axis_source_audit.py
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_literal_jacobi_packet_model.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_producer_side_gates.py
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_axis_source_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_literal_jacobi_packet_model.py
```

Observed:

```text
multiplicative_dictionary_rows=3/3
single_anchor_fingerprint_rows=3/3
unramified_selector_rows=3/3
conclusion=reported_p25_laneB_producer_side_gates
conclusion=reported_p25_laneB_axis_source_audit
conclusion=reported_p25_laneB_literal_jacobi_packet_model
```

## Gates Ported From p24

### 1. Multiplicative Dictionary

The p25 raw additive target

```text
g(r,0)+g(-r,0)=A0
g(r,c)+g(-r,-c)=A1, c != 0
sum_c g(r,c)-c*g(r,0)=B
```

is equivalent, in finite cyclic tori, to the multiplicative product-formula
target:

```text
U(r,0)U(-r,0)=alpha0
U(r,c)U(-r,-c)=alpha1, c != 0
prod_c U(r,c)/U(r,0)^c = beta
```

The script verifies this for:

```text
C_3 x C_13
C_3 x C_53
C_3 x C_169
```

with random equivalence checks, forced-product hits, and controls separating
pair-product constancy from selected row-ratio constancy.

### 2. Single Anchor Fingerprint

The p24 single degenerate-anchor correction ports as a finite fingerprint:

```text
raw correction = -e_(0,0)
selected defect = punctured right-zero row
```

For all three p25 axes, the anchor has the expected support and right-difference
profile:

```text
C_3 x C_13:  support 12/12
C_3 x C_53:  support 52/52
C_3 x C_169: support 168/168
```

As in p24, the anchor alone is not the full value identity.  It forces the
`C`-zero selected-defect behavior but still fails row-sum independence and
inversion-complement constancy.  Therefore the p25 producer must supply both:

```text
punctured product formula + selected anchor normalization
```

not just an isolated anchor.

### 3. Unramified Selector

For each p25 target, a full cyclic unramified character on the raw `rho` cycle
would descend exactly to the post-`B` quotient:

```text
tiny_C3xC13:
  raw_order = 12675
  B = 325
  quotient = 39
  twist_order = 39
  right_axis_order = 3
  c_axis_order = 13
  rho = (rho^13)^1 * (rho^3)^9 mod B

prime_axis_C3xC53:
  raw_order = 3975
  B = 25
  quotient = 159
  twist_order = 159
  right_axis_order = 3
  c_axis_order = 53
  rho = (rho^53)^2 * (rho^3)^18 mod B

square_axis_C3xC169:
  raw_order = 12675
  B = 25
  quotient = 507
  twist_order = 507
  right_axis_order = 3
  c_axis_order = 169
  rho = (rho^169)^1 * (rho^3)^113 mod B
```

In every case:

```text
quotient character exponents are exactly the B-trace survivors;
the coordinate exponents cover the quotient;
axis values determine the quotient character;
the unramified twist supplies the selector but not the embedded packet.
```

## Consequence

The finite producer side is no longer the obstacle.  The remaining missing
arithmetic object is sharply:

```text
an embedded p25 selected weighted packet Y[e] on the negative trace,
compatible with the raw rho cycle and the product-formula/anchor selector.
```

The local source audit makes the coupling target more explicit:

```text
tiny_C3xC13:
  n = 2^3 * 3 * 151 * 677
  mod 151 has ord(rho)=75=3*5^2; B=325 kills 5^2 and leaves right C_3
  mod 677 has ord(rho)=169=13^2; B=325 kills one 13 and leaves C_13

prime_axis_C3xC53:
  n = 2 * 3 * 7 * 17 * 107 * 151
  mod 107 has ord(rho)=53 and supplies C_53
  right C_3 is visible on both mod 7 and mod 151 after B=25

square_axis_C3xC169:
  n = 2^3 * 3 * 151 * 677
  mod 151 has ord(rho)=75=3*5^2; B=25 kills 5^2 and leaves right C_3
  mod 677 has ord(rho)=169 and supplies C_169
```

So the first packet-construction attempt should focus on the `151 x 677`
coupling for `C_3 x C_13`, with the `B=325` trace killing the unwanted
`5^2` and one `13` layer.

## Literal Carry Model

The follow-up artifact:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_literal_packet_model.md
```

shows that admissible Jacobi-carry divisors can be inflated into the exact raw
`Y[e]` contract:

```text
Y[c*r + 3*k + 3*c*j] = B^(-1) * theta_{u,v}(r,k)
g(r,k) = theta_{u,v}(r,k)
```

and then pass the selected-defect value identities exhaustively for
`C_3 x C_13` and `C_3 x C_53`.  The naive additive "carry plus single anchor"
does not pass; the embedded p25 packet should model the reduced product-formula
divisor as a whole.

The first executable falsifier remains:

```text
g(r,c)=sum_{j=0}^324 Y[13*r + 3*c + 39*j mod 12675]
f(r,c)=g(r,c)-g(r,0)
```

Then test:

```text
f(r,0)=0
sum_c f(r,c) independent of r
f(r,c)+f(-r,-c) constant for c != 0
```

## Continue / Kill Rule

Continue Lane B only by attacking the embedded packet construction:

- find a CM/Lang/Jacobi ratio whose unramified Artin coordinate is the selector
  above;
- prove the ratio supplies the punctured product formula plus selected anchor;
- or build a faithful small analogue with this exact right-3 contract and a
  non-enumerative selected packet.

Do not spend more effort on quotient arithmetic alone.  That part now passes.
