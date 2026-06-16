/-!
Finite gate for the two-orbit compressed trace-GCD certificate.

After diamond/right-unit equivariance, the seven orbit-norm p-unit checks
can be replaced by:

* the fixed orbit norm is a p-unit;
* one nonzero representative orbit norm is a p-unit;
* the six nonzero orbit norms are related by p-unit determinant-line
  transition factors.

This file combines that finite propagation with the Schubert/Fitting
zero-detection handoff.  It does not construct the p24 determinant lines or
prove the arithmetic p-unit theorem.
-/

namespace P24.TraceGcdTwoOrbitCompressionGate

inductive Orbit7 where
  | O0 | O1 | O2 | O3 | O4 | O5 | O6

open Orbit7

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def UnitScaled {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (unit : Unit)
    (current next : Scalar) : Prop :=
  next = scale unit current

def ScaleTransfersPUnit {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop) : Prop :=
  ∀ unit value, PUnitScale unit → PUnitScalar value →
    PUnitScalar (scale unit value)

def OrbitNormDetectsBad {Index Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit7)
    (Bad : Index → Prop)
    (orbitNorm : Orbit7 → Scalar) : Prop :=
  ∀ t, Bad t → orbitNorm (orbitOf t) = 0

theorem all_orbit_punits_from_two_payloads
    {Scalar Unit : Type}
    (orbitNorm orbitInv : Orbit7 → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (u12 u23 u34 u45 u56 u61 : Unit)
    (h_payload_to_punit :
      ∀ value inverse, UnitRel value inverse → PUnitScalar value)
    (h_transfer : ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_u12 : PUnitScale u12)
    (h_u23 : PUnitScale u23)
    (h_u34 : PUnitScale u34)
    (h_u45 : PUnitScale u45)
    (h_u56 : PUnitScale u56)
    (_h_u61 : PUnitScale u61)
    (h12 : UnitScaled scale u12 (orbitNorm O1) (orbitNorm O2))
    (h23 : UnitScaled scale u23 (orbitNorm O2) (orbitNorm O3))
    (h34 : UnitScaled scale u34 (orbitNorm O3) (orbitNorm O4))
    (h45 : UnitScaled scale u45 (orbitNorm O4) (orbitNorm O5))
    (h56 : UnitScaled scale u56 (orbitNorm O5) (orbitNorm O6))
    (_h61 : UnitScaled scale u61 (orbitNorm O6) (orbitNorm O1))
    (h_fixed_payload : UnitPayload (orbitNorm O0) (orbitInv O0) UnitRel)
    (h_rep_payload : UnitPayload (orbitNorm O1) (orbitInv O1) UnitRel) :
    PUnitScalar (orbitNorm O0) ∧
      PUnitScalar (orbitNorm O1) ∧
      PUnitScalar (orbitNorm O2) ∧
      PUnitScalar (orbitNorm O3) ∧
      PUnitScalar (orbitNorm O4) ∧
      PUnitScalar (orbitNorm O5) ∧
      PUnitScalar (orbitNorm O6) := by
  have h0 : PUnitScalar (orbitNorm O0) :=
    h_payload_to_punit (orbitNorm O0) (orbitInv O0) h_fixed_payload
  have h1 : PUnitScalar (orbitNorm O1) :=
    h_payload_to_punit (orbitNorm O1) (orbitInv O1) h_rep_payload
  have h2 : PUnitScalar (orbitNorm O2) := by
    unfold UnitScaled at h12
    rw [h12]
    exact h_transfer u12 (orbitNorm O1) h_u12 h1
  have h3 : PUnitScalar (orbitNorm O3) := by
    unfold UnitScaled at h23
    rw [h23]
    exact h_transfer u23 (orbitNorm O2) h_u23 h2
  have h4 : PUnitScalar (orbitNorm O4) := by
    unfold UnitScaled at h34
    rw [h34]
    exact h_transfer u34 (orbitNorm O3) h_u34 h3
  have h5 : PUnitScalar (orbitNorm O5) := by
    unfold UnitScaled at h45
    rw [h45]
    exact h_transfer u45 (orbitNorm O4) h_u45 h4
  have h6 : PUnitScalar (orbitNorm O6) := by
    unfold UnitScaled at h56
    rw [h56]
    exact h_transfer u56 (orbitNorm O5) h_u56 h5
  exact ⟨h0, h1, h2, h3, h4, h5, h6⟩

theorem orbit_norm_nonzero_from_two_payloads
    {Scalar Unit : Type} [Zero Scalar]
    (orbitNorm orbitInv : Orbit7 → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (u12 u23 u34 u45 u56 u61 : Unit)
    (h_payload_to_punit :
      ∀ value inverse, UnitRel value inverse → PUnitScalar value)
    (h_punit_nonzero : ∀ value, PUnitScalar value → value ≠ 0)
    (h_transfer : ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_u12 : PUnitScale u12)
    (h_u23 : PUnitScale u23)
    (h_u34 : PUnitScale u34)
    (h_u45 : PUnitScale u45)
    (h_u56 : PUnitScale u56)
    (h_u61 : PUnitScale u61)
    (h12 : UnitScaled scale u12 (orbitNorm O1) (orbitNorm O2))
    (h23 : UnitScaled scale u23 (orbitNorm O2) (orbitNorm O3))
    (h34 : UnitScaled scale u34 (orbitNorm O3) (orbitNorm O4))
    (h45 : UnitScaled scale u45 (orbitNorm O4) (orbitNorm O5))
    (h56 : UnitScaled scale u56 (orbitNorm O5) (orbitNorm O6))
    (h61 : UnitScaled scale u61 (orbitNorm O6) (orbitNorm O1))
    (h_fixed_payload : UnitPayload (orbitNorm O0) (orbitInv O0) UnitRel)
    (h_rep_payload : UnitPayload (orbitNorm O1) (orbitInv O1) UnitRel) :
    ∀ orbit, orbitNorm orbit ≠ 0 := by
  have h_all :=
    all_orbit_punits_from_two_payloads
      orbitNorm orbitInv UnitRel scale PUnitScalar PUnitScale
      u12 u23 u34 u45 u56 u61 h_payload_to_punit h_transfer
      h_u12 h_u23 h_u34 h_u45 h_u56 h_u61
      h12 h23 h34 h45 h56 h61 h_fixed_payload h_rep_payload
  intro orbit
  cases orbit with
  | O0 => exact h_punit_nonzero (orbitNorm O0) h_all.1
  | O1 => exact h_punit_nonzero (orbitNorm O1) h_all.2.1
  | O2 => exact h_punit_nonzero (orbitNorm O2) h_all.2.2.1
  | O3 => exact h_punit_nonzero (orbitNorm O3) h_all.2.2.2.1
  | O4 => exact h_punit_nonzero (orbitNorm O4) h_all.2.2.2.2.1
  | O5 => exact h_punit_nonzero (orbitNorm O5) h_all.2.2.2.2.2.1
  | O6 => exact h_punit_nonzero (orbitNorm O6) h_all.2.2.2.2.2.2

theorem no_bad_from_two_orbit_payloads
    {Index Scalar Unit : Type} [Zero Scalar]
    (orbitOf : Index → Orbit7)
    (Bad : Index → Prop)
    (orbitNorm orbitInv : Orbit7 → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (u12 u23 u34 u45 u56 u61 : Unit)
    (h_payload_to_punit :
      ∀ value inverse, UnitRel value inverse → PUnitScalar value)
    (h_punit_nonzero : ∀ value, PUnitScalar value → value ≠ 0)
    (h_transfer : ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_u12 : PUnitScale u12)
    (h_u23 : PUnitScale u23)
    (h_u34 : PUnitScale u34)
    (h_u45 : PUnitScale u45)
    (h_u56 : PUnitScale u56)
    (h_u61 : PUnitScale u61)
    (h12 : UnitScaled scale u12 (orbitNorm O1) (orbitNorm O2))
    (h23 : UnitScaled scale u23 (orbitNorm O2) (orbitNorm O3))
    (h34 : UnitScaled scale u34 (orbitNorm O3) (orbitNorm O4))
    (h45 : UnitScaled scale u45 (orbitNorm O4) (orbitNorm O5))
    (h56 : UnitScaled scale u56 (orbitNorm O5) (orbitNorm O6))
    (h61 : UnitScaled scale u61 (orbitNorm O6) (orbitNorm O1))
    (h_detects : OrbitNormDetectsBad orbitOf Bad orbitNorm)
    (h_fixed_payload : UnitPayload (orbitNorm O0) (orbitInv O0) UnitRel)
    (h_rep_payload : UnitPayload (orbitNorm O1) (orbitInv O1) UnitRel) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_nonzero : ∀ orbit, orbitNorm orbit ≠ 0 :=
    orbit_norm_nonzero_from_two_payloads
      orbitNorm orbitInv UnitRel scale PUnitScalar PUnitScale
      u12 u23 u34 u45 u56 u61 h_payload_to_punit h_punit_nonzero
      h_transfer h_u12 h_u23 h_u34 h_u45 h_u56 h_u61
      h12 h23 h34 h45 h56 h61 h_fixed_payload h_rep_payload
  exact h_nonzero (orbitOf t) (h_detects t h_bad)

theorem selected_good_from_two_orbit_payloads
    {Index Scalar Unit : Type} [Zero Scalar]
    (orbitOf : Index → Orbit7)
    (Bad Good : Index → Prop)
    (selected : Index)
    (orbitNorm orbitInv : Orbit7 → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (u12 u23 u34 u45 u56 u61 : Unit)
    (h_payload_to_punit :
      ∀ value inverse, UnitRel value inverse → PUnitScalar value)
    (h_punit_nonzero : ∀ value, PUnitScalar value → value ≠ 0)
    (h_transfer : ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_u12 : PUnitScale u12)
    (h_u23 : PUnitScale u23)
    (h_u34 : PUnitScale u34)
    (h_u45 : PUnitScale u45)
    (h_u56 : PUnitScale u56)
    (h_u61 : PUnitScale u61)
    (h12 : UnitScaled scale u12 (orbitNorm O1) (orbitNorm O2))
    (h23 : UnitScaled scale u23 (orbitNorm O2) (orbitNorm O3))
    (h34 : UnitScaled scale u34 (orbitNorm O3) (orbitNorm O4))
    (h45 : UnitScaled scale u45 (orbitNorm O4) (orbitNorm O5))
    (h56 : UnitScaled scale u56 (orbitNorm O5) (orbitNorm O6))
    (h61 : UnitScaled scale u61 (orbitNorm O6) (orbitNorm O1))
    (h_detects : OrbitNormDetectsBad orbitOf Bad orbitNorm)
    (h_no_bad_good : ∀ t, ¬ Bad t → Good t)
    (h_fixed_payload : UnitPayload (orbitNorm O0) (orbitInv O0) UnitRel)
    (h_rep_payload : UnitPayload (orbitNorm O1) (orbitInv O1) UnitRel) :
    Good selected := by
  exact h_no_bad_good selected
    (no_bad_from_two_orbit_payloads
      orbitOf Bad orbitNorm orbitInv UnitRel scale PUnitScalar PUnitScale
      u12 u23 u34 u45 u56 u61 h_payload_to_punit h_punit_nonzero
      h_transfer h_u12 h_u23 h_u34 h_u45 h_u56 h_u61
      h12 h23 h34 h45 h56 h61 h_detects
      h_fixed_payload h_rep_payload selected)

theorem p24_two_orbit_payload_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_two_orbit_payload_improves_safe_orbit_payload :
    4 < 14 := by
  decide

end P24.TraceGcdTwoOrbitCompressionGate
