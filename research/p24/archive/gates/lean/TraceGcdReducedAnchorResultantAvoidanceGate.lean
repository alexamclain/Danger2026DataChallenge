/-!
Finite handoff gate for reduced-anchor resultant avoidance.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_resultant_avoidance_gate.py

checks the finite algebra behind the local-unit criterion:

* `R_c(x)` is a unit iff `x^c - 1` is a unit in the selected finite algebra;
* this is equivalent to a nonzero resultant against the algebra polynomial;
* equivalently, it can be certified by a Bezout identity.

This file records the proof contract.  The missing p24 input is still the
selected p-integral CM/Lang coordinate or subgroup polynomial.
-/

namespace P24.TraceGcdReducedAnchorResultantAvoidanceGate

structure SelectedFiniteAlgebraCoordinate where
  pIntegralCoordinate : Prop
  xPowerCMinusOneUnit : Prop

structure ResultantAvoidanceCertificate where
  resultantPUnit : Prop
  bezoutIdentity : Prop

structure ReducedAnchorResidual where
  residualRUnit : Prop

def SatisfiesResultantAvoidance
    (coord : SelectedFiniteAlgebraCoordinate)
    (cert : ResultantAvoidanceCertificate) : Prop :=
  coord.pIntegralCoordinate ∧
  (coord.xPowerCMinusOneUnit ↔ cert.resultantPUnit) ∧
  (cert.resultantPUnit ↔ cert.bezoutIdentity)

theorem residual_unit_from_resultant_avoidance
    (coord : SelectedFiniteAlgebraCoordinate)
    (cert : ResultantAvoidanceCertificate)
    (residual : ReducedAnchorResidual)
    (h_criterion : SatisfiesResultantAvoidance coord cert)
    (h_bezout_to_residual :
      coord.pIntegralCoordinate → cert.bezoutIdentity → residual.residualRUnit)
    (h_integral : coord.pIntegralCoordinate)
    (h_xc_unit : coord.xPowerCMinusOneUnit) :
    residual.residualRUnit := by
  rcases h_criterion with ⟨_h_coord_integral, h_resultant, h_bezout⟩
  exact h_bezout_to_residual h_integral (h_bezout.mp (h_resultant.mp h_xc_unit))

structure P24ReducedAnchorResultantTarget where
  cDegree : Nat
  forbiddenPolynomialDegree : Nat
  kernelPolynomialDegree : Nat

def p24Target : P24ReducedAnchorResultantTarget where
  cDegree := 179
  forbiddenPolynomialDegree := 179
  kernelPolynomialDegree := 89

theorem p24_reduced_anchor_resultant_target_numbers :
    p24Target.cDegree = 179 ∧
    p24Target.forbiddenPolynomialDegree = 179 ∧
    p24Target.kernelPolynomialDegree = 89 := by
  decide

end P24.TraceGcdReducedAnchorResultantAvoidanceGate
