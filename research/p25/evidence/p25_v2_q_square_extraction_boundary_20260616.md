# P25 v2 Q Square Extraction Boundary

Updated: 2026-06-16

## Purpose

Correctly bound what an exact Q-square finite value would buy.

The Q-square payload router showed that an exact scalar-fixed `F_p` value for
the Q diagonal plus matching pure quartic split has only two square roots. This
is useful, but it is not automatically an operational DANGER3 payload:
`vpp.py` verifies `(p,A,x0)`, not a modular-unit row value.

So the right boundary is:

```text
exact Q-square value -> two row-value roots
two row-value roots -> still need DANGER3 extraction map
```

The missing map can be supplied by the usual downstream ladder: DANGER3
framing, same-j `X_1(8112)`, practical `X_1(16)` payload, and halving/direct
`x0`, or by a direct map from the row roots to concrete `(A,x0)` candidates.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_extraction_payload_contract_20260616.md`
- `evidence/p25_v2_extraction_minimal_hook_20260616.md`
- `evidence/p25_v2_post_theorem_extraction_router_20260616.md`
- `evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_square_extraction_boundary_gate.py
```

The gate returned `p25_v2_q_square_extraction_boundary_rows=1/1`.

## Boundary Rows

```text
q_square_exact_fp_value_only
  decision = repair_extraction_map_missing_after_two_root_row_payload
  meaning  = exact square value gives two modular-unit row-value roots
  missing  = DANGER3 framing plus same-j/X_1(16)/halving or direct A,x0 map

q_square_roots_plus_same_j_x16_map
  decision = route_mapped_roots_through_extraction_payload_contract
  meaning  = row roots are linked to the same-j / X_1(16) ladder
  missing  = halving chain, direct x0, or vpp.py depending on supplied map

q_square_roots_plus_direct_A_x0
  decision = extraction_ready_vpp_missing
  meaning  = row roots have been mapped to concrete A,x0 candidates
  missing  = official src/vpp.py verification for each concrete candidate

q_square_value_up_to_scalar
  decision = repair_scalar_and_root_orientation_missing
  missing  = specified scalar before even the two row roots are concrete

direct_vpp_on_row_value
  decision = reject_vpp_requires_A_x0_not_row_value
  falsifier = vpp.py verifies (p,A,x0), not a modular-unit row value
```

## Counts

```text
evidence_markers_ok = 5/5
row_value_payload_rows = 3
extraction_ready_rows = 1
submission_ready_rows = 0
repair_rows = 2
reject_rows = 1
current_extraction_ready_rows = 0
current_submission_ready_rows = 0
p25_v2_q_square_extraction_boundary_rows=1/1
```

## Verdict

Do not say that exact Q-square value data gives two DANGER3 candidates. It
gives two row-value roots. That is a much smaller search object, and it may be
a useful hook for extraction, but it still needs an explicit extraction map
before `vpp.py` can test anything.

Accepted phrasing:

```text
exact scalar-fixed Q-square value gives two row roots; extraction map missing
```

Rejected phrasing:

```text
exact scalar-fixed Q-square value gives two vpp.py candidates
```
