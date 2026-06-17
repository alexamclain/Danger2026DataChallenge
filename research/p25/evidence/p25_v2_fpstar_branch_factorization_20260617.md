# P25 v2 Fp-Star Branch Factorization

Updated: 2026-06-17

Marker: `p25_v2_fpstar_branch_factorization_rows=1/1`

## Purpose

Pin the finite-field branch arithmetic behind p25 value, power, and
root-of-unity claims. This is the small arithmetic layer under the
power/scalar ambiguity inventory and the period-156 branch contract.

It does not create a source theorem. It makes fake finite-value positives
easier to classify.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_fpstar_branch_factorization_gate.py
```

The gate returned `p25_v2_fpstar_branch_factorization_rows=1/1`.

## Factorization

```text
p = 10000000000000000000000013
p - 1 = 2^2 * 11 * 23 * 9881422924901185770751
p + 1 = 2 * 3 * 4703 * 21578093 * 16423310748511
```

Useful orders:

```text
ord_39(p) = 6
ord_507(p) = 78
ord_780(p) = 12
```

## Branch Rows

```text
n=2    kernel on F_p^* = 2   mu_n in F_p = yes  route = repair scalar/branch
n=3    kernel on F_p^* = 1   mu_n in F_p = no   route = unique power value
n=4    kernel on F_p^* = 4   mu_n in F_p = yes  route = repair scalar/branch
n=5    kernel on F_p^* = 1   mu_n in F_p = no   route = unique power value
n=6    kernel on F_p^* = 2   mu_n in F_p = no   route = repair power kernel
n=11   kernel on F_p^* = 11  mu_n in F_p = yes  route = repair scalar/branch
n=13   kernel on F_p^* = 1   mu_n in F_p = no   route = unique power value
n=22   kernel on F_p^* = 22  mu_n in F_p = yes  route = repair scalar/branch
n=39   kernel on F_p^* = 1   mu_n in F_p = no   route = unique power value
n=44   kernel on F_p^* = 44  mu_n in F_p = yes  route = repair scalar/branch
n=75   kernel on F_p^* = 1   mu_n in F_p = no   route = unique power value
n=156  kernel on F_p^* = 4   mu_n in F_p = no   route = support-period power kernel,
                                                     but support-period value
                                                     branch is unique
n=169  kernel on F_p^* = 1   mu_n in F_p = no   route = unique power value
n=507  kernel on F_p^* = 1   mu_n in F_p = no   route = unique power value
n=780  kernel on F_p^* = 4   mu_n in F_p = no   route = ambient-period power
                                                     kernel plus mu_11 debt
```

## Consequences

- Exact `R_m^3`, `R_m^5`, `R_m^13`, or `R_m^39` values remain accepted
  normalizer routes because their power maps are bijective on `F_p^*`.
- Exact `R_m^75`, `R_m^169`, or `R_m^507` values would also be uniquely
  invertible as finite-field power values, but they are not currently promoted
  as front-door asks because no source route is pinned for those outputs.
- `mu_11`, `mu_22`, and `mu_44` ambiguity is real in `F_p`; an 11th-power,
  quotient-by-`mu_11`, or ambient-period value claim is repair until it fixes
  the branch.
- A primitive order-39 scalar is not in `F_p`, even though the 39th-power map
  is bijective on `F_p^*`. This is why direct order-39-root shortcuts are
  rejected while exact `R_m^39` values are usable.
- The support-period-156 value route has unique branch behavior by the
  period-156 contract; the 156th power map itself still has a `mu_4` kernel,
  so a bare 156th-power value is not the same as a support-period theorem.

## Counts

```text
evidence_markers_ok = 4/4
unique_power_orders = 7 among checked source-relevant orders
root_groups_present = 5
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_fpstar_branch_factorization_rows=1/1
```

## Verdict

This arithmetic audit sharpens future value snippets. The usable object is an
exact finite value in a bijective power route, or a period-156 theorem with its
branch data. Ambient `mu_11`/`mu_44` language, bare 156th/780th powers, and
root-of-unity quotient language remain repair rows unless the source supplies
the missing scalar or branch.
