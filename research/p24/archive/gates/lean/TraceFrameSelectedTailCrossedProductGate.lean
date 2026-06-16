/-!
Finite gate for the selected-tail crossed-product norm theorem.

The p24 arithmetic theorem we now want is a p-unit theorem for the
crossed-product reduced norms of the selected-tail determinant sequence.

This file records only the finite handoff:

* a selected-tail bad event at beta forces the beta-orbit product to vanish;
* the crossed-product reduced norm equals that orbit product;
* all reduced norms are nonzero, or one global norm is nonzero and detects
  any zero orbit norm;
* therefore no selected-tail bad event occurs at any beta.

No CM arithmetic, interpolation, determinant construction, or p-adic unit
proof is formalized here.
-/

namespace P24.TraceFrameSelectedTailCrossedProductGate

def ReducedNormMatchesProduct {Orbit Scalar : Type}
    (reducedNorm orbitProduct : Orbit → Scalar) : Prop :=
  ∀ orbit, reducedNorm orbit = orbitProduct orbit

def BadForcesOrbitProductZero {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (orbitProduct : Orbit → Scalar) : Prop :=
  ∀ beta, Bad beta → orbitProduct (orbitOf beta) = 0

def SelectedTailGood {Beta : Type}
    (Bad : Beta → Prop)
    (beta : Beta) : Prop :=
  ¬ Bad beta

def AllSelectedTailsGood {Beta : Type}
    (Bad : Beta → Prop) : Prop :=
  ∀ beta, SelectedTailGood Bad beta

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

theorem orbit_product_nonzero_from_reduced_norm
    {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm orbitProduct : Orbit → Scalar)
    (orbit : Orbit)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_norm_nonzero : reducedNorm orbit ≠ 0) :
    orbitProduct orbit ≠ 0 := by
  intro h_zero
  exact h_norm_nonzero (by
    rw [h_match orbit, h_zero])

theorem no_selected_tail_bad_from_reduced_norms
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_bad_zero :
      BadForcesOrbitProductZero orbitOf Bad orbitProduct)
    (h_norms_nonzero :
      ∀ orbit, reducedNorm orbit ≠ 0) :
    AllSelectedTailsGood Bad := by
  intro beta h_bad
  have h_orbit_nonzero :
      orbitProduct (orbitOf beta) ≠ 0 :=
    orbit_product_nonzero_from_reduced_norm
      reducedNorm orbitProduct (orbitOf beta) h_match
      (h_norms_nonzero (orbitOf beta))
  exact h_orbit_nonzero (h_bad_zero beta h_bad)

theorem no_selected_tail_bad_from_reduced_norm_punits
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm orbitProduct reducedNormInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_bad_zero :
      BadForcesOrbitProductZero orbitOf Bad orbitProduct)
    (h_payload :
      ∀ orbit, UnitPayload (reducedNorm orbit) (reducedNormInv orbit) UnitRel) :
    AllSelectedTailsGood Bad :=
  no_selected_tail_bad_from_reduced_norms
    orbitOf Bad reducedNorm orbitProduct h_match h_bad_zero
    (fun orbit =>
      h_unit_nonzero
        (reducedNorm orbit)
        (reducedNormInv orbit)
        (h_payload orbit))

theorem reduced_norms_nonzero_from_global_norm
    {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm : Orbit → Scalar)
    (globalNorm : Scalar)
    (h_any_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_global_nonzero : globalNorm ≠ 0) :
    ∀ orbit, reducedNorm orbit ≠ 0 := by
  intro orbit h_zero
  exact h_global_nonzero (h_any_zero ⟨orbit, h_zero⟩)

theorem no_selected_tail_bad_from_global_reduced_norm
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (globalNorm : Scalar)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_bad_zero :
      BadForcesOrbitProductZero orbitOf Bad orbitProduct)
    (h_any_norm_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_global_nonzero : globalNorm ≠ 0) :
    AllSelectedTailsGood Bad :=
  no_selected_tail_bad_from_reduced_norms
    orbitOf Bad reducedNorm orbitProduct h_match h_bad_zero
    (reduced_norms_nonzero_from_global_norm
      reducedNorm globalNorm h_any_norm_zero h_global_nonzero)

theorem selected_tail_bad_forces_global_norm_zero
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (globalNorm : Scalar)
    (h_bad_zero :
      BadForcesOrbitProductZero orbitOf Bad orbitProduct)
    (h_orbit_product_zero_to_norm_zero :
      ∀ orbit, orbitProduct orbit = 0 → reducedNorm orbit = 0)
    (h_any_norm_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0) :
    (∃ beta, Bad beta) → globalNorm = 0 := by
  intro h_bad_exists
  rcases h_bad_exists with ⟨beta, h_bad⟩
  apply h_any_norm_zero
  exact ⟨orbitOf beta,
    h_orbit_product_zero_to_norm_zero
      (orbitOf beta)
      (h_bad_zero beta h_bad)⟩

theorem selected_tail_good_from_global_punit
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (globalNorm globalInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_bad_zero :
      BadForcesOrbitProductZero orbitOf Bad orbitProduct)
    (h_any_norm_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_payload :
      UnitPayload globalNorm globalInv UnitRel) :
    AllSelectedTailsGood Bad :=
  no_selected_tail_bad_from_global_reduced_norm
    orbitOf Bad reducedNorm orbitProduct globalNorm h_match h_bad_zero
    h_any_norm_zero
    (h_unit_nonzero globalNorm globalInv h_payload)

theorem p24_selected_tail_payload_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_orbit_count_subsqrt :
    560 < 1000000000000 := by
  decide

theorem p24_orbit_degree_subsqrt :
    5549 < 1000000000000 := by
  decide

end P24.TraceFrameSelectedTailCrossedProductGate
