# P27 BSM Next-Selector Relation Screen

Date: 2026-06-22

## Claim

The staged BSM surface does not visibly control the next selected gate.

The surface

```text
m^2*(B^2+s^2-4) = 4*s^2*(s^2-4)
```

already captures canonical `d3+` rows after restricting to legal `B`.  A
sqrt-beating BSM route would need the same staged object to control more than
one selected half-gate.  This screen therefore tests whether `d4+` after
`d3+` satisfies any additional low-degree relation in `(B,s)`, `(B,m)`,
`(s,m)`, or `(B,s,m)`.

Result: in q1607/q1847/q2087, `d4+` has no extra relation beyond the inherited
BSM equation in the screened degrees.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_bsm_next_selector_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_bsm_next_selector_relation_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_bsm_next_selector_relation_probe_q1607_q1847_q2087_pair12_triple4_20260622.txt
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_bsm_next_selector_relation_probe.py \
  --small-primes 607 \
  --pair-degrees 2,4 \
  --triple-degrees 2,4 \
  | tee research/p27/archive/probe_outputs/p27_bsm_next_selector_relation_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_bsm_next_selector_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --pair-degrees 2,4,6,8,10,12 \
  --triple-degrees 2,4 \
  | tee research/p27/archive/probe_outputs/p27_bsm_next_selector_relation_probe_q1607_q1847_q2087_pair12_triple4_20260622.txt
```

## Results

The BSM fiber over target B values is uniform:

```text
q1607:
  d3+ B = 28, rows = 896
  d4+ B = 19, rows = 608
  d4- B = 9, rows = 288
  rows per active B = 32

q1847:
  d3+ B = 45, rows = 1440
  d4+ B = 19, rows = 608
  d4- B = 26, rows = 832
  rows per active B = 32

q2087:
  d3+ B = 25, rows = 800
  d4+ B = 18, rows = 576
  d4- B = 7, rows = 224
  rows per active B = 32
```

Pair systems:

```text
systems = (B,s), (B,m), (s,m)
degrees = 2,4,6,8,10,12
fields = q1607, q1847, q2087
result = d4plus_minus_d3 is always 0
```

Triple system:

```text
system = (B,s,m)
degrees = 2,4
fields = q1607, q1847, q2087
degree 2: no extra relation
degree 4: legal_extra = d3_extra = d4plus_extra = d4minus_extra = 1
```

The degree-4 triple relation is exactly the inherited BSM surface equation.
It is shared by the legal surface, `d3+`, `d4+`, and `d4-`, so it does not
select the next gate.

Some high-degree extras appear for the smaller `d4-` subset in q1607/q2087
pair systems, but they are not stable across fields and do not help the
all-plus `d4+` target.

## Interpretation

Positive:

```text
The staged BSM surface remains a clean exact model with uniform target fibers.
It is still a useful CAS coordinate if combined with an actual legal B-cover
or extracted B-line Kummer class.
```

Negative:

```text
The BSM surface does not add a visible next-selector law for d4+.
It does not couple d3 and d4 in the screened coordinates.
It therefore does not provide a direct below-sqrt sampler or GPU route.
```

This sharpens the BSM lane:

```text
use BSM only after the legal B-cover or f3(B) class is named;
do not continue low-degree relation scans on the raw/legal BSM surface.
```

Update:
[P27 BSM Halving-Cover Identity](p27_bsm_halving_cover_identity_20260622.md)
further demotes the lane.  BSM is algebraically the same as the known
one-step halving cover: `x=m^2/16` and `z=s^2` turn the BSM equation into a
quadratic in `z` with discriminant `16*(x^2+A*x+1)`.  It should now be treated
as notation for inherited halving structure unless an added selector creates a
new quotient.

## Continue / Kill

```text
continue = BSM as CAS staging after B-line f3 extraction
continue = legal-cover/function-field normalization if a CAS system can handle it
continue = compare any named BSM quotient against the B-line fixture rows
continue = only with a non-inherited selector beyond x square and d square

kill = BSM next-selector low-degree relation in (B,s), (B,m), (s,m), (B,s,m)
kill = GPU sampling of legal-B-restricted BSM for d4+
kill = treating the inherited BSM equation as multi-gate coupling
kill = BSM as an independent first-class moonshot lane
```

```text
p27_bsm_next_selector_relation_rows=1/1
```
