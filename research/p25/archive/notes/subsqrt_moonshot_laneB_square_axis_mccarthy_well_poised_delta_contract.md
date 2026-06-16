# Subsqrt Moonshot Lane B McCarthy Well-Poised Delta Contract

Date: 2026-06-13

## Result

The Barnes/Greene scout found a concrete finite-field hypergeometric source
for a point-delta correction: McCarthy's well-poised transformation has an
exceptional term containing a character delta

```text
delta(A_0^-1 * A_{n-1} * A_n)
```

In `C_507` exponent notation this is a single linear condition.  Choosing

```text
a_0 - a_{n-1} - a_n = 138 mod 507
```

makes the pre-closure correction support exactly the live seed point `q=138`,
and the outer `S` image is exactly:

```text
{138,310,482}
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_well_poised_delta_contract_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_well_poised_delta_contract_gate.py
```

Observed:

```text
delta_support = (138,)
outer_s_image = (138,310,482)
order3_support_size = 169
p2_multiplier = 373
p2_orbit_length = 39
p2_orbit_outer_s_support_size = 117
square_axis_mccarthy_well_poised_delta_contract_rows=1/1
```

## Consequence

This revives the Barnes/Greene/McCarthy route as a precise point-delta producer
candidate.  It is stronger than the killed order-3-only HP product deltas
because it can impose a full `C_507` character equation before orbit closure.

This is not yet a numerical hypergeometric verification.  The next falsifier is
to instantiate the McCarthy transformation over a field with order-507
characters, such as `F_2029`, and check:

```text
support(LHS - transformed_main_sum) = {138}
S({138}) = {138,310,482}
```

Kill condition:

```text
the transformed difference leaks outside q=138 before S
the lower-order hypergeometric factor vanishes identically at the seed
the exceptional term collapses to the killed order-3-only support
the correction is forced closed under the full p^2 orbit before selection
```
