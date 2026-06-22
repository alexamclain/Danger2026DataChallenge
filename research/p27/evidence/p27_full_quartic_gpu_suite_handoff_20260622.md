# P27 Full Quartic GPU Suite Handoff

Date: 2026-06-22

## Claim

The next bounded GPU math-structure test is now the full B-line/K-line monic
quartic exact-support suite.

Do not spend GPU time on smaller proxy families.  The obvious shortcuts are
already killed:

```text
K-line even quartics:              zero hits
K-line Belyi-reciprocal quartics:  zero hits
B-line Belyi-involution quartics:  zero hits
B/K signed-root plane shortcut:    zero low-degree relation
```

So the remaining useful GPU question is exactly:

```text
Does the descended p27 d3 class have a visible genus-1 quartic model in B or K?
```

## Manifest

Machine-readable suite:

```text
research/p27/archive/fixtures/p27_full_quartic_gpu_suite_20260622.json
```

This manifest points to the frozen row packets, verifiers, reference chunk
runners, run order, expected random counts, and killed subfamilies.

## Run Order

Run these first:

```text
1. K q1471 d3_on_K
   implementation smoke, 3,183,010,111 coefficient triples

2. K q1607 d3_on_K
   guard field, 4,149,995,543 triples

3. K q1847 d3_on_K
   decisive promotion field, 6,300,872,423 triples

4. B q1607 d3_on_legalB
   implementation smoke / coordinate comparison, 4,149,995,543 triples

5. B q1847 d3_on_legalB
   decisive promotion field, 6,300,872,423 triples

6. B q2087 d3_on_legalB
   independent guard field, 9,090,072,503 triples
```

Run these only after the d3 screens are implemented and cheap enough, or after
a d3 signal appears:

```text
B q1847 gate4_prefix_on_legalB
B q2087 gate4_prefix_on_legalB
K q1847 d4_on_K_after_d3
B q1847 legal_on_coreB
```

## Algorithm Contract

For coordinate `X` equal to `B` or `K`, test:

```text
chi(X^4 + aX^3 + bX^2 + cX + d) = polarity * target_sign(X)
```

with both global polarities allowed.  Exclude any hit that vanishes on a
target row.

Flatten coefficient triples as:

```text
index = (a*q + b)*q + c
a = index // q^2
b = (index % q^2) // q
c = index % q
```

For each `(a,b,c)`, solve for all valid constants `d` by intersecting
precomputed Legendre-sign masks over the frozen target rows.

## Verification

Verify every reported hit with the official local verifier for that coordinate:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_quartic_verify.py \
  --field <q> --family <family> --coeffs <a,b,c,d> --polarity <1-or--1>
```

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_quartic_verify.py \
  --field <q> --family <family> --coeffs <a,b,c,d> --polarity <1-or--1>
```

Then run the promotion-side geometry analyzer:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_quartic_hit_geometry.py \
  --coordinate <B-or-K> \
  --field <q> \
  --family <family> \
  --coeffs <a,b,c,d> \
  --polarity <1-or--1>
```

See [P27 Quartic Hit Geometry Promotion Tool](p27_quartic_hit_geometry_promotion_tool_20260622.md).

Report:

```text
coordinate
field
family
triples scanned
exact quartics
hit coefficients and polarity
verifier result
geometry analyzer result
throughput
any implementation notes
```

## Interpretation

Promote:

```text
stable d3 hit in q1847 with at least one guard-field companion
```

Next promotion artifact:

```text
construct z^2=f(B) or z^2=f(K)
compute genus/sourceability
compare B/K pullback through K^2=(B-2)^4/(8B(B+2)^2)
test whether the class recurs or couples to gate4/d4
```

Kill:

```text
no stable q1847/guard-field d3 hit in the B-line and K-line screens
```

That would close the visible low-genus monic-quartic route.  The next route
would be offline branch/genus/Kummer extraction over `P1_B`, `P1_K`, or the
legal pullback cover, not more small proxy scans.

Fallback handoff:
[P27 Post-Quartic CAS Suite Handoff](p27_post_quartic_cas_suite_handoff_20260622.md)
packages that next route as an ordered CAS queue.

## Linked Artifacts

- [P27 B-Line Quartic GPU Test Card](p27_b_line_quartic_gpu_test_card_20260622.md)
- [P27 K-Line Quartic GPU Test Card](p27_kline_quartic_gpu_test_card_20260622.md)
- [P27 B-Line / K-Line Bridge](p27_b_kline_bridge_20260622.md)
- [P27 K-Line Even-Quartic Screen](p27_kline_even_quartic_screen_20260622.md)
- [P27 K-Line Belyi-Reciprocal Quartic Screen](p27_kline_reciprocal_quartic_screen_20260622.md)
- [P27 B-Line Belyi-Involution Quartic Screen](p27_b_line_involution_quartic_screen_20260622.md)
- [P27 Quartic Hit Geometry Promotion Tool](p27_quartic_hit_geometry_promotion_tool_20260622.md)
- [P27 Post-Quartic CAS Suite Handoff](p27_post_quartic_cas_suite_handoff_20260622.md)

```text
p27_full_quartic_gpu_suite_handoff_rows=1/1
```
