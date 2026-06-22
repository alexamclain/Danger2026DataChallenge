# P27 Conic-Pair Two-Step Kummer Trivariate Screen

Date: 2026-06-21

## Claim

The obvious three-coordinate surfaces in the two-step conic-pair Kummer tower
also do not expose a low-degree quotient.

This extends the pair screen from
[P27 Conic-Pair Two-Step Kummer Screen](p27_conic_pair_two_step_kummer_20260621.md).
After adjoining:

```text
Z0^2 = -(L0+a0)(L0-a0)c*r1
S1   = -(L1+a1)(L1-a1)c*r2
Z1^2 = S1, when S1 is square
```

all screened selector and root triples over q1607/q1847/q2087 were full-rank
through total degree `6`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_two_step_kummer_trivar_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_trivar_probe_q607_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_trivar_probe_q1607_q1847_q2087_deg6_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_two_step_kummer_trivar_probe.py \
  --small-primes 607 \
  --degrees 2 \
  --root-degrees 2 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_trivar_probe_q607_smoke_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_two_step_kummer_trivar_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 2,4,6 \
  --root-degrees 2,4,6 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_trivar_probe_q1607_q1847_q2087_deg6_20260621.txt
```

## Systems Tested

Selector triples:

```text
(A,Z0,S1), (A,R0,S1), (A,R1,S1), (A,L0,S1), (A,L1,S1),
(Z0,R0,S1), (Z0,R1,S1), (Z0/(L0+a0),Z0/(L0-a0),S1),
(Z0/(L0+a0),Z0/(cR0),S1), (L0,L1,S1)
```

Root triples:

```text
(A,Z0,Z1), (A,Z1/Z0,Z0*Z1), (A,Z0,Z1/Z0),
(R0,Z0,Z1), (R1,Z0,Z1),
(A,Z0/(L0+a0),Z1/(L1+a1)),
(A,Z0/(L0-a0),Z1/(L1-a1)),
(A,Z0/(cR0),Z1/(cR1))
```

## Results

At degrees `2,4,6`, every nonempty selector and root system over
q1607/q1847/q2087 had:

```text
extra_nullity = 0
```

Representative row sizes:

```text
q1607:
  selector_rows=38912
  root_rows=77824
  largest transform_unique=9696

q1847:
  selector_rows=38912
  root_rows=0
  largest selector transform_unique=9728

q2087:
  selector_rows=36864
  root_rows=73728
  largest transform_unique=9216
```

The `q607` smoke again has no active two-step layer, matching the pair screen.

## Interpretation

This does not prove the repeated Kummer tower is generic, but it kills the next
cheap bucket-search idea after pair relations: small trivariate surfaces in
`A`, `R_j`, `L_j`, `S1`, `Z0`, `Z1`, normalized roots, ratios, and products.

The next plausible sqrt-beating work remains:

```text
1. staged legal-pullback normalization/components,
2. direct E/E' double-cover divisor/Kummer class extraction,
3. a theorem-level repeated Kummer/Hilbert-90 identity.
```

```text
p27_conic_pair_two_step_kummer_trivar_rows=1/1
```
