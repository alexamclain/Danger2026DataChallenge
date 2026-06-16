---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# DANGER3 Source Rule Verdict

## Purpose

Capture the current rule ambiguity around CM and supersingular exploitation.

## Current Claim

The local fork's top-level README says the challenge is to find a Pomerance
triple "without exploiting supersingular curves or CM."  The archived upstream
DANGER3 README in `p24/archive/sources/upstream_DANGER3/` does not visibly
contain that phrase.  Until the source of authority is clarified, CM/Lang
work should be presented as conditional or diagnostic, not as an obviously
admissible final challenge solution.

## Decisive Evidence

- The local README contains the no-CM/no-supersingular sentence in the
  original upstream README section copied into this fork.
- The archived upstream README names the challenge and datasets but does not
  visibly include the no-CM phrase in the local copy.
- The theorem attempts ledger explicitly warns future work not to count a CM
  selector as final if that wording is binding.
- The Drew ask memo therefore asks rule clarification before asking for help
  with the CM/class-field theorem.

## Open Blockers

- Determine which README or problem statement is authoritative for p24.
- If no-CM is binding, decide whether the selected-product formula can be
  rephrased as a purely finite-field identity with no CM exploitation.

## Next Reads

- [DANGER3 upstream source dossier](../sources/danger3-upstream.md)
- [strict non-CM verdict](strict-non-cm-verdict.md)
- [expert ask Drew](../operations/expert-ask-drew.md)

## Linked Artifacts

- [local fork README](../../../README.md)
- [archived upstream README](../archive/sources/upstream_DANGER3/README.md)
- [theorem attempts ledger](../archive/handoffs/00_THEOREM_ATTEMPTS_LEDGER.md)
- [Drew ask memo](../archive/handoffs/00_DREW_SUTHERLAND_ASK_MEMO.md)
