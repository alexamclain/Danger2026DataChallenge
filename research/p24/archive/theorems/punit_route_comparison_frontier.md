# P-Unit Route Comparison Frontier

Date: 2026-06-05

This note compares the two live p24 p-unit surfaces after the trace-frame
Fitting compression and the mixed representative trace-GCD refinement.

## Summary

There are currently two viable sub-sqrt certificate fronts.

```text
trace-frame front:
  prove delta_all in A_all^*
  for A_all = O_E[Y]/(Y^3107441 - 1);

mixed representative front:
  prove the representative 140+16 relative-trace window is injective,
  equivalently prove a selected tail-on-kernel determinant is a p-unit.
```

The trace-frame front has the smallest verifier payload once its arithmetic
producer theorem is proved.  With tensor-factor equivariance, the p-unit
payload is one degree-8 norm and one inverse in `E=F_p(mu_66254)`, i.e.
`10920` base-field slots.

The mixed representative front has the sharper proof-facing finite object.
The raw `156 x 156` Moore determinant has been reduced to:

```text
four full right trace blocks leave a 16-dimensional kernel,
and the selected 16 tail trace coordinates are nonsingular on that kernel.
```

That is a local trace-intersection theorem, not an existential minor search.

The phrase "smallest" is therefore route-local:

```text
trace-frame is smallest as a verifier payload;
mixed trace-GCD is smallest as an explicit proof-facing p-unit object.
```

Also, "nonzero mod p" and "p-unit" are interchangeable only after fixing the
integral lift of the Lang/resolvent coordinates and proving the denominators
are p-units.  The finite gates check the nonzero implication after reduction;
the arithmetic theorem must supply the p-integral lift.

## Trace-Frame Object

For the third strict trace:

```text
p = 10^24 + 7
t = -1178414874616
h = 205880396014 = 66254 * 3107441
E = F_p(mu_66254),  [E:F_p] = 5460
```

The finite theorem target is:

```text
A_all = O_E[Y]/(Y^3107441 - 1)
delta_all = det(T_lead,all)
delta_all in A_all^*
```

Equivalently, for every beta orbit `Omega`:

```text
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }
  = {0}.
```

The intrinsic full-top-three avoidance `W_axis cap F_27={0}` is necessary but
not sufficient for this selected leading certificate.

The Lean-checked implication chain is:

```text
degree-8 leading norm nonzero
  => representative packet leading determinants nonzero
  => tensor-factor equivariance spreads nonzero-ness to all factors
  => beta-orbit coverage makes every beta orbit good.
```

This front is canonical and payload-optimal, but its proof target is still a
large determinant-line/Fitting p-unit statement.  The most concrete known
proof languages are:

```text
p-integral Fitting isomorphism;
crossed-product reduced norm;
CM-weighted Fourier/Toeplitz minor;
phase-aware Borcherds/local-intersection value.
```

None of those has yet produced the missing arithmetic p-unit theorem.

## Mixed Representative Object

Set:

```text
L = F_p(mu_157),        [L:F_p] = 156
R = F_p(mu_211),        [R:F_p] = 35
E = L R.
```

For the six right Frobenius-orbit representatives `v_j`, define:

```text
S_j = H_{157,211}(1,v_j) in E,
T_j(lambda) = Tr_{E/R}(lambda*S_j),  lambda in L.
```

The full mixed theorem is equivalent to:

```text
lambda |-> (T_1(lambda),...,T_6(lambda)) is injective on L,
```

or:

```text
L cap span_R{S_1,...,S_6}^perp = {0}.
```

The representative p24 certificate chooses:

```text
deleted O4,
prefix blocks B = {O2,O3,O5,O6},
tail block O1,
tail window = first 16 Lang/trace-dual coordinates of O1.
```

Let `A_B : L -> F_p^140` be the four full prefix trace blocks, and let
`tau_1,...,tau_16` be the selected tail functionals.  The refined arithmetic
theorem is:

```text
dim_Fp ker(A_B) = 16,
det(tau_a(k_b))_{1<=a,b<=16} is a p-unit
```

for any `F_p`-basis `k_1,...,k_16` of `ker(A_B)`.

Equivalently:

```text
gcd_p-lin(P_K, tail_16) = X,
K = ker(A_B).
```

This is the smallest proof-facing object currently visible.  It is equivalent
to the selected representative leading Moore determinant after choosing prefix
pivots.  This distinction matters: an arbitrary nonzero `156 x 156` Moore
minor would prove full mixed span, but it would not by itself give the fixed
equivariant representative certificate.  The selected `140+16` minor is the
object that the unit-orbit handoff knows how to propagate.

The trace-GCD form exposes the actual structure:

```text
prefix trace maps cut out a 16-dimensional local kernel;
the tail determinant is a 16 x 16 trace-pairing resultant.
```

The finite implication is checked by:

```text
p24/lean/UnitOrbitGate.lean
p24/lean/RepresentativeDualObstructionGate.lean
p24/lean/MixedSubspacePolynomialGate.lean
p24/lean/MixedRightOrbitSupportGate.lean
p24/lean/MixedTraceDualGate.lean
p24/lean/MixedTraceIntersectionGate.lean
p24/lean/TraceGcdGate.lean
p24/lean/TraceOriginProductGate.lean
```

The unit `2 mod 211` cycles the six right orbits, so one representative
tail-on-kernel p-unit plus the product-algebra equivariance theorem propagates
to all six deletion rows.

## Origin-Product Strengthening

The representative determinant is selected-origin data.  For `h=m*n`, write
an origin shift as:

```text
shift = n*alpha + m*beta mod h.
```

Small actual-CM audits support the covariance:

```text
Delta_i(alpha,beta) = u_i(alpha,beta) * F_i(alpha mod right_component),
```

where `u_i(alpha,beta)` is a p-unit.  For p24 this predicts a 211-term
right-origin product:

```text
Pi_trace,i = prod_{t mod 211} F_i(t).
```

A proof of:

```text
Pi_trace,i != 0 mod p
```

would prove every right-origin translate, hence the selected representative
determinant.  Equivalently, if `f_i(Y)` interpolates the right-translation
tail determinant sequence:

```text
Pi_trace,i = Res_Y(Y^211 - 1, f_i(Y)).
```

This is a better non-enumerative theorem target than the raw selected
determinant: it replaces class-set enumeration by a fixed right-component
cyclic resultant.  It is stronger than needed, but still tiny compared with
`sqrt(p)`.

## Current Choice

For producing the final certificate, the trace-frame front remains the most
compressed verifier surface.

For proving the missing theorem, the mixed representative trace-GCD front is
now the better next target:

```text
prove prefix rank 140 and p-unitness of the 16 x 16 tail-on-kernel determinant,
preferably through the 211-term origin-product resultant.
```

The proof-facing local-unit/Fitting statement is pinned in:

```text
p24/trace_gcd_local_unit_proof_target.md
```

The centered-profile route is the smallest base-field p-unit surface:

```text
p24/centered_profile_payload_frontier.md
```

It replaces the representative right-coordinate basis by the base-field
`156 x 210` centered Hermitian marginal.  The explicit matrix-plus-rank
witness payload is `57096` field elements, while a direct p-unit theorem for
the leading minor has a two-scalar verifier payload.  It proves the mixed
Schur rank correction but not the stronger delete-one/right-support theorem.

The tensor-factor/top-coefficient machinery remains adjacent but separate
from this selected Chow/Fitting determinant unless one proves an additional
determinant-line comparison:

```text
p24/trace_gcd_chow_tensor_bridge_boundary.md
```

In particular, tensor exterior nonvanishing or axis injectivity does not by
itself force a fixed selected trace-GCD Chow minor to be a p-unit.

The current producer-facing form of that resultant is the operator norm:

```text
p24/lang_trace_gcd_operator_norm_theorem.md
```

It states:

```text
prod_t Delta(t)
  = det(m_f on F[Y]/(Y^211 - 1)),
f(Y)=det(P diag(Y^v) A).
```

The p-integral lift and denominator conditions for interpreting this as a
p-unit statement are recorded in:

```text
p24/lang_trace_gcd_integrality_lift.md
```

The same theorem as Schubert-orbit avoidance is recorded in:

```text
p24/lang_trace_gcd_schubert_orbit_theorem.md
```

The support/distance dictionary for the same bad event is:

```text
p24/trace_gcd_schubert_support_dictionary.md
```

The finite payload manifest and no-smuggling Lean gate are:

```text
p24/trace_gcd_subsqrt_certificate_manifest.md
p24/lean/TraceGcdPayloadGate.lean
```

They distinguish the safe 211-value certificate from the seven-orbit-product
and one-norm certificates.  The compressed forms are valid only after a
producer theorem proves zero-detection for the actual determinant sequence.

The current boundary for using known Borcherds/Gross-Zagier machinery on this
Schubert determinant is:

```text
p24/trace_gcd_borcherds_literature_boundary.md
```

The reason is not that the mixed theorem is weaker.  It is that the objects
are explicit relative traces:

```text
T_j(lambda)=Tr_{E/R}(lambda*H_{157,211}(1,v_j)),
```

and the failure condition is a concrete local intersection:

```text
L cap span_R{S_j : j in B}^perp
  has dimension 16, and the O1 tail separates it.
```

This gives class-field, local-lattice, trace-formula, and cyclic-resultant
attacks something finite and structured to hold onto.  The trace-frame
determinant-line route should stay alive as the payload-optimal backend and
as a possible Borcherds/Fitting proof route, but the next theorem work should
focus on the mixed trace-GCD determinant.

## Fast Verification Run

On 2026-06-05 the finite mixed gates passed:

```text
lean p24/lean/UnitOrbitGate.lean
lean p24/lean/RepresentativeDualObstructionGate.lean
lean p24/lean/MixedSubspacePolynomialGate.lean
lean p24/lean/MixedRightOrbitSupportGate.lean
lean p24/lean/MixedTraceDualGate.lean
lean p24/lean/MixedTraceIntersectionGate.lean
lean p24/lean/TraceGcdGate.lean
```

and the manifest sanity check confirmed:

```text
p_mod_157 = 21
p_mod_211 = 114
left orbit count = 1, length = 156
right orbit count = 6, each length = 35
prefix dimension = 140
tail length = 16
unit 2 mod 211 cycles all six right orbits.
```

The pinned small actual-CM origin-action audit was also rerun:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_origin_action_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail
```

It reported:

```text
records = 280
det_zero_count = 0
gcd_failure_count = 0
omitted 0: alpha_value_period = 7, beta_value_period = 1
omitted 1: alpha_value_period = 7, beta_value_period = 1
```

This is evidence for the origin-product theorem shape, not evidence for the
p24 p-unit itself.

The finite origin-product handoff is checked by:

```text
p24/lean/TraceOriginProductGate.lean
```

It proves that a nonzero right-component product, together with covariance by
p-unit factors, makes the selected representative tail determinant nonzero.

These checks verify only the finite handoff.  The missing input remains the
selected-prime arithmetic p-unit theorem above.
