/-!
Finite tower-trace bookkeeping for the p24 embedded class-field route.

This file intentionally uses only Lean core.  It does not prove the arithmetic
CM input.  Instead it formalizes the small logical pieces that are now clear
from the tower toys:

* relative trace data determines child periods once an inverse transform is
  supplied;
* a relation whose roots are exactly the decoded children is also exact for
  the true child periods;
* a canonical equivariant section of a nontrivial child fiber is impossible
  once a parent returns to itself but the child has moved.

For p24 the missing theorem is the construction of the relative traces or the
exact child relation.  These lemmas record what such a construction would buy.
-/

namespace P24.TowerTrace

def HasExactlyChildRoots {α : Type} {d : Nat}
    (relation : α → Prop) (children : Fin d → α) : Prop :=
  (∀ r, relation (children r)) ∧
  (∀ y, relation y → ∃ r, y = children r)

theorem trace_equality_forces_child_equality
    {Child Trace : Type} {d : Nat}
    (encode : (Fin d → Child) → Trace)
    (decode : Trace → Fin d → Child)
    (h_left_inverse : ∀ v r, decode (encode v) r = v r)
    {v w : Fin d → Child}
    (h_trace : encode v = encode w) :
    ∀ r, v r = w r := by
  intro r
  calc
    v r = decode (encode v) r := (h_left_inverse v r).symm
    _ = decode (encode w) r := by rw [h_trace]
    _ = w r := h_left_inverse w r

theorem decoded_relation_exact
    {α Trace : Type} {d : Nat}
    (trace : Trace)
    (decode : Trace → Fin d → α)
    (children : Fin d → α)
    (relation : α → Prop)
    (h_decode : ∀ r, decode trace r = children r)
    (h_relation : HasExactlyChildRoots relation (decode trace)) :
    HasExactlyChildRoots relation children := by
  constructor
  · intro r
    rw [← h_decode r]
    exact h_relation.1 r
  · intro y hy
    rcases h_relation.2 y hy with ⟨r, hr⟩
    exact ⟨r, hr.trans (h_decode r)⟩

theorem exact_relation_gives_child
    {α : Type} {d : Nat}
    (relation : α → Prop)
    (children : Fin d → α)
    (h_relation : HasExactlyChildRoots relation children)
    {y : α}
    (hy : relation y) :
    ∃ r, y = children r :=
  h_relation.2 y hy

theorem no_equivariant_child_section
    {Parent Child : Type}
    (actParent : Nat → Parent → Parent)
    (actChild : Nat → Child → Child)
    (chooseChild : Parent → Child)
    (h_equivariant :
      ∀ n z, chooseChild (actParent n z) = actChild n (chooseChild z))
    {q : Nat} {z : Parent}
    (h_parent_fixed : actParent q z = z)
    (h_child_moved : actChild q (chooseChild z) ≠ chooseChild z) :
    False := by
  apply h_child_moved
  calc
    actChild q (chooseChild z) = chooseChild (actParent q z) :=
      (h_equivariant q z).symm
    _ = chooseChild z := by rw [h_parent_fixed]

end P24.TowerTrace
