# p24 Jacobi-Carry C/E-Centering Gate

Date: 2026-06-07

## Point

The plain Stickelberger element leaks in the forbidden bidegrees

```text
C_7^nontrivial x {trivial C/E character}.
```

A Jacobi sum divisor is different.  Its finite carry distribution has the
form

```text
theta_{u,v}(t) = [ut]_N + [vt]_N - [(u+v)t]_N,
N = 7 * 179,
```

where `[ ]_N` means least nonnegative residue.  This gate checks the Fourier
support of that carry on the exact p24 quotient axes `C_7 x C_179`.

## Result

There is a narrow positive support identity:

```text
c_axis_jacobi_forbidden_zero=48/48
both_c_axis_jacobi_forbidden_zero=48/48
```

When one Jacobi input is right-trivial and `C/E`-nontrivial, the carry has no
forbidden right-nontrivial / `C/E`-trivial bidegree.

The negative controls are just as important:

```text
plain_stickelberger_forbidden_nonzero=6/6
generic_jacobi_forbidden_leaks=48/48
c_axis_pure_right_partner_leaks=48/48
c_axis_sum_pure_right_leaks=48/48
```

So the Jacobi route is not generically solved.  The support cancellation only
appears when a genuine `C/E`-axis character participates and the carry does
not collapse back to a pure right-axis interaction.

## Consequence

This gives the first precise positive shape for a Stickelberger/Jacobi proof:

```text
Express the weighted trace-GCD obstruction, after B/C trace, as a combination
of Jacobi carry divisors with one right-trivial nontrivial C/E character.
```

If such a decomposition is constructed honestly from the selected CM/Lang
packet, the forbidden `C_7^nontrivial x {C/E trivial}` bidegrees vanish for
structural reasons.  The missing theorem becomes the decomposition into these
C-axis Jacobi carries, not the support calculation itself.

## Check

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate.py
```

The split Fourier field is `F_32579`, with

```text
32579 - 1 = 26 * 7 * 179.
```

No CM class set is enumerated.
