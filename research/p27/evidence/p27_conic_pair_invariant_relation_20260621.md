# P27 Conic-Pair Invariant Relation Screen

Date: 2026-06-21

## Claim

The legal d3-plus conic-pair preimages do not lie on a small low-degree plane
curve after the obvious involution-friendly coordinate changes.

This extends the raw `(R,L)` negative screen.  It tests the natural quotient
coordinates suggested by the conic-pair sampler and repeated Kummer selector:

```text
a = R - 1/R
s = R + 1/R
m = L + a^2/L
n = L - a^2/L
w = (L+a)(L-a) = L^2-a^2
```

In q1607/q1847/q2087, every tested pair system had zero stable extra nullity
through total degree `20`, after subtracting nullity forced by finite
interpolation.  The lone exception was a degree-20 q1607-only artifact in
`(a^2,m)` and `(a^2,n)`; it did not repeat in q1847 or q2087 and is not
promoted.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_invariant_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_invariant_relation_probe_q1607_q1847_q2087_deg14_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_invariant_relation_probe_q1607_q1847_q2087_deg16_20_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_invariant_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --pair-degrees 2,4,6,8,10,12,14 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_invariant_relation_probe_q1607_q1847_q2087_deg14_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_invariant_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --pair-degrees 16,18,20 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_invariant_relation_probe_q1607_q1847_q2087_deg16_20_20260621.txt
```

## Coordinate Systems Tested

```text
A_x       = target coordinates (A, x)
c_r       = signed conic coordinates (c, r)
r_d       = conic half-sum/half-difference coordinates (r, d)
s_m       = (R+1/R, L+a^2/L)
s_n       = (R+1/R, L-a^2/L)
a2_m      = ((R-1/R)^2, L+a^2/L)
a2_n      = ((R-1/R)^2, L-a^2/L)
s_w       = (R+1/R, (L+a)(L-a))
a2_w      = ((R-1/R)^2, (L+a)(L-a))
s_lsym    = (R+1/R, L+1/L)
s_lanti   = (R+1/R, L-1/L)
m_n       = (L+a^2/L, L-a^2/L)
```

For each system, the probe computes the rank of the total-degree monomial
matrix on unique transformed points.  It reports:

```text
extra_nullity = nullity - max(0, monomials - unique_points)
```

so that ordinary interpolation forced by too few unique points is not counted
as structure.

## Results

For degrees `2,4,6,8,10,12,14`, every pair system in q1607/q1847/q2087 had:

```text
extra_nullity = 0
```

For degrees `16,18,20`, every pair system in q1847/q2087 again had:

```text
extra_nullity = 0
```

The only nonzero extra-nullity rows were local to q1607:

```text
q1607 a2_m deg20:
  monomials = 231
  rank = 222
  nullity = 9
  forced = 7
  extra = 2

q1607 a2_n deg20:
  monomials = 231
  rank = 222
  nullity = 9
  forced = 7
  extra = 2
```

They do not repeat in q1847:

```text
q1847 a2_m deg20: rank = 231, extra = 0
q1847 a2_n deg20: rank = 231, extra = 0
```

or q2087:

```text
q2087 a2_m deg20: rank = 200, forced = 31, extra = 0
q2087 a2_n deg20: rank = 200, forced = 31, extra = 0
```

## Interpretation

This kills the next easiest quotient source after raw `(R,L)`: a low-degree
plane relation in the obvious symmetric coordinates of the conic-pair sampler.

The repeated Kummer tower is still live, but the next test needs to retain
tower variables such as the selector roots:

```text
Z_j^2 = -(L_j+a_j)(L_j-a_j)c*r_{j+1}
```

or compute a genuine staged pullback/normalization.  Another low-degree plane
screen in simple two-coordinate quotients is now low priority.

## Continue / Kill

```text
continue = staged tower pullback with Z_j variables
continue = Magma/Sage normalization or quotient search on the legal pullback
continue = GPU telemetry only for conic/Kummer/Dplus structure at scale

kill = raw (R,L) plane-curve source
kill = obvious invariant pair plane-curve source through degree 20
kill = treating q1607-only degree-20 artifacts as a promoted lead
```

```text
p27_conic_pair_invariant_relation_rows=1/1
```
