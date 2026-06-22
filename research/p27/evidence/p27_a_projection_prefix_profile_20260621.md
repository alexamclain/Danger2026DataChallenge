# P27 A-Projection Selected-Prefix Profile

Date: 2026-06-21

## Claim

Selected conic/Kummer prefix gates do not collapse the curve-parameter
`A`-space faster than they collapse the legal `(A,x)` source.

This kills a tempting source idea:

```text
maybe after a few selected gates, only a small A-set remains,
so enumerate A instead of searching raw X1(16) seeds.
```

On p27 train/heldout samples through depth 8, unique `A` and unique `(A,x)`
shrink in exact lockstep.  The scaled half-loss stays close to `1`, which is
the random-gate baseline rather than a sub-sqrt source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_projection_prefix_profile_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_a_projection_prefix_profile_probe_q607_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_a_projection_prefix_profile_probe_q1607_q1847_q2087_auto8_p27_depth8_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_a_projection_prefix_profile_probe.py \
  --small-primes 1607,1847,2087 \
  --auto-start 2200 \
  --auto-count 8 \
  --depth 8 \
  --p27-target 3000 \
  --p27-heldout-target 3000 \
  --p27-max-draws 2000000 \
  | tee research/p27/archive/probe_outputs/p27_a_projection_prefix_profile_probe_q1607_q1847_q2087_auto8_p27_depth8_20260621.txt
```

## P27 Sample Results

For each depth `d`, the prefix is:

```text
depth d = legal source plus selected gates d3..d_{d+2}
```

p27 train, 3,000 unique `(A,x)`:

```text
depth0: ax=3000 A=1500 scaled_A=1.000000
depth1: ax=1494 A=747  scaled_A=0.996000
depth2: ax=776  A=388  scaled_A=1.034667
depth3: ax=380  A=190  scaled_A=1.013333
depth4: ax=190  A=95   scaled_A=1.013333
depth5: ax=100  A=50   scaled_A=1.066667
depth6: ax=58   A=29   scaled_A=1.237333
depth7: ax=28   A=14   scaled_A=1.194667
depth8: ax=10   A=5    scaled_A=0.853333
```

p27 heldout, 3,000 unique `(A,x)`:

```text
depth0: ax=3000 A=1500 scaled_A=1.000000
depth1: ax=1558 A=779  scaled_A=1.038667
depth2: ax=758  A=379  scaled_A=1.010667
depth3: ax=362  A=181  scaled_A=0.965333
depth4: ax=182  A=91   scaled_A=0.970667
depth5: ax=80   A=40   scaled_A=0.853333
depth6: ax=50   A=25   scaled_A=1.066667
depth7: ax=22   A=11   scaled_A=0.938667
depth8: ax=12   A=6    scaled_A=1.024000
```

Here:

```text
scaled_A = (A_depth / A_depth0) * 2^depth.
```

Values near `1` mean ordinary independent half-loss.  The p27 samples show no
A-projection lift through depth 8.

The p27 samples also keep:

```text
avg_x_per_A = 2.000000
```

at every depth.  In other words, the prefix removes whole A-fibers and
surviving `(A,x)` rows in the same proportion; it does not leave a small A-set
with many exploitable x-lifts.

## Guard-Field Results

In q1607/q1847/q2087 and eight nearby `7 mod 8` primes, the same structural
pattern appears:

```text
unique (A,x) / unique A = 4
```

at every nonempty prefix depth.  Some small fields have local constant-tail or
zero-tail behavior, for example q2087 survives unchanged from depth 2 through
5 before dying at depth 6.  Those effects are field-local and do not match the
p27 train/heldout samples, where the prefix rates stay close to random
half-loss.

## Interpretation

Positive:

```text
The A-projection question is now directly tested.
The apparent univariate A relations seen in the Kummer-Z screen are explained:
small fields simply have small finite A-projections.
```

Negative:

```text
No A-only source or A-bucket search is supported.
The selected tower does not collapse A-space faster than it collapses
candidate rows in p27 samples.
```

This rules out another practical-looking sqrt-beating path.  The remaining
serious route is still the staged legal conic/Kummer tower as a function-field
object: normalization, components, quotient, or a named Kummer/Hilbert-90
identity.

## Continue / Kill

```text
continue = staged normalization/components of the conic/Kummer tower
continue = expert theorem ask for the repeated selector divisor
continue = GPU telemetry for structural capture rates, not A-bucket search

kill = A-projection prefix source
kill = GPU A-bucket search based on selected-prefix filters
kill = interpreting univariate small-field A polynomials as p27 source laws
```

```text
p27_a_projection_prefix_profile_rows=1/1
```
