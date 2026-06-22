# P27 A/B/K F4/F5 Transition Count

Date: 2026-06-22

## Claim

The A/B/K selected-component transition repeats one layer deeper:
on every guard-field B row with `f4=+1`, all four generic roots of

```text
F_A(V,W) = 0
```

have the same `chi(W+2)`, and that sign matches the frozen `f5(B)` class.

This is a positive CAS-routing result.  It does **not** by itself promote a
GPU production source, because the available guard-field `f5` rows are
one-sided field tails:

```text
q1607: f5 is all plus on 19 B rows
q1847: f5 is all minus on 19 B rows
q2087: f5 is all plus on 18 B rows
```

So the right interpretation is:

```text
the gamma-transition form recurs on the selected component;
the field-tail signs are not yet a p27 source law;
CAS should compare f4/f3 and f5/f4 as repeated Kummer classes.
```

## Probe

Probe:

```text
research/p27/archive/gates/p27_abk_f4_f5_transition_count_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_abk_f4_f5_transition_count_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_abk_f4_f5_transition_count_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_abk_f4_f5_transition_count_probe_20260622.txt
```

Inputs:

```text
research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json
research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json
```

The test uses:

```text
B rows with f4(B)=+1
v roots from the second reduced-fiber fixture
W roots of F_A(v,W)=0
gamma_next = chi(W+2)
f5(B) from the frozen Kummer fixture
```

## Results

```text
q1607:
  f4_plus_B_rows = 19
  W_roots_per_v_4 = 152
  gamma_1 = 608
  gamma_matches_f5 = 608
  B_all_gamma_matches_f5 = 19

q1847:
  f4_plus_B_rows = 19
  W_roots_per_v_4 = 152
  gamma_-1 = 608
  gamma_matches_f5 = 608
  B_all_gamma_matches_f5 = 19

q2087:
  f4_plus_B_rows = 18
  W_roots_per_v_4 = 144
  gamma_1 = 576
  gamma_matches_f5 = 576
  B_all_gamma_matches_f5 = 18
```

In all three fields:

```text
gamma_matches_f5_rate = 1.000000000
rho signs split half/half
orient signs split half/half
```

Thus the materialization/orientation halves remain ordinary, while the next
selector `chi(W+2)` is constant on each selected-component generic transition.

## Interpretation

Positive:

```text
The f4/f5 transition has the same staged shape as f3/f4.
The selected-component gamma sign is constant across the generic four-root
transition in q1607/q1847/q2087.
This is exactly the kind of recurrence-shaped structure CAS should compare.
```

Negative:

```text
The observed f5 signs are one-sided and field-dependent in the small guard fields.
This does not give a source denominator, direct sampler, or p27 heldout lift.
It does not justify GPU production from B buckets or gamma signs.
```

## CAS Consequence

The B-line/A-B-K CAS ask should now compare:

```text
gamma_4^2 = V + 2 on F_A(U,V)=0 over f3-plus
gamma_5^2 = W + 2 on F_A(V,W)=0 over f4-plus
```

Promote only if those two classes are the same pullback/translate/coboundary,
live on one quotient/Prym factor, or give an explicit sourceable recurrence.

Kill if the repeated shape is only formal and the normalized classes are fresh
unrelated half-covers.

## GPU Consequence

This creates a better bounded telemetry request but not a production run:

```text
emit B, U, V, W, gamma_4, gamma_5, rho/orient splits, and raw source denominators
on p27 samples;
promote only if gamma_4/gamma_5 coupling improves target/source_draw;
do not run large production from the guard-field one-sided f5 signs.
```

## Continue / Kill

```text
continue = CAS compare f4/f3 gamma with f5/f4 gamma
continue = use this as a regression fixture for normalized selected components
continue = bounded GPU telemetry can emit gamma_4/gamma_5 with denominators

kill = reading q1607/q1847/q2087 one-sided f5 tails as a source law
kill = gamma bucket production without raw-source lift
kill = materialization/orientation halves as production filters
```

## Linked Artifacts

- [P27 A/B/K F3/F4 Chart Count](p27_abk_f3_f4_chart_count_20260622.md)
- [P27 B-Line Second Reduced-Fiber Fixture](p27_b_line_second_reduced_fiber_20260622.md)
- [P27 B-Line Kummer Fixture Packet](p27_b_line_kummer_fixture_packet_20260622.md)
- [P27 B-Line Gamma Class Handoff](p27_b_line_gamma_class_handoff_20260622.md)

```text
p27_abk_f4_f5_transition_count_rows=1/1
```
