# P27 Conic-Pair Kummer-Z Relation Screen

Date: 2026-06-21

## Claim

Adjoining the first conic-pair Kummer selector root does not expose a cheap
two-coordinate quotient in the obvious coordinates.

The tested layer is:

```text
Z^2 = -(L+a)(L-a)cR
a = R - 1/R
```

on d4-plus roots over legal d3-plus conic-pair preimages.

Through total degree `20`, every tested pair system involving `Z` is full-rank
except `(A,Z)`.  The `(A,Z)` exception is not a Kummer-root relation: extracting
the basis shows the relation is univariate in `A`, and the `Z` relation is only
that same `A` polynomial multiplied by `Z`.

## Artifacts

Probes:

```text
research/p27/archive/gates/p27_conic_pair_kummer_z_relation_probe.py
research/p27/archive/gates/p27_conic_pair_kummer_az_relation_extract.py
research/p27/archive/gates/p27_conic_pair_kummer_a_projection_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_kummer_z_relation_probe_q607_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_kummer_z_relation_probe_q1607_q1847_q2087_deg14_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_kummer_z_relation_probe_q1607_q1847_q2087_deg16_20_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_kummer_az_relation_extract_q1607_q1847_q2087_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_kummer_a_projection_probe_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_kummer_z_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 2,4,6,8,10,12,14 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_kummer_z_relation_probe_q1607_q1847_q2087_deg14_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_kummer_z_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 16,18,20 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_kummer_z_relation_probe_q1607_q1847_q2087_deg16_20_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_kummer_az_relation_extract.py \
  --small-primes 1607,1847,2087 \
  --degrees 18,20 \
  --max-relations 3 \
  --max-terms 80 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_kummer_az_relation_extract_q1607_q1847_q2087_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_kummer_a_projection_probe.py \
  --small-primes 1607,1847,2087 \
  --auto-start 2200 \
  --auto-count 8 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_kummer_a_projection_probe_20260621.txt
```

## Z Coordinate Systems Tested

```text
(A,Z), (x,Z), (c,Z), (r,Z), (R,Z), (L,Z),
(R+1/R,Z), ((R-1/R)^2,Z),
(L+a^2/L,Z), (L-a^2/L,Z), ((L+a)(L-a),Z),
(R+1/R,Z/(L+a)), (R+1/R,Z/(L-a)), (R+1/R,Z/(cR)),
((R-1/R)^2,Z/(L+a)), ((R-1/R)^2,Z/(L-a)),
(L+a^2/L,Z/(L+a)), (L-a^2/L,Z/(L-a)).
```

## Results

For degrees `2,4,6,8,10,12,14`, all q1607/q1847/q2087 systems had:

```text
extra_nullity = 0
```

For degrees `16,18,20`, every system except `(A,Z)` again had:

```text
extra_nullity = 0
```

The repeated nonzero rows were:

```text
q1607 (A,Z) deg20:
  points = 604
  monomials = 231
  rank = 228
  nullity = 3

q1847 (A,Z) deg20:
  points = 598
  monomials = 231
  rank = 228
  nullity = 3

q2087 (A,Z) deg18:
  points = 570
  monomials = 190
  rank = 189
  nullity = 1

q2087 (A,Z) deg20:
  points = 570
  monomials = 231
  rank = 225
  nullity = 6
```

The extractor shows why this is not promoted.  The first q1607/q1847 degree-20
relation has:

```text
odd_z_terms = 0
max_Z_exp = 0
max_A_exp = 19
```

and the next relation is just the same polynomial multiplied by `Z`:

```text
odd_z_terms = 20
max_Z_exp = 1
```

q2087 similarly has a degree-18 univariate `A` relation and its `Z` multiple.

## A Projection Check

The univariate relation is explained by the finite A-projection of the selected
small-field rows.  The A count is not bounded; it is a small-field constant
fraction of `q`, with local sign degeneracies:

```text
q1607: d3_A=28, d4_A=19, d4_A/q=0.011823
q1847: d3_A=45, d4_A=19, d4_A/q=0.010287
q2087: d3_A=25, d4_A=18, d4_A/q=0.008625
q2239: d3_A=52, d4_A=26, d4_A/q=0.011612
q2287: d3_A=30, d4_A=30, d4_A/q=0.013118
q2311: d3_A=48, d4_A=48, d4_A/q=0.020770
q2351: d3_A=50, d4_A=35, d4_A/q=0.014887
q2383: d3_A=36, d4_A=24, d4_A/q=0.010071
```

This is not remotely small enough to imply a p27 source.  A p27 univariate
`A` projection at a comparable density would still be astronomical.

## Interpretation

Positive:

```text
The first Kummer root layer is now directly screened.
The apparent `(A,Z)` signal is explained rather than left ambiguous.
```

Negative:

```text
No cheap two-coordinate quotient was found after adjoining Z.
The only repeated relation is the univariate A-projection polynomial, not a
relation involving the Kummer root.
```

The live route is therefore narrower again: compute the staged legal tower
normalization/components, or find a named theorem for the repeated Kummer
divisor.  Do not spend more time on simple pair-coordinate relation screens
unless a new theorem suggests a specific coordinate.

## Continue / Kill

```text
continue = staged normalization/components of the legal conic/Kummer tower
continue = expert ask about the repeated divisor as a Kummer/Hilbert-90 boundary
continue = GPU telemetry for Dplus/conic/Kummer capture rates

kill = first-Z-layer simple pair quotient through degree 20
kill = interpreting the A-only projection polynomial as a Kummer source
kill = more unguided low-degree pair scans in this coordinate family
```

```text
p27_conic_pair_kummer_z_relation_rows=1/1
```
