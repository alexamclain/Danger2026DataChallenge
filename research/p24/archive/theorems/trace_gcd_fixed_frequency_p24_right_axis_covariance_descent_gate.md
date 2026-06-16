# p24 Right-Axis Covariance Plus Descent Gate

This is the seven-variable finite shadow of the current p24 theorem target.
After the Gauss reduction, the remaining verifier condition is that the
internally traced `G_chi` right profile has no nontrivial order-7 spectrum.
Equivalently, its seven `H=<2^7>` coset sums on `F_211^*` are equal.

Let `Y_c` denote those seven coset sums, with
`c=log_2(r) mod 7`.  The p24 arithmetic gives:

```text
rho = p^780
rho fixes F_p(mu_157)
rho shifts the right order-7 quotient by 6
rho^7 = p^5460 fixes the whole right 211 axis
```

Therefore the finite implication worth proving arithmetically is:

```text
Y_{c+6} = rho(Y_c)  and  rho(Y_0) = Y_0
----------------------------------------
        Y_0 = Y_1 = ... = Y_6
```

The executable gate checks the shape and its negative controls:

```text
covariance alone: leaks order-7 spectrum
descent alone: leaks order-7 spectrum
covariance plus one anchor descent: all H-coset sums equal
```

In fact, under the covariance relation, the six nontrivial order-7 projections
vanish if and only if the anchor sum `Y_0` descends.  This turns the next
arithmetic target into a single anchored descent identity for the internally
traced `G_chi` profile, provided the covariance relation is established
beforehand.

The Lean gate
`p24/lean/TraceGcdRightAxisAnchorDescentGate.lean` now records both directions
as `all_equal_iff_anchor_under_shift6_covariance`: under the seven shift-6
covariance equations, `rho(Y_0)=Y_0` is exactly equivalent to equality of all
seven H-coset sums.

This does not prove that the actual CM/Lang `G_chi` profile satisfies the two
inputs.  It refines the missing theorem to exactly those inputs, on the right
axis coordinates that the final certificate would verify.
