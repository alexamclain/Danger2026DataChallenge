/-!
Finite gate for a selected-tail Borcherds/local-intersection proof.

The selected-tail phase producer gate says that a nonzero phase payload that
detects selected-tail norm zeros rules out selected-tail bad events.  A
Borcherds or Chow local-intersection proof would provide that nonzero phase
payload by:

* constructing a phase-aware product/divisor value on each orbit;
* proving its selected local intersection is zero, hence its value is a
  p-unit;
* comparing that value to the selected-tail phase/Fitting payload up to
  p-units.

This file records only that finite handoff.  It does not construct a
Borcherds product, a Chow divisor, or a CM local-intersection formula.
-/

namespace P24.TraceFrameSelectedTailBorcherdsGate

def BadForcesReducedNormZero {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm : Orbit → Scalar) : Prop :=
  ∀ beta, Bad beta → reducedNorm (orbitOf beta) = 0

def PhaseDetectsReducedNormZero {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm phasePayload : Orbit → Scalar) : Prop :=
  ∀ orbit, reducedNorm orbit = 0 → phasePayload orbit = 0

def TransfersPUnit {Scalar : Type}
    (source target : Scalar)
    (PUnit : Scalar → Prop) : Prop :=
  PUnit source → PUnit target

theorem phase_punits_from_borcherds_local_intersections
    {Orbit Scalar LocalData : Type}
    (borcherdsValue phasePayload : Orbit → Scalar)
    (localData : Orbit → LocalData)
    (PUnit : Scalar → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (h_local_formula :
      ∀ orbit,
        LocalIntersectionZero (localData orbit) →
          PUnit (borcherdsValue orbit))
    (h_compare :
      ∀ orbit,
        TransfersPUnit (borcherdsValue orbit) (phasePayload orbit)
          PUnit)
    (h_zero_intersection :
      ∀ orbit, LocalIntersectionZero (localData orbit)) :
    ∀ orbit, PUnit (phasePayload orbit) := by
  intro orbit
  exact h_compare orbit (h_local_formula orbit (h_zero_intersection orbit))

theorem phase_payloads_nonzero_from_borcherds
    {Orbit Scalar LocalData : Type} [Zero Scalar]
    (borcherdsValue phasePayload : Orbit → Scalar)
    (localData : Orbit → LocalData)
    (PUnit : Scalar → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_local_formula :
      ∀ orbit,
        LocalIntersectionZero (localData orbit) →
          PUnit (borcherdsValue orbit))
    (h_compare :
      ∀ orbit,
        TransfersPUnit (borcherdsValue orbit) (phasePayload orbit)
          PUnit)
    (h_zero_intersection :
      ∀ orbit, LocalIntersectionZero (localData orbit)) :
    ∀ orbit, phasePayload orbit ≠ 0 := by
  intro orbit
  exact h_punit_nonzero (phasePayload orbit)
    (phase_punits_from_borcherds_local_intersections
      borcherdsValue phasePayload localData PUnit LocalIntersectionZero
      h_local_formula h_compare h_zero_intersection orbit)

theorem no_bad_from_borcherds_selected_tail
    {Beta Orbit Scalar LocalData : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm phasePayload borcherdsValue : Orbit → Scalar)
    (localData : Orbit → LocalData)
    (PUnit : Scalar → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_zero :
      BadForcesReducedNormZero orbitOf Bad reducedNorm)
    (h_phase_detects :
      PhaseDetectsReducedNormZero reducedNorm phasePayload)
    (h_local_formula :
      ∀ orbit,
        LocalIntersectionZero (localData orbit) →
          PUnit (borcherdsValue orbit))
    (h_compare :
      ∀ orbit,
        TransfersPUnit (borcherdsValue orbit) (phasePayload orbit)
          PUnit)
    (h_zero_intersection :
      ∀ orbit, LocalIntersectionZero (localData orbit)) :
    ∀ beta, ¬ Bad beta := by
  intro beta h_bad
  have h_phase_nonzero :
      phasePayload (orbitOf beta) ≠ 0 :=
    phase_payloads_nonzero_from_borcherds
      borcherdsValue phasePayload localData PUnit
      LocalIntersectionZero h_punit_nonzero h_local_formula h_compare
      h_zero_intersection (orbitOf beta)
  exact h_phase_nonzero
    (h_phase_detects (orbitOf beta) (h_bad_zero beta h_bad))

theorem p24_selected_tail_borcherds_orbit_payload_subsqrt :
    560 < 1000000000000 := by
  decide

end P24.TraceFrameSelectedTailBorcherdsGate
