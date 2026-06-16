/-!
Finite algebra lemmas for the p24 relative-resolvent reduction.

This file uses only Lean core.  It abstracts away the field/root-of-unity
calculation and checks the logical split-algebra step:

* the level-zero component of each quotient block is the relative fiber value;
* if a relative fiber is zero, every component in its split block is zero;
* therefore all split components vanish iff all relative fibers vanish.

The p24-specific CM input is the proof that the actual class-field components
have this shape, and then the still-open arithmetic nonvanishing theorem.
-/

namespace P24.RelativeResolvent

theorem splitBlock_zero {α : Type} [Zero α] {m n : Nat}
    (P : Fin m → α) (C : Fin m → Fin n → α)
    (hblock : ∀ u, P u = 0 → ∀ l, C u l = 0)
    {u : Fin m} (hu : P u = 0) :
    ∀ l, C u l = 0 := by
  exact hblock u hu

theorem splitComponents_all_zero_iff {α : Type} [Zero α] {m n : Nat}
    (hn : 0 < n) (P : Fin m → α) (C : Fin m → Fin n → α)
    (hlevel0 : ∀ u, C u ⟨0, hn⟩ = P u)
    (hblock : ∀ u, P u = 0 → ∀ l, C u l = 0) :
    (∀ u, ∀ l, C u l = 0) ↔ (∀ u, P u = 0) := by
  constructor
  · intro h u
    rw [← hlevel0 u]
    exact h u ⟨0, hn⟩
  · intro hp u l
    exact hblock u (hp u) l

end P24.RelativeResolvent

