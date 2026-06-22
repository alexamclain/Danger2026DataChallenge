# P27 B-Line Quartic GPU Test Card

Date: 2026-06-22

## Claim

The next GPU-worthy p27 math test is not a production search.  It is an exact
finite-field branch-support screen for the remaining genus-1 B-line family:

```text
chi(B^4 + aB^3 + bB^2 + cB + d)
```

with global polarity allowed.

This is the first bounded GPU test that would actually change the moonshot
state.  A stable positive would give a concrete elliptic/quartic double-cover
source candidate on `P1_B`.  A stable negative would close the last obvious
visible low-genus B-line support family after rational linears, split
quadratics, monic cubics, combined-prefix cubics, and Belyi orbits.

## Why This Is GPU-Worthy

The exact cubic solver already uses the right method: hold all coefficients
except the constant term fixed, then intersect shifted square/nonsquare masks.
For quartics, the same method fixes `(a,b,c)` and solves for `d`.

The work is too large for local Python but natural for GPU:

```text
q1607: q^3 = 4,150,168,943 coefficient triples
q1847: q^3 = 6,300,985,823 coefficient triples
q2087: q^3 = 9,091,731,703 coefficient triples
```

Each triple tests a bitset intersection over only `49..63` B rows for d3 or
gate4-prefix screens, with early exit when the intersection goes empty.

## Targets

Primary families:

```text
1. d3_on_legalB
   rows:
     q1607: 49 legal B, d3 plus/minus = 28/21
     q1847: 63 legal B, d3 plus/minus = 45/18
     q2087: 57 legal B, d3 plus/minus = 25/32

2. gate4_prefix_on_legalB
   rows:
     q1607: 49 legal B, gate4 plus/not-plus = 19/30
     q1847: 63 legal B, gate4 plus/not-plus = 19/44
     q2087: 57 legal B, gate4 plus/not-plus = 18/39
```

Secondary family, only if the solver is already fast:

```text
3. legal_on_coreB
   rows:
     q1607: 200 core B, legal/not-legal = 49/151
     q1847: 230 core B, legal/not-legal = 63/167
     q2087: 260 core B, legal/not-legal = 57/203
```

Do not prioritize `d4_on_d3plusB`: q1607/q2087 have too few rows and huge
random exact-hit expectation, so local hits would be interpolation artifacts.

## Expected Random Counts

For a balanced target on `n` rows, a crude random model gives:

```text
expected exact monic quartics ~= 2*q^4 / 2^n
```

For the primary d3/gate4 domains:

```text
q1607, n=49: expected ~= 2.37e-2
q1847, n=63: expected ~= 2.52e-6
q2087, n=57: expected ~= 2.63e-4
```

For the legal-on-core domain:

```text
q1607, n=200: expected ~= 8.30e-48
q1847, n=230: expected ~= 1.35e-56
q2087, n=260: expected ~= 2.05e-65
```

So:

```text
positive in q1847 or q2087 primary screens = highly non-random
positive in q1607 only = investigate, but treat as possible local artifact
positive in legal_on_coreB = extremely strong, but this is a secondary test
```

## Algorithm

Reuse the bitset convention from:

```text
research/p27/archive/gates/p27_b_line_cubic_support_probe.py
```

The target rows are frozen in a machine-readable packet:

```text
research/p27/archive/fixtures/p27_b_line_quartic_targets_20260622.json
```

Packet generator:

```text
research/p27/archive/gates/p27_b_line_quartic_target_packet.py
```

Hit verifier:

```text
research/p27/archive/gates/p27_b_line_quartic_verify.py
```

Generation command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_quartic_target_packet.py \
  --small-primes 1607,1847,2087 \
  --families d3_on_legalB,gate4_prefix_on_legalB,legal_on_coreB \
  > research/p27/archive/fixtures/p27_b_line_quartic_targets_20260622.json
```

For each field and target rows `(B_i, bit_i)`:

```text
targets are squareclass signs +/-1, after applying global polarity
precompute masks[desired][offset] over the constant term d

for a in F_q:
  for b in F_q:
    for c in F_q:
      intersection = all d values
      for each row i:
        offset_i = B_i^4 + aB_i^3 + bB_i^2 + cB_i
        desired_i = polarity * target_i
        intersection &= masks[desired_i][offset_i]
        early exit if empty
      any remaining d gives an exact monic quartic
```

Report both polarities.  Exclude zeros in the Legendre table as the existing
cubic solver does; an exact source selector should not vanish on the sampled B
domain.

Verifier command template for any returned hit:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_quartic_verify.py \
  --field <q> \
  --family <family> \
  --coeffs <a,b,c,d> \
  --polarity <1-or--1>
```

Packet sanity counts:

```text
q1607 d3_on_legalB:          rows=49  plus=28  minus=21
q1607 gate4_prefix_on_legalB rows=49  plus=19  minus=30
q1607 legal_on_coreB         rows=200 plus=49  minus=151

q1847 d3_on_legalB:          rows=63  plus=45  minus=18
q1847 gate4_prefix_on_legalB rows=63  plus=19  minus=44
q1847 legal_on_coreB         rows=230 plus=63  minus=167

q2087 d3_on_legalB:          rows=57  plus=25  minus=32
q2087 gate4_prefix_on_legalB rows=57  plus=18  minus=39
q2087 legal_on_coreB         rows=260 plus=57  minus=203
```

## Run Order

Recommended bounded GPU order:

```text
1. q1607 d3_on_legalB
   Purpose: implementation smoke and first signal.

2. q1847 d3_on_legalB
   Purpose: decisive promotion-field test.

3. q1847 gate4_prefix_on_legalB
   Purpose: direct two-gate source candidate.

4. q2087 d3_on_legalB and q2087 gate4_prefix_on_legalB
   Purpose: guard-field confirmation if q1847 or q1607 is positive, or final
   closure if q1847 is negative and runtime is acceptable.

5. q1607 legal_on_coreB
   Purpose: optional legal-domain quartic source test if the solver is fast.
```

## Report Back

For each `(field, family)`:

```text
field q
family
rows / plus / minus
coefficient triples scanned
exact quartics found by polarity
first few quartics, if any
wall time
GPU model
throughput triples/sec
whether zeros were excluded
```

If a hit is found, also test it immediately on the other promotion fields by
transporting only the family, not the coefficients.  Coefficients live in
different finite fields; the repeat condition is "an exact monic quartic exists
for the same named family," not "the same integer coefficients recur."

## Promotion / Kill

Promote:

```text
d3_on_legalB exact quartic in q1847 plus q2087
or gate4_prefix_on_legalB exact quartic in q1847 plus q2087
or legal_on_coreB exact quartic in any promotion field
```

Promotion artifact:

```text
write the quartic examples
build the genus-1 double cover z^2=f(B)
ask CAS for the map/sourceability and relation to f3/f4
only then consider a GPU sampler or p27 production mode
```

Kill:

```text
no exact quartic for d3_on_legalB in q1847 and q2087
no exact quartic for gate4_prefix_on_legalB in q1847 and q2087
```

That kill would close the visible genus-1 B-line branch-support route.  The
remaining B-line moonshot would be actual offline normalization/class
extraction, higher-genus structure, or a non-visible recurrence.

```text
p27_b_line_quartic_gpu_test_card_rows=1/1
```
