# P25 v2 KL Primitive-Word Source Split

Updated: 2026-06-17

Marker: `p25_v2_kl_primitive_word_source_split_rows=1/1`

## Purpose

Promote a source-facing addendum for the exact-P Kubert-Lang hook. The KL
selector boundary already says the finite packet is rigid. This page records
the sharper source forms of that same finite object:

```text
z^121 * (1 + z + z^2) * (1 - z^263)
```

and the equivalent three-term Hilbert-90 source-chain form. This is not a new
broad KL lane; it is a more precise intake screen for exact-P source snippets.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `sources/kubert-lang.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`
- `evidence/p25_v2_kubert_lang_selector_boundary_20260616.md`
- `evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_primitive_word_gate.py`
- `archive/gates/p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate.py`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_kl_primitive_word_source_split_gate.py
```

The gate returned `p25_v2_kl_primitive_word_source_split_rows=1/1`.

## Verified Split

The six-term KL primitive word is:

```text
z^121 * (1 + z + z^2) * (1 - z^263)
```

The normalized word is:

```text
(1 + z + z^2) * (1 - z^263)
= (1 - z^3) * (1 - z^263) / (1 - z)
```

That cyclotomic-unit form is useful source vocabulary, but it is not a source
theorem by itself. It still has to lift to the exact p25
Siegel/Kronecker/KSY packet with orientation and theta2/K-trace context.

The same bridge word is also recovered from the primitive Hilbert-90
source-chain screen:

```text
canonical chain = -(1 + z + z^-121)
first boundary step = 122
first boundary = (1 - z^122) * canonical chain
inversion boundary = z^121 * (1 + z + z^2) * (1 - z^263)
```

The only boundary steps that recover the bridge across the active orientations
are `122` and `385 = -122 mod 507`.

## Intake Rows

```text
six_term_primitive_word
  decision = continue_if_arithmetic_source_emits_exact_oriented_word
  missing  = arithmetic source theorem and DANGER3 framing after theorem hit

three_term_h90_source_chain
  decision = continue_if_source_emits_chain_boundary_step_and_k_trace
  missing  = raw K-trace/theta2 period-156 context and arithmetic source theorem

cyclotomic_unit_factorization
  decision = support_compression_not_source_theorem
  missing  = theorem-legal Siegel/Kronecker/KSY lift with orientation and p25
             payload

generic_kl_generator_or_congruence_theorem
  decision = repair_exact_selector_theorem_missing
  missing  = exact primitive word, mixed selector, or accepted theta2 payload

source_chain_without_k_trace_or_theta2_context
  decision = repair_k_trace_theta2_context_missing
  missing  = raw K-trace, orientation, and theta2/theta2-inverse bridge data
```

## Counts

```text
evidence_markers_ok = 5/5
accepted_source_hook_rows = 2
support_compression_rows = 1
repair_rows = 2
current_kl_source_theorems = 0
current_exactp_source_theorems = 0
current_source_stage_closers = 0
p25_v2_kl_primitive_word_source_split_rows=1/1
```

## Verdict

The exact-P/KL ask is now sharper:

```text
Find a theorem-legal arithmetic source result for the oriented six-term
primitive word, or for the three-term Hilbert-90 source chain plus unique
boundary step, together with the raw K-trace/theta2 period-156 bridge.
```

Generic KL generator theory, theorem-K congruence language, and the
cyclotomic-unit factorization alone remain support. A positive answer must
emit the p25 oriented selector/payload as an arithmetic theorem before exact-P
status changes.
