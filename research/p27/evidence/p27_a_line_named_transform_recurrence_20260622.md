# P27 A-Line Named-Transform Recurrence Screen

Date: 2026-06-22

## Claim

The visible A-branch symmetry route is killed.  The selected A-level classes
do not come from the small named transform group preserving
`A in {-2, 2, infinity}`, and successive selected gates are not related by
one of those transforms in any source-useful way.

This keeps the A-line route alive only as normalized-cover/Kummer-class
extraction, not as a cheap orbit or recurrence on the visible A-line.

## Transform Set

The probe fixes the six transforms before reading labels.  They are the S3
action on `z=(A+2)/4`, i.e. the group preserving the visible branch set
`{-2, 2, infinity}`:

```text
A
2-A
16/(A+2)-2
16/(2-A)-2
2*(A+6)/(A-2)
2*(A-6)/(A+2)
```

No arbitrary PGL2 interpolation or coefficient fitting is used.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_line_named_transform_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_a_line_named_transform_probe_q1607_q1847_q2087_20260622.txt
research/p27/archive/probe_outputs/p27_a_line_named_transform_probe_p27_train_heldout_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_named_transform_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 8 \
  | tee research/p27/archive/probe_outputs/p27_a_line_named_transform_probe_q1607_q1847_q2087_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_named_transform_probe.py \
  --small-primes '' \
  --depth 10 \
  --min-rows 40 \
  --p27-target 4000 \
  --p27-heldout-target 4000 \
  --p27-max-draws 3000000 \
  | tee research/p27/archive/probe_outputs/p27_a_line_named_transform_probe_p27_train_heldout_20260622.txt
```

## Results

Complete guard fields:

```text
q1607:
  d3 A rows = 49
  non-identity images landing back in d3 domain:
    2-A: 4
    all other transforms: 0
  d4 vs d3 via non-identity transforms:
    2-A: 3 covered rows
    all other transforms: 0

q1847:
  d3 A rows = 63
  non-identity images landing back in d3 domain: 0 for every transform
  d4 vs d3 via non-identity transforms: 0 covered rows

q2087:
  d3 A rows = 57
  non-identity images landing back in d3 domain:
    2-A: 2
    all other transforms: 0
  d4 vs d3 via non-identity transforms:
    2-A: 2 covered rows
    all other transforms: 0
```

p27 train/heldout samples:

```text
p27 train:
  unique A = 2000
  kept maps = d3..d8
  non-identity images landing back in sampled d3 domain: 0 for every transform
  non-identity d4..d8 vs previous-gate coverage: 0 for every transform

p27 heldout:
  unique A = 2000
  kept maps = d3..d8
  non-identity images landing back in sampled d3 domain: 0 for every transform
  non-identity d4..d8 vs previous-gate coverage: 0 for every transform
```

The identity comparison only restates the ordinary prefix labels.  In tiny
fields it can look perfect in late tails, but the direction is field-dependent
and p27 train/heldout stay near ordinary half-loss:

```text
p27 train d4/d5/d6/d7/d8 plus-minus along identity:
  510/474, 242/268, 119/123, 63/56, 34/29

p27 heldout d4/d5/d6/d7/d8 plus-minus along identity:
  491/514, 233/258, 119/114, 54/65, 35/19
```

## Interpretation

The legal A-domain is not a union of visible branch-S3 orbits.  Except for
tiny accidental `2-A` collisions in q1607/q2087, the named transforms do not
even stay inside the A-domain, so they cannot give a source sampler or a
successive-gate recurrence.

This is a useful kill because it prevents the A-cover packet from drifting
back into cheap visible symmetry searches.  The next A-line work has to compute
the actual normalized cover/divisor/Kummer class.

## Continue / Kill

```text
continue = normalized A-cover / divisor / Kummer-class extraction
continue = compare d3/d4/d5/d6 classes after the normalized model exists
continue = use p27 d3..d10 A-prefix rows as routing evidence

kill = visible A-branch S3 orbit sampler
kill = d_{j+1}(A) = +/- d_j(T(A)) for the named A-branch transforms
kill = GPU A-bucket run from branch-S3 images
```

```text
p27_a_line_named_transform_recurrence_rows=1/1
```
