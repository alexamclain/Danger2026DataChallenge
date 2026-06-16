/-!
Finite gate for Plucker-Kummer orbit norms.

The actual-CM descent audit suggests that individual Kummer powers of the
trace-GCD Plucker coordinate need not descend on nontrivial Frobenius orbits.
The robust payload is an orbit norm:

    normKummer O = product_{t in O} localKummer t.

This file records only the finite zero-detection logic.  The arithmetic
producer must still prove that the supplied `normKummer` is the actual orbit
norm of the actual determinant-level Kummer values.
-/

namespace P24.PluckerKummerOrbitNormGate

def KummerDetectsPluckerZero {Index Scalar : Type} [Zero Scalar]
    (plucker localKummer : Index → Scalar) : Prop :=
  ∀ i, plucker i = 0 → localKummer i = 0

def OrbitNormZeroOnLocalZero {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (localKummer : Index → Scalar)
    (normKummer : Orbit → Scalar) : Prop :=
  ∀ i, localKummer i = 0 → normKummer (orbitOf i) = 0

def OrbitNormUnitPayload {Orbit Scalar : Type}
    (normKummer normInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ orbit, UnitRel (normKummer orbit) (normInv orbit)

theorem pluckers_nonzero_from_orbit_norm_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (plucker localKummer : Index → Scalar)
    (normKummer normInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : KummerDetectsPluckerZero plucker localKummer)
    (h_norm_zero : OrbitNormZeroOnLocalZero orbitOf localKummer normKummer)
    (h_payload : OrbitNormUnitPayload normKummer normInv UnitRel) :
    ∀ i, plucker i ≠ 0 := by
  intro i h_plucker_zero
  have h_local_zero : localKummer i = 0 :=
    h_detects i h_plucker_zero
  have h_norm_zero_at_i : normKummer (orbitOf i) = 0 :=
    h_norm_zero i h_local_zero
  have h_norm_nonzero_at_i : normKummer (orbitOf i) ≠ 0 :=
    h_unit_nonzero (normKummer (orbitOf i)) (normInv (orbitOf i))
      (h_payload (orbitOf i))
  exact h_norm_nonzero_at_i h_norm_zero_at_i

theorem selected_good_from_orbit_norm_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (plucker localKummer : Index → Scalar)
    (normKummer normInv : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : KummerDetectsPluckerZero plucker localKummer)
    (h_norm_zero : OrbitNormZeroOnLocalZero orbitOf localKummer normKummer)
    (h_payload : OrbitNormUnitPayload normKummer normInv UnitRel)
    (h_plucker_to_good : ∀ i, plucker i ≠ 0 → Good i) :
    Good selected := by
  exact h_plucker_to_good selected
    (pluckers_nonzero_from_orbit_norm_units orbitOf plucker localKummer
      normKummer normInv UnitRel h_unit_nonzero h_detects h_norm_zero
      h_payload selected)

end P24.PluckerKummerOrbitNormGate
