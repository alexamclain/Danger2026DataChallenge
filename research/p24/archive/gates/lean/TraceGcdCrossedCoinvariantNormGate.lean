/-!
Finite gate for the nonzero-orbit crossed coinvariant norm.

For the fixed orbit, a square coinvariant map

    Phi_full : R^4 ⊕ C_tail -> E/(tau_R - 1)E

has p24 dimension `156`.  For a nonzero Frobenius orbit, the producer should
construct transported maps `Phi_t` and prove the crossed/block-cycle norm is
a p-unit.  This file records only the finite implication from such a norm to
absence of local bad events.
-/

namespace P24.TraceGcdCrossedCoinvariantNormGate

def LocalCoinvariantUnit {Index Scalar : Type} [Zero Scalar]
    (detPhi : Index → Scalar)
    (t : Index) : Prop :=
  detPhi t ≠ 0

def CrossedNormMatchesProduct {Orbit Scalar : Type}
    (crossedNorm orbitProduct : Orbit → Scalar) : Prop :=
  ∀ orbit, crossedNorm orbit = orbitProduct orbit

def OrbitProductZeroOnLocalSingular {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (detPhi : Index → Scalar)
    (orbitProduct : Orbit → Scalar) : Prop :=
  ∀ t, detPhi t = 0 → orbitProduct (orbitOf t) = 0

def LocalBad {Index : Type} (BadAt : Index → Prop) : Prop :=
  ∃ t, BadAt t

def LocalBadDetectedByCoinvariant {Index Scalar : Type} [Zero Scalar]
    (BadAt : Index → Prop)
    (detPhi : Index → Scalar) : Prop :=
  ∀ t, BadAt t → detPhi t = 0

def ChoiceNormUnitEquivalent {Choice Scalar Unit : Type}
    (choiceNorm : Choice → Scalar)
    (scale : Unit → Scalar → Scalar)
    (PUnitScale : Unit → Prop) : Prop :=
  ∀ source target, ∃ unit, PUnitScale unit ∧
    choiceNorm target = scale unit (choiceNorm source)

def ScaleTransfersPUnit {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop) : Prop :=
  ∀ unit value, PUnitScale unit → PUnitScalar value →
    PUnitScalar (scale unit value)

def ScalePreservesZero {Scalar Unit : Type} [Zero Scalar]
    (scale : Unit → Scalar → Scalar)
    (PUnitScale : Unit → Prop) : Prop :=
  ∀ unit value, PUnitScale unit → (scale unit value = 0 ↔ value = 0)

theorem local_units_from_crossed_coinvariant_norm
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (detPhi : Index → Scalar)
    (crossedNorm orbitProduct : Orbit → Scalar)
    (h_match : CrossedNormMatchesProduct crossedNorm orbitProduct)
    (h_zero_factor :
      OrbitProductZeroOnLocalSingular orbitOf detPhi orbitProduct)
    (h_crossed_nonzero : ∀ orbit, crossedNorm orbit ≠ 0) :
    ∀ t, LocalCoinvariantUnit detPhi t := by
  intro t h_det_zero
  have h_product_zero : orbitProduct (orbitOf t) = 0 :=
    h_zero_factor t h_det_zero
  have h_product_nonzero : orbitProduct (orbitOf t) ≠ 0 := by
    intro h_zero
    exact h_crossed_nonzero (orbitOf t) (by
      rw [h_match (orbitOf t)]
      exact h_zero)
  exact h_product_nonzero h_product_zero

theorem no_local_bad_from_crossed_coinvariant_norm
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (BadAt : Index → Prop)
    (detPhi : Index → Scalar)
    (crossedNorm orbitProduct : Orbit → Scalar)
    (h_match : CrossedNormMatchesProduct crossedNorm orbitProduct)
    (h_zero_factor :
      OrbitProductZeroOnLocalSingular orbitOf detPhi orbitProduct)
    (h_bad_detected : LocalBadDetectedByCoinvariant BadAt detPhi)
    (h_crossed_nonzero : ∀ orbit, crossedNorm orbit ≠ 0) :
    ∀ t, ¬ BadAt t := by
  intro t h_bad
  have h_unit : LocalCoinvariantUnit detPhi t :=
    local_units_from_crossed_coinvariant_norm
      orbitOf detPhi crossedNorm orbitProduct
      h_match h_zero_factor h_crossed_nonzero t
  exact h_unit (h_bad_detected t h_bad)

theorem no_global_local_bad_from_crossed_coinvariant_norm
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (BadAt : Index → Prop)
    (detPhi : Index → Scalar)
    (crossedNorm orbitProduct : Orbit → Scalar)
    (h_match : CrossedNormMatchesProduct crossedNorm orbitProduct)
    (h_zero_factor :
      OrbitProductZeroOnLocalSingular orbitOf detPhi orbitProduct)
    (h_bad_detected : LocalBadDetectedByCoinvariant BadAt detPhi)
    (h_crossed_nonzero : ∀ orbit, crossedNorm orbit ≠ 0) :
    ¬ LocalBad BadAt := by
  intro h_exists
  rcases h_exists with ⟨t, h_bad⟩
  exact
    (no_local_bad_from_crossed_coinvariant_norm
      orbitOf BadAt detPhi crossedNorm orbitProduct
      h_match h_zero_factor h_bad_detected h_crossed_nonzero t)
    h_bad

theorem all_choice_norms_punit_from_one_choice
    {Choice Scalar Unit : Type}
    (choiceNorm : Choice → Scalar)
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (baseChoice : Choice)
    (h_equiv :
      ChoiceNormUnitEquivalent choiceNorm scale PUnitScale)
    (h_transfer :
      ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_base : PUnitScalar (choiceNorm baseChoice)) :
    ∀ choice, PUnitScalar (choiceNorm choice) := by
  intro choice
  obtain ⟨unit, h_unit, h_scaled⟩ := h_equiv baseChoice choice
  rw [h_scaled]
  exact h_transfer unit (choiceNorm baseChoice) h_unit h_base

theorem all_choice_norms_nonzero_from_one_choice
    {Choice Scalar Unit : Type} [Zero Scalar]
    (choiceNorm : Choice → Scalar)
    (scale : Unit → Scalar → Scalar)
    (PUnitScale : Unit → Prop)
    (baseChoice : Choice)
    (h_equiv :
      ChoiceNormUnitEquivalent choiceNorm scale PUnitScale)
    (h_preserves_zero :
      ScalePreservesZero scale PUnitScale)
    (h_base_nonzero : choiceNorm baseChoice ≠ 0) :
    ∀ choice, choiceNorm choice ≠ 0 := by
  intro choice h_zero
  obtain ⟨unit, h_unit, h_scaled⟩ := h_equiv baseChoice choice
  rw [h_scaled] at h_zero
  have h_base_zero : choiceNorm baseChoice = 0 :=
    (h_preserves_zero unit (choiceNorm baseChoice) h_unit).mp h_zero
  exact h_base_nonzero h_base_zero

theorem p24_crossed_coinvariant_block_dim :
    156 * 35 = 5460 := by
  decide

theorem p24_crossed_coinvariant_sign_positive :
    (156 * (35 - 1)) % 2 = 0 := by
  decide

end P24.TraceGcdCrossedCoinvariantNormGate
