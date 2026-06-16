/-!
Finite gate for descended Plucker-Kummer payloads.

A Kummer power of a Plucker coordinate is useful as a class-field payload only
when it descends from the hidden cyclic labeling.  Abstractly, this file
records the finite logic:

* each local Kummer payload detects zero of the corresponding Plucker value;
* all local Kummer payloads equal one descended scalar;
* that descended scalar is nonzero;
* therefore every Plucker value in the orbit is nonzero.

If descent fails, one must supply an orbit-product/norm payload instead.
-/

namespace P24.PluckerKummerDescentGate

def KummerDetectsPluckerZero {Index Scalar : Type} [Zero Scalar]
    (plucker localKummer : Index → Scalar) : Prop :=
  ∀ i, plucker i = 0 → localKummer i = 0

def DescendsToScalar {Index Scalar : Type}
    (localKummer : Index → Scalar)
    (descended : Scalar) : Prop :=
  ∀ i, localKummer i = descended

theorem pluckers_nonzero_from_descended_kummer
    {Index Scalar : Type} [Zero Scalar]
    (plucker localKummer : Index → Scalar)
    (descended : Scalar)
    (h_detects : KummerDetectsPluckerZero plucker localKummer)
    (h_descends : DescendsToScalar localKummer descended)
    (h_descended_nonzero : descended ≠ 0) :
    ∀ i, plucker i ≠ 0 := by
  intro i h_plucker_zero
  have h_local_zero : localKummer i = 0 :=
    h_detects i h_plucker_zero
  have h_local_descended : localKummer i = descended :=
    h_descends i
  exact h_descended_nonzero (by
    rw [← h_local_descended]
    exact h_local_zero)

theorem selected_good_from_descended_kummer
    {Index Scalar : Type} [Zero Scalar]
    (plucker localKummer : Index → Scalar)
    (descended : Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (h_detects : KummerDetectsPluckerZero plucker localKummer)
    (h_descends : DescendsToScalar localKummer descended)
    (h_descended_nonzero : descended ≠ 0)
    (h_plucker_to_good : ∀ i, plucker i ≠ 0 → Good i) :
    Good selected := by
  exact h_plucker_to_good selected
    (pluckers_nonzero_from_descended_kummer
      plucker localKummer descended h_detects h_descends
      h_descended_nonzero selected)

end P24.PluckerKummerDescentGate
