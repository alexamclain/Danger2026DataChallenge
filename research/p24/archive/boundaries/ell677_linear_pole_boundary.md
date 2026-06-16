# Ell-677 Linear Pole Boundary

This note sharpens the closest Atkin-Lehner zero-lemma miss.

## Point

The scan in

```text
p24/atkin_zero_window_boundary.md
```

used the optimistic proxy

```text
delta_AL = ceil([SL2:Gamma0(677)] / 2) = 339.
```

That is a generous quotient-degree lower proxy.  It is not the pole degree of
the endpoint-linear functions whose character traces are forced to vanish by
relative-content collapse.

## Prime Edge Cusp Orders

On `X0(ell)`, write

```text
x = j(tau),
y = j(ell*tau).
```

At the two cusps:

```text
cusp infinity:  pole(x)=1,   pole(y)=ell
cusp 0:         pole(x)=ell, pole(y)=1
```

For `ell=677`, this gives:

```text
x alone on X0(677):     pole degree 678
y alone on X0(677):     pole degree 678
x+y on X0(677)^+:       pole degree 677
generic ax+by on X0:    pole degree 1354
```

The symmetric combination `x+y` is the best Atkin-Lehner-descended
endpoint-linear function, because the two cusps are identified on
`X0(ell)^+`; its descended pole degree is still `ell`, not `(ell+1)/2`.

## Audit

I added:

```text
p24/ell677_linear_pole_audit.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/ell677_linear_pole_audit.py
```

Output:

```text
optimistic_atkin_proxy=(ell+1)/2=339
optimistic_proxy_over_index=1.079618
best_forced_linear_degree=677
best_forced_linear_degree_over_index=2.156051
single_endpoint_degree_over_index=2.159236
```

## Consequence

The p24 `ell=677` zero-lemma window is not a near miss for the actual linear
relative-content theorem.

Harmful packet collapse forces vanishing of linear character traces of
endpoint `j`-values.  It does **not** force vanishing of arbitrary low-degree
functions on `X0(677)^+`, even if such functions exist by gonality or other
modular-curve geometry.

Thus the relevant comparison is:

```text
needed index = 314,
best forced endpoint-linear pole degree = 677.
```

The Atkin-Lehner quotient improves constants for symmetric endpoint data, but
it does not make the finite-field zero lemma fire for the `ell=677` first odd
layer.

## Automorphism Check

Nash's sidecar checked the modular-curve bookkeeping from the quotient side.
For prime level `677`:

```text
psi(677) = [SL2(Z):Gamma0(677)] = 678
W_677 = {1, w_677}
ceil(psi(677)/|W_677|) = 339 > 314
```

The standard prime-level automorphism theorem gives no extra automorphisms
beyond the Fricke involution for this level, so beating the zero-lemma window
would require a new special invariant rather than a further quotient of the
existing `X0(677)` correspondence.

The same bookkeeping gives:

```text
g(X0(677)) = 56
g(X0(677)^+) = 21
```

Low-gonality functions on `X0(677)^+` do not help by themselves, because
relative-content collapse does not force their character traces to vanish.

## Nonlinear Warning Toy

I added:

```text
p24/nonlinear_function_not_forced_toy.py
```

It works over `F_7` with a primitive third root `zeta=2` and values

```text
values = [5, 1, 0].
```

Output:

```text
linear_character_sum=0
square_character_sum=6
```

So even in a length-3 toy, vanishing of a linear character component does not
force vanishing of the same character component after applying a nonlinear
function.  This is the finite-algebra reason arbitrary low-degree functions
on `X0(677)^+` cannot be used in the current zero-lemma proof unless a new
theorem proves they carry the same relative packet phase.
