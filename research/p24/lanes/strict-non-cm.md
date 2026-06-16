---
type: lane
status: blocked
updated: 2026-06-16
canonical: true
owner: llm
---

# Strict Non-CM Lane

## Purpose

Track what survives if the challenge forbids exploiting CM or supersingular
structure.

## Current Claim

No strict/no-CM asymptotic speedup is known.  Exact trace residues,
Montgomery/Kloosterman spectra, and small additive/residue filters remain
information-rich but price back to `Theta(sqrt(p))`.

## Decisive Evidence

- [strict non-CM verdict](../evidence/strict-non-cm-verdict.md)
- [DANGER3 source rule verdict](../evidence/danger3-source-rule-verdict.md)
- [strict DANGER3 frontier](../archive/handoffs/strict_danger3_frontier.md)
- [trace residue selector audit](../archive/audits/trace_residue_selector_audit.py)
- [Montgomery trace transform audit](../archive/audits/montgomery_trace_transform_audit.py)
- [theorem attempts ledger](../archive/handoffs/00_THEOREM_ATTEMPTS_LEDGER.md)

## Open Blockers

- Need a genuinely new finite-field identity that forces the target trace or
  strict 2-adic Frobenius orientation.
- Need rule clarification: upstream DANGER3 and this fork differ on visible
  no-CM wording.

## Next Reads

- [DANGER3 upstream](../sources/danger3-upstream.md)
- [selected product formula](selected-product-formula.md)

## Linked Artifacts

- [exact trace residue oracle tradeoff](../archive/harness/exact_trace_residue_oracle_tradeoff.py)
- [additive spectrum trace bucket](../archive/harness/additive_spectrum_trace_bucket.py)
- [waterhouse/mestre fixed trace barrier](../archive/harness/waterhouse_mestre_fixed_trace_barrier.py)
