# p24 Research Wiki Workflow

This directory is a shareable research wiki layered over the p24 artifact
archive.  Treat the canonical pages as the working memory and the archive as
evidence/provenance.

## Canonical Surface

Top-level human entrypoints are:

- `frontier.md`: current cockpit and shortest complete status read.
- `index.md`: one-hop catalog of canonical pages.
- `log.md`: append-only chronological ledger.
- `lanes/`: active or demoted research lanes.
- `concepts/`: reusable facts, arithmetic, verifier surfaces, and Lean maps.
- `sources/`: source dossiers and prior-art bridges.
- `operations/`: live-run and expert-ask operational pages.
- `evidence/`: durable verdict pages cited by canonical pages.
- `archive/`: preserved generated notes, gates, scripts, source bundles, and handoffs.

## Page Interface

Canonical pages use:

```yaml
type: lane | source | concept | operations
status: active | background | blocked | archived
updated: YYYY-MM-DD
canonical: true
owner: llm
```

Use these sections: `Purpose`, `Current Claim`, `Decisive Evidence`,
`Open Blockers`, `Next Reads`, `Linked Artifacts`.

## Workflows

### Ingest

When adding a source or new research result:

1. Update the relevant source dossier or lane page first.
2. Update `frontier.md` if the current state changes.
3. Update `index.md` if a canonical page is added or removed.
4. Append a dated entry to `log.md`.
5. Put one-off gates, raw notes, and generated outputs in `archive/`.

### Query

Answer from `frontier.md`, canonical lanes, concepts, and sources first.
Open archive artifacts only for exact evidence, reproduction details, or
wording that is not captured in a canonical page.

### Lint

Periodically check:

- stale "current" claims across canonical pages;
- canonical pages with no decisive evidence links;
- archive artifacts that deserve promotion;
- orphan canonical pages not linked from `index.md`;
- old paths that still point to pre-reorganization locations.

## Rules

- Preserve artifacts; do not delete research evidence.
- Do not make raw gate scripts the primary reading path.
- New work defaults to updating canonical pages first.
- If a new executable gate is needed, cite it from a lane or evidence page.
- Keep live run logs outside this wiki; link them from operations pages.
