# p23 Research Ledger

This directory is a curated ledger of the p23 mathematical exploration. It is
not the full local workbench. Raw run logs, transient notes, compiled binaries,
and checkpoint files were intentionally left out.

The final result is recorded in `results/p23/`.

Some notes were written while the p23 run was still active, so live-run
instructions such as "keep waiting" or "do not restart" should be read as
time-stamped research context. The verified final outcome supersedes them.

## Core Result

- `p23_full_experiment_result_20260602.md`: full experiment/result write-up.
- `p23_ruled_maybe_untested_synthesis_20260601.md`: compact ledger of what was ruled out, what remained possible, and what moved to production.
- `p23_true_subsqrt_scaling_frontier_20260602.md`: interpretation of fixed-prime constant-factor wins versus true asymptotic sub-sqrt scaling.

## Successful Technique

- `p23_x16_halving_experiment.md`: original `X1(16)` prescribed-torsion halving experiment design.
- `x16_split_nonsplit_pullback_proof.md`: derivation of the y-level split/nonsplit Montgomery discriminant classifier.
- `x16_nonsplit_branch_collapse_proof_20260601.md`: proof that first-branch halving is complete in the nonsplit cyclic rational 2-Sylow case.
- `x16_nonsplit_branch_depth20_holdout_20260601.md`: p23 holdout supporting branch collapse through tested depths.
- `x16_nonsplit_depth_equals_v2_audit_20260602.md`: audit tying nonsplit marked-point halving depth to curve-level `v2(#E(Fp))`.

## Scaling And Rejected Routes

- `prescribed_torsion_scaling_barrier_20260602.md`: why generic growing `X1(N)` is not the asymptotic route.
- `danger3_short_certificate_transfer_recap_20260601.md`: transfer from the short-certificate experiments repo.
- `cm_exact_trace_audit.md`: CM exact-trace audit and obstruction.
- `x1_32_c_rootbench_20260602.md`: generic `X1(32)` p23 rootbench cost evidence.
- `p23_trace_filter_break_even_20260602.md`: exact trace-residue filter break-even analysis.

## Calibration

- `p23_conditioned_tail_model_update_30p9B_20260602.md`: live probability/tail model update shortly before the hit.
- `x16_exact_v2_distribution_calibration_20260602.md`: exact and sampled controls for the nonsplit v2 tail.
