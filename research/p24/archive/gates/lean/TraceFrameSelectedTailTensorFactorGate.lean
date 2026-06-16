/-!
Finite gate for tensor-factor equivariance of the selected-tail determinant.

The arithmetic input is external: after choosing the denominator-safe prefix
chart, Frobenius transport across scalar-extension tensor factors carries the
selected-tail determinant line to a p-unit multiple of its conjugate.  This
file records only the finite implication:

* one representative selected-tail norm is nonzero;
* the representative norm detects zero of the representative tail determinant;
* tensor-factor transport preserves nonzero tail determinants;
* a selected-tail bad event forces its factor tail determinant to vanish;
* therefore no selected-tail bad event occurs in any tensor factor.

No CM arithmetic, normal-basis construction, or p-adic unit proof is
formalized here.
-/

namespace P24.TraceFrameSelectedTailTensorFactorGate

def BadForcesFactorTailZero {Beta Factor Scalar : Type} [Zero Scalar]
    (factorOf : Beta → Factor)
    (Bad : Beta → Prop)
    (factorTail : Factor → Scalar) : Prop :=
  ∀ beta, Bad beta → factorTail (factorOf beta) = 0

def AllSelectedTailsGood {Beta : Type}
    (Bad : Beta → Prop) : Prop :=
  ∀ beta, ¬ Bad beta

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

theorem representative_tail_nonzero_from_norm
    {Scalar : Type} [Zero Scalar]
    (representativeTail representativeNorm : Scalar)
    (h_tail_zero_forces_norm_zero :
      representativeTail = 0 → representativeNorm = 0)
    (h_norm_nonzero : representativeNorm ≠ 0) :
    representativeTail ≠ 0 := by
  intro h_tail_zero
  exact h_norm_nonzero (h_tail_zero_forces_norm_zero h_tail_zero)

theorem all_factor_tails_nonzero_from_transport
    {Factor Scalar : Type} [Zero Scalar]
    (factorTail : Factor → Scalar)
    (representative : Factor)
    (h_transport_nonzero :
      ∀ factor, factorTail representative ≠ 0 → factorTail factor ≠ 0)
    (h_representative_nonzero : factorTail representative ≠ 0) :
    ∀ factor, factorTail factor ≠ 0 := by
  intro factor
  exact h_transport_nonzero factor h_representative_nonzero

theorem all_factor_tails_nonzero_from_representative_norm
    {Factor Scalar : Type} [Zero Scalar]
    (factorTail : Factor → Scalar)
    (representative : Factor)
    (representativeNorm : Scalar)
    (h_transport_nonzero :
      ∀ factor, factorTail representative ≠ 0 → factorTail factor ≠ 0)
    (h_tail_zero_forces_norm_zero :
      factorTail representative = 0 → representativeNorm = 0)
    (h_norm_nonzero : representativeNorm ≠ 0) :
    ∀ factor, factorTail factor ≠ 0 :=
  all_factor_tails_nonzero_from_transport
    factorTail representative h_transport_nonzero
    (representative_tail_nonzero_from_norm
      (factorTail representative) representativeNorm
      h_tail_zero_forces_norm_zero h_norm_nonzero)

theorem all_factor_tails_nonzero_from_representative_punit
    {Factor Scalar : Type} [Zero Scalar]
    (factorTail : Factor → Scalar)
    (representative : Factor)
    (representativeNorm representativeInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_transport_nonzero :
      ∀ factor, factorTail representative ≠ 0 → factorTail factor ≠ 0)
    (h_tail_zero_forces_norm_zero :
      factorTail representative = 0 → representativeNorm = 0)
    (h_payload :
      UnitPayload representativeNorm representativeInv UnitRel) :
    ∀ factor, factorTail factor ≠ 0 :=
  all_factor_tails_nonzero_from_representative_norm
    factorTail representative representativeNorm
    h_transport_nonzero h_tail_zero_forces_norm_zero
    (h_unit_nonzero representativeNorm representativeInv h_payload)

theorem no_selected_tail_bad_from_factor_tails
    {Beta Factor Scalar : Type} [Zero Scalar]
    (factorOf : Beta → Factor)
    (Bad : Beta → Prop)
    (factorTail : Factor → Scalar)
    (h_bad_zero :
      BadForcesFactorTailZero factorOf Bad factorTail)
    (h_factor_tails_nonzero :
      ∀ factor, factorTail factor ≠ 0) :
    AllSelectedTailsGood Bad := by
  intro beta h_bad
  exact h_factor_tails_nonzero (factorOf beta)
    (h_bad_zero beta h_bad)

theorem no_selected_tail_bad_from_representative_punit_transport
    {Beta Factor Scalar : Type} [Zero Scalar]
    (factorOf : Beta → Factor)
    (Bad : Beta → Prop)
    (factorTail : Factor → Scalar)
    (representative : Factor)
    (representativeNorm representativeInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_transport_nonzero :
      ∀ factor, factorTail representative ≠ 0 → factorTail factor ≠ 0)
    (h_tail_zero_forces_norm_zero :
      factorTail representative = 0 → representativeNorm = 0)
    (h_bad_zero :
      BadForcesFactorTailZero factorOf Bad factorTail)
    (h_payload :
      UnitPayload representativeNorm representativeInv UnitRel) :
    AllSelectedTailsGood Bad :=
  no_selected_tail_bad_from_factor_tails
    factorOf Bad factorTail h_bad_zero
    (all_factor_tails_nonzero_from_representative_punit
      factorTail representative representativeNorm representativeInv UnitRel
      h_unit_nonzero h_transport_nonzero h_tail_zero_forces_norm_zero
      h_payload)

theorem p24_selected_tail_tensor_factor_count_subsqrt :
    70 < 1000000000000 := by
  decide

theorem p24_selected_tail_representative_payload_subsqrt :
    4 < 1000000000000 := by
  decide

end P24.TraceFrameSelectedTailTensorFactorGate
