/-!
Finite gate for a phase-aware selected-tail producer theorem.

The selected-tail crossed-product gate already says that nonzero orbit
products or reduced norms rule out selected-tail bad events.  A class-field
producer may instead construct a Kummer/phase payload attached to the same
determinant line.  This file records the finite interface such a producer must
meet:

* selected-tail failure forces the local tail determinant to vanish;
* local tail determinant zero forces the orbit phase payload to vanish; and
* all orbit phase payloads are nonzero, or one global phase payload detects
  any zero orbit payload.

No CM arithmetic, Kummer construction, or p-adic unit proof is formalized
here.
-/

namespace P24.TraceFrameSelectedTailPhaseProducerGate

def BadForcesTailDetZero {Beta Scalar : Type} [Zero Scalar]
    (Bad : Beta → Prop)
    (tailDet : Beta → Scalar) : Prop :=
  ∀ beta, Bad beta → tailDet beta = 0

def PhaseDetectsTailDetZero {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (tailDet : Beta → Scalar)
    (phasePayload : Orbit → Scalar) : Prop :=
  ∀ beta, tailDet beta = 0 → phasePayload (orbitOf beta) = 0

def PhaseDetectsReducedNormZero {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm phasePayload : Orbit → Scalar) : Prop :=
  ∀ orbit, reducedNorm orbit = 0 → phasePayload orbit = 0

def BadForcesReducedNormZero {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm : Orbit → Scalar) : Prop :=
  ∀ beta, Bad beta → reducedNorm (orbitOf beta) = 0

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

theorem no_bad_from_tail_phase_payloads
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (tailDet : Beta → Scalar)
    (phasePayload : Orbit → Scalar)
    (h_bad_zero : BadForcesTailDetZero Bad tailDet)
    (h_phase_detects :
      PhaseDetectsTailDetZero orbitOf tailDet phasePayload)
    (h_phase_nonzero : ∀ orbit, phasePayload orbit ≠ 0) :
    ∀ beta, ¬ Bad beta := by
  intro beta h_bad
  exact h_phase_nonzero (orbitOf beta)
    (h_phase_detects beta (h_bad_zero beta h_bad))

theorem no_bad_from_reduced_norm_phase_payloads
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm phasePayload : Orbit → Scalar)
    (h_bad_zero :
      BadForcesReducedNormZero orbitOf Bad reducedNorm)
    (h_phase_detects :
      PhaseDetectsReducedNormZero reducedNorm phasePayload)
    (h_phase_nonzero : ∀ orbit, phasePayload orbit ≠ 0) :
    ∀ beta, ¬ Bad beta := by
  intro beta h_bad
  exact h_phase_nonzero (orbitOf beta)
    (h_phase_detects (orbitOf beta) (h_bad_zero beta h_bad))

theorem phase_payloads_nonzero_from_units
    {Orbit Scalar : Type} [Zero Scalar]
    (phasePayload phaseInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_units :
      ∀ orbit, UnitPayload (phasePayload orbit) (phaseInv orbit) UnitRel) :
    ∀ orbit, phasePayload orbit ≠ 0 := by
  intro orbit
  exact h_unit_nonzero
    (phasePayload orbit)
    (phaseInv orbit)
    (h_units orbit)

theorem no_bad_from_reduced_norm_phase_punits
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm phasePayload phaseInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_bad_zero :
      BadForcesReducedNormZero orbitOf Bad reducedNorm)
    (h_phase_detects :
      PhaseDetectsReducedNormZero reducedNorm phasePayload)
    (h_units :
      ∀ orbit, UnitPayload (phasePayload orbit) (phaseInv orbit) UnitRel) :
    ∀ beta, ¬ Bad beta :=
  no_bad_from_reduced_norm_phase_payloads
    orbitOf Bad reducedNorm phasePayload h_bad_zero h_phase_detects
    (phase_payloads_nonzero_from_units
      phasePayload phaseInv UnitRel h_unit_nonzero h_units)

theorem phase_payloads_nonzero_from_global_phase
    {Orbit Scalar : Type} [Zero Scalar]
    (phasePayload : Orbit → Scalar)
    (globalPhase : Scalar)
    (h_any_phase_zero :
      (∃ orbit, phasePayload orbit = 0) → globalPhase = 0)
    (h_global_nonzero : globalPhase ≠ 0) :
    ∀ orbit, phasePayload orbit ≠ 0 := by
  intro orbit h_zero
  exact h_global_nonzero (h_any_phase_zero ⟨orbit, h_zero⟩)

theorem no_bad_from_global_phase_payload
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm phasePayload : Orbit → Scalar)
    (globalPhase : Scalar)
    (h_bad_zero :
      BadForcesReducedNormZero orbitOf Bad reducedNorm)
    (h_phase_detects :
      PhaseDetectsReducedNormZero reducedNorm phasePayload)
    (h_any_phase_zero :
      (∃ orbit, phasePayload orbit = 0) → globalPhase = 0)
    (h_global_nonzero : globalPhase ≠ 0) :
    ∀ beta, ¬ Bad beta :=
  no_bad_from_reduced_norm_phase_payloads
    orbitOf Bad reducedNorm phasePayload h_bad_zero h_phase_detects
    (phase_payloads_nonzero_from_global_phase
      phasePayload globalPhase h_any_phase_zero h_global_nonzero)

theorem selected_tail_bad_forces_global_phase_zero
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (Bad : Beta → Prop)
    (reducedNorm phasePayload : Orbit → Scalar)
    (globalPhase : Scalar)
    (h_bad_zero :
      BadForcesReducedNormZero orbitOf Bad reducedNorm)
    (h_phase_detects :
      PhaseDetectsReducedNormZero reducedNorm phasePayload)
    (h_any_phase_zero :
      (∃ orbit, phasePayload orbit = 0) → globalPhase = 0) :
    (∃ beta, Bad beta) → globalPhase = 0 := by
  intro h_bad_exists
  rcases h_bad_exists with ⟨beta, h_bad⟩
  apply h_any_phase_zero
  exact ⟨orbitOf beta,
    h_phase_detects (orbitOf beta) (h_bad_zero beta h_bad)⟩

theorem p24_phase_orbit_count_subsqrt :
    560 < 1000000000000 := by
  decide

theorem p24_selected_chain_payload_subsqrt :
    3107811 < 1000000000000 := by
  decide

end P24.TraceFrameSelectedTailPhaseProducerGate
