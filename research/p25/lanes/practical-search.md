---
type: lane
status: archived
updated: 2026-06-19
canonical: true
owner: llm
---

# Practical Search

## Purpose

Track the production search surface, the verified p25 hit, and the accounting
boundary for the practical campaign.

## Current Claim

`x16halvenonsplit` found the p25 certificate for `p = 10^25 + 13`.
The core technique is the same practical `X1(16)` nonsplit / first-branch
halving route as p23 and Jane Shi's p24 result. For p25, `p mod 8 = 5`, so no
p24 square-root patch was needed.

Verified triple:

```text
p  = 10000000000000000000000013
A  = 5863342488035851054212447
x0 = 9636258147581954669181726
```

Successful run accounting:

```text
run_dir = runs/p25_x16hn_20260616_051158_py_seed26047290
workers = 10
successful_worker = worker08
found_at = 2026-06-18 02:32:33 PDT
successful_worker_local_accepted_trials = 19634415922
reconstructed_successful_run_aggregate_trials = 196343915922
sqrt_floor(p) = 3162277660168
successful_run_fraction_of_sqrt = 0.062089398
successful_run_speedup_vs_sqrt = about 16.11x
```

The immediately prior production chunk stopped partway through after
266.467B accepted trials and is treated as a partial unexplained termination,
not exhaustion and not a hit. Charging that chunk to the campaign gives
462.810915922B total accepted trials, or 0.146353662 of `sqrt_floor(p)`.

## Decisive Evidence

- [Run status](../operations/run-status.md) captures the successful chunk and
  the prior partial stop boundary.
- `results/p25/triple.txt` records the official triple line.
- `results/p25/p25-verification.txt` records independent doubling replay,
  OpenSSL primality, official DANGER3 `vpp.py`, and Lean certificate
  generation.
- `results/p25/p25-worker08-tail.txt` records the successful worker tail.
- [V2 post-theorem extraction router](../evidence/p25_v2_post_theorem_extraction_router_20260616.md)
  records the bridge from a theorem hit to the practical `x16halvenonsplit`
  surface: same-`j` `X_1(8112)`, `A,xP16`, 38 halvings or direct `x0`, and
  official `vpp.py`.
- [V2 extraction payload contract](../evidence/p25_v2_extraction_payload_contract_20260616.md)
  records the constructive downstream payload accepted after a theorem hit:
  same-j bridge, practical `X_1(16)` payload, halving/x-chain/direct `x0`, and
  official `vpp.py`.
- [V2 extraction minimal hook](../evidence/p25_v2_extraction_minimal_hook_20260616.md)
  is the compact post-theorem acceptance boundary: theorem hits and exact-P
  hooks still need DANGER3 framing, same-`j` `X_1(8112)`, practical
  `X_1(16)` payload, halving/direct `x0`, and official `vpp.py`.
- [V2 end-to-end answer router](../evidence/p25_v2_end_to_end_answer_router_20260616.md)
  classifies future source, theorem, extraction, or practical-search payloads
  from repair/reject through source-stage, framed theorem, extraction-ready,
  and official `vpp.py`-verified submission.
- [Lane D strict practical improvement note](../evidence/lane_D_strict_practical_improvement.md)
  keeps `x16halvenonsplit` ahead of dgate, dgateskip, full-branch, Atkin, and
  X1 tower variants on present evidence.
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
  keeps the production mode, relaunch policy, theorem-front order, exact-P
  demotion, and support-microscope boundary testable from the cockpit.
- [P24 prior art](../sources/p24-prior-art.md) remains the authority on why the
  strict X1(16) practical route survived earlier audits.

## Open Blockers

- No practical-search blocker remains for the p25 certificate.
- The prior chunk died without a clean exhausted marker and remains recorded as
  partial unexplained termination.
- No alternate production mode needs promotion for p25 now that the certificate
  is found.
- A theorem-side bridge is not enough unless it passes the extraction minimal
  hook and emits the practical payload accepted by the extraction contract.

## Next Reads

- [Run status](../operations/run-status.md)
- [Transfer matrix](../concepts/transfer-matrix.md)
- [P24 prior art](../sources/p24-prior-art.md)

## Linked Artifacts

- `runs/LATEST_P25_RUN.txt`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/HIT.txt`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/watch.log`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/COMMAND.txt`
- `results/p25/triple.txt`
- `results/p25/p25-success-summary.txt`
- `results/p25/p25-verification.txt`
- `results/p25/p25-worker08-tail.txt`
- `results/p25/pomerance_10000000000000000000000013.lean`
- [Legacy run ledger](../archive/notes/run_status_legacy_20260616.md)
- [Lane D evidence](../evidence/lane_D_strict_practical_improvement.md)
- [V2 extraction payload contract](../evidence/p25_v2_extraction_payload_contract_20260616.md)
- [V2 extraction minimal hook](../evidence/p25_v2_extraction_minimal_hook_20260616.md)
- [V2 end-to-end answer router](../evidence/p25_v2_end_to_end_answer_router_20260616.md)
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
