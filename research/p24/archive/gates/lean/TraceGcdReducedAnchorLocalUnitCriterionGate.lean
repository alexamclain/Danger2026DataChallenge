/-!
Finite handoff gate for the reduced-anchor local-unit criterion.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate.py

checks the exact finite algebra:

* `R_c(x) = Phi_c(x)/(x-1)^(c-1)` is a unit after reduction iff
  `x` avoids the `c`-th roots of unity;
* `K_H(T)` is a unit after reduction iff `T` is neither `O` nor a nonzero
  point of the subgroup `H`.

This file records the proof contract for the p24 producer: once the selected
CM/Lang coordinate is constructed p-integrally, the remaining p-unit claim is
the avoidance of the forbidden anchor/subgroup locus.
-/

namespace P24.TraceGcdReducedAnchorLocalUnitCriterionGate

structure CyclotomicSpecialization where
  pIntegralCoordinate : Prop
  avoidsMuC : Prop
  residualRIsUnit : Prop

def SatisfiesCyclotomicLocalCriterion
    (spec : CyclotomicSpecialization) : Prop :=
  spec.pIntegralCoordinate ∧
  (spec.avoidsMuC ↔ spec.residualRIsUnit)

structure KernelSpecialization where
  pIntegralPoint : Prop
  avoidsSubgroupAndPole : Prop
  kernelPolynomialIsUnit : Prop

def SatisfiesKernelLocalCriterion
    (spec : KernelSpecialization) : Prop :=
  spec.pIntegralPoint ∧
  (spec.avoidsSubgroupAndPole ↔ spec.kernelPolynomialIsUnit)

structure SelectedCMLangAnchor where
  pIntegralSelectedCoordinate : Prop
  cyclotomicAvoidance : Prop
  subgroupAvoidance : Prop

structure SelectedAnchorPUnit where
  cyclotomicResidualPUnit : Prop
  kernelPolynomialPUnit : Prop

theorem selected_anchor_punit_from_local_avoidance
    (cyc : CyclotomicSpecialization)
    (ker : KernelSpecialization)
    (anchor : SelectedCMLangAnchor)
    (out : SelectedAnchorPUnit)
    (h_cyc : SatisfiesCyclotomicLocalCriterion cyc)
    (h_ker : SatisfiesKernelLocalCriterion ker)
    (h_anchor_cyc :
      anchor.pIntegralSelectedCoordinate →
      anchor.cyclotomicAvoidance →
      cyc.pIntegralCoordinate ∧ cyc.avoidsMuC)
    (h_anchor_ker :
      anchor.pIntegralSelectedCoordinate →
      anchor.subgroupAvoidance →
      ker.pIntegralPoint ∧ ker.avoidsSubgroupAndPole)
    (h_out :
      cyc.residualRIsUnit →
      ker.kernelPolynomialIsUnit →
      out.cyclotomicResidualPUnit ∧ out.kernelPolynomialPUnit)
    (h_integral : anchor.pIntegralSelectedCoordinate)
    (h_cyc_avoid : anchor.cyclotomicAvoidance)
    (h_ker_avoid : anchor.subgroupAvoidance) :
    out.cyclotomicResidualPUnit ∧ out.kernelPolynomialPUnit := by
  rcases h_cyc with ⟨_h_cyc_integral, h_cyc_iff⟩
  rcases h_ker with ⟨_h_ker_integral, h_ker_iff⟩
  rcases h_anchor_cyc h_integral h_cyc_avoid with ⟨_h_ci, h_ca⟩
  rcases h_anchor_ker h_integral h_ker_avoid with ⟨_h_ki, h_ka⟩
  exact h_out (h_cyc_iff.mp h_ca) (h_ker_iff.mp h_ka)

def p24C : Nat := 179
def p24ForbiddenCyclotomicAnchorCount : Nat := p24C
def p24KernelForbiddenSubgroupCount : Nat := p24C

theorem p24_forbidden_cyclotomic_anchor_count :
    p24ForbiddenCyclotomicAnchorCount = 179 := by
  decide

theorem p24_kernel_forbidden_subgroup_count :
    p24KernelForbiddenSubgroupCount = 179 := by
  decide

end P24.TraceGcdReducedAnchorLocalUnitCriterionGate
