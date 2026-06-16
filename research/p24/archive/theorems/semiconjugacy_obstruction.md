# Kummer Power-Map Semiconjugacy Obstruction

For the Montgomery x-only map, the quotient coordinate

```text
s = x + 1/x
```

gives a rational map

```text
y = (s^2 - 4)/(4*(s + A))
R_A(s) = y + 1/y.
```

The tempting shortcut is a rational map `S` with

```text
R_A(S(u)) = S(u^2 - 2),
```

where `u=z+z^-1`.  This would turn the depth-`k` inverse problem into a
multiplicative-order/root-extraction problem.

The low-degree probes found no such nonconstant nonsingular maps.  The
conceptual reason is the orbifold type of the two dynamical systems:

```text
u -> u^2 - 2       Chebyshev/power quotient, parabolic type (2,2,infinity)
R_A, A^2 != 4      elliptic Lattes quotient, parabolic type (2,2,2,2)
```

Here `R_A` is the quotient of multiplication-by-2 on a nonsingular elliptic
curve by the involution `P -> -P`.  A nonconstant rational semiconjugacy between
postcritically finite parabolic maps must respect the associated orbifold
structure.  The Chebyshev/power orbifold and the nonsingular elliptic Lattes
orbifold are different parabolic types, so the only power-map semiconjugacies
come from degenerate/singular limits (`A = +/-2`) or constant maps.

This explains the computations:

```text
kummer_semiconjugacy_probe.py
  degree-1/LFT maps: no nonconstant nonsingular examples

kummer_degree2_semiconjugacy_probe.py
  degree <= 2 maps over p=5,7,11,13: no nonconstant nonsingular examples
```

Therefore the power-map shortcut is closed as a route to a DANGER3 certificate
for `p = 10^24 + 7`: it would collapse the elliptic Lattes dynamics to torus
power dynamics, which is possible only in the singular cases rejected by the
verifier.
