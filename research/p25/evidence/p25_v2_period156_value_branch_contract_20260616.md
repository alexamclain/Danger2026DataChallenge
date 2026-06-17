# P25 v2 Period-156 Value Branch Contract

Updated: 2026-06-16

## Purpose

Promote the branch rule for value-side H0/conductor-39 theorem claims.  The
finite target is already pinned; this page says when a value theorem is usable,
when it is only repairable, and which shortcut shapes are arithmetically dead
for `p = 10^25 + 13`.

This is not a source-stage theorem.  It is a first-falsifier contract for future
paper snippets, expert answers, and value-route probes.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `archive/notes/p25_ksy_y_conductor39_degree6_value_descent_packet_20260614.md`
- `evidence/p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_period156_value_branch_contract_gate.py
```

The gate returned `p25_v2_period156_value_branch_contract_rows=1/1`.

## Arithmetic Contract

```text
p mod 39 = 23
ord_39(p) = 6
p^3 = -1 mod 39
sqrt(-39) in F_p = no
support period = 156
ambient period = 780
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
small period gcds = (39,1), (78,1), (156,1), (312,1), (507,1), (780,11)
```

Consequences:

```text
direct F_p primitive order-39 root = unavailable
sqrt(-39) scalar shortcut          = unavailable
support-period-156 value root      = unique in F_p^*
ambient-period-780 value route     = 11 branches in F_p^*
```

## Accepted Shapes

These would close source stage, subject to DANGER3 framing and extraction:

```text
divisor_additive_with_h90_source
  shape    = finite divisor/additive identity for one legal row with H90 boundary
  decision = source_stage_win_danger3_framing_missing

period156_value_with_source
  shape    = finite value identity for one legal row with support-period-156 context
  decision = source_stage_win_danger3_framing_missing
```

The divisor/additive route remains preferred because it avoids value-branch
ambiguity entirely.  The value route is viable only when the theorem itself
supplies support-period-156 branch/root/telescoping context.

## Repair Or Reject Rows

```text
ambient780_value_only
  decision = repair_ambient_period780_mu11_branch
  missing  = period-156 branch/root/telescoping context

ambient780_mu11_power_only
  decision = repair_mu11_power_or_quotient_not_value
  missing  = actual period-156 branch/root/telescoping data; an 11th power or
             mu_11 quotient does not select one F_p value

value_without_period156_context
  decision = repair_value_theorem_without_period156_context
  missing  = support-period-156 branch/root/telescoping context

degree6_orbit_no_descent
  decision = repair_degree6_orbit_without_descent
  missing  = conjugate/norm descent to F_p or Hilbert-90 ratio boundary

degree6_norm_value_no_period156
  decision = repair_value_theorem_without_period156_context
  missing  = support-period-156 branch/root/telescoping context

h90_boundary_without_value
  decision = repair_boundary_without_value_or_divisor_theorem
  missing  = finite value identity or divisor/additive theorem

finite_payload_no_source
  decision = repair_finite_payload_without_arithmetic_source
  missing  = arithmetic source theorem

direct_fp_order39_root
  decision = reject_direct_Fp_order39_root_shortcut
  falsifier = ord_39(p)=6

sqrt_minus39_scalar
  decision = reject_sqrt_minus39_scalar_shortcut
  falsifier = (-39/p)=-1
```

## Counts

```text
accepted_source_stage_shapes = 2
repair_rows = 7
rejected_shortcuts = 2
current_source_stage_closers = 0
```

## Verdict

Future value-side claims should be classified by this contract before they are
promoted:

```text
divisor/additive + H90 boundary + arithmetic source -> source-stage win
value theorem + period-156 context + arithmetic source -> source-stage win
ambient-780 value only -> repair, not a close
ambient-780 11th-power or mu_11 quotient only -> repair, not a close
degree-6 value without descent or period-156 context -> repair, not a close
direct F_p order-39 root or sqrt(-39) shortcut -> reject
```

This materially narrows the H0/conductor-39 moonshot: the remaining accepted
source-stage exits are exactly the divisor/additive row or the period-156 value
row.  No current theorem payload satisfies either row.
