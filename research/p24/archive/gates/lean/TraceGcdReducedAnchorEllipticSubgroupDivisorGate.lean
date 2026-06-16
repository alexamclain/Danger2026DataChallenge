/-!
Finite handoff gate for the elliptic-subgroup reading of the reduced-anchor
diamond residual.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_elliptic_subgroup_divisor_gate.py

checks the cyclic Abel-Jacobi criterion behind the following correction:

* `[P] - [O]` is not a principal elliptic divisor for nonzero torsion `P`;
* `c[P] - c[O]` is principal, but diamond-norming it gives `R_c^c`;
* the whole subgroup divisor `sum_{Q in H, Q != O} [Q] - (c-1)[O]`
  is already principal for odd `c`.

Thus the p24 producer should target the whole diamond/subgroup divisor, or a
descended cyclotomic coordinate, not an individual nonprincipal point divisor.
-/

namespace P24.TraceGcdReducedAnchorEllipticSubgroupDivisorGate

structure OnePointEllipticDivisor where
  degreeZero : Prop
  abelClassNonzero : Prop

def OnePointIsObstructed
    (divisor : OnePointEllipticDivisor) : Prop :=
  divisor.degreeZero ∧ divisor.abelClassNonzero

structure MillerMultipleDivisor where
  principal : Prop
  diamondNormIsCthPowerResidual : Prop

def MillerMultipleIsOvershoot
    (divisor : MillerMultipleDivisor) : Prop :=
  divisor.principal ∧ divisor.diamondNormIsCthPowerResidual

structure DiamondSubgroupDivisor where
  degreeZero : Prop
  abelClassZero : Prop
  equalsCyclotomicResidual : Prop
  pIntegralCMLangSpecialization : Prop

def DiamondSubgroupDivisorReady
    (divisor : DiamondSubgroupDivisor) : Prop :=
  divisor.degreeZero ∧
  divisor.abelClassZero ∧
  divisor.equalsCyclotomicResidual ∧
  divisor.pIntegralCMLangSpecialization

theorem producer_target_is_subgroup_divisor
    (onePoint : OnePointEllipticDivisor)
    (miller : MillerMultipleDivisor)
    (subgroup : DiamondSubgroupDivisor)
    (h_one : OnePointIsObstructed onePoint)
    (h_miller : MillerMultipleIsOvershoot miller)
    (h_subgroup : DiamondSubgroupDivisorReady subgroup) :
    subgroup.equalsCyclotomicResidual ∧
    subgroup.pIntegralCMLangSpecialization ∧
    onePoint.abelClassNonzero ∧
    miller.diamondNormIsCthPowerResidual := by
  rcases h_one with ⟨_h_one_deg, h_one_nonzero⟩
  rcases h_miller with ⟨_h_miller_principal, h_miller_power⟩
  rcases h_subgroup with
    ⟨_h_subgroup_degree, _h_subgroup_abel, h_residual, h_integral⟩
  exact ⟨h_residual, h_integral, h_one_nonzero, h_miller_power⟩

def p24C : Nat := 179
def p24NonzeroSubgroupDivisorDegree : Nat := p24C - 1
def p24NonzeroSubgroupSumModC : Nat := ((p24C - 1) * p24C / 2) % p24C
def p24OnePointAbelClass : Nat := 1 % p24C
def p24MillerMultipleAbelClass : Nat := p24C % p24C

theorem p24_nonzero_subgroup_divisor_degree :
    p24NonzeroSubgroupDivisorDegree = 178 := by
  decide

theorem p24_nonzero_subgroup_sum_mod_c :
    p24NonzeroSubgroupSumModC = 0 := by
  decide

theorem p24_one_point_abel_class_nonzero :
    p24OnePointAbelClass ≠ 0 := by
  decide

theorem p24_miller_multiple_abel_class_zero :
    p24MillerMultipleAbelClass = 0 := by
  decide

end P24.TraceGcdReducedAnchorEllipticSubgroupDivisorGate
