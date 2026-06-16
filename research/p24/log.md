---
type: operations
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# p24 Research Log

## Purpose

Append-only ledger for canonical p24 wiki changes.

## Current Claim

The first wiki reorganization pass preserved the artifact forest while
promoting a small research cockpit.

## Decisive Evidence

- [frontier](frontier.md)
- [index](index.md)
- [archive](archive/)

## Open Blockers

This page does not track proof blockers in detail.  See [frontier](frontier.md).

## Next Reads

Read latest entries first, then follow linked canonical pages.

## Linked Artifacts

- [old handoff index](archive/handoffs/00_HANDOFF_INDEX_20260607.md)
- [fresh-eyes synthesis](archive/handoffs/00_FRESH_EYES_SYNTHESIS_20260607.md)

## [2026-06-16] evidence | initial verdict layer

Added five curated evidence verdict pages:

- [selected product formula verdict](evidence/selected-product-formula-verdict.md)
- [strict non-CM verdict](evidence/strict-non-cm-verdict.md)
- [Lean gate coverage](evidence/lean-gate-coverage.md)
- [DANGER3 source rule verdict](evidence/danger3-source-rule-verdict.md)
- [p24 certificate surface verdict](evidence/p24-certificate-surface-verdict.md)

Wired the verdict layer into [index](index.md), [frontier](frontier.md), and
the affected lane, concept, source, and operations pages.  These pages
synthesize the current findings without replacing the raw archive artifacts.

## [2026-06-16] organization | move wiki under research/p24

Moved the p24 wiki from the temporary top-level `p24/` working directory to
`research/p24/` to match the existing p23 research convention.  Removed the
nested upstream `.git` metadata from the archived DANGER3 source fixture so
the fixture is stored as ordinary source files rather than an embedded Git
repository.

## [2026-06-16] organization | p24 wiki first pass

Reorganized p24 in place using the p25 wiki schema.  Created canonical lanes,
concepts, sources, operations, evidence, and archive tiers.  Preserved the old
artifact forest under `archive/`, including Python gates, Lean gates, audits,
scans, toys, boundaries, theorem notes, handoffs, harness scripts, and source
bundles.  Removed generated `__pycache__` caches from the share surface.

Move counts after the first pass:

- `archive/audits/`: 236 files
- `archive/boundaries/`: 204 files
- `archive/fixtures/`: 8 files
- `archive/gates/lean/`: 136 Lean files
- `archive/gates/py/`: 67 Python gate files
- `archive/handoffs/`: 58 files
- `archive/harness/`: 116 files
- `archive/notes/`: 106 files
- `archive/scans/`: 82 files
- `archive/sources/`: `lit/`, `paper_pages/`, `upstream_DANGER3/`
- `archive/theorems/`: 219 files
- `archive/toys/`: 148 files
