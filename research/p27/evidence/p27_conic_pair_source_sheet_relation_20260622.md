# P27 Conic-Pair Source-Sheet Relation Screen

Date: 2026-06-22

## Claim

Adding the actual residual source sheets `X,W,T` to the B-enhanced conic-pair
staging surface does not expose a cheap direct legal pullback.

The only stable low-degree relations are inherited:

```text
B-line staging surface:  m^2*(B^2+s^2-4) = 4*s^2*(s^2-4)
source elliptic sheet:   W^2 = X^3 - X
source T-cover:          T^2 = X*(X^2+1)*(X^2+2X-1)
B-line quotient:         B = 8*X^2/(X^2-1)^2
```

No screened source/conic coordinate system gives a new low-degree relation
that would turn the staged surface into a below-sqrt sampler.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_source_sheet_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_source_sheet_relation_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_conic_pair_source_sheet_relation_probe_q1607_q1847_q2087_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_conic_pair_source_sheet_relation_probe.py \
  --small-primes 607 \
  --pair-degrees 4,8 \
  --triple-degrees 4 \
  --quad-degrees 4 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_source_sheet_relation_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_conic_pair_source_sheet_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --pair-degrees 4,8,12,16 \
  --triple-degrees 4,8,12 \
  --quad-degrees 4,6,8 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_source_sheet_relation_probe_q1607_q1847_q2087_20260622.txt
```

## Rows

The probe joins legal `d3=+1` source sheets to their conic-pair preimages.

```text
q1607: d3plus_Ax=112, d3plus_source_rows=448, joined_rows=7168
q1847: d3plus_Ax=180, d3plus_source_rows=720, joined_rows=11520
q2087: d3plus_Ax=100, d3plus_source_rows=400, joined_rows=6400
```

## Negative Screens

Pair projections with one source sheet and one conic/staging coordinate are
full rank through total degree `16` in all three guard fields:

```text
(X,s), (X,m), (X,R), (X,L), (W,s), (T,s), (B,s), (K,s)
```

The raw source/conic triple is full rank through total degree `12`:

```text
(X,R,L): extra_nullity=0 in q1607/q1847/q2087
```

The source-sheet staged triples with `W` or `T` are also full rank through
total degree `12`:

```text
(W,s,m): extra_nullity=0 in q1607/q1847/q2087
(T,s,m): extra_nullity=0 in q1607/q1847/q2087
```

The direct `(X,s,m)` pullback has no relation through degree `8`; degree-12
relations are weak/inconsistent and look like the cleared-denominator
pullback of the known B-staging surface, not a new selector:

```text
q1607 (X,s,m): deg8 extra=0, deg12 extra=21
q1847 (X,s,m): deg8 extra=0, deg12 extra=1
q2087 (X,s,m): deg8 extra=0, deg12 extra=9
```

## Inherited Relations

The known `(B,s,m)` relation appears in all guard fields:

```text
q1607/q1847/q2087 (B,s,m):
  deg4 extra=1, relation_terms=5
```

The four-variable systems expose inherited bookkeeping:

```text
(X,W,s,m): source elliptic relation, relation_terms=3
(X,T,s,m): source T-cover relation, relation_terms=5
(X,B,s,m): B-staging surface first; B(X) relation only at higher degree
(X,s,m,w): derived w/staging relation, relation_terms=9
```

These are useful CAS checks, but they do not select the sparse legal B-domain
or provide a new source law.

## Interpretation

Positive:

```text
The conic-pair staging equation is stable after joining to source sheets.
The probe cleanly separates inherited source/staging relations from possible
new pullback relations.
```

Negative:

```text
No low-degree source-sheet relation makes the legal pullback directly
sampleable.
The staged surface plus X/W/T does not beat the same legal-B denominator.
GPU production from this coordinate remains unjustified.
```

## Continue / Kill

```text
continue = offline CAS normalization of the staged surface plus legal cover
continue = factor out inherited E/T/B/staging relations before testing a new quotient
continue = add Kummer selector roots only after the legal pullback is normalized

kill = direct GPU sampler from (X,s,m), (X,R,L), (W,s,m), or (T,s,m)
kill = treating inherited source-cover equations as a sqrt-beating relation
kill = broad source-sheet relation scans without a named quotient/class target
```

```text
p27_conic_pair_source_sheet_relation_rows=1/1
```
