# P25 Transfer Matrix

Date: 2026-06-12

Target:

```text
p = 10000000000000000000000013 = 10^25 + 13
p mod 8 = 5
sqrt_floor = 3162277660168
k = 42
```

Admissible curve-side traces:

```text
t =  5808037298190   v2(p+1-t)=42   odd_part=2273736754431
  D = -6266702742833805022723952
  factor(D) = -2^4 * 7 * 1199351729 * 46652455412449

t =  1409990787086   v2(p+1-t)=50   odd_part=8881784197
  D = -38011925980332602215628656
  factor(D) = -2^4 * 11 * 2465641 * 2910709 * 30093907049

t = -2988055724018   v2(p+1-t)=42   odd_part=2273736754433
  D = -31071522990163265817935728
  factor(D) = -2^4 * 7 * 11 * 13 * 1493 * 1299417385618536931
```

The middle trace has unusually high 2-adic depth (`v2=50`) and a much smaller
odd part, so it is the initial moonshot focus unless class-group computation
shows one of the `v2=42` traces has a markedly better p24-style quotient.

## Source Queue

Use these p24 files first. Do not load the full `p24/` archive unless a row
below names a specific follow-up file.

```text
p24/00_HANDOFF_INDEX_20260607.md
p24/00_DREW_SUTHERLAND_ASK_MEMO.md
p24/00_FRESH_EYES_SYNTHESIS_20260607.md
p24/00_GLOBAL_SYNTHESIS_HANDOFF.md
p24/00_THEOREM_ATTEMPTS_LEDGER.md
p24/strict_danger3_frontier.md
```

## Transfer Rows

| Lane | p24 input | p25 transfer question | First falsifier or positive artifact | Discard condition |
| --- | --- | --- | --- | --- |
| Two-resultant surface | Four-field-element payload via two p-unit producers plus transport | Does any p25 trace have a class-field split with a small selected fixed orbit and one transportable nonzero orbit? | Compute class group/factor structure for all three p25 discriminants; compare to p24 `2*157*211*3107441` split. | No trace has smooth/sub-sqrt quotient structure or transportable orbit analogue. |
| Fixed-frequency / Jacobi | Selected CM/Lang/Jacobi product identity after `Tr_{B/C}` on `C_7 x C_179`; value-side identities feed Lean gates | Does p25 produce a smaller/cleaner two-axis quotient or admissible-span target? | For each trace, derive candidate class quotient factors and Frobenius orders; test whether a p24-style `C_a x C_b` surface exists. | Only generic actual-CM covariance appears, with no selected weighted packet or quotient improvement. |
| Low-moment selector | 28 new selected relative traces / 8172 parent-field coefficients in p24 | Are p25 quotient layers small enough for a selected-chain or low-moment payload below `sqrt_floor`? | Compute candidate layer sizes from class group; estimate selected moments and payload counts. | Payload is not sub-sqrt or requires dense class-set enumeration before the selected data exists. |
| `W_axis` / trace-frame | `dim W_axis=368`, one-factor Moore/normality theorem, trace-frame leading coordinate | Does p25 have an axis space and tensor factor with dimension gap analogous to `368 < 5549`? | Instantiate `W_axis` dimensions from candidate class factors; identify any one-factor Moore target. | No dimension gap or no arithmetic p-unit/nonvanishing target survives transfer. |
| Selected-chain fallback | p24 selected-chain payload `3107811` slots, sub-sqrt for fixed p24 | Does p25 have a selected recovery surface that remains below `3.162e12` slots? | Use class group factorization to price selected child/recovery objects. | Recovery degree or producer cost returns to sqrt-scale. |
| Strict / X1 tower | Fixed `X1(16)` is strong constant factor; generic growing X1 did not show beta `< 1` | Does p25's `p mod 8=5` and `v2=50` trace admit a practical improvement to `x16halvenonsplit`? | Tiny stats/inspection only while production runs; accept only measured hit-per-CPU-hour improvement. | No measured rate/probability improvement or only speculative filter. |

## Immediate Actions

1. Keep the production `x16halvenonsplit` fleet running unless a hit, instability,
   or verified better mode appears.
2. Get actual class-group data for all three p25 trace discriminants; this is
   the critical input for every moonshot lane.
3. Compare p25 factors against p24's live surfaces before inventing new theorem
   shapes.
4. Keep lane reports compact: one artifact, files inspected, command/probe,
   continue/kill recommendation.
