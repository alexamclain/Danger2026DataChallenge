# P27 B-Line Transition Closure And Orientation

Date: 2026-06-22

## Claim

The second reduced B-line fiber factors cleanly into a generic quotient
transition plus a visible materialization half-selector.

For `A=B^2-2`, first reduced coordinate `u=x6+1/x6`, and second reduced
coordinate `v=x7+1/x7`, the quotient halving transition is:

```text
(v^2 - 4)^2 - 4*u*(v^2 - 4)*(v + A) + 16*(v + A)^2 = 0.
```

Over each legal `f3=+1` B row, this generic transition has `4` v-roots per
u-root, but the actual selected source uses exactly `2`.  The actual half is
not mysterious:

```text
actual selected half  <=>  chi(v^2 - 4) = +1
                       <=> chi(v + A) = +1
```

All generic v-roots, including the discarded half, already have the same
`chi(v+2)=f4(B)` sign.  Therefore the visible half-selector is only the
materialization/lift-to-`x7` layer; the remaining sqrt-beating question is the
separate Kummer class `gamma^2 = v+2`.

## Artifacts

Transition closure probe:

```text
research/p27/archive/gates/p27_b_line_transition_closure_probe.py
```

Transition closure output:

```text
research/p27/archive/probe_outputs/p27_b_line_transition_closure_probe_20260622.txt
```

Orientation squareclass probe:

```text
research/p27/archive/gates/p27_b_line_transition_orientation_probe.py
```

Orientation output:

```text
research/p27/archive/probe_outputs/p27_b_line_transition_orientation_probe_20260622.txt
```

Input fixtures:

```text
research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json
research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_transition_closure_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_transition_closure_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_transition_orientation_probe.py \
  --small-primes 1607,1847,2087 \
  --max-weight 4 \
  | tee research/p27/archive/probe_outputs/p27_b_line_transition_orientation_probe_20260622.txt
```

## Transition Results

The generic transition is twice the actual selected source at the v-level:

```text
q1607:
  first f3-plus B rows = 28
  generic roots per u = 4 on 112 parent pairs
  actual roots per u = 2 on 112 parent pairs
  generic v roots per B = 16 on 28 B rows
  fixture v roots per B = 8 on 28 B rows

q1847:
  first f3-plus B rows = 45
  generic roots per u = 4 on 180 parent pairs
  actual roots per u = 2 on 180 parent pairs
  generic v roots per B = 16 on 45 B rows
  fixture v roots per B = 8 on 45 B rows

q2087:
  first f3-plus B rows = 25
  generic roots per u = 4 on 100 parent pairs
  actual roots per u = 2 on 100 parent pairs
  generic v roots per B = 16 on 25 B rows
  fixture v roots per B = 8 on 25 B rows
```

The f4 sign is already constant on the larger generic quotient transition:

```text
q1607: generic_vplus2_matches_f4 = 28/28
q1847: generic_vplus2_matches_f4 = 45/45
q2087: generic_vplus2_matches_f4 = 25/25
```

## Orientation Results

The orientation screen labeled generic v-roots as actual versus missing and
tested low-weight products of natural squareclass atoms.  In every field,
there are exact weight-1 classifiers:

```text
n = v^2 - 4
d = v + A
v + A
```

with:

```text
q1607: exact_products > 0, best = 448/448
q1847: exact_products > 0, best = 720/720
q2087: exact_products > 0, best = 400/400
```

Thus:

```text
actual selected v-root  <=>  chi(v^2 - 4) = +1
actual selected v-root  <=>  chi(v + A) = +1
```

The equality of these two characters on transition roots is also the generic
identity `x6=(v^2-4)/(4*(v+A))` together with the already-imposed
`chi(x6)=+1`.

## Interpretation

Positive:

```text
The f4/f3 transition now has a precise smaller CAS model:
  F_A(u,v)=0,
  rho^2 = v^2 - 4  (or the same squareclass cut delta^2 = v + A),
  gamma^2 = v + 2  for the f4 selector.

The materialization half is explicit, so future CAS does not need the full
second x7 root forest to know which quotient roots lift to actual x7.
```

Norm/coboundary follow-up:
[P27 B-Line Gamma Norm/Coboundary Boundary](p27_b_line_gamma_norm_coboundary_20260622.md)
checks the remaining `gamma^2=v+2` class.  The generic four-root norm is
`16*(A-2)^2`, and the actual/missing two-root gamma norms are always squares
in q1607/q1847/q2087.  But the naive parent-`x6` norm formula is false, and
low-weight visible pair invariants do not predict `f4`.  This sharpens the
next CAS ask to an explicit Hilbert-90 quotient/coboundary computation, not a
visible norm sampler.

Negative:

```text
The 2-of-4 half-selector is not the moonshot.  It is the ordinary lift from
quotient v to actual x7.

Because chi(v+2)=f4(B) is constant even on the discarded generic roots, the
real obstacle remains the gamma^2=v+2 Kummer class.  No production GPU bucket
follows from the materialization selector alone.
```

## Continue / Kill

```text
continue = normalize the staged cover F_A(u,v)=0 plus rho^2=v^2-4
continue = compute the H90 quotient for gamma^2=v+2 on that staged cover
continue = compare gamma^2=v+2 against the f3 class on that normalized cover
continue = ask CAS/expert whether gamma is a pullback, coboundary, iterate, or low-genus quotient

kill = treating generic 4-to-actual 2 v-root shrink as a new search-space win
kill = naive Norm_2(v+2)=4*x6*(2-A) as the missing formula
kill = GPU production from chi(v^2-4) or chi(v+A) alone
kill = searching more visible orientation atoms for this materialization half
```

```text
p27_b_line_transition_closure_orientation_rows=1/1
```
