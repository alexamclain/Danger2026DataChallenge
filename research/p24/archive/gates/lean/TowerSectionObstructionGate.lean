/-!
Finite gate for the embedded class-field tower section obstruction.

The note `p24/tower_section_obstruction.md` uses a simple equivariance
argument.  In a refinement layer `L <= K <= G`, a seedless `G`-equivariant
rule cannot choose one child `L`-coset over a parent `K`-coset unless the
refinement is trivial.

This file avoids formal group theory.  It records the stabilizer logic:

* every element of `K` fixes the parent base point;
* an equivariant selector sends that parent point to a child point;
* therefore every element of `K` fixes the selected child;
* if the selected child's stabilizer is exactly `L`, then `K <= L`.

Thus a witness `k in K \\ L` rules out such a selector.
-/

namespace P24.TowerSectionObstructionGate

def Equivariant {G Parent Child : Type}
    (actParent : G → Parent → Parent)
    (actChild : G → Child → Child)
    (selector : Parent → Child) : Prop :=
  ∀ g parent, selector (actParent g parent) = actChild g (selector parent)

def FixesParent {G Parent : Type}
    (actParent : G → Parent → Parent)
    (K : G → Prop)
    (parent : Parent) : Prop :=
  ∀ g, K g → actParent g parent = parent

def ChildStabilizerContainedIn {G Child : Type}
    (actChild : G → Child → Child)
    (L : G → Prop)
    (child : Child) : Prop :=
  ∀ g, actChild g child = child → L g

theorem parent_stabilizer_contained_in_child_stabilizer
    {G Parent Child : Type}
    (actParent : G → Parent → Parent)
    (actChild : G → Child → Child)
    (K L : G → Prop)
    (selector : Parent → Child)
    (parent : Parent)
    (h_equiv : Equivariant actParent actChild selector)
    (h_fix_parent : FixesParent actParent K parent)
    (h_child_stab :
      ChildStabilizerContainedIn actChild L (selector parent)) :
    ∀ g, K g → L g := by
  intro g h_g_in_K
  apply h_child_stab g
  have h_equiv_at_parent :
      selector (actParent g parent) = actChild g (selector parent) :=
    h_equiv g parent
  rw [h_fix_parent g h_g_in_K] at h_equiv_at_parent
  exact h_equiv_at_parent.symm

theorem no_equivariant_selector_for_proper_refinement
    {G Parent Child : Type}
    (actParent : G → Parent → Parent)
    (actChild : G → Child → Child)
    (K L : G → Prop)
    (selector : Parent → Child)
    (parent : Parent)
    (h_equiv : Equivariant actParent actChild selector)
    (h_fix_parent : FixesParent actParent K parent)
    (h_child_stab :
      ChildStabilizerContainedIn actChild L (selector parent))
    (h_proper : ∃ g, K g ∧ ¬ L g) :
    False := by
  obtain ⟨g, h_g_in_K, h_g_not_L⟩ := h_proper
  have h_K_subset_L :
      ∀ g, K g → L g :=
    parent_stabilizer_contained_in_child_stabilizer
      actParent actChild K L selector parent h_equiv h_fix_parent h_child_stab
  exact h_g_not_L (h_K_subset_L g h_g_in_K)

end P24.TowerSectionObstructionGate
