/-!
Finite gate for the ordinary trace-GCD Fitting disjointness criterion.

The arithmetic theorem still has to construct the phase-aware Fitting section
and prove its p-adic valuation at the selected ordinary CM point.  This file
records the finite handoff around that theorem:

* zero local intersection gives a p-unit Fitting determinant;
* equivalently, the reduced block map is an isomorphism, or the cokernel has
  unit zeroth Fitting ideal;
* p-unit Fitting determinants detect and exclude every translated
  trace-GCD Schubert bad event.

No p-adic geometry, determinant algebra, or CM class-field construction is
formalized here.
-/

namespace P24.TraceGcdOrdinaryFittingCriterionGate

def Transfers {α : Type} (source target : α) (P : α → Prop) : Prop :=
  P source → P target

def SameStatus {α : Type} (left right : α) (P : α → Prop) : Prop :=
  P left ↔ P right

def FittingPUnitPayload {Orbit α : Type}
    (xi : Orbit → α)
    (PUnit : α → Prop) : Prop :=
  ∀ orbit, PUnit (xi orbit)

def ReducedIsoPayload {Orbit IsoWitness : Type}
    (isIso : Orbit → IsoWitness → Prop)
    (witness : Orbit → IsoWitness) : Prop :=
  ∀ orbit, isIso orbit (witness orbit)

def CokerFittingUnitPayload {Orbit FittingWitness : Type}
    (cokerFittingUnit : Orbit → FittingWitness → Prop)
    (witness : Orbit → FittingWitness) : Prop :=
  ∀ orbit, cokerFittingUnit orbit (witness orbit)

def ZeroLocalIntersectionPayload {Orbit LocalData : Type}
    (ZeroLocalIntersection : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData) : Prop :=
  ∀ orbit, ZeroLocalIntersection orbit (localData orbit)

def OrdinaryFittingCriterion
    {Orbit α IsoWitness FittingWitness LocalData : Type}
    (xi : Orbit → α)
    (PUnit : α → Prop)
    (isIso : Orbit → IsoWitness → Prop)
    (isoWitness : Orbit → IsoWitness)
    (cokerFittingUnit : Orbit → FittingWitness → Prop)
    (fittingWitness : Orbit → FittingWitness)
    (ZeroLocalIntersection : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData) : Prop :=
  ∀ orbit,
    (ZeroLocalIntersection orbit (localData orbit) → PUnit (xi orbit)) ∧
    (isIso orbit (isoWitness orbit) → PUnit (xi orbit)) ∧
    (cokerFittingUnit orbit (fittingWitness orbit) → PUnit (xi orbit))

def OrbitNormDetectsDeltaZero {Index Orbit α : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (delta : Index → α)
    (xi : Orbit → α) : Prop :=
  ∀ t, delta t = 0 → xi (orbitOf t) = 0

def SchubertBadForcesDeltaZero {Index α : Type} [Zero α]
    (Bad : Index → Prop)
    (delta : Index → α) : Prop :=
  ∀ t, Bad t → delta t = 0

theorem fitting_punits_from_zero_local_intersections
    {Orbit α IsoWitness FittingWitness LocalData : Type}
    (xi : Orbit → α)
    (PUnit : α → Prop)
    (isIso : Orbit → IsoWitness → Prop)
    (isoWitness : Orbit → IsoWitness)
    (cokerFittingUnit : Orbit → FittingWitness → Prop)
    (fittingWitness : Orbit → FittingWitness)
    (ZeroLocalIntersection : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_criterion :
      OrdinaryFittingCriterion xi PUnit isIso isoWitness cokerFittingUnit
        fittingWitness ZeroLocalIntersection localData)
    (h_zero :
      ZeroLocalIntersectionPayload ZeroLocalIntersection localData) :
    FittingPUnitPayload xi PUnit := by
  intro orbit
  exact (h_criterion orbit).1 (h_zero orbit)

theorem fitting_punits_from_reduced_isomorphisms
    {Orbit α IsoWitness FittingWitness LocalData : Type}
    (xi : Orbit → α)
    (PUnit : α → Prop)
    (isIso : Orbit → IsoWitness → Prop)
    (isoWitness : Orbit → IsoWitness)
    (cokerFittingUnit : Orbit → FittingWitness → Prop)
    (fittingWitness : Orbit → FittingWitness)
    (ZeroLocalIntersection : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_criterion :
      OrdinaryFittingCriterion xi PUnit isIso isoWitness cokerFittingUnit
        fittingWitness ZeroLocalIntersection localData)
    (h_iso : ReducedIsoPayload isIso isoWitness) :
    FittingPUnitPayload xi PUnit := by
  intro orbit
  exact (h_criterion orbit).2.1 (h_iso orbit)

theorem fitting_punits_from_coker_fitting_units
    {Orbit α IsoWitness FittingWitness LocalData : Type}
    (xi : Orbit → α)
    (PUnit : α → Prop)
    (isIso : Orbit → IsoWitness → Prop)
    (isoWitness : Orbit → IsoWitness)
    (cokerFittingUnit : Orbit → FittingWitness → Prop)
    (fittingWitness : Orbit → FittingWitness)
    (ZeroLocalIntersection : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_criterion :
      OrdinaryFittingCriterion xi PUnit isIso isoWitness cokerFittingUnit
        fittingWitness ZeroLocalIntersection localData)
    (h_fitting : CokerFittingUnitPayload cokerFittingUnit fittingWitness) :
    FittingPUnitPayload xi PUnit := by
  intro orbit
  exact (h_criterion orbit).2.2 (h_fitting orbit)

theorem delta_nonzero_from_fitting_punits
    {Index Orbit α : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (delta : Index → α)
    (xi : Orbit → α)
    (PUnit : α → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_detects : OrbitNormDetectsDeltaZero orbitOf delta xi)
    (h_punits : FittingPUnitPayload xi PUnit) :
    ∀ t, delta t ≠ 0 := by
  intro t h_delta_zero
  have h_xi_nonzero : xi (orbitOf t) ≠ 0 :=
    h_punit_nonzero (xi (orbitOf t)) (h_punits (orbitOf t))
  exact h_xi_nonzero (h_detects t h_delta_zero)

theorem no_schubert_bad_from_fitting_punits
    {Index Orbit α : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (Bad : Index → Prop)
    (delta : Index → α)
    (xi : Orbit → α)
    (PUnit : α → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_zero : SchubertBadForcesDeltaZero Bad delta)
    (h_detects : OrbitNormDetectsDeltaZero orbitOf delta xi)
    (h_punits : FittingPUnitPayload xi PUnit) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_delta_nonzero : delta t ≠ 0 :=
    delta_nonzero_from_fitting_punits orbitOf delta xi PUnit
      h_punit_nonzero h_detects h_punits t
  exact h_delta_nonzero (h_bad_zero t h_bad)

theorem no_schubert_bad_from_zero_local_intersections
    {Index Orbit α IsoWitness FittingWitness LocalData : Type} [Zero α]
    (orbitOf : Index → Orbit)
    (Bad : Index → Prop)
    (delta : Index → α)
    (xi : Orbit → α)
    (PUnit : α → Prop)
    (isIso : Orbit → IsoWitness → Prop)
    (isoWitness : Orbit → IsoWitness)
    (cokerFittingUnit : Orbit → FittingWitness → Prop)
    (fittingWitness : Orbit → FittingWitness)
    (ZeroLocalIntersection : Orbit → LocalData → Prop)
    (localData : Orbit → LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_criterion :
      OrdinaryFittingCriterion xi PUnit isIso isoWitness cokerFittingUnit
        fittingWitness ZeroLocalIntersection localData)
    (h_zero :
      ZeroLocalIntersectionPayload ZeroLocalIntersection localData)
    (h_bad_zero : SchubertBadForcesDeltaZero Bad delta)
    (h_detects : OrbitNormDetectsDeltaZero orbitOf delta xi) :
    ∀ t, ¬ Bad t := by
  exact no_schubert_bad_from_fitting_punits orbitOf Bad delta xi PUnit
    h_punit_nonzero h_bad_zero h_detects
    (fitting_punits_from_zero_local_intersections
      xi PUnit isIso isoWitness cokerFittingUnit fittingWitness
      ZeroLocalIntersection localData h_criterion h_zero)

theorem p24_orbit_fitting_payload_subsqrt :
    2 * 7 < 1000000000000 := by
  decide

theorem p24_diamond_compressed_fitting_payload_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_diamond_compressed_payload_improves_orbit_payload :
    4 < 2 * 7 := by
  decide

theorem p24_hcoset_equation_count_is_separate_verifier_interface :
    156 * 7 = 1092 ∧ 4 < 1092 := by
  decide

end P24.TraceGcdOrdinaryFittingCriterionGate
