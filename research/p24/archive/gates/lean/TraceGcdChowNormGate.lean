/-!
Finite gate for the orbit Chow-norm formulation of the trace-GCD theorem.

The arithmetic/geometric theorem should identify the determinant value

    Delta(t) = det(P V_t W)

with a Chow/Schubert hyperplane evaluation of the translated complementary
subspace against the CM 16-plane.  This file records only the finite
consequence:

* Chow zero is the Schubert bad event;
* the orbit Chow norm detects any Chow zero in that orbit;
* orbit Chow norms are units;
* therefore no Schubert bad event occurs, and the determinant values are
  nonzero when determinant zero forces Chow zero.

No Grassmannian, Chow form, determinant, or class-field construction is
formalized here.
-/

namespace P24.TraceGcdChowNormGate

def ZeroCompatible {Index Scalar : Type} [Zero Scalar]
    (left right : Index → Scalar) : Prop :=
  ∀ t, left t = 0 ↔ right t = 0

def ChowDetectsBad {Index Scalar : Type} [Zero Scalar]
    (chow : Index → Scalar)
    (Bad : Index → Prop) : Prop :=
  ∀ t, Bad t → chow t = 0

def BadDetectsChowZero {Index Scalar : Type} [Zero Scalar]
    (chow : Index → Scalar)
    (Bad : Index → Prop) : Prop :=
  ∀ t, chow t = 0 → Bad t

def OrbitChowNormSound {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (chow : Index → Scalar)
    (orbitNorm : Orbit → Scalar) : Prop :=
  ∀ t, chow t = 0 → orbitNorm (orbitOf t) = 0

def OrbitUnitPayload {Orbit Scalar : Type}
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ orbit, UnitRel (orbitNorm orbit) (orbitInv orbit)

theorem no_chow_zero_from_orbit_norm_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (chow : Index → Scalar)
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_sound : OrbitChowNormSound orbitOf chow orbitNorm)
    (h_payload : OrbitUnitPayload orbitNorm orbitInv UnitRel) :
    ∀ t, chow t ≠ 0 := by
  intro t h_chow_zero
  have h_norm_nonzero : orbitNorm (orbitOf t) ≠ 0 :=
    h_unit_nonzero (orbitNorm (orbitOf t)) (orbitInv (orbitOf t))
      (h_payload (orbitOf t))
  exact h_norm_nonzero (h_sound t h_chow_zero)

theorem no_bad_from_chow_orbit_norm_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (chow : Index → Scalar)
    (Bad : Index → Prop)
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_sound : OrbitChowNormSound orbitOf chow orbitNorm)
    (h_payload : OrbitUnitPayload orbitNorm orbitInv UnitRel) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_chow_nonzero : chow t ≠ 0 :=
    no_chow_zero_from_orbit_norm_units
      orbitOf chow orbitNorm orbitInv UnitRel h_unit_nonzero h_sound
      h_payload t
  exact h_chow_nonzero (h_bad_chow t h_bad)

theorem deltas_nonzero_from_chow_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (delta chow : Index → Scalar)
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_delta_chow_zero : ∀ t, delta t = 0 → chow t = 0)
    (h_sound : OrbitChowNormSound orbitOf chow orbitNorm)
    (h_payload : OrbitUnitPayload orbitNorm orbitInv UnitRel) :
    ∀ t, delta t ≠ 0 := by
  intro t h_delta_zero
  have h_chow_nonzero : chow t ≠ 0 :=
    no_chow_zero_from_orbit_norm_units
      orbitOf chow orbitNorm orbitInv UnitRel h_unit_nonzero h_sound
      h_payload t
  exact h_chow_nonzero (h_delta_chow_zero t h_delta_zero)

theorem selected_good_from_chow_orbit_norm_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (chow : Index → Scalar)
    (Bad Good : Index → Prop)
    (selected : Index)
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_sound : OrbitChowNormSound orbitOf chow orbitNorm)
    (h_payload : OrbitUnitPayload orbitNorm orbitInv UnitRel)
    (h_no_bad_good : ∀ t, ¬ Bad t → Good t) :
    Good selected := by
  exact h_no_bad_good selected
    (no_bad_from_chow_orbit_norm_units
      orbitOf chow Bad orbitNorm orbitInv UnitRel h_unit_nonzero h_bad_chow
      h_sound h_payload selected)

def p24NonzeroOrbitChowTermCount : Nat := 4059928950

theorem p24_nonzero_orbit_chow_terms_subsqrt :
    p24NonzeroOrbitChowTermCount < 1000000000000 := by
  decide

theorem p24_orbit_chow_payload_subsqrt :
    2 * 7 < 1000000000000 := by
  decide

end P24.TraceGcdChowNormGate
