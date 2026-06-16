/-!
Finite payload gates for the p24 trace-GCD certificate surface.

The arithmetic object is the determinant sequence

    Delta t = det(P V_t A),        t : Z/211Z.

This file deliberately uses only Lean core.  It does not formalize finite
field multiplication or determinants.  Instead it records the finite
interfaces that prevent a compressed certificate from smuggling in an
unproved product identity:

* pointwise value/inverse payloads prove every `Delta t` nonzero directly;
* orbit-product payloads also need a soundness theorem saying any zero
  `Delta t` would zero the named orbit product;
* one-scalar norm/resultant payloads need the analogous zero-detection
  theorem for the actual determinant sequence.

The missing p24 work is the arithmetic producer theorem instantiating one of
these soundness interfaces for the embedded CM trace-GCD data.
-/

namespace P24.TraceGcdPayloadGate

def PointwiseUnitPayload {Index Scalar : Type}
    (Delta Inv : Index → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ t, UnitRel (Delta t) (Inv t)

def OrbitUnitPayload {Orbit Scalar : Type}
    (orbitProduct orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ orbit, UnitRel (orbitProduct orbit) (orbitInv orbit)

def ScalarUnitPayload {Scalar : Type}
    (norm normInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel norm normInv

def OrbitProductSound {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (orbitProduct : Orbit → Scalar) : Prop :=
  ∀ t, Delta t = 0 → orbitProduct (orbitOf t) = 0

def CompressedNormSound {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (norm : Scalar) : Prop :=
  (∃ t, Delta t = 0) → norm = 0

def SchubertAvoids {Index : Type} (TrivialIntersection : Index → Prop) :
    Prop :=
  ∀ t, TrivialIntersection t

theorem values_nonzero_from_pointwise_units
    {Index Scalar : Type} [Zero Scalar]
    (Delta Inv : Index → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_payload : PointwiseUnitPayload Delta Inv UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t
  exact h_unit_nonzero (Delta t) (Inv t) (h_payload t)

theorem values_nonzero_from_orbit_product_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (orbitProduct orbitInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_sound : OrbitProductSound orbitOf Delta orbitProduct)
    (h_payload : OrbitUnitPayload orbitProduct orbitInv UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_product_nonzero :
      orbitProduct (orbitOf t) ≠ 0 :=
    h_unit_nonzero (orbitProduct (orbitOf t)) (orbitInv (orbitOf t))
      (h_payload (orbitOf t))
  exact h_product_nonzero (h_sound t h_delta_zero)

theorem values_nonzero_from_compressed_norm_unit
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (norm normInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_sound : CompressedNormSound Delta norm)
    (h_payload : ScalarUnitPayload norm normInv UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_norm_nonzero : norm ≠ 0 :=
    h_unit_nonzero norm normInv h_payload
  exact h_norm_nonzero (h_sound ⟨t, h_delta_zero⟩)

theorem schubert_avoidance_from_pointwise_units
    {Index Scalar : Type} [Zero Scalar]
    (Delta Inv : Index → Scalar)
    (TrivialIntersection : Index → Prop)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_payload : PointwiseUnitPayload Delta Inv UnitRel)
    (h_det_to_intersection :
      ∀ t, Delta t ≠ 0 → TrivialIntersection t) :
    SchubertAvoids TrivialIntersection := by
  intro t
  exact h_det_to_intersection t
    (values_nonzero_from_pointwise_units Delta Inv UnitRel
      h_unit_nonzero h_payload t)

theorem schubert_avoidance_from_orbit_product_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (orbitProduct orbitInv : Orbit → Scalar)
    (TrivialIntersection : Index → Prop)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_sound : OrbitProductSound orbitOf Delta orbitProduct)
    (h_payload : OrbitUnitPayload orbitProduct orbitInv UnitRel)
    (h_det_to_intersection :
      ∀ t, Delta t ≠ 0 → TrivialIntersection t) :
    SchubertAvoids TrivialIntersection := by
  intro t
  exact h_det_to_intersection t
    (values_nonzero_from_orbit_product_units orbitOf Delta
      orbitProduct orbitInv UnitRel h_unit_nonzero h_sound h_payload t)

theorem schubert_avoidance_from_compressed_norm_unit
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (norm normInv : Scalar)
    (TrivialIntersection : Index → Prop)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_sound : CompressedNormSound Delta norm)
    (h_payload : ScalarUnitPayload norm normInv UnitRel)
    (h_det_to_intersection :
      ∀ t, Delta t ≠ 0 → TrivialIntersection t) :
    SchubertAvoids TrivialIntersection := by
  intro t
  exact h_det_to_intersection t
    (values_nonzero_from_compressed_norm_unit Delta norm normInv UnitRel
      h_unit_nonzero h_sound h_payload t)

theorem selected_from_pointwise_units
    {Index Scalar : Type} [Zero Scalar]
    (Delta Inv : Index → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_payload : PointwiseUnitPayload Delta Inv UnitRel)
    (h_det_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_det_to_good selected
    (values_nonzero_from_pointwise_units Delta Inv UnitRel
      h_unit_nonzero h_payload selected)

theorem selected_from_orbit_product_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (orbitProduct orbitInv : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_sound : OrbitProductSound orbitOf Delta orbitProduct)
    (h_payload : OrbitUnitPayload orbitProduct orbitInv UnitRel)
    (h_det_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_det_to_good selected
    (values_nonzero_from_orbit_product_units orbitOf Delta
      orbitProduct orbitInv UnitRel h_unit_nonzero h_sound h_payload
      selected)

theorem selected_from_compressed_norm_unit
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (norm normInv : Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_sound : CompressedNormSound Delta norm)
    (h_payload : ScalarUnitPayload norm normInv UnitRel)
    (h_det_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_det_to_good selected
    (values_nonzero_from_compressed_norm_unit Delta norm normInv UnitRel
      h_unit_nonzero h_sound h_payload selected)

end P24.TraceGcdPayloadGate
