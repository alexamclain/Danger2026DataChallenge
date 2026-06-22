# P27 Conic Tower D6 A-Descent

Date: 2026-06-22

## Claim

The conic tower's selector descent persists one level past the d5 sign quotient:
after conditioning on d4-plus and d5-plus, the d6 selector is still
well-defined on the `A` projection in p27 train/heldout samples.

This is a real structural lead, but not a production GPU filter by itself.
Combined with [P27 A-Projection Selected-Prefix Profile](p27_a_projection_prefix_profile_20260621.md),
it says the selected prefix removes whole `A` fibers while still thinning at
roughly independent half-loss.  The asset is therefore an `A`-level Kummer
sequence to extract, not an `A` bucket search.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_tower_d6_quotient_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_tower_d6_quotient_probe_q1607_q1847_q2087_p27_300_20260622.txt
research/p27/archive/probe_outputs/p27_conic_tower_d6_quotient_probe_p27_1000_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_conic_tower_d6_quotient_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 300 \
  --p27-heldout-target 300 \
  --p27-max-draws 700000 \
  | tee research/p27/archive/probe_outputs/p27_conic_tower_d6_quotient_probe_q1607_q1847_q2087_p27_300_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_conic_tower_d6_quotient_probe.py \
  --small-primes '' \
  --p27-target 1000 \
  --p27-heldout-target 1000 \
  --p27-max-draws 1500000 \
  | tee research/p27/archive/probe_outputs/p27_conic_tower_d6_quotient_probe_p27_1000_20260622.txt
```

## Screen

The probe starts from d4-plus/d5-plus conic tower rows, materializes the third
transition, and groups the resulting d6 target by:

```text
base_A
base_Ax
first_unsigned
two_signed
two_square
two_reciprocal
two_selector_signless
z01_signless
three_signed
three_drop_L2_sign
three_square
three_reciprocal
```

A mixed group would mean that d6 is not determined by that quotient.  The
important first test is `base_A`: if it is mixed, the A-level sequence idea is
dead; if it is unmixed, the next step is class extraction on the A-line.

## P27 Results

In the larger p27 train run:

```text
unique_ax = 1000
d5_plus_second_lifts = 25088
third_lifts_after_d5plus = 802816
d6_plus_third_lifts = 475136
d6_minus_third_lifts = 327680

base_A groups = 49
base_A plus/minus groups = 29 / 20
base_A mixed_groups = 0
base_A rows = 802816
```

Heldout:

```text
unique_ax = 1000
d5_plus_second_lifts = 27648
third_lifts_after_d5plus = 884736
d6_plus_third_lifts = 475136
d6_minus_third_lifts = 409600

base_A groups = 54
base_A plus/minus groups = 29 / 25
base_A mixed_groups = 0
base_A rows = 884736
```

Every finer quotient also had:

```text
mixed_groups = 0
mixed_rows = 0
```

The smaller `300 + 300` p27 train/heldout screen showed the same zero-mixed
pattern.

## Guard Fields

The guard fields are again useful for multiplicity bookkeeping but less useful
as p27 predictors:

```text
q1607: d6 is all minus on the d5-plus slice
q1847: no d5-plus root rows, so no d6 quotient rows
q2087: d6 is all plus on the d5-plus slice
```

This mirrors earlier local plateau behavior: small fields can be constant or
empty at a given depth.  The p27 train/heldout samples are the decisive
anti-overfit evidence.

## Interpretation

Positive:

```text
d6 descends to A after the d4/d5 selected prefix.
The sign quotient is not merely a one-level d5 accident.
The live conic target is now an A-level sequence of Kummer characters.
```

Negative:

```text
The A projection still thins at ordinary half-loss in p27 prefix counts.
This does not justify a large GPU A-bucket or sign-bucket run.
Finite sign quotienting is still only CAS staging unless it yields a source.
```

## Concrete Next Tests

1. A-level Kummer class extraction.

```text
Construct the normalized A-level cover carrying the d4,d5,d6 characters.
Compute the branch divisors/classes of the three quadratic characters.
Promote if d5/d6 are pullbacks, translates, coboundaries, or iterates of one
low-genus class that can control many gates at once.
Kill if the classes are independent fresh half-covers on the normalized
A-level object.
```

2. Deeper A-prefix sanity screen.

```text
Use the cheap selected_gate_bits/A grouping path, not branch-sign expansion, to
check whether d7..d12 keep removing whole A fibers on larger p27 samples.
This is only a CAS-routing screen; it does not promote GPU production unless a
source law appears.
```

Completed by [P27 A-Level Prefix Descent](p27_a_level_prefix_descent_20260622.md):
on `12000 + 12000` p27 train/heldout samples, gates d3..d14 all have zero
mixed A groups.  The survivor counts remain geometric, so this promotes
A-line class extraction but not A-bucket production.

The first cheap A-line recurrence is also killed:
[P27 A-Line Affine Recurrence Screen](p27_a_line_affine_recurrence_screen_20260622.md).
There is no full-coverage affine recurrence from `d3` to `d4` in
q1607/q1847/q2087.  This rules out the easiest sourceable-map interpretation
of the A-descent and pushes the conic tower back to normalized class
extraction or theorem-guided correspondences.

The broader degree-one rational version is killed too:
[P27 A-Line PGL2 Recurrence Screen](p27_a_line_pgl2_recurrence_screen_20260622.md).
No full-coverage PGL2 map `A -> (a*A+b)/(c*A+d)` carries `d3` to `d4` in
q1607/q1847/q2087; the best full-coverage maps are identity majority baselines.
This closes the cheap PGL2 recurrence interpretation before CAS class
extraction.

3. GPU boundary.

```text
Do not run a large GPU search from this result alone.
Use GPU only to collect bounded A/prefix telemetry or to test a direct
legal-pullback/A-level sampler after CAS produces one.
```

## Continue / Kill

```text
continue = A-level Kummer class extraction for d4,d5,d6
continue = quotient finite signs before normalized A-cover computation
continue = theorem-guided non-affine correspondence tests only if sourced

kill = GPU sign-bucket search in conic tower signs
kill = A-prefix counts as a source shrink without a low-genus/source law
kill = affine A-line recurrence d_{j+1}(A)=+/-d_j(m*A+b)
kill = degree-one rational A-line recurrence d_{j+1}(A)=+/-d_j((a*A+b)/(c*A+d))
kill = treating small-field constant tails as p27 production evidence
```

```text
p27_conic_tower_d6_a_descent_rows=1/1
```
