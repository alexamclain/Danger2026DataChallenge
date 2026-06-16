---
type: source
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# DANGER3 Upstream

## Purpose

Track challenge-source ambiguity and upstream datasets without absorbing raw
source bundles into the wiki surface.

## Current Claim

The local fork and upstream-looking DANGER3 source differ in visible no-CM
wording.  Until clarified, CM/Lang routes should be labeled conditional or
diagnostic.

## Decisive Evidence

- [DANGER3 source rule verdict](../evidence/danger3-source-rule-verdict.md)
- This fork's top-level README reportedly includes "without exploiting
  supersingular curves or CM."
- Archived `upstream_DANGER3/README.md` does not visibly contain that phrase.
- Upstream fixture data includes `pp10`, `pp20`, and compressed `pp12`,
  `pp16A`, `pp24`.

## Open Blockers

- Need authoritative rule clarification before presenting a CM route as
  challenge-final.

## Next Reads

- [strict non-CM](../lanes/strict-non-cm.md)
- [expert ask Drew](../operations/expert-ask-drew.md)

## Linked Artifacts

- [archived upstream DANGER3](../archive/sources/upstream_DANGER3/)
- [upstream dataset experiment audit](../archive/audits/upstream_dataset_experiment_audit.md)
- [upstream feature audit](../archive/audits/upstream_dataset_feature_audit.py)
