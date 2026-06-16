/-!
Finite gate for Plucker-Kummer determinant payloads.

Coordinatewise Kummer p-units do not imply that a determinant is nonzero.
The useful payload is a Kummer/p-unit attached to the Plucker coordinate
itself.  This file records the finite implication:

* if determinant zero forces the corresponding Plucker-Kummer payload zero,
* and the Plucker-Kummer payload is nonzero,
* then the determinant is nonzero.

This is the interface needed for a direct p24 trace-GCD producer theorem that
constructs Kummer powers of `det(P V_t A)` or of orbit products thereof.
-/

namespace P24.PluckerKummerGate

def KummerDetectsPluckerZero {Index Scalar : Type} [Zero Scalar]
    (plucker kummer : Index → Scalar) : Prop :=
  ∀ i, plucker i = 0 → kummer i = 0

def OrbitKummerDetectsPluckerZero {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (plucker : Index → Scalar)
    (orbitKummer : Orbit → Scalar) : Prop :=
  ∀ i, plucker i = 0 → orbitKummer (orbitOf i) = 0

theorem pluckers_nonzero_from_plucker_kummers
    {Index Scalar : Type} [Zero Scalar]
    (plucker kummer : Index → Scalar)
    (h_detects : KummerDetectsPluckerZero plucker kummer)
    (h_kummer_nonzero : ∀ i, kummer i ≠ 0) :
    ∀ i, plucker i ≠ 0 := by
  intro i h_zero
  exact h_kummer_nonzero i (h_detects i h_zero)

theorem pluckers_nonzero_from_orbit_kummers
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (plucker : Index → Scalar)
    (orbitKummer : Orbit → Scalar)
    (h_detects :
      OrbitKummerDetectsPluckerZero orbitOf plucker orbitKummer)
    (h_kummer_nonzero : ∀ orbit, orbitKummer orbit ≠ 0) :
    ∀ i, plucker i ≠ 0 := by
  intro i h_zero
  exact h_kummer_nonzero (orbitOf i) (h_detects i h_zero)

theorem selected_good_from_plucker_kummers
    {Index Scalar : Type} [Zero Scalar]
    (plucker kummer : Index → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (h_detects : KummerDetectsPluckerZero plucker kummer)
    (h_kummer_nonzero : ∀ i, kummer i ≠ 0)
    (h_plucker_to_good : ∀ i, plucker i ≠ 0 → Good i) :
    Good selected := by
  exact h_plucker_to_good selected
    (pluckers_nonzero_from_plucker_kummers plucker kummer
      h_detects h_kummer_nonzero selected)

theorem selected_good_from_orbit_kummers
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (plucker : Index → Scalar)
    (orbitKummer : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (h_detects :
      OrbitKummerDetectsPluckerZero orbitOf plucker orbitKummer)
    (h_kummer_nonzero : ∀ orbit, orbitKummer orbit ≠ 0)
    (h_plucker_to_good : ∀ i, plucker i ≠ 0 → Good i) :
    Good selected := by
  exact h_plucker_to_good selected
    (pluckers_nonzero_from_orbit_kummers orbitOf plucker orbitKummer
      h_detects h_kummer_nonzero selected)

end P24.PluckerKummerGate
