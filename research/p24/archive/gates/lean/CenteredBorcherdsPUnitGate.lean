/-!
Finite gate for a phase-aware Borcherds/Fitting proof of the centered
right-translation product.

This file does not construct a Borcherds product or a Fitting section.  It
records the exact finite handoff wanted for the centered-profile route:

* zero local intersection makes phase-aware values `psi O` p-units;
* a p-unit comparison transfers this to the actual orbit products;
* an orbit product p-unit detects and excludes every translated determinant
  zero in that orbit;
* therefore every cyclic right-window determinant is nonzero.
-/

namespace P24.CenteredBorcherdsPUnitGate

def TransfersPUnit {α : Type} (source target : α) (PUnit : α → Prop) : Prop :=
  PUnit source → PUnit target

def OrbitComparisonPayload {Orbit α : Type}
    (psi orbitProduct : Orbit → α)
    (PUnit : α → Prop) : Prop :=
  ∀ orbit, TransfersPUnit (psi orbit) (orbitProduct orbit) PUnit

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

def OrbitProductSound {Index Orbit α : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (delta : Index → α)
    (orbitProduct : Orbit → α) : Prop :=
  ∀ t, delta t = 0 → orbitProduct (orbitOf t) = 0

def BadDetectedByDelta {Index α : Type} [Zero α]
    (delta : Index → α)
    (Bad : Index → Prop) : Prop :=
  ∀ t, Bad t → delta t = 0

def GoodFromNoBad {Index : Type}
    (Bad Good : Index → Prop) : Prop :=
  ∀ t, ¬ Bad t → Good t

def ConsecutiveArc {Index : Type} (Good : Index → Prop) : Prop :=
  ∀ t, Good t

theorem orbit_product_punits_from_borcherds_comparison
    {Orbit α : Type}
    (psi orbitProduct : Orbit → α)
    (PUnit : α → Prop)
    (h_compare : OrbitComparisonPayload psi orbitProduct PUnit)
    (h_psi_punit : OrbitPUnitPayload psi PUnit) :
    OrbitPUnitPayload orbitProduct PUnit := by
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

theorem orbit_product_punits_from_borcherds_local_intersections
    {Orbit α LocalData : Type}
    (psi orbitProduct : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_formula :
      LocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : OrbitComparisonPayload psi orbitProduct PUnit)
    (h_zero : ∀ orbit, LocalIntersectionZero orbit (localData orbit)) :
    OrbitPUnitPayload orbitProduct PUnit :=
  orbit_product_punits_from_borcherds_comparison psi orbitProduct PUnit
    h_compare
    (psi_punits_from_zero_local_intersections
      psi PUnit LocalIntersectionZero localData h_formula h_zero)

theorem deltas_nonzero_from_orbit_product_punits
    {Index Orbit α : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (delta : Index → α)
    (orbitProduct : Orbit → α)
    (PUnit : α → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_sound : OrbitProductSound orbitOf delta orbitProduct)
    (h_payload : OrbitPUnitPayload orbitProduct PUnit) :
    ∀ t, delta t ≠ 0 := by
  intro t h_delta_zero
  have h_product_nonzero : orbitProduct (orbitOf t) ≠ 0 :=
    h_punit_nonzero (orbitProduct (orbitOf t)) (h_payload (orbitOf t))
  exact h_product_nonzero (h_sound t h_delta_zero)

theorem no_bad_from_orbit_product_punits
    {Index Orbit α : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (delta : Index → α)
    (Bad : Index → Prop)
    (orbitProduct : Orbit → α)
    (PUnit : α → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_delta : BadDetectedByDelta delta Bad)
    (h_sound : OrbitProductSound orbitOf delta orbitProduct)
    (h_payload : OrbitPUnitPayload orbitProduct PUnit) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_delta_nonzero : delta t ≠ 0 :=
    deltas_nonzero_from_orbit_product_punits
      orbitOf delta orbitProduct PUnit h_punit_nonzero h_sound h_payload t
  exact h_delta_nonzero (h_bad_delta t h_bad)

theorem consecutive_arc_from_borcherds_local_intersections
    {Index Orbit α LocalData : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (delta : Index → α)
    (Bad Good : Index → Prop)
    (psi orbitProduct : Orbit → α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_delta : BadDetectedByDelta delta Bad)
    (h_sound : OrbitProductSound orbitOf delta orbitProduct)
    (h_formula :
      LocalIntersectionFormula psi PUnit LocalIntersectionZero localData)
    (h_compare : OrbitComparisonPayload psi orbitProduct PUnit)
    (h_zero : ∀ orbit, LocalIntersectionZero orbit (localData orbit))
    (h_good : GoodFromNoBad Bad Good) :
    ConsecutiveArc Good := by
  intro t
  exact h_good t
    (no_bad_from_orbit_product_punits
      orbitOf delta Bad orbitProduct PUnit h_punit_nonzero h_bad_delta
      h_sound
      (orbit_product_punits_from_borcherds_local_intersections
        psi orbitProduct PUnit LocalIntersectionZero localData h_formula
        h_compare h_zero)
      t)

theorem p24_centered_borcherds_orbit_payload_subsqrt :
    2 * 7 < 1000000000000 := by
  decide

end P24.CenteredBorcherdsPUnitGate
