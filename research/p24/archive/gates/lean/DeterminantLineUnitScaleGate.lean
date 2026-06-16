/-!
Finite gate for determinant-line unit scaling.

Many p24 determinant surfaces are only canonical as determinant-line sections:
changing p-integral source/target bases multiplies the displayed scalar by a
p-unit.  This file records the finite handoff used by the trace-GCD
block-cycle/Fitting target:

* unit-scaled representatives have the same zero/nonzero status;
* a p-unit proof for one representative transfers to any unit-scaled
  representative;
* therefore basis choices cannot affect the finite certificate logic.

No determinant algebra or p-adic geometry is formalized here.
-/

namespace P24.DeterminantLineUnitScaleGate

def ZeroCompatible {α : Type} [Zero α] (left right : α) : Prop :=
  left = 0 ↔ right = 0

def UnitScalePreservesZero {α Unit : Type} [Zero α]
    (scale : Unit → α → α)
    (PUnit : Unit → Prop) : Prop :=
  ∀ unit value, PUnit unit → (scale unit value = 0 ↔ value = 0)

def UnitScaled {α Unit : Type}
    (scale : Unit → α → α)
    (unit : Unit)
    (original changed : α) : Prop :=
  changed = scale unit original

theorem zero_compatible_from_unit_scale
    {α Unit : Type} [Zero α]
    (scale : Unit → α → α)
    (PUnit : Unit → Prop)
    (unit : Unit)
    (original changed : α)
    (h_preserve : UnitScalePreservesZero scale PUnit)
    (h_unit : PUnit unit)
    (h_scaled : UnitScaled scale unit original changed) :
    ZeroCompatible changed original := by
  unfold ZeroCompatible
  unfold UnitScaled at h_scaled
  rw [h_scaled]
  exact h_preserve unit original h_unit

theorem nonzero_transfers_from_unit_scale
    {α Unit : Type} [Zero α]
    (scale : Unit → α → α)
    (PUnit : Unit → Prop)
    (unit : Unit)
    (original changed : α)
    (h_preserve : UnitScalePreservesZero scale PUnit)
    (h_unit : PUnit unit)
    (h_scaled : UnitScaled scale unit original changed)
    (h_original_nonzero : original ≠ 0) :
    changed ≠ 0 := by
  intro h_changed_zero
  have h_zero_iff : changed = 0 ↔ original = 0 :=
    zero_compatible_from_unit_scale
      scale PUnit unit original changed h_preserve h_unit h_scaled
  exact h_original_nonzero (h_zero_iff.mp h_changed_zero)

theorem punit_transfers_from_unit_scale
    {α Unit : Type}
    (scale : Unit → α → α)
    (PUnitα : α → Prop)
    (PUnitScale : Unit → Prop)
    (unit : Unit)
    (original changed : α)
    (h_transfer : ∀ unit value, PUnitScale unit → PUnitα value →
      PUnitα (scale unit value))
    (h_unit : PUnitScale unit)
    (h_scaled : UnitScaled scale unit original changed)
    (h_original_punit : PUnitα original) :
    PUnitα changed := by
  unfold UnitScaled at h_scaled
  rw [h_scaled]
  exact h_transfer unit original h_unit h_original_punit

theorem certificate_nonzero_is_basis_independent
    {α Unit : Type} [Zero α]
    (scale : Unit → α → α)
    (PUnitScale : Unit → Prop)
    (unit : Unit)
    (canonical displayed : α)
    (h_preserve : UnitScalePreservesZero scale PUnitScale)
    (h_unit : PUnitScale unit)
    (h_scaled : UnitScaled scale unit canonical displayed)
    (h_displayed_nonzero : displayed ≠ 0) :
    canonical ≠ 0 := by
  intro h_canonical_zero
  have h_zero_iff : displayed = 0 ↔ canonical = 0 :=
    zero_compatible_from_unit_scale
      scale PUnitScale unit canonical displayed h_preserve h_unit h_scaled
  exact h_displayed_nonzero (h_zero_iff.mpr h_canonical_zero)

end P24.DeterminantLineUnitScaleGate
