# Lane C: Low-Moment / W_axis p25 Check

Date: 2026-06-12

## Files inspected

- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/00_HANDOFF_INDEX_20260607.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/00_FRESH_EYES_SYNTHESIS_20260607.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/l1_axis_injectivity_theorem.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/trace_frame_split_frontier.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/trace_gcd_low_moment_relative_trace_gate.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/trace_gcd_low_moment_function_complexity_gate.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/trace_gcd_low_moment_automatic_p1_entropy_gate.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/trace_gcd_low_moment_truncated_polynomial_gate.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_transfer_matrix.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/lane_A_cm_lang_transfer.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/lane_B_fixed_frequency_jacobi.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/lane_D_strict_practical_improvement.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/README.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/RESULT.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/LATEST_P25_RUN.txt`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/p25_x16hn_20260612_084611/pids.txt`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/p25_x16hn_20260612_084611/watch.log`

No fleet process was touched. The `p25_x16hn_20260612_084611` worker/watch logs
in this checkout were still zero bytes when inspected.

## p25 arithmetic facts

Target:

```text
p = 10000000000000000000000013
sqrt_floor = 3162277660168
k = 42
```

The three Pomerance-admissible curve-side traces are:

| trace `t` | `v2(p+1-t)` | odd part of `p+1-t` |
|---:|---:|---|
| `5808037298190` | `42` | `2273736754431 = 3^2 * 601 * 420361759` |
| `1409990787086` | `50` | `8881784197 = 11 * 13 * 1543 * 40253` |
| `-2988055724018` | `42` | `2273736754433 = 17 * 5503 * 24304783` |

Exact PARI `quadclassunit` on the trace order discriminants
`Delta=t^2-4p=f^2 D_K` gives conductor `f=4` for all three rows:

| trace `t` | order class number and group | factorization |
|---:|---|---|
| `5808037298190` | `h(Delta)=907242623448`, group `C_226810655862 x C_2 x C_2` | `2^3 * 3 * 7 * 17^2 * 37 * 505027` |
| `1409990787086` | `h(Delta)=2397272743184`, group `C_299659092898 x C_2 x C_2 x C_2` | `2^4 * 11 * 13620867859` |
| `-2988055724018` | `h(Delta)=999672108288`, group `C_62479506768 x C_2^4` | `2^8 * 3 * 7 * 17 * 107 * 151 * 677` |

## Concrete sub-sqrt surfaces

Selected-chain accounting is positive for all three traces if a selected
producer exists. Conservative prime-power slot counts are:

| trace `t` | selected-chain slots | ratio to `sqrt_floor` |
|---:|---:|---:|
| `5808037298190` | `505371` | `1.60e-7` |
| `1409990787086` | `13620867886` | `4.31e-3` |
| `-2988055724018` | `1218` | `3.85e-10` |

Low-moment transfer is also comfortably sub-sqrt. The p24 gate transfers as a
counting surface: two selected refinement layers use `30` verifier constraints
but only `28` new higher moments because both `P_1` values are parent periods.
Example parent-field function surfaces, using the p24 `4+26` moment schedule:

```text
t=5808037298190:
  chain example top=168, child=37, child=289
  parent-field coefficients = 168*4 + (168*37)*26 = 162288

t=1409990787086:
  only one small pre-recovery child in the natural split
  16*4 = 64 low-moment coefficients, or 16*11 = 176 full child coefficients

t=-2988055724018:
  chain example top=3, child=107, child=151
  parent-field coefficients = 3*4 + (3*107)*26 = 8358
```

These are verifier/theorem surfaces, not producers. The p24 anti-collision and
relative-trace construction theorems have not been proved for the p25 fibers.

`W_axis` / packet-rank accounting is positive after checking the necessary
dimension condition `ord_n(p) >= dim(W_axis)`. Natural odd choices:

| trace `t` | recovery `n` | `dim(W_axis)` | `ord_n(p)` | packets | all-packet rank surface |
|---:|---:|---:|---:|---:|---:|
| `5808037298190` | `505027` | `336` | `252513` | `2` | `169688736` |
| `1409990787086` | `13620867859` | `15` | `6810433929` | `2` | `204313017870` |
| `-2988055724018` | `2031 = 3*677` | `298` | `338` | `4` | `402896` |

Guardrail: for the third trace, the largest-prime-only split `n=677` is not a
valid one-factor axis-rank target because `ord_677(p)=169 < dim(W_axis)`. It
becomes dimension-possible only after bundling a small odd factor, e.g.
`n=2031`.

## Transferable gates

Transferable from p24:

- Low-moment dictionary: child power sums are relative traces; by Newton,
  low power sums are equivalent to truncated selected child-polynomial
  coefficients.
- Automatic `P_1`: the first moment is the parent period, so the producer
  target is `28` new values, while the verifier/anti-collision target still
  uses `30` constraints.
- `W_axis` accounting: instantiate an axis space from the non-recovery class
  factors and price the all-packet rank surface as `phi(n) * dim(W_axis)`.
- Moore/annihilator style: a p25 axis route would need the same kind of
  nonzero Moore determinant / p-unit hyperplane-avoidance theorem as p24.

Not transferred:

- p24's squarefree cyclic class group. The p25 trace-order class groups have
  extra 2-primary direct factors.
- p24's `n=3107441`, `ord_n(p)=388430`, and tensor factor gap `368 < 5549`.
- Any selected CM/Lang/trace-GCD producer. The counts above do not find a root,
  a selected section, or a DANGER3 triple.

## First falsifier / positive next command

The cheap positive arithmetic gate has passed: all three traces have sub-sqrt
selected-chain and at least one dimension-possible `W_axis` rank surface.

First real falsifier, when CPU is available, should be the smallest p25-native
axis pilot on the smooth negative trace:

```sh
cd /Users/agent/Documents/Codex
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  python3 Danger2026DataChallenge/p24/l1_axis_injectivity_scan.py \
  --max-cases 40 --min-h 20 --max-h 1200 --max-abs-D 200000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 2031 --q-stop 500000 \
  --include-linear --require-deg-ge-axis-dim --summary-only
```

This does not prove p25. It is the right first falsifier for the proposed
`dim=298`, `n=2031`, `ord=338` shape: if small eligible analogues show
axis-injectivity failures once the dimension gap is this narrow, kill the p25
`W_axis` side quest.

First positive after that is not another count. It would be an actual p25
Moore-rank certificate for one packet/tensor factor or a constructed selected
relative-trace producer for the low-moment coefficients.

## Recommendation

Continue Lane C only as a low-priority theorem microscope; do not disturb the
main `x16halvenonsplit` p25 fleet.

The counts are genuinely sub-sqrt, so Lane C is not killed on payload size.
But it is killed as an immediate producer: the work remaining is a p25
anti-collision / p-unit / Moore-nonvanishing theorem, not a small executable
search. Best narrow target is the negative trace's bundled odd axis
`n=2031`, because its surface is tiny (`402896`) and falsifiable. The middle
trace has the cleanest huge-prime axis but a much larger rank surface
(`204313017870`), still below `sqrt_floor`.
