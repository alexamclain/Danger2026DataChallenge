# Subagent Selected-Minor Norm Compression

Date: 2026-06-05

This note reviews the selected-origin Toeplitz-symbol compression from:

```text
p24/trace_frame_selected_minor_certificate_spec.md
p24/trace_frame_selected_minor_certificate_accounting.py
```

and asks whether beta-orbit coverage can be norm-compressed without listing
degree-5549 orbit-algebra symbols.

## Verdict

One theorem candidate survives, but it is a determinant-line/Fitting norm
theorem, not a generic Toeplitz-Schur identity.

The selected-origin Toeplitz normal form halves the finite verifier surface:

```text
368 * 368 = 135424 E-entries
```

becomes one length-`m` cyclic symbol:

```text
m = 66254 E-entries.
```

But the same symbol over one nonzero beta-orbit algebra would have:

```text
66254 * 5549 = 367643446 E-entries,
```

already `2.00733321516 * sqrt(p)` in base-field slots for one orbit.  Thus
orbit coverage cannot be literal symbol data.  The producer theorem has to
prove a p-unit norm or unit Fitting ideal directly.

## Candidate Theorem

Let `O_E` be the p-integral coefficient ring and let:

```text
A_all = O_E[Y] / (Y^n - 1)
      ~= O_E x product_{Omega != 0} A_Omega
```

after localizing at the selected ordinary prime.  Let:

```text
T_lead,all : Lambda_axis tensor A_all -> O_E^368 tensor A_all
```

be the universal selected leading trace-frame map in the Toeplitz/translate
minor normal form, using fixed p-integral Fourier and flag trivializations.
Let:

```text
delta_all = det(T_lead,all) in A_all.
```

The concrete theorem worth trying is:

```text
Selected-minor Fitting norm theorem:
  Fitt_0(coker T_lead,all) = A_all
  after localization at the selected prime over p.
```

Equivalently:

```text
delta_all in A_all^*.
```

In class-field language, the same statement should be realized by a global
determinant-line section `Xi_lead` whose residues are the selected
Toeplitz/Schur determinants up to p-units, together with a divisor/local
intersection proof that `Xi_lead` has no zero at the selected prime.

## Why It Compresses

Projecting `delta_all` to the beta-zero factor gives `D_0`.  Projecting to a
nonzero orbit factor gives:

```text
delta_Omega = det(T_lead,Omega) in A_Omega.
```

Taking the finite etale norm gives the already checked crossed-product
identity:

```text
Norm_{A_Omega/O_E}(delta_Omega)
  = R_lead,Omega
  = product_{gamma in Omega} Delta_lead(theta^(-gamma)).
```

Therefore:

```text
delta_all in A_all^*
  => D_0 in O_E^*
  => every R_lead,Omega in O_E^*.
```

Equivalently, the global norm:

```text
Norm_{A_all/O_E}(delta_all)
  = D_0 * product_{Omega != 0} R_lead,Omega
```

is a p-unit, hence every factor is a p-unit because the residue ring is a
product of fields at the selected prime.

If the determinant-line section descends equivariantly through:

```text
S = K_m Q(zeta_n)^<p>,
```

and tensor-factor Frobenius transports the fixed leading flag up to p-units,
this further compresses to the existing degree-8 target:

```text
Norm_{S/K_m}(Xi_lead) mod p != 0.
```

Without that tensor-factor equivariance, the compressed target is still only:

```text
70 degree-8 norms, one per scalar-extension tensor factor.
```

## Why Toeplitz-Schur Alone Does Not Compress

The Toeplitz/Jacobi-Trudi form rewrites:

```text
Delta_lead = det(c_{r-s})
```

as a selected cyclic skew-Schur value of the CM symbol.  Existing toys and
audits rule out the generic shortcuts:

```text
full circulant reduced normality does not imply the selected minor;
nonzero symbol coefficients do not imply the selected minor;
full Cauchy-Binet support can still cancel;
ordinary beta norm collapse R_Omega = D_rep^5549 is false;
the selected Toeplitz matrix touches all 66254 symbol positions and has no
disjoint support product factorization.
```

So a Toeplitz-Schur theorem would need extra CM arithmetic: a p-adic divisor
formula, a p-unit row/column/block equivalence, or a unique local leading term
for this specific CM symbol.  Without that, it is only a restatement of the
same Fitting determinant.

## Small Experiment

The highest-information small test is an equivariant Fitting audit on compact
CM rows:

```text
1. Build the fixed Toeplitz/translate-minor T_lead,all for a small row where
   the beta algebra splits into several E-Frobenius orbit factors.
2. Compute delta_all once in the product algebra, then compare its projections
   with the per-orbit determinants delta_Omega and with the checked products
   R_Omega.
3. Track the determinant under packet and tensor-factor Frobenius.  The
   desired outcome is:

     delta_{sigma(a),sigma(i)}
       = unit(sigma,a,i) * sigma(delta_{a,i})

   with all units nonzero.
```

Support for the candidate would be exact Fitting/norm compatibility plus
unit equivariance for the fixed leading flag.  A falsification would be any
compact row where packetwise determinants are nonzero but the fixed
determinant-line section fails equivariance, or where tensor-factor Frobenius
preserves rank but sends the selected leading minor to a different Plucker
coordinate not related by a p-unit.

That falsification would not kill the local-unit theorem, but it would kill
the single degree-8 norm compression and leave only the 70 separate
degree-8 determinant-line p-unit targets.

The first tensor-factor version of this experiment is now recorded in:

```text
p24/trace_frame_tensor_factor_equivariance_boundary.md
p24/trace_frame_tensor_factor_equivariance_audit.py
```

It found no compact-row obstruction: determinant base norms and fixed leading
pivot shapes matched across the split tensor factors in the tested rows.
