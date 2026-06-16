# Reduced-Anchor Kernel Final-Curve Guardrail

The reduced-anchor residual has a formal `c=179` subgroup/kernel-polynomial
shape, but for the selected p24 trace it is not a final-curve rational
`179`-isogeny computation.

For

```text
p = 10^24 + 7
t = -1178414874616
#E(F_p) = p + 1 - t = 2^41 * 454747350887
```

we have:

```text
179 does not divide #E(F_p)
t^2 - 4p is a nonsquare modulo 179
Frobenius has no roots modulo 179
```

Thus `179` is Atkin for the final curve.  There is no `F_p`-rational cyclic
`179`-subgroup and no `F_p`-rational `179`-isogeny/kernel polynomial to
enumerate on the final curve.

The kernel-polynomial target from the reduced-anchor notes remains useful as
an auxiliary CM/Lang/cyclotomic quotient object.  The guardrail is only that
the “two signs after kernel collapse” surface is conditional on producing
that auxiliary selected object; it is not a direct final-curve Vélu
enumeration over `F_p`.
