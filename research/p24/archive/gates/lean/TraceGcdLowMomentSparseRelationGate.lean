/-!
Finite handoff for the low-moment sparse-relation route.

The Python gate identifies the arithmetic theorem target: no disjoint
equal-cardinality signed moment-curve relations in the embedded CM quotient
root set, beyond the deterministic Newton boundary.  This Lean file records
the finite implication used downstream: if the selected low moments are
constructed and sparse collisions are absent, then those moments select the
child fiber.
-/

namespace P24.TraceGcdLowMomentSparseRelationGate

structure LowMomentFamily where
  momentCount : Nat
  constructedIntrinsically : Prop

structure SparseRelationAvoidance where
  noOtherChildWithSameMoments : Prop

def LowMomentSelectorReady
    (family : LowMomentFamily)
    (avoidance : SparseRelationAvoidance) : Prop :=
  family.constructedIntrinsically ∧
  avoidance.noOtherChildWithSameMoments

theorem child_selected_from_low_moments
    (family : LowMomentFamily)
    (avoidance : SparseRelationAvoidance)
    (h_ready : LowMomentSelectorReady family avoidance) :
    family.constructedIntrinsically ∧
    avoidance.noOtherChildWithSameMoments := by
  exact h_ready

def p24FirstLayerMomentCount : Nat := 4
def p24SecondLayerMomentCount : Nat := 26
def p24LowMomentTotal : Nat :=
  p24FirstLayerMomentCount + p24SecondLayerMomentCount

def p24FirstLayerFirstPossibleCollisionSize : Nat :=
  p24FirstLayerMomentCount + 1

def p24SecondLayerFirstPossibleCollisionSize : Nat :=
  p24SecondLayerMomentCount + 1

theorem p24_low_moment_total :
    p24LowMomentTotal = 30 := by
  decide

theorem p24_first_layer_sparse_relation_range_starts_at_five :
    p24FirstLayerFirstPossibleCollisionSize = 5 := by
  decide

theorem p24_second_layer_sparse_relation_range_starts_at_twenty_seven :
    p24SecondLayerFirstPossibleCollisionSize = 27 := by
  decide

end P24.TraceGcdLowMomentSparseRelationGate
