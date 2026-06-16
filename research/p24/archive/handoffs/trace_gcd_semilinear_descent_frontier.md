# Trace-GCD Semilinear Descent Frontier

Date: 2026-06-06

This note isolates a key local/class-field distinction for the p24 trace-GCD
route.

## Principal Hilbert Frobenius

For the third p24 trace:

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
t^2 - 4p = 4D_K
```

and:

```text
Norm(t/2 + sqrt(D_K)) = p.
```

Thus the selected prime above `p` is principal in the conductor-2 CM order.
Its Artin symbol in the unramified ring-class/Hilbert class field is
trivial.  This proves that the target CM roots are `F_p`-rational after
reduction.

It does **not** choose one CM root.  Trivial Frobenius fixes the whole class
torsor, not a distinguished point.

## Nontrivial Cyclotomic Frobenius

The trace-GCD determinant is not just a Hilbert-class value.  It uses
Lang/Fourier coordinates at the `157` and `211` layers.  Frobenius still acts
on roots of unity:

```text
zeta_157 -> zeta_157^p,     ord_157(p)=156,
zeta_211 -> zeta_211^p,     ord_211(p)=35.
```

For the right `211` phase:

```text
p mod 211 = 114
right Frobenius orbits = {0} plus six length-35 orbits.
```

Therefore a determinant section built from embedded CM phase data naturally
lives in a semilinear/crossed-product orbit algebra:

```text
Hilbert/ring-class part: fixed by p;
cyclotomic phase part: permuted by zeta -> zeta^p.
```

This explains the repeated small-row observation:

```text
right phase descent succeeds,
ordinary base-polynomial descent fails.
```

## Consequence For The Producer

The honest p24 object is:

```text
Xi_O = Nrd_O(det(P V_univ A))
```

or equivalently the determinant of the block-cycle/Fitting operator over a
right Frobenius orbit.

The false shortcut is:

```text
p is principal in the CM field
=> f_trace has ordinary coefficients in F_p[Y]
=> use a base-field resultant.
```

The correct statement is:

```text
p is principal on the unramified CM torsor,
but p acts nontrivially on the 157/211 phase coordinates;
therefore the producer must prove a semilinear/crossed-product norm p-unit.
```

This matches the actual-CM norm triangle:

```text
p24/trace_gcd_actual_cm_norm_triangle_audit.py
```

where:

```text
product_equals_signed_block_cycle=1
product_equals_split_norm=1
naive_base_polynomial_possible=0
```

## Audit

The arithmetic facts are checked by:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/trace_gcd_principal_cyclotomic_split_audit.py
```

It reports:

```text
prime_above_p_is_principal=1
hilbert_class_frobenius_order=1
principal_frobenius_selects_one_root=0
ord_157(p)=156
ord_211(p)=35
ordinary_base_polynomial_descent_is_not_forced=1
crossed_product_orbit_norm_is_the_honest_phase_payload=1
```

## Current Theorem

The remaining theorem should be phrased semilinearly:

```text
Construct the actual phase-aware determinant-line element in the
157/211 semilinear crossed-product algebra and prove each right-orbit
reduced norm is a p-unit at the selected ordinary prime.
```

This is the same local target as:

```text
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
```

but it explains why principal ordinary reduction alone is insufficient and
why the finite certificate must keep the seven orbit norms or one honest
global operator norm.
