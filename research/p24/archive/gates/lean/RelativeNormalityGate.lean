/-!
Finite certificate gate for the prime relative-normality route.

This file uses only Lean core.  It does not prove the CM arithmetic theorem.
It formalizes the interface we now want:

* for each quotient coordinate `u`, a relative-normality determinant is
  nonzero;
* any vanished relative character coordinate forces that determinant to zero;
* therefore every coordinate in every relative packet is nonzero;
* hence no packet can be all zero, so the harmful event is ruled out.

The p24-specific arithmetic input is the p-unit/nonvanishing proof for those
relative-normality determinants at the selected prime.
-/

namespace P24.RelativeNormalityGate

def AllZero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u = 0

def AllNonzero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u ≠ 0

theorem determinant_nonzero_forces_coordinate_nonzero
    {α : Type} [Zero α]
    (value determinant : α)
    (h_zero_forces_det_zero : value = 0 → determinant = 0)
    (h_det_nonzero : determinant ≠ 0) :
    value ≠ 0 := by
  intro hvalue
  exact h_det_nonzero (h_zero_forces_det_zero hvalue)

theorem coordinate_determinants_force_all_nonzero
    {α : Type} [Zero α] {m : Nat}
    (packet determinant : Fin m → α)
    (h_zero_forces_det_zero :
      ∀ u, packet u = 0 → determinant u = 0)
    (h_det_nonzero :
      ∀ u, determinant u ≠ 0) :
    AllNonzero packet := by
  intro u
  exact determinant_nonzero_forces_coordinate_nonzero
    (packet u) (determinant u)
    (h_zero_forces_det_zero u) (h_det_nonzero u)

theorem all_nonzero_no_all_zero
    {α : Type} [Zero α] {m : Nat}
    (hm : 0 < m)
    (packet : Fin m → α)
    (h_nonzero : AllNonzero packet) :
    ¬ AllZero packet := by
  intro hzero
  exact h_nonzero ⟨0, hm⟩ (hzero ⟨0, hm⟩)

theorem determinant_certificate_no_harmful
    {α : Type} [Zero α] {m : Nat}
    (hm : 0 < m)
    (harmful : Prop)
    (packet determinant : Fin m → α)
    (h_harmful_all_zero : harmful → AllZero packet)
    (h_zero_forces_det_zero :
      ∀ u, packet u = 0 → determinant u = 0)
    (h_det_nonzero :
      ∀ u, determinant u ≠ 0) :
    ¬ harmful := by
  intro hh
  have h_nonzero : AllNonzero packet :=
    coordinate_determinants_force_all_nonzero
      packet determinant h_zero_forces_det_zero h_det_nonzero
  have h_not_all_zero : ¬ AllZero packet :=
    all_nonzero_no_all_zero hm packet h_nonzero
  exact h_not_all_zero (h_harmful_all_zero hh)

theorem all_packets_no_harmful_from_coordinate_determinants
    {α : Type} [Zero α] {orbitCount m : Nat}
    (hm : 0 < m)
    (harmful : Fin orbitCount → Prop)
    (packet determinant : Fin orbitCount → Fin m → α)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_zero_forces_det_zero :
      ∀ orbit u, packet orbit u = 0 → determinant orbit u = 0)
    (h_det_nonzero :
      ∀ orbit u, determinant orbit u ≠ 0) :
    ∀ orbit, ¬ harmful orbit := by
  intro orbit
  exact determinant_certificate_no_harmful
    hm (harmful orbit) (packet orbit) (determinant orbit)
    (h_harmful_all_zero orbit)
    (h_zero_forces_det_zero orbit)
    (h_det_nonzero orbit)

end P24.RelativeNormalityGate
