/-!
Finite gate for the prefix-Gram obstruction in the trace-GCD/Schur route.

For a prefix row space `U` with trace pairing `<_,_>`, singularity of the
restricted Gram matrix is the existence of a nonzero vector

    u in U and <u,v> = 0 for every v in U.

This file does not formalize matrices, determinants, trace pairings, or the
dimension theorem identifying the kernel with the orthogonal complement.  It
records the finite logical shape needed by the p24 arithmetic theorem:

* prefix Gram nondegeneracy is the same as absence of a nonzero
  self-orthogonal prefix vector;
* if the radical of the kernel complement transfers into the prefix radical,
  then prefix nondegeneracy forces kernel nondegeneracy.
-/

namespace P24.PrefixGramSelfOrthogonalGate

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

def SelfOrthogonalObstruction {V : Type} [Zero V]
    (PairZero : V → V → Prop)
    (Subspace : V → Prop) : Prop :=
  ∃ x, x ≠ 0 ∧ RestrictedRadical PairZero Subspace x

theorem no_obstruction_iff_nondegenerate_on
    {V : Type} [Zero V]
    (PairZero : V → V → Prop)
    (Subspace : V → Prop) :
    ¬ SelfOrthogonalObstruction PairZero Subspace
      ↔ NondegenerateOn PairZero Subspace := by
  constructor
  · intro h_no_obstruction x h_radical
    by_cases h_zero : x = 0
    · exact h_zero
    · exfalso
      exact h_no_obstruction ⟨x, h_zero, h_radical⟩
  · intro h_nondegenerate h_obstruction
    rcases h_obstruction with ⟨x, h_nonzero, h_radical⟩
    exact h_nonzero (h_nondegenerate x h_radical)

def RadicalTransfers {V : Type}
    (PairZero : V → V → Prop)
    (Prefix Kernel : V → Prop) : Prop :=
  ∀ x,
    RestrictedRadical PairZero Kernel x →
      RestrictedRadical PairZero Prefix x

theorem kernel_nondegenerate_from_prefix_nondegenerate
    {V : Type} [Zero V]
    (PairZero : V → V → Prop)
    (Prefix Kernel : V → Prop)
    (h_prefix_nondegenerate :
      NondegenerateOn PairZero Prefix)
    (h_transfer :
      RadicalTransfers PairZero Prefix Kernel) :
    NondegenerateOn PairZero Kernel := by
  intro x h_kernel_radical
  exact h_prefix_nondegenerate x (h_transfer x h_kernel_radical)

theorem no_kernel_obstruction_from_no_prefix_obstruction
    {V : Type} [Zero V]
    (PairZero : V → V → Prop)
    (Prefix Kernel : V → Prop)
    (h_no_prefix_obstruction :
      ¬ SelfOrthogonalObstruction PairZero Prefix)
    (h_transfer :
      RadicalTransfers PairZero Prefix Kernel) :
    ¬ SelfOrthogonalObstruction PairZero Kernel := by
  have h_prefix_nondegenerate :
      NondegenerateOn PairZero Prefix :=
    (no_obstruction_iff_nondegenerate_on PairZero Prefix).mp
      h_no_prefix_obstruction
  have h_kernel_nondegenerate :
      NondegenerateOn PairZero Kernel :=
    kernel_nondegenerate_from_prefix_nondegenerate
      PairZero Prefix Kernel h_prefix_nondegenerate h_transfer
  exact
    (no_obstruction_iff_nondegenerate_on PairZero Kernel).mpr
      h_kernel_nondegenerate

def UnitPayload {Index Scalar : Type}
    (value inverse : Index → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ i, UnitRel (value i) (inverse i)

def PrefixGramDetectsNondegenerate
    {Orbit V Scalar : Type} [Zero Scalar] [Zero V]
    (prefixGram : Orbit → Scalar)
    (PairZero : Orbit → V → V → Prop)
    (Prefix : Orbit → V → Prop) : Prop :=
  ∀ orbit,
    prefixGram orbit ≠ 0 →
      NondegenerateOn (PairZero orbit) (Prefix orbit)

theorem no_prefix_obstruction_from_prefix_gram_unit
    {Orbit V Scalar : Type} [Zero Scalar] [Zero V]
    (prefixGram prefixGramInv : Orbit → Scalar)
    (PairZero : Orbit → V → V → Prop)
    (Prefix : Orbit → V → Prop)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects :
      PrefixGramDetectsNondegenerate prefixGram PairZero Prefix)
    (h_units :
      UnitPayload prefixGram prefixGramInv UnitRel) :
    ∀ orbit,
      ¬ SelfOrthogonalObstruction (PairZero orbit) (Prefix orbit) := by
  intro orbit
  have h_prefix_nonzero : prefixGram orbit ≠ 0 :=
    h_unit_nonzero (prefixGram orbit) (prefixGramInv orbit)
      (h_units orbit)
  have h_nondegenerate :
      NondegenerateOn (PairZero orbit) (Prefix orbit) :=
    h_detects orbit h_prefix_nonzero
  exact
    (no_obstruction_iff_nondegenerate_on
      (PairZero orbit) (Prefix orbit)).mpr
      h_nondegenerate

theorem no_kernel_obstruction_from_prefix_gram_unit
    {Orbit V Scalar : Type} [Zero Scalar] [Zero V]
    (prefixGram prefixGramInv : Orbit → Scalar)
    (PairZero : Orbit → V → V → Prop)
    (Prefix Kernel : Orbit → V → Prop)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects :
      PrefixGramDetectsNondegenerate prefixGram PairZero Prefix)
    (h_transfer :
      ∀ orbit, RadicalTransfers (PairZero orbit)
        (Prefix orbit) (Kernel orbit))
    (h_units :
      UnitPayload prefixGram prefixGramInv UnitRel) :
    ∀ orbit,
      ¬ SelfOrthogonalObstruction (PairZero orbit) (Kernel orbit) := by
  intro orbit
  exact no_kernel_obstruction_from_no_prefix_obstruction
    (PairZero orbit) (Prefix orbit) (Kernel orbit)
    (no_prefix_obstruction_from_prefix_gram_unit
      prefixGram prefixGramInv PairZero Prefix UnitRel
      h_unit_nonzero h_detects h_units orbit)
    (h_transfer orbit)

end P24.PrefixGramSelfOrthogonalGate
