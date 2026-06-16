/-!
Finite gate for the trace-GCD Schubert-orbit formulation.

The arithmetic theorem can be stated as an origin-product determinant, or as
avoidance of translated Schubert divisors:

    Delta t ≠ 0  <=>  W ∩ V_t^{-1} C = {0}.

Lean does not formalize the vector spaces here.  It checks the finite
certificate interface: if the determinant product forces every determinant
nonzero, and each determinant nonzero is equivalent to the corresponding
trivial-intersection predicate, then all translated Schubert intersections
are trivial, in particular the selected one.
-/

namespace P24.TraceGcdSchubertOrbitGate

def ProductDetectsZeros {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (product : Scalar) : Prop :=
  (∃ t, Delta t = 0) → product = 0

def SchubertAvoids {Index : Type} (index : Index → Prop) : Prop :=
  ∀ t, index t

theorem determinant_nonzero_from_product
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (product : Scalar)
    (h_detects : ProductDetectsZeros Delta product)
    (h_product : product ≠ 0) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_zero
  exact h_product (h_detects ⟨t, h_zero⟩)

theorem schubert_avoidance_from_product
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (TrivialIntersection : Index → Prop)
    (product : Scalar)
    (h_detects : ProductDetectsZeros Delta product)
    (h_product : product ≠ 0)
    (h_det_to_intersection :
      ∀ t, Delta t ≠ 0 → TrivialIntersection t) :
    SchubertAvoids TrivialIntersection := by
  intro t
  exact h_det_to_intersection t
    (determinant_nonzero_from_product Delta product h_detects h_product t)

theorem selected_schubert_avoidance_from_product
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (TrivialIntersection : Index → Prop)
    (product : Scalar)
    (selected : Index)
    (h_detects : ProductDetectsZeros Delta product)
    (h_product : product ≠ 0)
    (h_det_to_intersection :
      ∀ t, Delta t ≠ 0 → TrivialIntersection t) :
    TrivialIntersection selected :=
  schubert_avoidance_from_product
    Delta TrivialIntersection product h_detects h_product
    h_det_to_intersection selected

theorem determinant_intersection_equivalence_transfers
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (TrivialIntersection : Index → Prop)
    (h_equiv : ∀ t, (Delta t ≠ 0) ↔ TrivialIntersection t)
    (h_delta : ∀ t, Delta t ≠ 0) :
    SchubertAvoids TrivialIntersection := by
  intro t
  exact (h_equiv t).mp (h_delta t)

end P24.TraceGcdSchubertOrbitGate
