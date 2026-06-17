# P25 V2 Kubert-Lang Selector Boundary

Date: 2026-06-16

Marker: `p25_v2_kubert_lang_selector_boundary_rows=1/1`

## Purpose

Promote the finite Kubert-Lang boundary for exact-P into one compact v2
verdict: what KL-style exponent/product machinery already verifies, and what
it still does not supply.

## Pages And Gates Read

- `sources/kubert-lang.md`
- `lanes/exact-p.md`
- `evidence/p25_ksy_y_kubert_lang_visual_theorem_boundary_20260614.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate.py`
- `archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_primitive_word_gate.py`
- `archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_gate.py`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_kubert_lang_selector_boundary_gate.py
```

## Findings

The exact p25 finite payload passes the necessary Kubert-Lang exponent-matrix
screen:

- source packet level `507`, support `6`
- theta2 raw level `12675`, support `300`
- exact source packet, theta2, and theta2-inverse profiles pass the quadratic
  congruence tests
- truncated `D`, wrong `D`, wrong `T`, and positive-only controls are rejected

The prime-power `C_169` projection is not a closer. It passes only after losing
the right-class and `T`-edge data needed for the p25 packet.

The primitive KL word is the previously audited rigid bridge word:

```text
z^121 * (1 + z + z^2) * (1 - z^263)
normalized: (1 + z + z^2) * (1 - z^263)
```

The selector is rigid on the quotient `C_3 x C_169`: all `257049` center/D
pairs were scanned; there are two forward matches, two reverse matches, four
support-only matches, and no zero-D support matches. This is exactly the
expected orientation and D-reversal ambiguity.

## Verdict

Kubert-Lang is now a precise finite selector boundary, not a current source
closer. A useful KL/Siegel/Kronecker theorem must emit the exact row-labeled
mixed selector, the primitive bridge word above, or an accepted
theta2/theta2-inverse payload.

Reject or repair:

- generic KL dependence/generation statements
- raw exponent balance without the selector theorem
- prime-power `C_169` projection results
- wrong, truncated, or unoriented `D/T/center` packets

Decision:
`finite_selector_rigid_but_kl_source_theorem_missing`.

## Continue / Kill

Continue only if a source snippet includes a theorem-legal mixed
`C_3 x C_169` product or exact primitive word with p25 orientation. Kill broad
KL rereads and projection-only claims.
