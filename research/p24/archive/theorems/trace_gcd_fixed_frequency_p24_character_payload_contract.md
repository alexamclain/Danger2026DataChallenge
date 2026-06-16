# Fixed-Frequency p24 Character Payload Contract

Date: 2026-06-06

## Purpose

The 1092 p24 scalar equations are cheap only after the tower proof has already
produced the compressed H-coset sums.  This note records the exact finite
handoff:

```text
ordinary centering
+ six nontrivial order-7 L-valued character sums
<=> seven H-coset sums vanish.
```

This is the legitimate interface between the missing CM/Lang theorem and the
constant-size verifier.  It is not a license to compute the full
`156 x 210` mixed marginal by class-set enumeration.

## Setup

```text
p = 10^24 + 7
Gamma = (Z/211Z)^*
H = <2^7>, |H| = 30
Gamma/H ~= C_7
left coordinates = [F_p(mu_157):F_p] = 156
```

For one fixed left coordinate, let

```text
y_r = sum_{s in 2^r H} C(a,s),   r in Z/7Z.
```

The 1092 scalar verifier checks `y_r=0` for all `156` left coordinates and
all seven residues `r`.

Since `p = 1 mod 7`, choose `zeta_7 in F_p`.  The quotient Fourier transform is

```text
Y_k = sum_{r in Z/7Z} zeta_7^(k r) y_r,   k in Z/7Z.
```

The `7 x 7` character matrix has full rank over `F_p`.  Therefore

```text
all y_r = 0
<=> all Y_k = 0.
```

The `k=0` equation is exactly ordinary centering on the seven H-coset sums.
Thus, once centering is part of the construction, the actual nontrivial tower
payload is:

```text
Y_k = 0 for k=1,...,6.
```

Across the 156 left coordinates this is `6*156 = 936` scalar coordinates,
plus `156` centering coordinates, totaling the same `1092` scalar equations.

## Contract

A sub-sqrt p24 proof may use the 1092 verifier in either of these two forms:

```text
compressed form:
  provide the 156 x 7 matrix of H-coset sums and check it is zero;

character form:
  prove ordinary centering and prove the six L-valued nontrivial
  quotient-character sums vanish.
```

The character form is the live proof target because it matches the current
Gauss-normalized covariance-plus-descent theorem:

```text
S_chi = sum_a T_{1,0,a} R_{chi,-a} = 0
for all nontrivial chi on Gamma/H.
```

The theorem must produce these six `L`-valued zeros tower-natively.  A route
that first materializes `C(a,s)` for all `156*210 = 32760` marginal entries by
enumerating the CM class set does not give the requested asymptotic speedup,
even though the final scalar check would be small.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_character_payload_contract.py
```

Key output:

```text
character_matrix_rank=7
nontrivial_character_rank=6
nontrivial_plus_center_rank=7
six_nontrivial_L_equations_scalar_count=936
ordinary_centering_scalar_count=156
p24_scalar_equations=1092
ordinary_centering_plus_six_character_sums_equiv_h_coset_zero=1
full_marginal_materialization_is_not_a_subsqrt_certificate=1
omitting_centering_or_one_character_leaves_false_positives=1
```

The last line matters: six nontrivial character identities are sufficient only
with centering, and all six are needed.  Omitting either condition leaves
finite false positives.
