# p24 Admissible Jacobi Dual Conditions Gate

Date: 2026-06-07

## Point

The admissible Jacobi theorem is no longer only a rank-`621` membership
statement.  In Fourier coordinates on `C_7 x C_c`, the admissible C-axis
Jacobi-carry span is cut out by four explicit condition families in small exact
models.

For p24, `c = 179`, so the ambient Fourier space has dimension:

```text
7 * 179 = 1253.
```

The admissible span has dimension:

```text
621.
```

Equivalently, it is the solution space of `632` independent linear equations.

## Four Condition Families

Write Fourier coefficients as `F(a,b)`, where `a in C_7` is the right quotient
character and `b in C_179` is the `C/E` character.

The four families are:

```text
1. C/E-trivial, right-nontrivial vanishing:
   F(a,0) = 0, a = 1,...,6.

2. Nontrivial-right conjugate skew:
   F(a,b) + F(-a,-b) = 0,
   a = 1,...,6, b up to conjugate C/E pairs.

3. Right-trivial conjugate C/E pair sums:
   F(0,b) + F(0,-b) = lambda_c * F(0,0),
   b up to conjugate C/E pairs.

4. Three global right-pair balances:
   sum_{b>0} (F(-a,b) - F(a,b)) = 0,
   a = 1,2,3.
```

The scalar `lambda_c` depends on the chosen Fourier root normalization.  The
condition is intrinsic once that normalization is fixed.

For p24 the independent count is:

```text
6 + 6*89 + 89 + 3 = 632.
```

Thus:

```text
solution dimension = 1253 - 632 = 621.
```

## Consequence

The current proof target can be made more concrete:

```text
prove that the selected weighted trace-GCD packet satisfies these four
Fourier condition families after Tr_{B/C}.
```

This is sharper than asking for an unnamed admissible Jacobi decomposition. It
also gives computation a precise microscope:

```text
look for the source of conjugate skew,
identify the right-trivial pair-sum normalization,
and explain the three terminal global balances.
```

If these four families are proved for the selected packet, the existing formal
gates give:

```text
admissible span membership
=> no forbidden C_7^nontrivial x {C/E trivial} bidegrees
=> final internal trace zero
=> matching right coboundary
=> product coboundary
=> 1092 H-coset verifier equations.
```

The Lean companion records this formal path without pretending to prove the
CM producer theorem:

```text
p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate.py

lean p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean
```

Observed:

```text
dual_condition_matches=3/3
p24_conjugate_C_pair_count=89
p24_dual_condition_count=6+6*89+89+3=632
p24_dual_solution_dim=1253-632=621
```

No p24 class set or CM root enumeration is used.
