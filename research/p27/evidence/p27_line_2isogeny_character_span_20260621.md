# P27 Line 2-Isogeny Character Span

Date: 2026-06-21

## Claim

The p27 line bits are not products of the visible branch and first 2-isogeny
divisor characters on the elliptic model

```text
E: v^2 = u^3 - u.
```

This closes the most obvious finite-field character family after the small
torsion/coset audit: the bits are not explained by multiplying the simple
branch characters from `a`, `u`, or the three rational 2-isogeny x-coordinates.

## Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_line_character_span_gate.py
```

The evaluator was also expanded to include the first 2-isogeny x-coordinates:

```text
phi0  = u - 1/u
phi1  = u*(u + 1)/(u - 1) - 2
phim1 = u*(u - 1)/(u + 1) + 2
```

Run:

```bash
python3 research/p27/archive/gates/p27_line_character_span_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --max-records 8192 \
  --prefix-size 2048 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_line_character_span_64tid_2chunk_256draw_8192rows_20260621.txt
```

## Basis

The scanned GF(2) basis had 16 named divisor characters:

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
phi0
phi0^2 + 4
phi1
phi1^2 - 6phi1 + 1
phim1
phim1^2 + 6phim1 + 1
```

This is `65,536` products, with a `2,048`-row prefix exactness screen and the
remaining held-out rows used as a falsifier.

## Result

Sample:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
domain_records = 8192
target_records = 8048
domain_inconsistent = 0
target_line_inconsistent = 0
```

Domain line:

```text
rows = 8192
target_+1 = 4022
target_-1 = 4170
candidate_count = 65536
prefix_exact_survivors = 0
full_exact_count = 0
best_lift = 1.029386925
```

Target line:

```text
rows = 8048
target_+1 = 4068
target_-1 = 3980
candidate_count = 65536
prefix_exact_survivors = 0
full_exact_count = 0
best_lift = 1.029794807
```

The top lifts are noise-scale and not exact.  More importantly, no product even
survived the prefix exactness test.

## Interpretation

Positive:

```text
The p27 line-test harness now covers first 2-isogeny x-coordinates and their
branch divisors.
```

Negative:

```text
domain_line is not in the 16-character visible divisor span.
T_line is not in the 16-character visible divisor span.
The first 2-isogeny layer does not provide a direct squareclass identity.
```

The next theorem-shaped ask is therefore narrower:

```text
Find a non-visible theta/divisor/additive identity on E: v^2=u^3-u, not merely
a product of first 2-isogeny branch characters.
```

The next joint/product screen confirms that there is no separate visible
product shortcut:
[P27 Line Half-Norm And Joint Stratum](p27_line_half_norm_joint_stratum_20260621.md).
It also records the half-norm formula for `domain_line`.

## Continue / Kill

```text
continue = named theta/additive identity on the supersingular j=1728 curve
continue = named R(a,u,phi*) proposals can be tested in p27_line_rational_evaluator.py
continue = GPU practical A/B remains baseline vs trace/norm D prefilter

kill = products of visible branch and first 2-isogeny characters
kill = treating the ~1.03x best span lifts as structural
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_line_character_span_gate.py`
- Gate: `research/p27/archive/gates/p27_line_rational_evaluator.py`
- Output: `research/p27/archive/probe_outputs/p27_line_character_span_64tid_2chunk_256draw_8192rows_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_line_rational_2isogeny_default_64tid_2chunk_256draw_8192rows_20260621.txt`

```text
p27_line_2isogeny_character_span_rows=1/1
```
