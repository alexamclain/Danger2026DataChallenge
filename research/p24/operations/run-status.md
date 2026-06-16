---
type: operations
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# p24 Run Status

## Purpose

Record live run state without absorbing bulky run logs into the wiki.

## Current Claim

The generic p24 sqrt-scale baseline is a fallback lottery, not the requested
asymptotic certificate.  It remains useful for throughput accounting and
opportunistic hit detection.

Latest checked in-thread: the watcher reported `no_hit`, with no
`HIT_DETECTED.txt` marker in the run directory.

## Decisive Evidence

- Run directory: `../runs/p24_generic_ladderfix_1p65sqrt_20260608_111143`
- Pointer file: `/tmp/p24_run_dir.txt`
- Watcher log: `../runs/p24_generic_ladderfix_1p65sqrt_20260608_111143/watcher.log`

## Open Blockers

- This run does not solve the asymptotic goal.
- If a hit appears, it must be independently verified before stopping workers.

## Next Reads

- [frontier](../frontier.md)
- [certificate surfaces](../concepts/certificate-surfaces.md)

## Linked Artifacts

- [old current context](../archive/handoffs/00_CURRENT_CONTEXT.md)
- [pomerance type2 audit](../archive/audits/pomerance_type2_audit.py)
