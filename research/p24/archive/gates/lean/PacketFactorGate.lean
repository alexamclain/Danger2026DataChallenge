/-!
Finite logic for packet-factor vanishing.

This file uses only Lean core.  It formalizes the bookkeeping distinction
behind `relative_packet_factor_vanishing_shape.md`:

* one Frobenius packet factor can vanish for one coordinate;
* this is weaker than saying all primitive packet factors vanish;
* exact content only needs each packet vector to be nonzero;
* coordinate/resultant nonvanishing is a stronger sufficient certificate.

The arithmetic meaning of a packet factor is external to Lean here: in p24 it
is one irreducible factor `f_a | Phi_n`.
-/

namespace P24.PacketFactorGate

def AllZero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u = 0

def AnyZero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∃ u, v u = 0

def AllNonzero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u ≠ 0

def PacketContentNonzero {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α) : Prop :=
  ∀ orbit, ¬ AllZero (packet orbit)

def CoordinateNonzero {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α) : Prop :=
  ∀ orbit u, packet orbit u ≠ 0

theorem coordinate_nonzero_implies_content
    {α : Type} [Zero α] {orbitCount m : Nat}
    (hm : 0 < m)
    (packet : Fin orbitCount → Fin m → α)
    (hcoord : CoordinateNonzero packet) :
    PacketContentNonzero packet := by
  intro orbit hall
  exact hcoord orbit ⟨0, hm⟩ (hall ⟨0, hm⟩)

theorem content_rules_out_harmful
    {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (harmful : Fin orbitCount → Prop)
    (hcontent : PacketContentNonzero packet)
    (hharmful : ∀ orbit, harmful orbit → AllZero (packet orbit)) :
    ∀ orbit, ¬ harmful orbit := by
  intro orbit h
  exact hcontent orbit (hharmful orbit h)

theorem coordinate_nonzero_rules_out_harmful
    {α : Type} [Zero α] {orbitCount m : Nat}
    (hm : 0 < m)
    (packet : Fin orbitCount → Fin m → α)
    (harmful : Fin orbitCount → Prop)
    (hcoord : CoordinateNonzero packet)
    (hharmful : ∀ orbit, harmful orbit → AllZero (packet orbit)) :
    ∀ orbit, ¬ harmful orbit := by
  have hcontent : PacketContentNonzero packet :=
    coordinate_nonzero_implies_content hm packet hcoord
  exact content_rules_out_harmful packet harmful hcontent hharmful

def TwoOrbitExample : Fin 2 → Nat :=
  fun orbit => if orbit.val = 0 then 0 else 1

theorem one_packet_zero_does_not_force_full_primitive_zero :
    ∃ packet : Fin 2 → Nat,
      AnyZero packet ∧ ¬ AllZero packet := by
  refine ⟨TwoOrbitExample, ?_, ?_⟩
  · exact ⟨⟨0, by decide⟩, rfl⟩
  · intro hall
    have h_one : TwoOrbitExample ⟨1, by decide⟩ = 1 := by
      rfl
    have h_zero : TwoOrbitExample ⟨1, by decide⟩ = 0 :=
      hall ⟨1, by decide⟩
    rw [h_one] at h_zero
    exact Nat.succ_ne_zero 0 h_zero

end P24.PacketFactorGate
