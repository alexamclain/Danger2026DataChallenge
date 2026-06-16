# Subsqrt Moonshot Lane B Local Pullback

Date: 2026-06-12

## Result

The literal Jacobi-carry packet model factors through the actual p25 local
source coordinates identified for the negative trace.  This is the strongest
Lane B checkpoint so far: the working quotient-level `Y[e]` model is not just
formal in `C_3 x C_c`; it can be pulled back from the local factors that survive
the `B` trace.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_local_pullback_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_local_pullback_gate.py
```

Observed:

```text
tiny_C3xC13:
  coordinate_hits = 12675/12675
  B_block_coordinate_constancy = 39/39
  local_pair_hits = 264/264
  Y_pullback_hits = 264/264
  B_trace_hits = 264/264

prime_axis_C3xC53:
  coordinate_hits = 3975/3975
  right_source_agreement = 3975/3975
  B_block_coordinate_constancy = 159/159
  local_pair_hits = 5304/5304
  Y_pullback_hits = 5304/5304
  B_trace_hits = 5304/5304

square_axis_C3xC169:
  coordinate_hits = 12675/12675
  B_block_coordinate_constancy = 507/507
  local_pair_hits = 4/4
  Y_pullback_hits = 4/4
  B_trace_hits = 4/4

local_pullback_rows = 3/3
conclusion=reported_p25_laneB_local_pullback_gate
```

## Coordinate Maps

Let `e` be the raw `rho` exponent.  The post-`B` quotient coordinate is always:

```text
e == c_axis*r + 3*k mod 3*c_axis
```

The local pullback recovers `(r,k)` from discrete logs in the local source
factors.

### `C_3 x C_13`

Source:

```text
mod 151: ord(rho)=75=3*5^2, B=325 kills 5^2 and leaves right C_3
mod 677: ord(rho)=169=13^2, B=325 kills one 13 and leaves C_13
```

Coordinates:

```text
right_visible = log_151(rho^e) mod 3
r = right_visible
k = 9 * (log_677(rho^e) mod 13) mod 13
```

The first embedding target is therefore a `151 x 677` local pullback.

### `C_3 x C_53`

Source:

```text
mod 107: ord(rho)=53 and supplies C_53
mod 7 and mod 151: both see the same right C_3 coordinate after B=25
```

Coordinates:

```text
right_visible = log_7(rho^e) mod 3 = log_151(rho^e) mod 3
r = 2 * right_visible mod 3
k = 18 * (log_107(rho^e) mod 53) mod 53
```

This row is cleaner on the C-axis but has two visible right-axis sources.

### `C_3 x C_169`

Source:

```text
mod 151: ord(rho)=75=3*5^2, B=25 kills 5^2 and leaves right C_3
mod 677: ord(rho)=169 and supplies C_169
```

Coordinates:

```text
right_visible = log_151(rho^e) mod 3
r = right_visible
k = 113 * (log_677(rho^e) mod 169) mod 169
```

## Pullback Formula

For an admissible Jacobi carry `theta_{u,v}` on `C_3 x C_c`, the raw local
packet is:

```text
Y[e] = B^(-1) * theta_{u,v}(r(e), k(e))
```

where `(r(e),k(e))` is recovered from the local coordinates above.

Then:

```text
g(r,k) = sum_j Y[c*r + 3*k + 3*c*j] = theta_{u,v}(r,k)
f(r,k) = g(r,k) - g(r,0)
```

The script checks this for every raw `e`, every `B` block, and every admissible
carry for `C_3 x C_13` and `C_3 x C_53`.

## Consequence

The missing embedded packet is now sharply localized:

```text
construct a p25 CM/Lang or modular-unit specialization whose local discrete-log
pullback is the Jacobi carry on the 151 x 677 source coupling.
```

This is no longer a quotient arithmetic problem.  The finite quotient,
producer, literal carry, and local pullback gates all pass.  The next
mathematical step is to identify the arithmetic object that realizes this
local pullback in the actual negative-trace class-field setting without full
class-set enumeration.

The follow-up footprint gate records one more constraint on that object:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_divisor_footprint.md
```

The raw Jacobi-carry divisor has a nonzero scalar character component.  Once
that scalar is removed, the divisor is degree-zero and row-balanced, but it
remains genuinely mixed across the local sources.  So the first embedding
falsifier is not just "find local units"; it is:

```text
global scalar/polar normalization + coupled 151 x 677 local divisor footprint
```
