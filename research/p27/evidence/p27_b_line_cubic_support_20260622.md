# P27 B-Line Cubic Support Screen

Date: 2026-06-22

## Claim

The two front-door B-line genus-1 cubic routes are negative in the p27-signature
promotion fields `q=1607,1847,2087`.

The exact screen tests monic cubic branch support on `P1_B`:

```text
chi(B^3 + aB^2 + bB + c)
```

with global polarity allowed.  A surviving cubic for either the legal B-domain
or `d3(B)` would give a genus-1 double cover `z^2=f(B)` and therefore a real
source candidate.  No such cubic exists in the three promotion fields.

## Artifacts

Gate:

```text
research/p27/archive/gates/p27_b_line_cubic_support_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_cubic_support_probe_q1607_q1847_q2087_d3_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_cubic_support_probe_q1607_q1847_q2087_legal_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_cubic_support_probe_q1607_q1847_q2087_d4_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_cubic_support_probe.py \
  --small-primes 1607,1847,2087 \
  --families d3 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_cubic_support_probe_q1607_q1847_q2087_d3_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_cubic_support_probe.py \
  --small-primes 1607,1847,2087 \
  --families legal \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_cubic_support_probe_q1607_q1847_q2087_legal_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_cubic_support_probe.py \
  --small-primes 1607,1847,2087 \
  --families d4 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_cubic_support_probe_q1607_q1847_q2087_d4_20260622.txt
```

## Method

For fixed `a,b`, the constant term `c` is handled by intersecting shifted
square/nonsquare masks across all B rows.  This tests all monic cubics exactly
in `O(q^2 * rows)` bitset operations instead of brute-forcing all `q^3`
coefficient triples.

This screen covers arbitrary monic cubic support, including irreducible cubic
support.  It is not a small-coefficient fit.

## Results

For the decisive `d3(B)` selector:

```text
q1607: legal_B = 49, d3 plus/minus = 28/21, exact cubics = 0
q1847: legal_B = 63, d3 plus/minus = 45/18, exact cubics = 0
q2087: legal_B = 57, d3 plus/minus = 25/32, exact cubics = 0
```

For the legal B-domain inside the core B bucket:

```text
q1607: core_B = 200, legal/core split = 49/151, exact cubics = 0
q1847: core_B = 230, legal/core split = 63/167, exact cubics = 0
q2087: core_B = 260, legal/core split = 57/203, exact cubics = 0
```

For `d4(B)` after `d3=+1`, local cubics appear only in small-row fields and do
not survive the promotion set:

```text
q1607: d4 rows = 28, exact cubics = 24
q1847: d4 rows = 45, exact cubics = 0
q2087: d4 rows = 25, exact cubics = 520
```

The q1607/q2087 d4 hits are interpolation artifacts, not structure: q1847 is
non-degenerate for d4 and has zero exact cubics.

## Interpretation

Positive:

```text
The B-line has now been screened for another named low-genus source family.
The exact cubic solver is reusable and avoids blind q^3 brute force.
```

Negative:

```text
No genus-1 cubic source explains the legal B-domain.
No genus-1 cubic source explains d3(B).
Local d4 cubics are unstable and should not be promoted.
```

This closes the irreducible-cubic / monic-cubic B-line route.  Together with
the prior rational-linear, one-quadratic-plus-linears, two-quadratic, and
Belyi-orbit negatives, the remaining B-line moonshot is not a visible
low-degree branch-support sampler.  It needs actual Kummer/divisor extraction,
irreducible quartic or cubic-plus-linear support found by that extraction, a
higher class, or a recurrence/coupling among `f3(B), f4(B), ...`.

## Continue / Kill

```text
continue = B-line Kummer/divisor extraction for the full f_j(B) sequence
continue = irreducible quartic or cubic-plus-linear only as a named class test
continue = compare f3/f4/f5 if a tractable class is recovered

kill = monic cubic support for legal B-domain
kill = monic cubic support for d3(B)
kill = q1607/q2087 local d4 cubics as promotion evidence
kill = GPU production from B buckets without an extracted source or recurrence
```

```text
p27_b_line_cubic_support_rows=1/1
```
