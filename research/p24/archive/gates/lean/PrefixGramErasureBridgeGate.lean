/-!
Finite bridge between the metric prefix-Gram formulation and the prefix
subcode/erasure formulation.

For a parameter `lambda` in the prefix span, the associated trace word vanishes
on the prefix exactly when the corresponding field vector is orthogonal to the
prefix subspace.  Thus nondegeneracy of the metric prefix Gram rules out a
nonzero prefix parameter that vanishes on the prefix.

This file is deliberately abstract: it does not formalize matrices, trace, or
the construction of the word.  It records the finite implication needed to
identify the Gram, self-orthogonal, and support/distance theorem statements.
-/

namespace P24.PrefixGramErasureBridgeGate

def OrthogonalToSubspace {V : Type}
    (PairZero : V → V → Prop)
    (Subspace : V → Prop)
    (x : V) : Prop :=
  ∀ y, Subspace y → PairZero x y

def RestrictedRadical {V : Type}
    (PairZero : V → V → Prop)
    (Subspace : V → Prop)
    (x : V) : Prop :=
  Subspace x ∧ OrthogonalToSubspace PairZero Subspace x

def NondegenerateOn {V : Type} [Zero V]
    (PairZero : V → V → Prop)
    (Subspace : V → Prop) : Prop :=
  ∀ x, RestrictedRadical PairZero Subspace x → x = 0

def PrefixErasureInjective {Param : Type}
    (Active Nonzero VanishesOnPrefix : Param → Prop) : Prop :=
  ∀ param, Active param → Nonzero param → ¬ VanishesOnPrefix param

theorem prefix_erasure_from_metric_prefix_nondegenerate
    {Param V : Type} [Zero V]
    (toVector : Param → V)
    (Active Nonzero VanishesOnPrefix : Param → Prop)
    (PairZero : V → V → Prop)
    (Prefix : V → Prop)
    (h_active_in_prefix :
      ∀ param, Active param → Prefix (toVector param))
    (h_nonzero_vector :
      ∀ param, Nonzero param → toVector param ≠ 0)
    (h_vanishes_to_orthogonal :
      ∀ param, VanishesOnPrefix param →
        OrthogonalToSubspace PairZero Prefix (toVector param))
    (h_prefix_nondegenerate :
      NondegenerateOn PairZero Prefix) :
    PrefixErasureInjective Active Nonzero VanishesOnPrefix := by
  intro param h_active h_nonzero h_vanishes
  have h_radical :
      RestrictedRadical PairZero Prefix (toVector param) :=
    ⟨h_active_in_prefix param h_active,
      h_vanishes_to_orthogonal param h_vanishes⟩
  have h_vector_zero : toVector param = 0 :=
    h_prefix_nondegenerate (toVector param) h_radical
  exact (h_nonzero_vector param h_nonzero) h_vector_zero

theorem prefix_self_orthogonal_from_bad_erasure
    {Param V : Type} [Zero V]
    (toVector : Param → V)
    (Active Nonzero VanishesOnPrefix : Param → Prop)
    (PairZero : V → V → Prop)
    (Prefix : V → Prop)
    (h_active_in_prefix :
      ∀ param, Active param → Prefix (toVector param))
    (h_nonzero_vector :
      ∀ param, Nonzero param → toVector param ≠ 0)
    (h_vanishes_to_orthogonal :
      ∀ param, VanishesOnPrefix param →
        OrthogonalToSubspace PairZero Prefix (toVector param))
    (param : Param)
    (h_active : Active param)
    (h_nonzero : Nonzero param)
    (h_vanishes : VanishesOnPrefix param) :
    ∃ x, x ≠ 0 ∧ RestrictedRadical PairZero Prefix x := by
  exact
    ⟨toVector param,
      h_nonzero_vector param h_nonzero,
      ⟨h_active_in_prefix param h_active,
        h_vanishes_to_orthogonal param h_vanishes⟩⟩

theorem prefix_erasure_iff_no_bad_param
    {Param : Type}
    (Active Nonzero VanishesOnPrefix : Param → Prop)
    :
    PrefixErasureInjective Active Nonzero VanishesOnPrefix
      ↔
    ∀ param,
      Active param → Nonzero param → VanishesOnPrefix param → False := by
  constructor
  · intro h_erasure param h_active h_nonzero h_vanishes
    exact h_erasure param h_active h_nonzero h_vanishes
  · intro h_no_bad param h_active h_nonzero h_vanishes
    exact h_no_bad param h_active h_nonzero h_vanishes

end P24.PrefixGramErasureBridgeGate
