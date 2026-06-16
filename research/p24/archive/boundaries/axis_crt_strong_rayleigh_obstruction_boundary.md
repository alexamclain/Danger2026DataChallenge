# Axis CRT Strong-Rayleigh Obstruction Boundary

Date: 2026-06-06

This note closes a sharper version of the CS/probability shortcut for the
current p24 trace-frame theorem.

## Tempting Shortcut

The selected-origin CRT-axis Cauchy-Binet support is the basis set of the
complete multipartite incidence matroid with parts:

```text
2, 157, 211.
```

Since matroid basis polynomials have strong Hodge/Lorentzian structure, it is
tempting to hope for a probability-theory certificate:

```text
negative dependence / strong Rayleigh / real stability
  => no cancellation of the weighted Plucker expansion
  => det(T_lead) is a p-unit.
```

The live determinant is:

```text
P(lambda) = det(A diag(lambda) B)
          = sum_U Delta_A(U) Delta_B(U) prod_{u in U} lambda_u,
```

where the support is the CRT-axis hypertree matroid but the coefficients are
mixed Plucker weights and the evaluation point is the cyclotomic CM vector
`lambda = Lambda_CM`.

## Exact Small Obstruction

I added:

```text
p24/axis_crt_strong_rayleigh_obstruction_toy.py
```

For a multiaffine basis generating polynomial

```text
B(x) = sum_{basis U} prod_{u in U} x_u,
```

strong Rayleigh implies every Rayleigh difference

```text
partial_i B * partial_j B - B * partial_i partial_j B
```

is nonnegative at every positive real weight vector.

The script constructs the abstract multipartite incidence matroid directly.
It first reports that the smallest tripartite all-ones check is positive:

```text
parts = (2,2,2)
edges = 8
rank = 4
bases = 58
min_rayleigh_delta = 87
```

So ordinary all-ones balancedness is not the obstruction.

But the next small tripartite analogue has an exact positive integer weighted
Rayleigh violation:

```text
parts = (2,2,3)
edges = 12
rank = 5
bases = 504
pair = (0,0,1), (0,0,2)

rayleigh_delta =
  -7988395388171953562263529025459059314667521815134984779980
```

Thus the complete tripartite incidence support is not strongly Rayleigh in
the sense needed by real-stable basis-polynomial arguments.

## Consequence

This does not contradict matroid Hodge theory.  The support matroid can still
have Lorentzian/log-concavity properties.  The point is narrower:

```text
strong-Rayleigh / real-stability / negative-dependence positivity
cannot be the missing p24 certificate mechanism for the CRT-axis support.
```

The remaining useful CS/probability imports are therefore exactly the ones
that become arithmetic statements:

```text
1. p-unit PIT for the selected mixed Plucker determinant;
2. explicit p-unit block equivalence to an MSRD/LRS code;
3. phase-aware Borcherds/local-intersection p-unit theorem;
4. data/ML mining only when it proposes an exact identity with holdouts.
```

The live theorem is unchanged:

```text
delta_all = det(T_lead,all) in
  (O_E[Y]/(Y^3107441 - 1))^*
```

or orbitwise:

```text
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }
  = {0}.
```

The intrinsic `W_axis cap F_27={0}` condition follows from this selected
theorem but does not imply it.

The probability boundary is now sharper: the ordinary support polynomial does
not supply a real-stability route, and the actual p24 determinant has the
harder mixed Plucker coefficients and non-real cyclotomic CM evaluation.
