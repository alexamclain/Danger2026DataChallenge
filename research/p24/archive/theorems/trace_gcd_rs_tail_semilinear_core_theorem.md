# Trace-GCD RS-Tail Semilinear Core Theorem

Date: 2026-06-06

## Point

The fixed square coinvariant theorem can be stated without prefix-kernel bases
and without pretending the selected tail is a full group-ring summand.

It is the semilinear-core theorem for the full `140+16` Gaussian/RS-tail
matrix.

Let

```text
p = 10^24 + 7
K = F_p(mu_35)  = F_{p^4}
L = F_p(mu_157) = F_{p^156}
K subset L
```

and let `V_{a,j} in L`, `a in Z/35Z`, be the first collapsed Gaussian DFT
component of the p24 mixed coefficients, with

```text
j in {2,3,5,6}       prefix blocks
j = 1                selected tail block.
```

Define the first-component RS-tail map

```text
M_RS : K^{35*4} + K[z]_{<16} -> L

M_RS(x,Z) =
  sum_{a,j in {2,3,5,6}} x_{a,j} V_{a,j}
  + sum_{a in Z/35Z} Z(a) V_{a,1},
```

where

```text
Z(a) = sum_{s=0}^{15} z_s omega^{a*s}.
```

This is the first component of the scalar-extended full square map

```text
Phi_0 : R^4 + C_tail -> E/(tau_R - 1)E.
```

## Semilinear Operator

Let

```text
p mod 35 = 22,        ord_35(p)=4.
```

Define the semilinear order-4 operator

```text
T(x,Z) = (x',Z')
x'_{b,j} = x_{p^{-1}b,j}^p
Z'(z) has coefficients z_s^p.
```

The `r`th product-algebra component equation of the full Gaussian DFT map is
equivalent to

```text
M_RS(T^r(x,Z)) = 0.
```

Therefore the fixed square-map determinant is nonzero if and only if

```text
core_T(ker M_RS)
  := { (x,Z) : T^r(x,Z) in ker(M_RS), r=0,1,2,3 }
   = {0}.
```

This is the full-tail analogue of the older prefix-only condition
`core_T(ker M_0)=0`.

## Hilbert-90 Descent

By finite Hilbert 90 for the semilinear order-4 action, the core is nonzero
if and only if it contains a nonzero `T`-fixed vector.

The fixed source is explicit:

```text
fixed frequency prefix variables:        F_p^28
length-4 frequency orbit prefix data:    K^28
tail polynomial coefficients:            F_p^16
```

The dimension is

```text
28 + 4*28 + 16 = 156.
```

Thus the fixed theorem is equivalently the p-unit determinant theorem for an
explicit `F_p`-linear map

```text
Psi_RS : F_p^28 + K^28 + F_p^16 -> L.
```

Its determinant is the same p-unit determinant-line section as `det(Phi_0)`,
up to the already isolated p-unit Gaussian DFT and basis-change factors.

## Explicit Fixed-Relation Columns

Write the seven fixed frequencies as

```text
F = {0,5,10,15,20,25,30}
```

and the seven length-4 `p`-orbits on `Z/35Z` as

```text
A = {a, pa, p^2a, p^3a}.
```

Then `Psi_RS` has the following `F_p`-linear columns.

1. Fixed-frequency prefix columns:

```text
V_{a,j},        a in F, j in {2,3,5,6}.
```

These give `7*4 = 28` scalar variables over `F_p`.

2. Length-4 prefix-orbit columns.  For each orbit representative `a` and
prefix block `j`, one variable `c in K` contributes the linearized period

```text
U_{a,j}(c)
  = c V_{a,j}
  + c^p V_{pa,j}
  + c^{p^2} V_{p^2a,j}
  + c^{p^3} V_{p^3a,j}.
```

Choosing an `F_p`-basis of `K` turns the `7*4 = 28` variables `c` into
`28*4 = 112` scalar columns.

3. RS-tail columns.  Since a `T`-fixed tail polynomial has coefficients in
`F_p`, the tail columns are

```text
W_s = sum_{a in Z/35Z} omega^{a*s} V_{a,1},
0 <= s < 16.
```

Thus

```text
28 + 112 + 16 = 156
```

columns in `L`.  The fixed p-unit theorem is:

```text
det_Fp(
  V_{a,j},
  U_{a,j}(kappa_l),
  W_s
) in O_p^*,
```

where `kappa_l` is any p-integral `F_p`-basis of `K`; changing this basis
scales the determinant by a p-unit.

## Trace-Adjoint Syndrome

The same theorem can be dualized by the nondegenerate trace pairings on `L`
and `K`.  Identify the dual of the fixed source with

```text
F_p^28 + K^28 + F_p^16.
```

Then the trace adjoint sends `lambda in L` to the following syndrome:

```text
fixed scalar coordinates:
  Tr_{L/F_p}(lambda V_{a,j}),
  a in F, j in {2,3,5,6};

length-4 orbit K-coordinates:
  S_{a,j}(lambda)
    = sum_{r=0}^3 Tr_{L/K}(lambda V_{p^r a,j})^(p^{4-r}),
  A={a,pa,p^2a,p^3a}, j in {2,3,5,6};

tail scalar coordinates:
  Tr_{L/F_p}(lambda W_s),
  0 <= s < 16.
```

Here the exponent `p^{4-r}` means the inverse Frobenius on `K` for the
`c^(p^r)` coefficient in `U_{a,j}(c)`.  Thus:

```text
Psi_RS injective
  <=> det(Psi_RS) in O_p^*
  <=> the syndrome map L -> F_p^28 + K^28 + F_p^16 is surjective.
```

This gives a second explicit finite-field identity to prove: the `156`
syndrome coordinates of `lambda` span the full fixed-source dual.

## Moore/Schur Split

Choose an `F_p`-basis of `K`.  The syndrome theorem is equivalent to
`F_p`-linear independence of the `156` displayed column elements of `L`.
Equivalently, the Moore determinant

```text
Delta_156(C_RS) != 0,
```

where

```text
C_RS = {V_{a,j}} union {U_{a,j}(kappa_l)} union {W_s}.
```

The intrinsic split is:

```text
C_prefix = {V_{a,j}} union {U_{a,j}(kappa_l)},     |C_prefix| = 140
C_tail   = {W_s : 0 <= s < 16}.
```

Let `P_prefix` be the monic `p`-linearized annihilator of the span of
`C_prefix`.  Then

```text
Delta_156(C_RS) != 0
```

is equivalent to the two p-unit statements

```text
Delta_140(C_prefix) != 0,
Delta_16(P_prefix(W_0),...,P_prefix(W_15)) != 0.
```

This is the Moore/Schur form of the same fixed theorem.  It is strictly
stronger as a proof plan than saying the RS tail is generically helpful:
prefix fullness alone is not enough, and tail rank must be measured in the
quotient by the prefix span.

## Theorem To Prove

For the selected p24 ordinary orientation above `p`, prove:

```text
det(Psi_RS) in O_p^*.
```

Equivalently:

```text
core_T(ker M_RS) = {0}.
```

Equivalently:

```text
det(Phi_0) in O_p^*.
```

For one nonzero right Frobenius orbit `O`, the matching statement is the
crossed reduced norm of transported square maps:

```text
Nrd_O(Phi_t) = det(block_cycle(Phi_t : t in O)) in O_p^*.
```

Then unit-2/diamond determinant-line transport supplies the other five
nonzero right orbits by p-unit scaling.  The verifier payload remains:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}.
```

## Why This Is A Better Proof Target

This theorem keeps all three constraints that the data says are necessary:

```text
1. the selected tail is a degree-<16 Reed-Solomon subspace;
2. the tensor product L tensor K has four Frobenius-twisted components;
3. the nonzero orbit is a crossed/skew reduced norm, not an ordinary
   F_p[Y] resultant.
```

It also gives a concrete finite-field identity to attack:

```text
no nonzero T-fixed RS-tail relation maps to zero in L.
```

That is the place where a future Jacobi-sum, class-field, MSRD/LRS, or
phase-aware divisor argument has to enter.

## Existing Checks

The component and finite equivalences are checked by:

```text
p24/trace_gcd_full_gaussian_rs_tail_toy.py
p24/trace_gcd_actual_cm_gaussian_rs_tail_audit.py
p24/trace_gcd_rs_tail_semilinear_core_toy.py
p24/trace_gcd_rs_tail_fixed_adjoint_toy.py
p24/trace_gcd_rs_tail_syndrome_moore_schur_toy.py
p24/trace_gcd_rs_tail_block_support_profile_toy.py
p24/trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_displacement_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_theorem_candidate.md
p24/trace_gcd_rs_tail_shift_displacement_boundary_toy.py
p24/trace_gcd_rs_tail_cyclic_operator_boundary_toy.py
p24/trace_gcd_rs_tail_frequency_defect_gate_theorem.md
p24/trace_gcd_rs_tail_frequency_defect_gate_toy.py
p24/trace_gcd_rs_tail_basis_free_frequency_gate_toy.py
p24/trace_gcd_rs_tail_frequency_moore_schur_factor_toy.py
p24/trace_gcd_rs_tail_frequency_resultant_gate.md
p24/trace_gcd_rs_tail_frequency_resultant_gate_toy.py
p24/trace_gcd_rs_tail_cyclic_section_descent.md
p24/trace_gcd_rs_tail_cyclic_section_descent_toy.py
p24/trace_gcd_actual_cm_frequency_defect_boundary.py
p24/trace_gcd_actual_cm_basis_free_section_audit.py
p24/lean/TraceGcdFrequencyDefectGate.lean
p24/trace_gcd_rs_tail_visible_lrs_signature_toy.py
p24/trace_gcd_actual_cm_rs_tail_semilinear_core_audit.py
p24/trace_gcd_prefix_semilinear_core_toy.py
p24/trace_gcd_prefix_semilinear_descent_toy.py
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
p24/lean/TraceGcdFullCoinvariantTailGate.lean
p24/lean/TraceGcdCrossedCoinvariantNormGate.lean
```

The actual-CM fixed-column audit checks the explicit `V/U/W_s` columns on the
same bounded rows as the Gaussian/RS-tail audit.  Its current signature is:

```text
explicit_column_count_mismatches=0
rank_mismatches=0
full_rank_rows=6/10
singular_control_rows=4/10
actual_prefix_plus_tail_rows=4/10
prefix_failures_on_prefix_tail_rows=4
tail_quotient_failures_on_prefix_tail_rows=4
actual_cm_rs_tail_fixed_columns_match_time_rank=1
actual_cm_hilbert90_fixed_relation_shape_survives=1
actual_cm_rs_tail_schur_split_measured=1
```

The actual arithmetic gap is unchanged and now sharply localized:

```text
prove det(Psi_RS) and one transported crossed norm are p-units at the selected
ordinary p24 prime.
```

In this explicit-column language, the fixed gap is a single Moore/trace
determinant for the `156` displayed columns in `L=F_p(mu_157)`.

The coding-theory shortcut boundary is now also explicit.  The selected square
uses `156` of the `210` natural fixed-source columns, leaving `54` unused
columns.  The selected-block support-profile gate checks the five block
dimensions `35,35,35,35,16` across all `31` nonempty block subsets.  A
direct-sum pass on the selected blocks is a necessary hidden-LRS compatibility
check, not a proof of LRS structure.  A natural-coordinate visible GRS/LRS
signature is rejected by
`trace_gcd_rs_tail_visible_lrs_signature_toy.py`; any productive MSRD/LRS
theorem must construct the hidden p-unit block equivalence or exploit moduli
from the full `210`-column object.

The first full-object modulus is the Plucker chart of the omitted `54`
columns relative to the selected `156`-column basis.  A visible scalar GRS/MDS
model would make this `156 x 54` chart scaled Cauchy, equivalently the
entrywise inverse chart would have rank at most `2`.  The Cauchy toy records
this invariant and its row/column-scaling stability.  The arithmetic p24
version would have `8424` chart entries, so a positive theorem here would need
to identify a block/skew Cauchy structure for the actual CM Plucker ratios, not
merely re-check selected-square rank.

The sharpened block/skew candidate is a Sylvester displacement theorem.  After
the selected basis is fixed, the chart `C` should satisfy

```text
A C - C B = R S,       rank(R S) = small,
```

for p-integral transported CM/Lang operators `A` and `B`.  Scalar Cauchy gives
rank-one displacement, and the entrywise-inverse rank `<= 2` condition is only
that scalar shadow.  The p24 proof obligation is to identify the arithmetic
operators, not to fit low-rank displacement after seeing the chart.

The finite handoff is now isolated: if the full selected-plus-omitted column
family `X=[S O]` satisfies `T S = S A + E_s` and `T O = O B + E_o`, then for
the Plucker chart `C=S^{-1}O`,

```text
A C - C B = S^{-1}(E_o - E_s C).
```

So a p-integral low-rank boundary for the actual `210` columns would imply the
block/skew Cauchy chart condition.  The handoff toy also shows why `A,B`
chosen after seeing `C` are not certificate evidence.

For the RS-tail selection there is a canonical first operator to try: the
common cyclic/Lang shift on the six full right blocks.  Four selected full
blocks and the wholly omitted block are shift-stable; only the split tail
block crosses the selected/omitted boundary, giving two rank-one cut maps.
The corresponding row-space Riccati toy and column-boundary toy both record
the expected rank-two residue.

The current smaller actual-CM rows do not yet calibrate that full chart: the
tail-only full-rank rows have selected dimension `2`, where the inverse-rank
condition is automatic, and the nontrivial prefix-plus-tail rows are singular
before the selected columns form an ambient basis.  This boundary is recorded
by `trace_gcd_actual_cm_full_plucker_chart_boundary.py`.

The matching frequency-defect boundary is recorded by
`trace_gcd_actual_cm_frequency_defect_boundary.py`.  It measures the local
frequency profile on those same rows and reports no clean p24-like shape:
tail-only rows are not calibrations, while prefix-plus-tail singular rows fail
the local frequency-profile gate.  Therefore the actual-CM data currently
localizes the missing arithmetic theorem but does not prove it.

The current proof-facing refinement is the frequency-resultant gate: construct
cyclic sections `P_24,T_24,S_24` for the local Plucker determinant, defect
tail residue, and defect support.  Then the fixed determinant follows from
`Res(P_24,x^35-1)`, `Res(T_24,S_24)`, and selector/discriminant p-units via
the frequency-defect theorem.  The cyclic-section descent gate adds that the
local values must satisfy `F_{p a}=F_a^p` and the defect support must be a
Frobenius-stable size-16 set.  For p24, descent alone leaves two support
types: four length-4 orbits (`35` choices), or four fixed frequencies plus
three length-4 orbits (`1225` choices).  Reducing to the pure length-4 case
requires the additional arithmetic theorem that fixed frequencies are
ordinary.  The proof-facing local form is `tau_a in image(P_a)` at each fixed
frequency `a in 5Z/35Z`, equivalently `rank(P_a,tau_a)=rank(P_a)`.
