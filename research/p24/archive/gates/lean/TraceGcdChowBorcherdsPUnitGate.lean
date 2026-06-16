/-!
Finite gate for a phase-aware Borcherds/Fitting proof of the trace-GCD
Chow orbit norms.

This file does not construct Borcherds products, Chow divisors, local
intersection numbers, or class-field sections.  It records the exact finite
handoff needed by the current theorem target:

* a phase-aware value `psi O` is a p-unit, e.g. by zero local intersection;
* a comparison transfers p-unitness from `psi O` to the actual Chow orbit
  norm `orbitNorm O`;
* Chow orbit norm p-units exclude every translated Schubert bad event.

The arithmetic input is the construction and local valuation theorem for
`psi`.  The finite output is the same selected trace-GCD certificate as in
`TraceGcdChowNormGate.lean`.
-/

namespace P24.TraceGcdChowBorcherdsPUnitGate

def TransfersPUnit {α : Type} (source target : α) (PUnit : α → Prop) : Prop :=
  PUnit source → PUnit target

def OrbitComparisonPayload {Orbit α : Type}
    (psi orbitNorm : Orbit → α)
    (PUnit : α → Prop) : Prop :=
  ∀ orbit, TransfersPUnit (psi orbit) (orbitNorm orbit) PUnit

def OrbitPUnitPayload {Orbit α : Type}
    (value : Orbit → α)
    (PUnit : α → Prop) : Prop :=
  ∀ orbit, PUnit (value orbit)

def LocalIntersectionFormula {Orbit α LocalData : Type}
    (psi : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData) : Prop :=
  ∀ orbit, LocalIntersectionZero orbit (localData orbit) → PUnit (psi orbit)

def GlobalLocalIntersectionFormula {α LocalData : Type}
    (psi : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData) : Prop :=
  LocalIntersectionZero localData → PUnit psi

def ChowDetectsBad {Index α : Type} [Zero α]
    (chow : Index → α)
    (Bad : Index → Prop) : Prop :=
  ∀ t, Bad t → chow t = 0

def OrbitChowNormSound {Index Orbit α : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (chow : Index → α)
    (orbitNorm : Orbit → α) : Prop :=
  ∀ t, chow t = 0 → orbitNorm (orbitOf t) = 0

def GlobalChowNormSound {Index α : Type} [Zero α]
    (chow : Index → α)
    (globalNorm : α) : Prop :=
  ∀ t, chow t = 0 → globalNorm = 0

theorem orbit_norm_punits_from_borcherds_comparison
    {Orbit α : Type}
    (psi orbitNorm : Orbit → α)
    (PUnit : α → Prop)
    (h_compare : OrbitComparisonPayload psi orbitNorm PUnit)
    (h_psi_punit : OrbitPUnitPayload psi PUnit) :
    OrbitPUnitPayload orbitNorm PUnit := by
  intro orbit
  exact h_compare orbit (h_psi_punit orbit)

theorem psi_punits_from_zero_local_intersections
    {Orbit α LocalData : Type}
    (psi : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_formula :
      LocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_zero : ∀ orbit, LocalIntersectionZero orbit (localData orbit)) :
    OrbitPUnitPayload psi PUnit := by
  intro orbit
  exact h_formula orbit (h_zero orbit)

theorem orbit_norm_punits_from_borcherds_local_intersections
    {Orbit α LocalData : Type}
    (psi orbitNorm : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_formula :
      LocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : OrbitComparisonPayload psi orbitNorm PUnit)
    (h_zero : ∀ orbit, LocalIntersectionZero orbit (localData orbit)) :
    OrbitPUnitPayload orbitNorm PUnit :=
  orbit_norm_punits_from_borcherds_comparison psi orbitNorm PUnit h_compare
    (psi_punits_from_zero_local_intersections
      psi PUnit LocalIntersectionZero localData h_formula h_zero)

theorem global_norm_punit_from_borcherds_comparison
    {α : Type}
    (psi globalNorm : α)
    (PUnit : α → Prop)
    (h_compare : TransfersPUnit psi globalNorm PUnit)
    (h_psi_punit : PUnit psi) :
    PUnit globalNorm :=
  h_compare h_psi_punit

theorem global_psi_punit_from_zero_local_intersection
    {α LocalData : Type}
    (psi : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_formula :
      GlobalLocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_zero : LocalIntersectionZero localData) :
    PUnit psi :=
  h_formula h_zero

theorem global_norm_punit_from_borcherds_local_intersection
    {α LocalData : Type}
    (psi globalNorm : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_formula :
      GlobalLocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psi globalNorm PUnit)
    (h_zero : LocalIntersectionZero localData) :
    PUnit globalNorm :=
  global_norm_punit_from_borcherds_comparison psi globalNorm PUnit h_compare
    (global_psi_punit_from_zero_local_intersection
      psi PUnit LocalIntersectionZero localData h_formula h_zero)

theorem no_chow_zero_from_borcherds_orbit_norms
    {Index Orbit α LocalData : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (chow : Index → α)
    (psi orbitNorm : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_sound : OrbitChowNormSound orbitOf chow orbitNorm)
    (h_formula :
      LocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : OrbitComparisonPayload psi orbitNorm PUnit)
    (h_zero : ∀ orbit, LocalIntersectionZero orbit (localData orbit)) :
    ∀ t, chow t ≠ 0 := by
  intro t h_chow_zero
  have h_norm_punit : PUnit (orbitNorm (orbitOf t)) :=
    orbit_norm_punits_from_borcherds_local_intersections
      psi orbitNorm PUnit LocalIntersectionZero localData h_formula h_compare
      h_zero (orbitOf t)
  have h_norm_nonzero : orbitNorm (orbitOf t) ≠ 0 :=
    h_punit_nonzero (orbitNorm (orbitOf t)) h_norm_punit
  exact h_norm_nonzero (h_sound t h_chow_zero)

theorem no_chow_zero_from_global_borcherds_norm
    {Index α LocalData : Type} [Zero α]
    (chow : Index → α)
    (psi globalNorm : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_sound : GlobalChowNormSound chow globalNorm)
    (h_formula :
      GlobalLocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psi globalNorm PUnit)
    (h_zero : LocalIntersectionZero localData) :
    ∀ t, chow t ≠ 0 := by
  intro t h_chow_zero
  have h_norm_punit : PUnit globalNorm :=
    global_norm_punit_from_borcherds_local_intersection
      psi globalNorm PUnit LocalIntersectionZero localData h_formula h_compare
      h_zero
  have h_norm_nonzero : globalNorm ≠ 0 :=
    h_punit_nonzero globalNorm h_norm_punit
  exact h_norm_nonzero (h_sound t h_chow_zero)

theorem no_bad_from_borcherds_orbit_norms
    {Index Orbit α LocalData : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (chow : Index → α)
    (Bad : Index → Prop)
    (psi orbitNorm : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_sound : OrbitChowNormSound orbitOf chow orbitNorm)
    (h_formula :
      LocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : OrbitComparisonPayload psi orbitNorm PUnit)
    (h_zero : ∀ orbit, LocalIntersectionZero orbit (localData orbit)) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_chow_nonzero : chow t ≠ 0 :=
    no_chow_zero_from_borcherds_orbit_norms
      orbitOf chow psi orbitNorm PUnit LocalIntersectionZero localData
      h_punit_nonzero h_sound h_formula h_compare h_zero t
  exact h_chow_nonzero (h_bad_chow t h_bad)

theorem no_bad_from_global_borcherds_norm
    {Index α LocalData : Type} [Zero α]
    (chow : Index → α)
    (Bad : Index → Prop)
    (psi globalNorm : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_sound : GlobalChowNormSound chow globalNorm)
    (h_formula :
      GlobalLocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psi globalNorm PUnit)
    (h_zero : LocalIntersectionZero localData) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_chow_nonzero : chow t ≠ 0 :=
    no_chow_zero_from_global_borcherds_norm
      chow psi globalNorm PUnit LocalIntersectionZero localData h_punit_nonzero
      h_sound h_formula h_compare h_zero t
  exact h_chow_nonzero (h_bad_chow t h_bad)

theorem selected_good_from_borcherds_chow_norms
    {Index Orbit α LocalData : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (chow : Index → α)
    (Bad Good : Index → Prop)
    (selected : Index)
    (psi orbitNorm : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_sound : OrbitChowNormSound orbitOf chow orbitNorm)
    (h_formula :
      LocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : OrbitComparisonPayload psi orbitNorm PUnit)
    (h_zero : ∀ orbit, LocalIntersectionZero orbit (localData orbit))
    (h_no_bad_good : ∀ t, ¬ Bad t → Good t) :
    Good selected := by
  exact h_no_bad_good selected
    (no_bad_from_borcherds_orbit_norms
      orbitOf chow Bad psi orbitNorm PUnit LocalIntersectionZero localData
      h_punit_nonzero h_bad_chow h_sound h_formula h_compare h_zero selected)

theorem selected_good_from_global_borcherds_chow_norm
    {Index α LocalData : Type} [Zero α]
    (chow : Index → α)
    (Bad Good : Index → Prop)
    (selected : Index)
    (psi globalNorm : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_sound : GlobalChowNormSound chow globalNorm)
    (h_formula :
      GlobalLocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psi globalNorm PUnit)
    (h_zero : LocalIntersectionZero localData)
    (h_no_bad_good : ∀ t, ¬ Bad t → Good t) :
    Good selected := by
  exact h_no_bad_good selected
    (no_bad_from_global_borcherds_norm
      chow Bad psi globalNorm PUnit LocalIntersectionZero localData
      h_punit_nonzero h_bad_chow h_sound h_formula h_compare h_zero selected)

theorem p24_chow_borcherds_payload_subsqrt :
    2 * 7 < 1000000000000 := by
  decide

theorem p24_global_chow_borcherds_payload_subsqrt :
    2 < 1000000000000 := by
  decide

end P24.TraceGcdChowBorcherdsPUnitGate
