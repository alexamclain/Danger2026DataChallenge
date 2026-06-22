# P27 B-Line Mixed-F5 Recurrence Screen

Date: 2026-06-22

## Claim

The exact mixed-`f5` transition is not explained by the targeted visible
recurrence families:

```text
f5(B) = +/- f4(phi(B)).
```

The screen tested:

```text
1. full-coverage PGL2 maps on the visible B-line;
2. Belyi-conjugated hidden-X power maps X -> X^m for m=2,3,4,5,6.
```

It found no exact recurrence in `q4999,q5783,q6007,q6247`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_mixedf5_recurrence_probe.py
```

Input fixture:

```text
research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_mixedf5_recurrence_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_mixedf5_recurrence_probe.py \
  --small-primes 4999,5783,6007,6247 \
  --kummer-fixture research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json \
  --powers 2,3,4,5,6 \
  --keep-best 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_mixedf5_recurrence_probe_20260622.txt
```

## Results

No exact visible PGL2 recurrence:

```text
field   PGL2 maps tested   exact   best full-coverage match
4999    728,910            0       27/39
5783    2,048,256          0       41/42
6007    1,224,936          0       20/38
6247    226,920            0       18/34
```

The `q5783` near miss is the identity map with flipped sign.  It is not stable
evidence: that field has only one `f5=+1` row, and the balanced fields
`q6007,q6247` do not show the same near-exact behavior.

No exact hidden-X power recurrence:

```text
field   best forward coverage   best reverse coverage
4999    6/39                    6/91
5783    9/42                    10/128
6007    7/38                    8/108
6247    4/34                    5/62
```

The best power-map hits cover only a small part of the relevant rows, so they
are not source laws for the repeated transition.

## Interpretation

Positive:

```text
The f4/f5 repeated gamma transition remains exact and nontrivial.
The mixed-f5 guard fields are still good regression fixtures for CAS.
```

Negative:

```text
The transition is not a visible degree-one B-line recurrence.
The transition is not explained by the tested hidden-X power maps.
This does not supply a GPU production bucket or direct sampler.
```

## Consequence

The live A/B/K route remains:

```text
normalize the selected components;
compare gamma4^2 = V+2 and gamma5^2 = Wnext+2 as Kummer/divisor classes;
look for a quotient, coboundary, Prym relation, or source map there.
```

Do not spend more effort on visible PGL2 or hidden-X power-map recurrence
screens for this `f4 -> f5` object unless a theorem changes the coordinate.

## Continue / Kill

```text
continue = CAS/Prym comparison of repeated gamma classes
continue = use q4999/q5783/q6007/q6247 as mixed-sign regression fixtures
continue = ask for quotient/coboundary/source relations, not broad fits

kill = visible PGL2 maps as the f4->f5 recurrence
kill = Belyi-conjugated X^m, m<=6, as the f4->f5 recurrence
kill = GPU production from these recurrence buckets
```

```text
p27_b_line_mixedf5_recurrence_rows=1/1
```
