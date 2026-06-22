# P27 Conic-Pair D5 Tower

Date: 2026-06-21

## Claim

The conic-pair selector product repeats one level beyond d4.

For any transition in the conic-chain tower:

```text
h_j^2 = r_j^2 + c*r_j + 1
g_j^2 = r_j^2 - c*r_j + 1
r_{j+1}^2 - (h_j + g_j)*r_{j+1} + 1 = 0
```

write:

```text
a_j = r_{j+1} - 1/r_{j+1}
L_j = h_j - g_j - 2r_j
```

Then, in the p27 `chi(2)=+1` regime, the next selector is:

```text
chi(r_{j+1}^2 + c*r_{j+1} + 1)
  = chi(-(L_j+a_j)(L_j-a_j)c*r_{j+1}).
```

The previous d4 result is the `j=0` case.  This screen validates the `j=1`
case against d5 on q1607/q1847/q2087 and on p27 train/heldout samples.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_d5_tower_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_conic_pair_d5_tower_probe_q1607_q1847_q2087_p27_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_d5_tower_probe_q1607_q1847_q2087_p27_1500_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_d5_tower_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 500 \
  --p27-heldout-target 500 \
  --p27-max-draws 1000000 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_d5_tower_probe_q1607_q1847_q2087_p27_20260621.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_conic_pair_d5_tower_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 1500 \
  --p27-heldout-target 1500 \
  --p27-max-draws 1500000 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_d5_tower_probe_q1607_q1847_q2087_p27_1500_20260622.txt
```

## Guard-Field Results

```text
q1607:
  d4-plus unique (A,x) = 76
  d5 split = 76 plus / 0 minus
  second lifts = 19,456
  d5 product mismatches = 0
  universal product mismatches = 0
  selected two-step coordinate re-enters legal source = 0/19,456

q1847:
  d4-plus unique (A,x) = 76
  d5 split = 0 plus / 76 minus
  second lifts = 19,456
  d5 product mismatches = 0
  universal product mismatches = 0
  selected two-step coordinate re-enters legal source = 0/19,456

q2087:
  d4-plus unique (A,x) = 72
  d5 split = 72 plus / 0 minus
  second lifts = 18,432
  d5 product mismatches = 0
  universal product mismatches = 0
  selected two-step coordinate re-enters legal source = 0/18,432
```

The guard fields have constant d5 on the screened d4-plus slice, with sign
depending on the field.  The actual p27 samples show d5 is not globally
constant.

## P27 Sample Results

```text
p27 train:
  sampled pairs = 500
  d4-plus unique (A,x) = 128
  d5 split = 50 plus / 78 minus
  second lifts = 32,768
  d5 product mismatches = 0
  universal product mismatches = 0

p27 heldout:
  sampled pairs = 500
  d4-plus unique (A,x) = 104
  d5 split = 52 plus / 52 minus
  second lifts = 26,624
  d5 product mismatches = 0
  universal product mismatches = 0
```

The larger 2026-06-22 p27 run confirms the same result:

```text
p27 train:
  sampled pairs = 1500
  d4-plus unique (A,x) = 368
  d5 split = 156 plus / 212 minus
  second lifts = 94,208
  d5 product mismatches = 0
  universal product mismatches = 0

p27 heldout:
  sampled pairs = 1500
  d4-plus unique (A,x) = 360
  d5 split = 166 plus / 194 minus
  second lifts = 92,160
  d5 product mismatches = 0
  universal product mismatches = 0
```

## Interpretation

Positive:

```text
The conic-chain tower has a repeated Kummer selector, not an unrelated new
quartic at each step.
The d4 formula was not an isolated accident; d5 follows the same transition
identity after the d4 root is present.
This gives a concrete recursive tower object for CAS/expert work.
```

Negative:

```text
The selected two-step coordinate still does not re-enter the original legal
label-2/compactD source in q1607/q1847/q2087.
So the path to beating sqrt is not direct iteration of the original legal
source; it must be a legal pullback/quotient/source for the tower itself.
```

## Next Tests

```text
1. Build a staged legal pullback for the tower variables:
   legal label-2/compactD source
   + first conic pair
   + Z0^2 = -(L0+a0)(L0-a0)c*r1
   + second conic pair
   + Z1^2 = -(L1+a1)(L1-a1)c*r2.

2. Compute dimension/genus/components or a quotient map for this tower over
   q7 or a p27-signature field.

3. Ask an expert/CAS agent whether the repeated divisor
   `-(L+a)(L-a)cR` is a known Kummer/Hilbert-90 boundary on an iterated
   conic bundle.

These tasks are now packaged as:
[P27 Conic Tower Quotient CAS Handoff](p27_conic_tower_quotient_cas_handoff_20260622.md).
```

## Continue / Kill

```text
continue = staged legal pullback/quotient for the repeated selector tower
continue = expert review of the Kummer/H90 interpretation

kill = direct legal-source reentry as the mechanism
kill = GPU production until a legal tower sampler or quotient exists
```

```text
p27_conic_pair_d5_tower_rows=1/1
```

Update: the legal-source depth screen is recorded in
[P27 Legal Conic Tower Depth](p27_legal_conic_tower_depth_20260621.md).  Lift
existence matches selected-prefix bits through depth 5, but p27 sample prefix
rates still thin roughly like ordinary selected gates.
