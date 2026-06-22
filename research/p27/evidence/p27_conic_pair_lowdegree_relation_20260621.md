# P27 Conic-Pair Low-Degree Relation Screen

Date: 2026-06-21

## Claim

The legal d3-plus preimages inside the free conic-pair sampler do not lie on a
small obvious plane curve in raw `(R,L)` coordinates.

For q1607/q1847/q2087, the sampler preimages of legal d3-plus `(A,x5)` classes
have no nonzero polynomial relation of total degree `<= 20` in `(R,L)`.

This is a negative result for the easiest quotient/source hope:

```text
kill = "legal pullback is a low-degree plane curve in raw R,L"
continue = use the repeated Kummer tower variables or a non-plane quotient
```

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_lowdegree_relation_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_conic_pair_lowdegree_relation_probe_q1607_q1847_q2087_deg20_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_lowdegree_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 4,6,8,10,12,14,16,18,20 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_lowdegree_relation_probe_q1607_q1847_q2087_deg20_20260621.txt
```

## Results

```text
q1607:
  legal d3-plus classes = 112
  sampler d3-plus preimages = 1,792
  degree <=20 monomials = 231
  rank = 231
  nullity = 0

q1847:
  legal d3-plus classes = 180
  sampler d3-plus preimages = 2,880
  degree <=20 monomials = 231
  rank = 231
  nullity = 0

q2087:
  legal d3-plus classes = 100
  sampler d3-plus preimages = 1,600
  degree <=20 monomials = 231
  rank = 231
  nullity = 0
```

All lower tested degrees `4,6,8,10,12,14,16,18` also had nullity `0`.

As a control, the sampler still has zero d3-minus legal preimages in these
fields, matching the earlier incidence screen.

## Interpretation

The legal subset is not captured by a small raw plane relation in `(R,L)`.
This explains why the free two-dimensional sampler has a `constant/q` legal
hit rate: the useful source is not visible as a low-degree plane equation in
these coordinates.

The result does not kill the conic/Kummer tower.  It narrows the next search:
look for a quotient or source in the tower coordinates including the repeated
selector roots:

```text
Z_j^2 = -(L_j+a_j)(L_j-a_j)c*r_{j+1}.
```

## Next Tests

```text
1. Staged CAS quotient:
   build the legal pullback with R,L and Z_j variables, then ask for
   dimension/components/genus without projecting to a raw R,L plane curve.

2. Structured quotient search:
   test low-degree relations in invariants such as R+1/R, L+1/L,
   (L+a)(L-a), or the Kummer selector roots, rather than raw R,L.

3. Expert ask:
   is the repeated divisor -(L+a)(L-a)cR a known Kummer/Hilbert-90 boundary
   on an iterated conic bundle?
```

## Continue / Kill

```text
continue = non-plane quotient/source search in repeated Kummer tower variables
continue = CAS normalization of the legal tower pullback

kill = raw low-degree plane-curve sampler in R,L up to degree 20
kill = GPU production from random R,L
```

```text
p27_conic_pair_lowdegree_relation_rows=1/1
```
