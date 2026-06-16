---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Transfer Matrix

## Purpose

Carry the p24-to-p25 transfer map: which surfaces port, which only become
microscopes, and which are dead enough not to lead the frontier.

## Current Claim

The transfer picture is now stable enough to prioritize around it.

Target:

```text
p = 10000000000000000000000013
p mod 8 = 5
sqrt_floor = 3162277660168
k = 42
```

Admissible traces:

```text
t =  5808037298190   v2 = 42   odd_part = 2273736754431
t =  1409990787086   v2 = 50   odd_part = 8881784197
t = -2988055724018   v2 = 42   odd_part = 2273736754433
```

Working summary:

- Practical `x16halvenonsplit` transfers directly and remains the live search.
- H0 and mixed conductor 39 are the best first-pass theorem fronts because the
  source objects are already certified.
- Exact-P remains the high-payoff heavy route.
- Literal p24 CM/Lang transfer is dead.
- Fixed-frequency/Jacobi and low-moment/W-axis still matter, but now as
  p25-specific theorem microscopes rather than as immediate closers.

## Decisive Evidence

- [Lane A CM/Lang transfer note](../evidence/lane_A_cm_lang_transfer.md)
  kills the literal p24 transfer.
- [Lane B fixed-frequency/Jacobi note](../evidence/lane_B_fixed_frequency_jacobi.md)
  leaves behind real quotient skeletons but not a producer.
- [Lane C low-moment/W-axis note](../evidence/lane_C_low_moment_w_axis.md)
  shows sub-sqrt payload counts but only theorem-shaped next steps.
- [Lane D strict practical improvement note](../evidence/lane_D_strict_practical_improvement.md)
  keeps the production mode anchored.
- [External source-theorem obligation matrix](../evidence/p25_ksy_y_external_source_theorem_obligation_matrix_20260614.md)
  prioritizes H0 and conductor 39 over exact-P as first asks.

## Open Blockers

- No transfer row has yet yielded a source-stage closing theorem.
- The theorem microscopes still need exact arithmetic producers or nonvanishing
  theorems, not just favorable counts.
- Exact extraction from any source object to DANGER3 payload remains missing.

## Next Reads

- [Practical search](../lanes/practical-search.md)
- [H0](../lanes/h0.md)
- [Conductor 39](../lanes/conductor39.md)
- [Exact P](../lanes/exact-p.md)
- [P24 prior art](../sources/p24-prior-art.md)

## Linked Artifacts

- [Lane A evidence](../evidence/lane_A_cm_lang_transfer.md)
- [Lane B evidence](../evidence/lane_B_fixed_frequency_jacobi.md)
- [Lane C evidence](../evidence/lane_C_low_moment_w_axis.md)
- [Lane D evidence](../evidence/lane_D_strict_practical_improvement.md)
- [Legacy transfer-matrix note](../archive/notes/p25_transfer_matrix_legacy_20260616.md)
