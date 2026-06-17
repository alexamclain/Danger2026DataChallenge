# P25 v2 Q Square Payload Router

Updated: 2026-06-16

## Purpose

Separate the source-theorem requirement from the practical payload consequence
of the Q split route.

The Q split quartic-selector screen shows that the Q diagonal aggregate plus
the matching pure quartic split recovers twice one legal edge:

```text
(Q diagonal) + (matching Q split) = 2*edge
```

That is not a source-stage close by itself, because a square has two roots and
the sign is invisible to divisor, Hilbert-90 boundary, and exponent-character
data. If a source theorem gives an exact scalar-fixed finite `F_p` value for
that square, the row-value consequence is small: compute the two square roots.
Those are row-value roots, not `vpp.py` candidates.

So the Q square route is not promoted to a theorem close, but it is no longer
just a vague "root missing" blocker. It has a precise two-root row-value
payload row when the exact finite value is present, and a separate extraction
map is still required before anything can be verified by `vpp.py`.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_coefficient6_root_normalization_20260616.md`
- `evidence/p25_v2_extraction_payload_contract_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_square_payload_router_gate.py
```

The gate returned `p25_v2_q_square_payload_router_rows=1/1`.

## Root Invariants

For `p = 10^25 + 13`:

```text
p mod 4 = 1
p is odd = yes
square root kernel size in F_p^* = 2
modular-unit values live in F_p^*
constant sign is invisible to divisor/H90/phase data
```

The sign invisibility is the same obstruction as before:

```text
(-R)^2 = R^2
(-1) / Frob_p(-1) = 1
```

Thus divisor language, Hilbert-90 boundary language, and quotient-`C4`
character language cannot choose `R` over `-R`.

## Routes

```text
q_square_exact_fp_value
  decision = repair_extraction_map_missing_after_two_root_row_payload
  meaning  = compute both F_p row-value roots
  missing  = DANGER3 framing and same-j/X_1(16)/halving or direct A,x0
             extraction map

q_square_divisor_or_boundary_only
  decision = repair_exact_fp_value_or_oriented_root_missing
  missing  = exact finite value or oriented one-edge theorem

q_square_value_up_to_scalar
  decision = repair_scalar_and_root_orientation_missing
  missing  = specified scalar before the two-root payload is concrete

q_square_with_oriented_root
  decision = normalize_root_then_apply_source_snippet_intake
  missing  = same theorem data after oriented-root normalization

q_direct_one_edge_theorem
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

sign_from_divisor_h90_or_quartic_phase
  decision = reject_sign_invisible_to_current_invariants
  falsifier = constant sign has zero divisor/H90 boundary and does not alter
              exponent-character data
```

## Counts

```text
evidence_markers_ok = 5/5
invariants_ok = 5/5
source_stage_candidates = 2
bounded_payload_rows = 1
normalize_rows = 1
repair_rows = 3
reject_rows = 1
current_source_theorems = 0
p25_v2_q_square_payload_router_rows=1/1
```

## Verdict

The Q square route has a useful bounded row-value consequence:

```text
exact scalar-fixed value for 2*edge -> two row-value roots
```

But this only helps if the source gives an exact finite value. Divisor-only,
boundary-only, phase-only, or value-up-to-scalar statements remain repair
rows. Trying to choose the sign from divisor, Hilbert-90 boundary, or
quartic-character phase is a reject row, because the constant sign is invisible
to all of those invariants. Trying to feed the row-value roots directly to
`vpp.py` is also wrong: `vpp.py` needs `(p,A,x0)`, so an extraction map remains
missing.
