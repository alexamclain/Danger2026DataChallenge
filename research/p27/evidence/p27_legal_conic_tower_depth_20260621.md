# P27 Legal Conic Tower Depth

Date: 2026-06-21

## Claim

The legal conic-chain pullback is exactly the selected-prefix tower through
the tested depths.  This confirms the conic tower is the right source-side
object, but it does not by itself beat sqrt on the original legal source.

Depth `d` of the legal conic pullback corresponds to the selected gate
`d_{d+2}`:

```text
depth 1 -> d3 plus
depth 2 -> d4 plus after d3
depth 3 -> d5 plus after d3,d4
depth 4 -> d6 plus after d3,d4,d5
```

In q1607/q1847/q2087, lift existence matched the selected-prefix indicator
for every legal candidate through depth 4.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_legal_conic_tower_depth_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_legal_conic_tower_depth_probe_q1607_q1847_q2087_p27_depth4_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_legal_conic_tower_depth_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 4 \
  --p27-target 1000 \
  --p27-heldout-target 1000 \
  --p27-max-draws 1000000 \
  | tee research/p27/archive/probe_outputs/p27_legal_conic_tower_depth_probe_q1607_q1847_q2087_p27_depth4_20260621.txt
```

## Guard-Field Results

```text
q1607:
  depth1 lift candidates = 448/784
  depth2 lift candidates = 304/784
  depth3 lift candidates = 304/784
  depth4 lift candidates = 0/784
  depth1/2/3/4 prefix mismatches = 0

q1847:
  depth1 lift candidates = 720/1008
  depth2 lift candidates = 304/1008
  depth3 lift candidates = 0/1008
  depth4 lift candidates = 0/1008
  depth1/2/3/4 prefix mismatches = 0

q2087:
  depth1 lift candidates = 400/912
  depth2 lift candidates = 288/912
  depth3 lift candidates = 288/912
  depth4 lift candidates = 288/912
  depth1/2/3/4 prefix mismatches = 0
```

Lift multiplicity grows by a factor of `8` per added conic step on candidates
that remain alive:

```text
depth1 average lifts per lifted candidate = 32
depth2 average lifts per lifted candidate = 256
depth3 average lifts per lifted candidate = 2048
depth4 average lifts per lifted candidate = 16384
```

This is useful for modeling the tower, but it is not a source-density win by
itself.

## P27 Sample Results

On actual p27 legal-source samples, the selected prefix rates are:

```text
p27 train, 1000 unique (A,x):
  depth1/d3 rate = 0.484
  depth2/d4 rate = 0.244
  depth3/d5 rate = 0.098
  depth4/d6 rate = 0.058

p27 heldout, 1000 unique (A,x):
  depth1/d3 rate = 0.526
  depth2/d4 rate = 0.232
  depth3/d5 rate = 0.108
  depth4/d6 rate = 0.058
```

So p27 itself does not show the constant-tail behavior seen in some small
fields.  It still thins roughly like a sequence of selected half-gates.

## Interpretation

Positive:

```text
The legal conic-chain pullback is exact through depth 4 in guard fields.
The repeated selector tower is the correct mathematical object to hand to CAS
or an expert.
The finite-field lift multiplicity is regular enough to model.
```

Negative:

```text
On the original legal source, the p27 prefix rates still look like ordinary
successive halving.
The tower does not beat sqrt until we find a quotient, recurrence, or direct
sampler for the tower itself.
```

## Next Tests

```text
1. Staged Magma/Sage pullback:
   avoid #Points on the large intermediate scheme;
   compute dimension/components/genus for the legal tower through depth 2 or 3.

2. Quotient search:
   use the repeated selector divisor
   Z_j^2=-(L_j+a_j)(L_j-a_j)c*r_{j+1}
   to look for a low-genus quotient of the tower.

3. GPU boundary:
   only use GPU for telemetry or for a legal tower sampler/quotient.
   The original legal source plus conic tower still thins at p27.
```

## Continue / Kill

```text
continue = staged CAS/legal tower quotient
continue = expert review of the repeated Kummer selector tower

kill = claiming sqrt-beating from legal depth-lift existence alone
kill = raw GPU production from the original legal source without a quotient
```

```text
p27_legal_conic_tower_depth_rows=1/1
```

Update: the raw `(R,L)` plane-curve shortcut is now screened and negative.
See [P27 Conic-Pair Low-Degree Relation Screen](p27_conic_pair_lowdegree_relation_20260621.md):
no total-degree relation `<=20` on q1607/q1847/q2087 legal d3-plus preimages.
