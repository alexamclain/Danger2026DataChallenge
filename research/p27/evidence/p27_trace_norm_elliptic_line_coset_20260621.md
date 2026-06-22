# P27 Trace/Norm Elliptic Line / Coset Audit

Date: 2026-06-21

## Claim

The trace/norm quotient line has a clean elliptic interpretation, but the first
small group-coset explanations are negative.

The quotient

```text
C: b^2 = 16 - a^4
```

maps to the lemniscatic curve

```text
E: v^2 = u^3 - u
u = 4/a^2
v = 2b/a^3
```

For p27, `p = 10^27 + 103` is `3 mod 4`, so this `j=1728` curve is in the
supersingular regime.  The sample verifies:

```text
[p + 1]P = O
[(p + 1)/2]P = O
```

on every checked quotient point.  This gives a real structural home for the
line bits, but small torsion/coset projections do not explain either bit.

## Gates

Added:

```bash
python3 -m py_compile \
  research/p27/archive/gates/p27_trace_norm_elliptic_coset_gate.py \
  research/p27/archive/gates/p27_line_rational_evaluator.py
```

Runs:

```bash
python3 research/p27/archive/gates/p27_trace_norm_elliptic_coset_gate.py \
  --tids 0:32 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --max-records 4096 \
  --order-check-limit 128 \
  --moduli 2,3,4,6,12 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_elliptic_coset_32tid_2chunk_256draw_4096rows_20260621.txt

python3 research/p27/archive/gates/p27_line_rational_evaluator.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --max-records 8192 \
  | tee research/p27/archive/probe_outputs/p27_line_rational_default_64tid_2chunk_256draw_8192rows_20260621.txt
```

## Elliptic Model Result

Medium coset sample:

```text
raw_draws = 16384
nonsplit_y = 8248
k_points = 16496
domain_records = 4096
target_records = 3984
domain_inconsistent = 0
target_line_inconsistent = 0
```

Order checks:

```text
domain p_plus_1_zero = 128/128
domain half_order_zero = 128/128
target p_plus_1_zero = 128/128
target half_order_zero = 128/128
```

Small exponent-coset projections are mixed and flat:

```text
domain m=2,3,4,6,12: every class mixed, class_lift = 1.000000000
target m=2,3,6: every class mixed, class_lift = 1.000000000
target m=4,12: every class mixed, class_lift = 1.001966568
```

So neither `domain_line` nor `T_line` is determined by the visible small
torsion projection of the supersingular elliptic curve.

## Rational Evaluator Result

The reusable evaluator accepts named `R(a,u)` formulas, where:

```text
u = 4/a^2
variables = a, a2, a4, u, u2
```

Default branch-coordinate run:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
domain_records = 8192
target_records = 8048
domain_inconsistent = 0
target_line_inconsistent = 0
```

No default formula is exact for either bit.  The visible branch functions

```text
a
a - 2
a + 2
a^2 - 4
a^2 + 4
u
u - 1
u + 1
u^2 - 1
u^2 + 1
```

are exact for neither `domain_line` nor `T_line`.  The best observed lifts are
noise-scale:

```text
domain best_lift <= 1.019143432
target best_lift <= 1.012476280
```

The follow-up first 2-isogeny span is also negative:
[P27 Line 2-Isogeny Character Span](p27_line_2isogeny_character_span_20260621.md).
It scans all `65,536` products of visible branch and first 2-isogeny divisor
characters and finds no exact survivors for either line bit.

The later visible line-divisor screen is negative:
[P27 Trace/Norm Elliptic Line-Divisor Screen](p27_trace_norm_elliptic_line_divisor_screen_20260622.md).
On train and heldout samples, vertical divisors `u-c` and affine divisors
`v+m*u+c` with `|m|,|c| <= 4` have no exact survivors; the best heldout
target lift is only `1.011x` with a raw-source denominator.

The later large-factor quotient collision audit is negative as well:
[P27 Elliptic Large-Factor Collision Audit](p27_elliptic_large_factor_collision_20260621.md).
Repeated classes for the p27-specific factor `345451` and small multiples are
mixed at roughly random rates.

## Interpretation

Positive:

```text
The p27 line quotient has a canonical elliptic model E: v^2 = u^3 - u.
The expected supersingular p+1 behavior is verified on sampled points.
There is now a reusable named R(a,u) evaluator for theorem/expert candidates.
```

Negative:

```text
Small torsion/coset projections do not explain the bits.
Visible branch-divisor rational functions do not explain the bits.
The next positive result needs a nontrivial divisor/theta/additive identity,
not a small torsion class or low-complexity branch character.
```

## Continue / Kill

```text
continue = ask for a theta/divisor/additive identity on E: v^2=u^3-u
continue = test named R(a,u) proposals with p27_line_rational_evaluator.py
continue = GPU A/B remains practical: baseline vs trace/norm D prefilter

kill = small torsion/coset explanation for domain_line or T_line
kill = large-factor quotient-class explanation for m=345451 and small multiples
kill = branch functions a, a±2, a^2±4, u, u±1, u^2±1 as exact bits
kill = products of visible first 2-isogeny branch characters as exact bits
kill = visible elliptic line divisors u-c and v+m*u+c with |m|,|c| <= 4
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_trace_norm_elliptic_coset_gate.py`
- Gate: `research/p27/archive/gates/p27_line_rational_evaluator.py`
- Gate: `research/p27/archive/gates/p27_trace_norm_elliptic_line_divisor_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_elliptic_coset_32tid_2chunk_256draw_4096rows_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_line_rational_default_64tid_2chunk_256draw_8192rows_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_elliptic_line_divisor_probe_20260622.txt`

```text
p27_trace_norm_elliptic_line_coset_rows=1/1
```
