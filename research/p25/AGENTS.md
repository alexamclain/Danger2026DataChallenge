# P25 Research Wiki Agent Guide

## Schema

This wiki is the primary reading surface for `research/p25`.

- `frontier.md`: research cockpit and current state.
- `index.md`: one-hop catalog of canonical pages only.
- `log.md`: append-only ledger using `## [YYYY-MM-DD] kind | title`.
- `lanes/`: active research theses and route status.
- `sources/`: source dossiers and source-boundary summaries.
- `concepts/`: cross-lane synthesis such as transfer maps.
- `operations/`: live operational state for runs and verification boundaries.
- `evidence/`: durable cited notes a human may still need to read directly.
- `archive/`: gates, harnesses, fixtures, and dated notes that are preserved but
  not part of the normal reading path.

Supporting layers remain outside the wiki core. In the original run workspace
these included local `runs/`, `src/`, and `incoming/` trees; this published copy
preserves the research record, while some operational and intake references
remain archival pointers rather than live repo-local paths.

## Canonical Page Contract

Every canonical page inside `lanes/`, `sources/`, `concepts/`, and
`operations/` must:

1. Use frontmatter:
   - `type`
   - `status`
   - `updated`
   - `canonical`
   - `owner`
2. Keep these sections, in this order:
   - `Purpose`
   - `Current Claim`
   - `Decisive Evidence`
   - `Open Blockers`
   - `Next Reads`
   - `Linked Artifacts`
3. Prefer durable workspace paths or canonical wiki links.
4. Never promote `/tmp` references into canonical pages.
5. Summarize first; use `evidence/` or `archive/` only for proof, exact wording,
   or historical provenance.

## Promotion And Demotion

- Promote a page into the canonical layer only if a human should realistically
  read it first during active research.
- Put a note in `evidence/` if canonical pages cite it directly and it remains a
  durable piece of reasoning.
- Put a note in `archive/notes/` if it is a dated checkpoint, an intake packet,
  a generated summary, or a conclusion now captured canonically.
- Put all `*_gate.py` files in `archive/gates/`.
- Put helper scripts and one-off harnesses in `archive/harness/`.
- Put packet fixtures, sample payloads, export directories, and caches in
  `archive/fixtures/`.

Default rule: update canonical pages first. Create a new gate or dated note only
when executable checking or archival provenance is genuinely needed.

## P25 v2 Operating Discipline

- Treat the local private p25 workspace as the live cockpit.
- Treat this public `Danger2026DataChallenge/research/p25` copy as a mirror
  that is updated only after meaningful canonical changes.
- Organize work by canonical artifact: operations/practical-search, H0,
  conductor 39, exact-P, or a named support microscope.
- Every artifact-producing pass must name pages read, commands or probes run,
  and one continue/kill recommendation.
- Expert and literature asks must be lane-shaped, never broad: H0
  divisor/additive with H90 boundary; conductor-39 mixed `U_chi/W` with Yang
  lift/descent; exact-P 75-atom product, orientation, or period-156 bridge.
- Keep Lane A killed as a literal p24 CM/Lang transfer; use Lane B and Lane C
  only as support microscopes tied to a live theorem idea.

## Workflow: Ingest

Use this when a raw source arrives in `incoming/` or by external absolute path.

1. Read the raw source or extracted text.
2. Update exactly one source dossier in `sources/`.
3. Update any affected lane pages in `lanes/`.
4. Refresh `frontier.md` if the active story changed.
5. Add or update one durable note in `evidence/` only if the source needs a
   preserved theorem screen, clause matrix, or verdict page.
6. Append one entry to `log.md`.
7. Touch `index.md` only if a canonical page was added, renamed, or retired.

## Workflow: Query

Answer from this order:

1. `frontier.md`
2. relevant `lanes/` pages
3. relevant `sources/` pages
4. `concepts/transfer-matrix.md`
5. `operations/run-status.md`
6. `evidence/` only if exact wording, proof shape, or provenance is needed
7. `archive/` only if the canonical layer cannot answer the question

When answering, prefer citing canonical pages over replaying archive artifacts.

## Workflow: Lint

Run this check whenever the wiki feels drifted:

1. Find stale "current" claims older than the latest decisive evidence.
2. Find canonical pages that nothing links to from `frontier.md` or `index.md`.
3. Find canonical pages with no `Decisive Evidence` links.
4. Find archive-heavy topics that now deserve one canonical summary page.
5. Find canonical pages that still mention removed paths, especially `/tmp`.
6. Confirm `frontier.md` still tells the full current story without archive
   notes.
7. Prefer the lightweight v2 cockpit gate:
   `python3 research/p25/archive/gates/p25_v2_wiki_cockpit_lightweight_check_gate.py`.
   Its marker list includes the first-class-run v2 plan guard, which checks
   that practical search remains primary, H0/conductor 39 remain the first-pass
   theorem fronts, exact-P remains second-pass, support microscopes stay
   subordinate, and the private/public mirror boundary remains documented.
   Do not run a broad `p25_v2_*_gate.py` glob during production-search-first
   work. These archived recomputation gates are intentionally heavy and should
   be run only when that lane is the active object:
   - `archive/gates/p25_v2_exactp_to_unified_target_spine_gate.py`
   - `archive/gates/p25_v2_h0_conductor39_unified_target_gate.py`

## Editing Rules

- Do not edit raw sources in `incoming/` or outside the repo.
- Preserve history by moving old artifacts instead of deleting them.
- Keep canonical prose compact and thesis-first.
- Treat `log.md` as append-only.
