# Trace-GCD Residual-Product P-Unit Theorem

Date: 2026-06-06

## Point

The current two-resultant theorem can now be stated in the most explicit
finite-field normality language: prove two subspace-polynomial residual
products are p-units.

This is not a new payload.  It is the same four-field certificate surface:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}.
```

The bridge is:

```text
trace-GCD resultant p-unit
  <=> selected leading trace-pairing determinant p-unit
  <=> selected leading Lang coordinates span the left field
  <=> all-coordinate Moore residual product p-unit.
```

The finite bridge is checked by:

```text
p24/trace_gcd_trace_pairing_subspace_bridge_audit.py
p24/trace_gcd_trace_pairing_subspace_bridge_toy.py
p24/lean/TraceGcdTracePairingSubspaceBridgeGate.lean
```

The low-rank toy is important: the residual product is the product over all
selected coordinates.  Dependent coordinates contribute a zero residual.

The p24 `140+16` split is checked by:

```text
p24/trace_gcd_residual_prefix_tail_bridge_audit.py
p24/lean/TraceGcdResidualPrefixTailGate.lean
```

The audit verifies that the all-coordinate residual product factors as the
four-block prefix product times the quotient-tail product, and includes
controls where the prefix or tail is deliberately dependent.

The section-level interpretation is recorded in:

```text
p24/trace_gcd_residual_moore_chow_section.md
p24/trace_gcd_residual_moore_chow_toy.py
```

It identifies the residual product with a Moore determinant, identifies the
full `156`-coordinate scalar with a fixed Moore-basis unit times the ordinary
coordinate Chow determinant, and identifies the tail scalar as the Moore
determinant of the tail after applying the prefix annihilator.

## Residual Product

Let

```text
L = F_p(mu_157),  [L:F_p] = 156.
```

For a selected ordered tuple

```text
c_1,...,c_156 in L,
```

define `P_0(X)=X`.  Inductively, let `P_i` be the monic p-linearized
annihilator of the `F_p`-span of `c_1,...,c_i`.  Equivalently, before
adjoining `c_i`, compute

```text
r_i = P_{i-1}(c_i).
```

If `r_i != 0`, update by the standard subspace-polynomial recurrence

```text
P_i(X) = P_{i-1}(X)^p - r_i^(p-1) P_{i-1}(X).
```

If `r_i = 0`, the span did not grow.  The determinant-line scalar is

```text
R(c_1,...,c_156) = product_{i=1}^{156} Norm_{L/F_p}(r_i).
```

Then

```text
R != 0
```

if and only if the selected `c_i` form an `F_p`-basis of `L`.

## Fixed Orbit Theorem

For the p24 representative support:

```text
deleted orbit = O4
prefix orbits = O2,O3,O5,O6
tail orbit    = O1
tail length   = 16
```

let `c_1,...,c_156` be the corresponding ordered Lang/trace-dual coordinates:

```text
4 full right blocks = 4*35 = 140 coordinates,
then first 16 tail coordinates.
```

The fixed theorem is:

```text
R_fixed = R(c_1,...,c_156) is a p-unit
```

at the selected ordinary prime above `p=10^24+7`.

This is equivalent to:

```text
Xi_O0 = Res_p-lin(P_K0,T_0) is a p-unit.
```

Equivalently, write:

```text
B_fixed = product of residual norms for the first 140 prefix coordinates,
T_fixed = product of residual norms for the 16 quotient-tail coordinates.
```

Then:

```text
B_fixed and T_fixed are p-units
  <=> R_fixed is a p-unit.
```

In the Moore/Chow section language this is:

```text
B_fixed = Norm(Delta_140(prefix)),
T_fixed = Norm(Delta_16(P_U(tail_1),...,P_U(tail_16))),
```

where `U` is the `F_p`-span of the four prefix blocks and `P_U` is its monic
p-linearized annihilator.  The second determinant is the quotient-tail
section; it is not the Moore determinant of the raw tail coordinates.

## Nonzero Orbit Theorem

Transport the same ordered-coordinate construction around one nonzero
right Frobenius orbit `O1` of length `35`.  This gives residual products

```text
R_t = R(c_1(t),...,c_156(t)),  t in O1.
```

The nonzero theorem is the crossed/Frobenius norm:

```text
R_nonzero = product_{t in O1} R_t is a p-unit
```

with determinant-line p-unit conventions.

This is equivalent to:

```text
Xi_O1 = Nrd_O1(Res_p-lin(P_Kt,T_t)) is a p-unit.
```

Equivalently, prove the crossed norm of the transported prefix products and
the crossed norm of the transported quotient-tail products are p-units.

## Remaining Arithmetic Input

Everything above is finite algebra.  The missing theorem is now:

```text
For the actual embedded p24 157/211 CM trace family, R_fixed and R_nonzero
are p-units at the selected ordinary prime above p.
```

Potential proof languages are now sharply aligned:

```text
1. subspace-polynomial normality:
   no p-linearized polynomial of p-degree <156 kills the selected tuple;

2. trace-intersection:
   L cap span_R{S_j}^perp = {0}, with the representative 140+16 erasure;

3. Fitting/Schubert:
   the selected ordinary CM point has zero local intersection with the
   pulled-back phase-aware Schubert divisor;

4. Borcherds/local intersection:
   construct a p-integral phase-aware section whose CM value is the residual
   product up to p-units and whose local p-intersection is zero.
```

The Moore/Chow note makes the fourth route more concrete: the missing section
should be the prefix Moore-Wronskian together with the Moore-Wronskian of
prefix-annihilator tail images.  The hard arithmetic step remains proving
that those phase-aware sections have zero local intersection at the selected
ordinary p24 CM point, without computing the p24 class set.
