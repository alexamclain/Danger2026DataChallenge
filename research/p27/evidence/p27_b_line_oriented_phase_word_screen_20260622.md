# P27 B-Line Oriented Phase-Word Screen

Date: 2026-06-22

## Claim

The natural materialization orientation does not rescue the alpha/beta phase
route.  It collapses the V4 decomposition to a tautology:

```text
H = (x + 1)/sqrt(x)
alpha = chi(H + R) = +1
beta = chi(H + S) = alpha*beta = actual next selected gate bit
```

So the materialization-oriented phase words do not expose a new recurrence or
source law.  They simply re-label already-known gate bits.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_oriented_phase_word_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_oriented_phase_word_probe_train_heldout_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_oriented_phase_word_probe.py \
  --p27-target 6000 \
  --p27-heldout-target 6000 \
  --max-draws 2000000 \
  --max-gate 9 \
  --target-gate 8 \
  --min-selected 500 \
  --small-primes '' \
  | tee research/p27/archive/probe_outputs/p27_b_line_oriented_phase_word_probe_train_heldout_20260622.txt
```

## Result

Train:

```text
source x-draws = 47241
unique A/x5/B = 6000
phase paths = 26052
target gate = 8
baseline target/source = 0.178827713
alpha_not_plus counters = 0
beta_product_mismatch counters = 0
```

Heldout:

```text
source x-draws = 48307
unique A/x5/B = 6000
phase paths = 27124
target gate = 8
baseline target/source = 0.196079243
alpha_not_plus counters = 0
beta_product_mismatch counters = 0
```

The best-looking oriented words only select on previously known gate bits.
They capture all target paths but do not improve target/source:

```text
train best conditional lift = 1.205
train selected target/source = 0.178827713 = baseline

heldout best conditional lift = 1.211
heldout selected target/source = 0.196079243 = baseline
```

## Interpretation

Positive:

```text
The sheet-orientation loophole is now bounded.
The algebra explains the result: H+R = 2*sqrt(x), so alpha is constant for
the deterministic selected square-root convention.
```

Negative:

```text
The natural materialization orientation does not produce a new phase recurrence.
The oriented beta factor is just the selected gate bit itself.
Conditional lift is only a post-hoc gate filter and gives no raw-source gain.
```

## Continue / Kill

```text
continue = offline divisor/Kummer-class extraction for gamma on the normalized no-R base
continue = compare gamma/f4 with the next f5/f4 class only after a normalized model exists
continue = GPU phase telemetry only if essentially free during another named-class run

kill = materialization-oriented alpha/beta phase words as a source law
kill = treating alpha=+1, beta=gate-bit as a recurrence
kill = larger CPU/GPU phase-word fitting without a new sheet transport theorem
```

```text
p27_b_line_oriented_phase_word_screen_rows=1/1
```
