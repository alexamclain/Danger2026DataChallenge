/-!
Finite gate for the cyclic class-tower choice obstruction.

The p24 third-trace class group is cyclic of squarefree order, so the
subgroups in the `2,157,211,3107441` tower are unique.  This does not choose
compatible roots after reduction at the completely split prime above `p`.

This file records the finite reason: if an element stabilizes a parent tower
fiber but moves a child fiber, then no equivariant rule can choose that child.
The statement is deliberately abstract; it does not formalize CM, class
fields, or reduction modulo `p`.
-/

namespace P24.CyclicTowerSectionObstructionGate

def IsSection {Parent Child : Type}
    (projection : Child → Parent)
    (choice : Parent → Child) : Prop :=
  ∀ parent, projection (choice parent) = parent

def EquivariantChoice {Parent Child Actor : Type}
    (actParent : Actor → Parent → Parent)
    (actChild : Actor → Child → Child)
    (choice : Parent → Child) : Prop :=
  ∀ actor parent, choice (actParent actor parent) =
    actChild actor (choice parent)

theorem no_equivariant_child_choice_from_moving_stabilizer
    {Parent Child Actor : Type}
    (actParent : Actor → Parent → Parent)
    (actChild : Actor → Child → Child)
    (choice : Parent → Child)
    (actor : Actor)
    (parent : Parent)
    (h_equivariant :
      EquivariantChoice actParent actChild choice)
    (h_parent_fixed : actParent actor parent = parent)
    (h_child_moved :
      actChild actor (choice parent) ≠ choice parent) :
    False := by
  have h_choice_fixed :
      choice parent = actChild actor (choice parent) := by
    calc
      choice parent = choice (actParent actor parent) := by
        rw [h_parent_fixed]
      _ = actChild actor (choice parent) := by
        exact h_equivariant actor parent
  exact h_child_moved h_choice_fixed.symm

theorem no_equivariant_section_from_moving_stabilizer
    {Parent Child Actor : Type}
    (projection : Child → Parent)
    (actParent : Actor → Parent → Parent)
    (actChild : Actor → Child → Child)
    (choice : Parent → Child)
    (actor : Actor)
    (parent : Parent)
    (_h_section : IsSection projection choice)
    (h_equivariant :
      EquivariantChoice actParent actChild choice)
    (h_parent_fixed : actParent actor parent = parent)
    (h_child_moved :
      actChild actor (choice parent) ≠ choice parent) :
    False :=
  no_equivariant_child_choice_from_moving_stabilizer
    actParent actChild choice actor parent h_equivariant
    h_parent_fixed h_child_moved

theorem p24_third_trace_smooth_tower_product :
    2 * 157 * 211 * 3107441 = 205880396014 := by
  decide

theorem p24_odd_refinement_layers_nontrivial :
    1 < 157 ∧ 1 < 211 ∧ 1 < 3107441 := by
  decide

theorem p24_recovery_degree_subsqrt_but_not_constant :
    3107441 < 1000000000000 ∧ 1 < 3107441 := by
  decide

theorem p24_hcoset_verifier_count_separate_from_four_payload :
    156 * 7 = 1092 ∧ 4 < 1092 := by
  decide

end P24.CyclicTowerSectionObstructionGate
