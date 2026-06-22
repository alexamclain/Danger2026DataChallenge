# P27 Conic-Pair B/K-Enhanced Pullback Screen

Date: 2026-06-22

## Claim

Adding the legal B/K source coordinates to the conic-pair sampler exposes one
useful staged pullback equation, but not a source sampler.

The raw conic-pair preimage screens in `(R,L)` and obvious invariant
coordinates were negative.  This screen keeps the legal source coordinate

```text
B = 8*X^2/(X^2 - 1)^2
K = x([2]P) on E': V^2 = U^3 + 4U
```

alongside conic-pair sampler invariants.  The only stable relations found in
q1607/q1847/q2087 are:

```text
B^2 + c^2 = 4

m^2*(B^2 + s^2 - 4) = 4*s^2*(s^2 - 4)
```

where `s=R+1/R` and `m=L+a^2/L` with `a=R-1/R`.

The first equation is the expected overlap of `A=B^2-2` and `A=2-c^2`.
The second is useful as a staged legal-pullback coordinate, but it is still a
surface equation over the already sparse legal B-domain.  It does not by
itself give a below-sqrt sampler.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_b_enhanced_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_b_enhanced_relation_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_conic_pair_b_enhanced_relation_probe_q1607_q1847_q2087_deg12_20260622.txt
research/p27/archive/probe_outputs/p27_conic_pair_b_enhanced_relation_extract_q1607_q1847_q2087_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_b_enhanced_relation_probe.py \
  --small-primes 607 \
  --pair-degrees 2,4 \
  --triple-degrees 2 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_b_enhanced_relation_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_b_enhanced_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --pair-degrees 2,4,6,8,10,12 \
  --triple-degrees 2,4,6 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_b_enhanced_relation_probe_q1607_q1847_q2087_deg12_20260622.txt
```

The relation-extraction output records the stable coefficient vectors.

## Systems Tested

Pair systems:

```text
(B,R), (B,L), (B,s), (B,m), (B,n), (B,w), (B,c), (B,r),
(K,R), (K,L), (K,s), (K,m), (S,R), (S,L)
```

Triple systems:

```text
(B,R,L), (B,s,m), (B,c,r), (B,s,w),
(K,R,L), (K,s,m), (S,R,L)
```

The `S` coordinate is not single-valued on these rows in the current grouping,
so all `S` systems degenerate in the screen.

## Results

Base row counts:

```text
q1607:
  d3plus_targets = 112
  target_preimage_rows = 1792
  unique_preimage_rows = 1792

q1847:
  d3plus_targets = 180
  target_preimage_rows = 2880
  unique_preimage_rows = 2880

q2087:
  d3plus_targets = 100
  target_preimage_rows = 1600
  unique_preimage_rows = 1600
```

Full-rank negatives:

```text
(B,R), (B,L), (B,s), (B,m), (B,n), (B,w), (B,r)
(K,R), (K,L), (K,s), (K,m)
(B,R,L), (K,R,L), (K,s,m)
```

all have no extra nullity through the screened degrees.

Stable relations:

```text
(B,c):     B^2 + c^2 - 4 = 0
(B,c,r):   same relation, independent of r
(B,s,m):   m^2*(B^2 + s^2 - 4) - 4*s^2*(s^2 - 4) = 0
```

There is also a stable degree-6 relation in `(B,s,w)`, where
`w=L^2-a^2`.  With `1/4` interpreted in the field, it is:

```text
-64 + 16w - w^2 + 32s^2 + 16B^2
-4s^2w -4B^2w + (1/4)s^2w^2 -4s^4
+ (1/4)B^2w^2 -8B^2s^2 + B^2s^2w + B^2s^4 = 0
```

This appears derived from the same staged conic identities.  It is useful
bookkeeping, not a separate sampler.

## Interpretation

Positive:

```text
The B-enhanced conic pullback has a stable low-degree staging equation.
This gives CAS a smaller named surface:
  m^2*(B^2+s^2-4) = 4*s^2*(s^2-4)
instead of the raw R,L sampler.
```

Negative:

```text
No low-degree relation appears in (B,R), (B,L), (K,R), (K,L), or (B,R,L).
The found equations do not select the sparse legal B-domain.
They do not reduce the source denominator enough to justify GPU production.
```

So the next legal-pullback test is not another bucket scan.  It is to use the
`(B,s,m)` equation as a staging coordinate and then add the legal B-cover /
next Kummer selector, asking for components, genus, or a sourceable quotient.

## Continue / Kill

```text
continue = staged CAS over the surface m^2*(B^2+s^2-4)=4*s^2*(s^2-4)
continue = add the legal B-domain and next selector root to this staged model
continue = compare against the B-line Kummer class sequence f3(B), f4(B), ...

kill = B/K-enhanced GPU buckets from (B,R), (B,L), (K,R), or (K,L)
kill = interpreting B^2+c^2=4 as a new source
kill = treating the (B,s,m) surface alone as below-sqrt
```

```text
p27_conic_pair_b_enhanced_pullback_rows=1/1
```
