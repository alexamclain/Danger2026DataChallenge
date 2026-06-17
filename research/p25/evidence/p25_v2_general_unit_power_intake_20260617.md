# P25 v2 General Unit-Power Intake

Updated: 2026-06-17

Marker: `p25_v2_general_unit_power_intake_rows=1/1`

## Purpose

Promote the general unit-power intake rule behind the named row-power hooks.
The existing kernel names the source-relevant powers
`e in {3,5,13,39,75,169,507}`. This note records the broader finite-field
classifier for future source snippets without turning arbitrary powers into a
new search lane.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_fpstar_branch_factorization_20260617.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_general_unit_power_intake_gate.py
```

The gate returned `p25_v2_general_unit_power_intake_rows=1/1`.

## Rule

For p25,

```text
p - 1 = 2^2 * 11 * 23 * 9881422924901185770751
```

So the general unit-power intake rule is:

```text
exact finite F_p value for one labeled row R_m^e
+ arithmetic source theorem
+ row label/orientation
+ Norm_156(Y_507) boundary or accepted period-156 bridge
+ gcd(e, p - 1) = 1
=> recover R_m by inverse exponent and route through source-stage intake
```

If `gcd(e, p - 1) > 1`, the row value has root/branch/scalar debt unless the
source supplies the missing selector. A powered divisor/additive or
H90-boundary statement is not enough by itself, even when `gcd(e, p - 1) = 1`;
it still needs finite value/additive normalization before rooting.
In short: a powered divisor/additive or H90-boundary statement is not enough
without the finite payload.

## Sample Classification

Named/current unique-power hooks remain:

```text
e in {3,5,13,39,75,169,507}
```

The general rule also classifies other accidental exact row-power snippets:

```text
unique sample exponents:
  7, 9, 25, 65, 1521

ambiguous sample exponents:
  2,4,6,8,11,22,23,33,44,46,69,78,115,121,143,156,253,300,338,676,780,1014,2028,8112
```

## 23-Branch Warning

The previous named branch rows emphasized `mu_4` and `mu_11` because those are
the dominant period/value ambiguities. The full factorization adds a small but
real warning:
this is the 23-branch warning.

```text
R_m^23
kernel = 23
decision = repair unless a source supplies the selected 23rd root / branch /
           scalar normalization
```

Thus a future exact `R_m^23`, `R_m^46`, `R_m^69`, `R_m^115`, or `R_m^253`
claim is not a unique-power close. It is bounded payload data with branch debt.

## Non-Promotion Boundary

This note does not ask agents to search broadly for arbitrary powers. It only
prevents two mistakes:

```text
do not reject an exact row-labeled R_m^e theorem when gcd(e,p-1)=1;
do not promote an exact R_m^23 or other nonunit-power value without branch data.
```

Rowless powers, values up to scalar, boundary-only powered divisor statements,
and finite payloads without arithmetic source theorem remain repair/reject
rows.

## Counts

```text
unique_sample_rows = 12
ambiguous_sample_rows = 24
current_general_power_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_general_unit_power_intake_rows=1/1
```

## Verdict

Continue using the named source-relevant powers in the current theorem kernel.
For future snippets, classify exact row-labeled finite power values by
`gcd(e, p - 1)` before deciding whether they are unique-root intake or
branch-debt repair.
