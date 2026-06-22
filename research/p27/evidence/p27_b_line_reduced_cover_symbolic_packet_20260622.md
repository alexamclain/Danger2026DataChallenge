# P27 B-Line Reduced-Cover Symbolic Packet

Date: 2026-06-22

## Claim

The reduced B-line d3 cover has an explicit symbolic handoff that avoids the
heavier reverse `z,Y` source.

Let `x5` be the current selected x-coordinate and let:

```text
Unext = x6 + 1/x6
```

for the next halving branch.  Then:

```text
(Unext - 2*x5)^2 = 4*(x5^2 + A*x5 + 1)
```

and the selected squareclass is:

```text
f3 = chi(Unext + 2)
```

The packet writes this equation in the existing B-line source variables
`X,W,T,beta,R,eta,Bline,Unext` so CAS can normalize the reduced 4-u cover over
`P1_Bline`.

## Artifacts

Generator:

```text
research/p27/archive/gates/p27_b_line_reduced_cover_symbolic_packet.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_symbolic_packet_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_reduced_cover_symbolic_packet.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_cover_symbolic_packet_20260622.txt
```

## Reduced Equation

The packet emits:

```text
eta_branch
E_W
T_cover
compactD_R
Bline_relation
first_half_beta
reduced_Unext
```

where the reduced equation is printed in compact named form:

```text
reduced_Unext =
  A_den*(Unext*U_den - x5_num)^2
  - (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2)
```

with:

```text
x5 = x5_num / x5_den
x5_den = 2*U_den
A = A_num / A_den
selector = Unext + 2
optional materialization: x6^2 - Unext*x6 + 1 = 0
```

## Validation

The guard-field validation checks the reduced equation and selector on all
enumerated legal branches:

```text
q1607:
  d2_plus_candidates = 784
  validated_branches = 1568
  A_B_identity_mismatch = 0
  reduced_equation_mismatch = 0
  selector_mismatch = 0

q1847:
  d2_plus_candidates = 1008
  validated_branches = 2016
  A_B_identity_mismatch = 0
  reduced_equation_mismatch = 0
  selector_mismatch = 0

q2087:
  d2_plus_candidates = 912
  validated_branches = 1824
  A_B_identity_mismatch = 0
  reduced_equation_mismatch = 0
  selector_mismatch = 0
```

## Interpretation

Positive:

```text
The reduced 4-u cover is now an explicit symbolic CAS target.
It removes the reverse z/Y materialization from the first normalization pass.
It preserves the exact f3 selector as chi(Unext+2).
```

Negative:

```text
This is not yet a sampler or proof of low genus.
The prior reduced-fiber relation screen still kills visible plane models
through degree 20.
Promotion requires normalization/genus/quotient output from this symbolic
cover.
```

## Continue / Kill

```text
continue = run CAS normalization of the reduced_Unext cover over P1_Bline
continue = compute genus/components/quotients and compare against the fixture
continue = only then pull back f4/f3

kill = full reverse z/Y normalization as the first CAS attempt if reduced_Unext is feasible
kill = GPU production before reduced-cover genus/sourceability is known
```

```text
p27_b_line_reduced_cover_symbolic_packet_rows=1/1
```
