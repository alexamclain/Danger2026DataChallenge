---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Strict Non-CM Verdict

## Purpose

Summarize what remains if the p24 solution must avoid exploiting
supersingular curves or CM.

## Current Claim

No strict/no-CM asymptotic speedup is currently known.  The strict DANGER3
problem is not primality or broad elliptic certification: those are easy for
this prime.  The hard part is constructing a Montgomery curve with one of the
six exact x-only target traces without paying trace entropy.

Known non-CM-looking filters are informative, but they remain filters.  Exact
trace residues, mixed CRT conditions, Montgomery/Kloosterman transforms, and
small additive spectra can isolate or enrich the target classes only when
their information is treated as a free oracle.  Constructively imposing that
information grows modular or trace data back toward `Theta(sqrt(p))`.

## Decisive Evidence

- The strict frontier separates broad certificates from DANGER3 verifier
  compatibility: Pocklington and near-square ECPP certify easy facts, but do
  not produce the required exact x-only order `2^40` Montgomery triple.
- The trace target has only six signed Hasse lifts compatible with the
  verifier; after such a trace is known, finding an accepted `x0` is constant
  expected work.
- The exact trace-residue selector audit shows odd residues can isolate the
  targets as information, but the audit itself labels this an oracle filter,
  not a construction.
- Waterhouse/Mestre/fixed-trace audits reduce strict construction back to
  fixed isogeny-class or CM/root-selection work for discriminants of size
  comparable to p.
- Cheap near-square and small-CM routes hit only low 2-adic depth, not the
  p24 DANGER3 depth.

## Open Blockers

- Find a new finite-field identity that forces the target trace or the strict
  2-adic Frobenius orientation without CM/root selection.
- Clarify whether the challenge rule allows CM as a certificate strategy.  If
  it does not, the selected-product formula route is diagnostic unless
  rephrased as a non-CM finite-field identity.

## Next Reads

- [strict non-CM lane](../lanes/strict-non-cm.md)
- [DANGER3 source-rule verdict](danger3-source-rule-verdict.md)
- [DANGER3 upstream](../sources/danger3-upstream.md)

## Linked Artifacts

- [strict DANGER3 frontier](../archive/handoffs/strict_danger3_frontier.md)
- [trace residue selector audit](../archive/audits/trace_residue_selector_audit.py)
- [Montgomery trace transform audit](../archive/audits/montgomery_trace_transform_audit.py)
- [exact trace residue oracle tradeoff](../archive/harness/exact_trace_residue_oracle_tradeoff.py)
- [waterhouse/mestre fixed trace barrier](../archive/harness/waterhouse_mestre_fixed_trace_barrier.py)
