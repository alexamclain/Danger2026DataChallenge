# P27 B-Line Belyi-Involution Quartic Screen

Date: 2026-06-22

## Claim

The visible order-2 Belyi symmetries of the B-line branch set do not explain
the p27 B-line quartic target.

The B-line branch set is `{0, -2, infinity}`.  Its three order-2 Möbius
symmetries give five small monic quartic families:

```text
B -> -B-2:
  B^4 + 4B^3 + bB^2 + (2b-8)B + d

B -> 4/B:
  B^4 + aB^3 + bB^2 + 4aB + 16
  B^4 + aB^3 - 4aB - 16

B+2 -> 4/(B+2):
  (B+2)^4 + a(B+2)^3 + b(B+2)^2 + 4a(B+2) + 16
  (B+2)^4 + a(B+2)^3 - 4a(B+2) - 16
```

Exhausting these families gives zero exact hits over q1607/q1847/q2087 for
both primary B-line GPU targets: `d3_on_legalB` and
`gate4_prefix_on_legalB`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_involution_quartic_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_involution_quartic_probe_q1607_q1847_q2087_20260622.txt
```

Frozen target packet:

```text
research/p27/archive/fixtures/p27_b_line_quartic_targets_20260622.json
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_involution_quartic_probe.py \
  --small-primes 1607,1847,2087 \
  --families d3_on_legalB,gate4_prefix_on_legalB \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_involution_quartic_probe_q1607_q1847_q2087_20260622.txt
```

## Results

All primary field/family combinations had zero exact involution quartics:

```text
q1607 d3_on_legalB:          rows=49, shapes=7,750,561, exact=0
q1607 gate4_prefix_on_legalB rows=49, shapes=7,750,561, exact=0

q1847 d3_on_legalB:          rows=63, shapes=10,237,921, exact=0
q1847 gate4_prefix_on_legalB rows=63, shapes=10,237,921, exact=0

q2087 d3_on_legalB:          rows=57, shapes=13,070,881, exact=0
q2087 gate4_prefix_on_legalB rows=57, shapes=13,070,881, exact=0
```

Crude random expected exact counts for the d3 row counts are tiny:

```text
q1607 d3/gate4 rows=49: 2.75e-8
q1847 d3/gate4 rows=63: 2.22e-12
q2087 d3/gate4 rows=57: 1.81e-10
```

As with the K-line reciprocal screen, the statistical miss is expected.  The
structural point is that the later full B-line q1847 d3 screen was the right
decisive test, rather than a branch-involution-only proxy.

## Interpretation

Positive:

```text
The B-line GPU target is now cleaner.
The obvious Belyi-involution quartic shortcuts are exhausted locally.
```

Negative:

```text
No visible B-line branch-set involution gives the missing source class.
No q^2 B-line involution family should be handed to GPU as the main test.
```

Continue:

```text
bounded GPU exact support for full monic quartics
chi(B^4+aB^3+bB^2+cB+d)
```

Kill:

```text
B-line Belyi-involution quartics as the p27 d3/gate4 source
```

```text
p27_b_line_involution_quartic_screen_rows=1/1
```
