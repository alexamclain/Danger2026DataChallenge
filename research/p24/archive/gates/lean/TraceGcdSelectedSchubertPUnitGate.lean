/-!
Finite gate for the selected Schubert p-unit form of the trace-GCD route.

The arithmetic theorem should construct an honest p-integral determinant
section whose norm detects the selected Schubert bad events:

    Bad t  <=>  Delta(t) = 0

and then prove that the total norm or the seven orbit norms are p-units at the
selected prime above p.  This file checks only the finite consequence:

* a p-unit norm is nonzero;
* a norm that detects bad events cannot be nonzero if a bad event occurs;
* therefore every translated Schubert bad event is absent.

No determinant, local intersection, class-field, or p-adic unit theorem is
formalized here.
-/

namespace P24.TraceGcdSelectedSchubertPUnitGate

def NormDetectsBad {Index Scalar : Type} [Zero Scalar]
    (Bad : Index → Prop) (norm : Scalar) : Prop :=
  (∃ t, Bad t) → norm = 0

def OrbitNormDetectsBad {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Bad : Index → Prop)
    (orbitNorm : Orbit → Scalar) : Prop :=
  ∀ t, Bad t → orbitNorm (orbitOf t) = 0

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def OrbitUnitPayload {Orbit Scalar : Type}
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ orbit, UnitRel (orbitNorm orbit) (orbitInv orbit)

theorem no_bad_from_norm_punit
    {Index Scalar : Type} [Zero Scalar]
    (Bad : Index → Prop)
    (norm normInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : NormDetectsBad Bad norm)
    (h_payload : UnitPayload norm normInv UnitRel) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_norm_nonzero : norm ≠ 0 :=
    h_unit_nonzero norm normInv h_payload
  exact h_norm_nonzero (h_detects ⟨t, h_bad⟩)

theorem no_bad_from_orbit_norm_punits
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Bad : Index → Prop)
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : OrbitNormDetectsBad orbitOf Bad orbitNorm)
    (h_payload : OrbitUnitPayload orbitNorm orbitInv UnitRel) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_orbit_nonzero : orbitNorm (orbitOf t) ≠ 0 :=
    h_unit_nonzero (orbitNorm (orbitOf t)) (orbitInv (orbitOf t))
      (h_payload (orbitOf t))
  exact h_orbit_nonzero (h_detects t h_bad)

theorem determinants_nonzero_from_schubert_avoidance
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (Bad : Index → Prop)
    (h_delta_zero_bad : ∀ t, Delta t = 0 → Bad t)
    (h_no_bad : ∀ t, ¬ Bad t) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_zero
  exact h_no_bad t (h_delta_zero_bad t h_zero)

theorem selected_good_from_norm_punit
    {Index Scalar : Type} [Zero Scalar]
    (Bad Good : Index → Prop)
    (selected : Index)
    (norm normInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : NormDetectsBad Bad norm)
    (h_payload : UnitPayload norm normInv UnitRel)
    (h_no_bad_good : ∀ t, ¬ Bad t → Good t) :
    Good selected := by
  exact h_no_bad_good selected
    (no_bad_from_norm_punit
      Bad norm normInv UnitRel h_unit_nonzero h_detects h_payload selected)

theorem selected_good_from_orbit_norm_punits
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Bad Good : Index → Prop)
    (selected : Index)
    (orbitNorm orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : OrbitNormDetectsBad orbitOf Bad orbitNorm)
    (h_payload : OrbitUnitPayload orbitNorm orbitInv UnitRel)
    (h_no_bad_good : ∀ t, ¬ Bad t → Good t) :
    Good selected := by
  exact h_no_bad_good selected
    (no_bad_from_orbit_norm_punits
      orbitOf Bad orbitNorm orbitInv UnitRel h_unit_nonzero h_detects
      h_payload selected)

theorem p24_pointwise_payload_subsqrt :
    2 * 211 < 1000000000000 := by
  decide

theorem p24_orbit_payload_subsqrt :
    2 * 7 < 1000000000000 := by
  decide

theorem p24_metric_gram_payload_subsqrt :
    4 * 7 < 1000000000000 := by
  decide

end P24.TraceGcdSelectedSchubertPUnitGate
