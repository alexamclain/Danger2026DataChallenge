# P27 Conic-Pair Two-Step Kummer Screen

Date: 2026-06-21

## Claim

Two consecutive conic-pair Kummer selector layers do not expose a cheap
low-degree two-coordinate quotient in the obvious tower coordinates.

The screened tower is:

```text
Z0^2 = -(L0+a0)(L0-a0)c*r1
S1   = -(L1+a1)(L1-a1)c*r2
Z1^2 = S1, when S1 is square
```

Selector-value rows and second-root rows were full-rank through total degree
`12` over the p27-signature guard fields `q=1607`, `q=1847`, and `q=2087`.
The `q=1847` second-root family is empty in this local field because the next
selector is all nonsquare there; its selector-value rows were still tested and
also showed no extra nullity.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_two_step_kummer_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_probe_q607_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_probe_q1607_q1847_q2087_deg8_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_probe_q1607_q1847_q2087_deg10_12_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_two_step_kummer_probe.py \
  --small-primes 607 \
  --degrees 2,4 \
  --root-degrees 2 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_probe_q607_smoke_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_two_step_kummer_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 2,4,6,8 \
  --root-degrees 2,4,6,8 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_probe_q1607_q1847_q2087_deg8_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_two_step_kummer_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 10,12 \
  --root-degrees 10,12 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_two_step_kummer_probe_q1607_q1847_q2087_deg10_12_20260621.txt
```

## Systems Tested

Selector-value systems:

```text
(A,S1), (Z0,S1), (Z0/(L0+a0),S1), (Z0/(L0-a0),S1),
(Z0/(cR0),S1), (R0,S1), (R1,S1), (a0,S1), (a1,S1),
(L0,S1), (L1,S1), (w0,S1), (w1,S1)
```

Root systems:

```text
(A,Z1), (Z0,Z1), (Z0/(L0+a0),Z1/(L1+a1)),
(Z0/(L0-a0),Z1/(L1-a1)), (Z0/(cR0),Z1/(cR1)),
(A,Z1/Z0), (A,Z0*Z1), (R0,Z1), (R1,Z0)
```

## Results

Base row counts:

```text
q1607:
  d3_plus_Ax=112
  d4_plus_first_lifts=2432
  selector_rows=38912
  d5_plus_second_lifts=19456
  root_rows=77824

q1847:
  d3_plus_Ax=180
  d4_plus_first_lifts=2432
  selector_rows=38912
  d5_minus_second_lifts=19456
  root_rows=0

q2087:
  d3_plus_Ax=100
  d4_plus_first_lifts=2304
  selector_rows=36864
  d5_plus_second_lifts=18432
  root_rows=73728
```

For every nonempty selector and root system at degrees `2,4,6,8,10,12`:

```text
extra_nullity = 0
```

The `q607` smoke has no active two-step layer:

```text
d3_plus_Ax=64
d4_minus_first_lifts=2048
d4_plus_first_lifts=0
selector_rows=0
root_rows=0
```

## Interpretation

This kills the nearest "maybe two Kummer roots reveal a plane quotient" route.
It rules out the obvious low-degree pairs involving `S1`, `Z0`, `Z1`,
normalized roots, root ratios, and root products through degree `12` on the
promotion guard fields.

The conic-chain tower remains exact, but the live route is now staged
normalization/component work or a theorem-level repeated Kummer/Hilbert-90
identity.  GPU should not search buckets in these simple two-step coordinates
unless a new theorem-specified coordinate is supplied.

```text
p27_conic_pair_two_step_kummer_rows=1/1
```
