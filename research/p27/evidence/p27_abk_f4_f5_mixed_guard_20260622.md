# P27 A/B/K F4/F5 Mixed-Guard Transition

Date: 2026-06-22

## Claim

The repeated gamma-transition result survives mixed-`f5` guard fields.

Earlier f4/f5 evidence used `q1607,q1847,q2087`, where the available `f5`
rows were one-sided.  This probe extends to larger `q = 7 mod 16` fields where
`f5` has both signs.  On every selected `f4=+1` B row, all roots of

```text
F_A(V,W)=0
```

still have:

```text
chi(W+2) = f5(B).
```

This strengthens the CAS class-comparison target: the f5/f4 gamma class is not
just a one-sided small-field tail.  It is still not a GPU production source
without a quotient, coboundary, recurrence, or direct source map.

## Artifacts

Fixtures:

```text
research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json
research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_mixedf5_20260622.json
```

Output:

```text
research/p27/archive/probe_outputs/p27_abk_f4_f5_transition_count_probe_mixedf5_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_kummer_fixture_packet.py \
  --small-primes 4999,5783,6007,6247 \
  --max-gate 7 \
  --json \
  > research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_second_reduced_fiber_fixture_packet.py \
  --small-primes 4999,5783,6007,6247 \
  --json \
  > research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_mixedf5_20260622.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_abk_f4_f5_transition_count_probe.py \
  --small-primes 4999,5783,6007,6247 \
  --second-fixture research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_mixedf5_20260622.json \
  --kummer-fixture research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json \
  | tee research/p27/archive/probe_outputs/p27_abk_f4_f5_transition_count_probe_mixedf5_20260622.txt
```

## Mixed F5 Rows

The generated Kummer fixture has mixed `f5` signs:

```text
field   f4+ rows   f5+   f5-
4999    39         27    12
5783    42         1     41
6007    38         18    20
6247    34         18    16
```

## Transition Result

For all four fields:

```text
gamma_matches_f5_rate = 1.000000000
B_all_gamma_matches_f5 = f4_plus_B_rows
W_roots_per_v_4 for every tested v root
rho signs split half/half
orient signs split half/half
```

Detailed counts:

```text
field   f4+ B rows   gamma+   gamma-   matches
4999    39           864      384      1248/1248
5783    42           32       1312     1344/1344
6007    38           576      640      1216/1216
6247    34           576      512      1088/1088
```

At the B-row level:

```text
field   B target plus   B target minus
4999    27              12
5783    1               41
6007    18              20
6247    18              16
```

Each target-plus B has gamma profile `(32,0,0)` and each target-minus B has
gamma profile `(0,32,0)`.

## Interpretation

Positive:

```text
The f4/f5 repeated gamma class survives mixed-sign guard fields.
The result is exact on every selected B row in the tested mixed-f5 fields.
The f4/f5 CAS question is now stronger than a one-sided-tail artifact.
```

Negative:

```text
This still does not name a source parameter or denominator.
P27 train/heldout and GPU recurrence-coupling telemetry still kill current
gamma/sign-word buckets as production modes.
The evidence says "extract the repeated class", not "run a large GPU bucket".
```

## Consequence

Upgrade the A/B/K CAS ask:

```text
compare gamma_4^2 = V+2 and gamma_5^2 = W+2 on selected components;
use mixed-f5 guard fields as regression fixtures;
promote only a quotient/Prym/coboundary/source relation that explains the
exact B-row transition and improves source-normalized half-loss.
```

GPU remains limited to bounded named-coordinate telemetry or the separate
Dplus fused/native exchange-rate test.

## Continue / Kill

```text
continue = CAS compare f4/f3 and f5/f4 repeated gamma classes
continue = use mixed-f5 q4999/q5783/q6007/q6247 as regression fields
continue = search for a theorem-shaped quotient/coboundary explaining the exact transition

kill = dismissing f4/f5 recurrence as merely one-sided q1607/q1847/q2087 tails
kill = GPU gamma bucket production without source-normalized lift
kill = materialization/orientation halves as production filters
```

```text
p27_abk_f4_f5_mixed_guard_rows=1/1
```
