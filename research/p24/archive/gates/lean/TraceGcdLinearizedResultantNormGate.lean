/-!
Finite gate for the linearized trace-GCD resultant norm.

The remaining p24 arithmetic theorem can be phrased as a p-unit statement for
linearized resultants:

* fixed orbit: a single resultant `Res_0` for the prefix kernel and selected
  tail is a p-unit;
* nonzero orbit: a Frobenius/crossed norm `Norm_1` of the same resultant
  section over a degree-35 right factor is a p-unit.

This file records only the finite implication:

* a resultant detects a nontrivial common zero of prefix kernel plus tail;
* an orbit norm detects any zero resultant in that orbit;
* p-unit payloads are nonzero;
* therefore the fixed and nonzero-orbit trace-GCD bad events are absent.

No subspace polynomial, resultant, CM period, or p-adic theorem is
constructed here.
-/

namespace P24.TraceGcdLinearizedResultantNormGate

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def ResultantDetectsBad {Index Scalar : Type} [Zero Scalar]
    (Bad : Index → Prop)
    (resultant : Index → Scalar) : Prop :=
  ∀ t, Bad t → resultant t = 0

def OrbitNormDetectsResultantZero {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (resultant : Index → Scalar)
    (orbitNorm : Orbit → Scalar) : Prop :=
  ∀ t, resultant t = 0 → orbitNorm (orbitOf t) = 0

theorem no_bad_from_fixed_resultant_punit
    {Index Scalar : Type} [Zero Scalar]
    (Bad : Index → Prop)
    (resultant : Index → Scalar)
    (fixed : Index)
    (fixedInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : ResultantDetectsBad Bad resultant)
    (h_payload : UnitPayload (resultant fixed) fixedInv UnitRel) :
    ¬ Bad fixed := by
  intro h_bad
  have h_res_nonzero : resultant fixed ≠ 0 :=
    h_unit_nonzero (resultant fixed) fixedInv h_payload
  exact h_res_nonzero (h_detects fixed h_bad)

theorem no_bad_on_orbit_from_resultant_norm_punit
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Bad : Index → Prop)
    (resultant : Index → Scalar)
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_bad_resultant : ResultantDetectsBad Bad resultant)
    (h_norm_detects :
      OrbitNormDetectsResultantZero orbitOf resultant orbitNorm)
    (h_payload : ∀ orbit, UnitPayload (orbitNorm orbit) (orbitInv orbit) UnitRel) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_orbit_norm_nonzero : orbitNorm (orbitOf t) ≠ 0 :=
    h_unit_nonzero (orbitNorm (orbitOf t)) (orbitInv (orbitOf t))
      (h_payload (orbitOf t))
  exact h_orbit_norm_nonzero
    (h_norm_detects t (h_bad_resultant t h_bad))

def TwoResultantPayload {Orbit Scalar : Type}
    (fixedResultant fixedInv : Scalar)
    (orbitNorm orbitInv : Orbit → Scalar)
    (representativeOrbit : Orbit)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitPayload fixedResultant fixedInv UnitRel ∧
    UnitPayload (orbitNorm representativeOrbit) (orbitInv representativeOrbit)
      UnitRel

theorem two_resultant_payload_components
    {Orbit Scalar : Type}
    (fixedResultant fixedInv : Scalar)
    (orbitNorm orbitInv : Orbit → Scalar)
    (representativeOrbit : Orbit)
    (UnitRel : Scalar → Scalar → Prop)
    (h_payload :
      TwoResultantPayload fixedResultant fixedInv orbitNorm orbitInv
        representativeOrbit UnitRel) :
    UnitPayload fixedResultant fixedInv UnitRel ∧
      UnitPayload (orbitNorm representativeOrbit)
        (orbitInv representativeOrbit) UnitRel := by
  exact h_payload

theorem p24_two_resultant_payload_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_nonzero_orbit_degree_subsqrt :
    35 < 1000000000000 := by
  decide

end P24.TraceGcdLinearizedResultantNormGate
