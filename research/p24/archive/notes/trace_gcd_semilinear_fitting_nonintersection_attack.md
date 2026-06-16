# Trace-GCD Semilinear Fitting Nonintersection Attack

Date: 2026-06-06

## Purpose

This note is the current direct proof attack for the missing p24 theorem.  It
does not introduce another payload.  It states exactly what has to be proved
to make the existing four-field-element certificate sound.

The machine-readable version is:

```text
p24/trace_gcd_two_resultant_theorem_manifest.py
```

## Exact Theorem

Let

```text
p = 10^24 + 7
L = F_p(mu_157),        [L:F_p] = 156
R_j = one degree-35 right factor of F_p(mu_211)
S_j = H_{157,211}(1,v_j)
a_j(lambda) = Tr_{L R_j / R_j}(lambda*S_j).
```

For the representative support:

```text
deleted O4
prefix B = {O2,O3,O5,O6}
tail O1 = first 16 Lang coordinates
```

define

```text
K_0 = ker(a_2,a_3,a_5,a_6)
Xi_O0 = Res_p-lin(P_K0,T_0).
```

For one nonzero right Frobenius orbit `O1`, transport the same construction
around the orbit and define

```text
Xi_O1 = Nrd_O1(Res_p-lin(P_Kt,T_t)).
```

The theorem to prove is:

```text
Xi_O0 in O_p^*
Xi_O1 in O_p^*
```

at one of the two explicit ordinary primes above `p`, and multiplication by
`2 mod 211` transports the nonzero-orbit determinant lines by p-unit factors.

The finite payload is then:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

with `4 / floor(sqrt(p)) = 4e-12`.

## Lemma Stack

### 1. Integral Setup

Use:

```text
p mod 157 = 21,      ord_157(p)=156
p mod 211 = 114,     ord_211(p)=35
t^2 - 4p = 4D_K
sqrt(D_K)=+/-t/2 mod p
gcd(p,2*157*211*3107441*h)=1
```

All Lang, Fourier, trace-dual, and determinant-line denominators from the
`157/211` model are p-units.  Therefore the p-local problem is not
integrality; it is nonvanishing.

### 2. Determinant-Line Construction

Construct `K_t` and `T_t` from the mixed periods `S_j`, not from a printed
class list.  The determinant line is allowed to change by p-units under
basis changes.  This is why the theorem must be phrased with p-unit
transition factors, not scalar equality.

### 3. Fitting/Resultant Identification

Show:

```text
det(T_t|K_t) = p-unit * Res_p-lin(P_Kt,T_t)
```

and, for a nonzero right orbit,

```text
Nrd_O(det(T_t|K_t))
  = p-unit * det(block-cycle Fitting operator).
```

The finite versions of these equalities are already tested by the norm
triangle and holdout audits.

### 4. Ordinary Local Nonintersection

Prove that the selected ordinary CM point has zero local intersection with
the fixed and representative nonzero orbit Schubert/Fitting divisors:

```text
v_p(Xi_O0(x_p24)) = 0
v_p(Xi_O1(x_p24)) = 0.
```

This is the actual arithmetic input.  It may be proved directly by showing
the reduced Fitting map is an isomorphism, or indirectly by constructing a
phase-aware Borcherds/Fitting section with the same local divisor.

For `Xi_O0`, the sharpest current direct-isomorphism formulation is the
RS-tail Hilbert-90 fixed-relation map:

```text
p24/trace_gcd_rs_tail_semilinear_core_theorem.md
Psi_RS : F_p^28 + K^28 + F_p^16 -> L.
```

Proving `det(Psi_RS)` is a p-unit is equivalent to the fixed square
coinvariant determinant and keeps the selected 16-tail as a
degree-`<16` Reed-Solomon subspace.

### 5. Diamond Transport

Prove:

```text
Xi_{2O} = epsilon_O * Xi_O,      epsilon_O in O_p^*.
```

The actual-CM unit-action falsifier shows why this must be p-unit scaling:
literal equality of printed norms is false even in right-7 holdouts.

## Why This Is The Preferred Route

The current holdout evidence says:

```text
selected_two_punit_groups=4/4
all_nonzero_groups=4/4
punit_transport_edges=8/8
literal_equal_nonzero_edges=0/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
```

So the theorem shape survives independent actual-CM holdout data while the
two easiest shortcuts fail:

```text
ordinary base-field resultant descent;
literal unit-invariance of orbit norms.
```

The same data does not prove p24.  It tells us the next proof should be a
semilinear Fitting local-nonintersection proof, not a broader random-rank or
unit-span search.

## Cheapest Current Checks

Use:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/trace_gcd_two_resultant_theorem_manifest.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_two_resultant_holdout_audit.py
```

The first checks the exact p24 constants and theorem surface.  The second is
the best seconds-scale falsifier for the theorem shape.

Avoid broad actual-CM row searches unless a new invariant is being tested.
A bounded scan for rows with the exact nondegenerate `prefix>0, tail>0`
small analogue did not emit rows quickly and was stopped; this is a data
limitation, not a theorem obstruction.

## CS-Theory Side Door

There is one precise uncertainty-principle side door:

```text
p24/trace_gcd_difference_dft_bridge.md
p24/trace_gcd_lambda_profile_bridge.md
p24/trace_gcd_dual_sparse_uncertainty_bridge.md
p24/lean/TraceGcdDualSparseBridgeGate.lean
```

The finite coordinate identity

```text
DFT_right(P_b - P_{b-1})_v
  = (1 - zeta_right^v) * DFT_right(P_b)_v
```

is now audited on the two actual-CM holdouts.  The multiplier is a p-unit for
nonzero right frequencies.  This proves the cyclic-difference part of the
bridge but not the arithmetic parameter identification.

The lambda-level parameter identification through the centered profile,
right Fourier periods, and Lang/Fitting coordinates is now also audited:

```text
profile_dft_mismatches=0
lambda_fourier_trace_mismatches=0
lang_reconstruction_mismatches=0
lang_zero_equivalence_failures=0
```

Thus the frequency-side trace-GCD bad event really can be read as a statement
about the same `lambda` in the centered profile word.  What remains missing is
the arithmetic implication that this bad `lambda` is constant on the selected
157-term plateau.

Equivalently, with `B_leading` the selected leading Lang/Fitting coordinate
map and `C_plateau` the centered plateau quotient map, prove:

```text
rowspace(C_plateau) subset rowspace(B_leading).
```

The rowspace audit reports no failures in current small actual-CM rows, but
also no nonvacuous containment:

```text
nonvacuous_containments=0
vacuous_full_leading_rank=10/10
```

So this remains a real theorem target, not an audited identity.

There is now a finite bridge from this trace-pairing determinant language to
the Moore/subspace-polynomial certificate language:

```text
p24/trace_gcd_trace_pairing_subspace_bridge.md
p24/trace_gcd_trace_pairing_subspace_bridge_audit.py
```

It verifies on actual-CM rows that the selected trace-GCD leading matrix,
the `F_p`-span of the same leading Lang coordinates, and the incremental
subspace-polynomial residual norm product detect exactly the same nonzero
event.  Thus the missing p24 nonintersection theorem may be attacked as a
Moore/subspace-polynomial p-unit theorem without changing the four-field
payload surface.

The p-unit theorem in this language is isolated in:

```text
p24/trace_gcd_residual_product_punit_theorem.md
p24/trace_gcd_residual_moore_chow_section.md
```

The residual product is over all selected leading coordinates, so dependent
coordinates contribute zero residuals.  This convention is guarded by the
low-rank finite toy.

The newest refinement identifies the section itself:

```text
full residual product = Moore determinant
full Moore determinant = fixed basis unit * coordinate Chow determinant
tail residual product = Moore determinant of P_prefix(tail_i)
```

For p24, the arithmetic nonintersection can therefore be targeted as
p-unitness of the 140-prefix Moore-Wronskian and the 16-dimensional
quotient-tail Moore-Wronskian, plus the same crossed norm around one nonzero
right Frobenius orbit.  A proof that uses the raw tail Moore determinant
instead of the prefix-annihilator images would miss the actual Fitting
section.

If the actual CM trace family further supplies a bridge from representative
leading-erasure sparsity to centered plateau-difference sparsity for the same
nonzero bad parameter, then prime cyclic uncertainty gives an immediate
finite contradiction:

```text
support_time <= 54
support_frequency <= 54
54 + 54 < 212.
```

The audit also shows the naive direct equality of the time-difference rowspace
and the Lang trace-word rowspace is false on the holdout.  Thus the only live
uncertainty route is a Schur/Lang/Fitting theorem identifying the kernel
parameter through the Fourier diagonal identity above.  Generic cyclic-code
and plateau uncertainty shortcuts are already negative.  This is therefore a
possible way to prove the local nonintersection lemma, not a completed proof.
