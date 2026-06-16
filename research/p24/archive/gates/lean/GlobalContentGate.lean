/-!
Global content and scalar-projection gates for the p24 relative packets.

This file uses only Lean core.  It formalizes the finite logic behind the
aggregate theorem target:

* the exact relative-content condition is that no packet vector is all zero;
* a global Bezout/content certificate proves that condition packetwise;
* any fixed scalar projection, such as a quotient moment or Hermitian energy,
  is a sufficient certificate when harmful vanishing forces that scalar to
  vanish and the scalar is known to be nonzero.

The open p24 arithmetic theorem is still the selected-prime nonvanishing of a
structured scalar/content certificate.
-/

namespace P24.GlobalContentGate

def AllZero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u = 0

def PacketContentGood {α : Type} [Zero α] {m : Nat}
    (packet : Fin m → α) : Prop :=
  ¬ AllZero packet

def GlobalContentGood {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α) : Prop :=
  ∀ orbit, PacketContentGood (packet orbit)

theorem global_content_iff_packetwise
    {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α) :
    GlobalContentGood packet ↔ ∀ orbit, ¬ AllZero (packet orbit) := by
  rfl

theorem global_content_no_harmful
    {α : Type} [Zero α] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_content : GlobalContentGood packet) :
    ∀ orbit, ¬ harmful orbit := by
  intro orbit hh
  exact h_content orbit (h_harmful_all_zero orbit hh)

theorem packet_content_from_coordinate
    {α : Type} [Zero α] {m : Nat}
    (packet : Fin m → α)
    (u : Fin m)
    (h_nonzero : packet u ≠ 0) :
    PacketContentGood packet := by
  intro hzero
  exact h_nonzero (hzero u)

theorem global_content_from_coordinates
    {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (chosen : Fin orbitCount → Fin m)
    (h_nonzero : ∀ orbit, packet orbit (chosen orbit) ≠ 0) :
    GlobalContentGood packet := by
  intro orbit
  exact packet_content_from_coordinate (packet orbit) (chosen orbit)
    (h_nonzero orbit)

theorem projection_certificate_content
    {α β : Type} [Zero α] [Zero β] {m : Nat}
    (packet : Fin m → α)
    (projection : (Fin m → α) → β)
    (h_zero_projection : AllZero packet → projection packet = 0)
    (h_projection_nonzero : projection packet ≠ 0) :
    PacketContentGood packet := by
  intro hzero
  exact h_projection_nonzero (h_zero_projection hzero)

theorem projection_family_certificate_content
    {α β : Type} [Zero α] [Zero β] {m projectionCount : Nat}
    (packet : Fin m → α)
    (projection : Fin projectionCount → (Fin m → α) → β)
    (h_zero_projection :
      AllZero packet → ∀ i, projection i packet = 0)
    (chosen : Fin projectionCount)
    (h_projection_nonzero : projection chosen packet ≠ 0) :
    PacketContentGood packet := by
  intro hzero
  exact h_projection_nonzero ((h_zero_projection hzero) chosen)

theorem global_content_from_projections
    {α β : Type} [Zero α] [Zero β] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (projection : Fin orbitCount → (Fin m → α) → β)
    (h_zero_projection :
      ∀ orbit, AllZero (packet orbit) →
        projection orbit (packet orbit) = 0)
    (h_projection_nonzero :
      ∀ orbit, projection orbit (packet orbit) ≠ 0) :
    GlobalContentGood packet := by
  intro orbit
  exact projection_certificate_content (packet orbit) (projection orbit)
    (h_zero_projection orbit) (h_projection_nonzero orbit)

theorem global_content_from_projection_families
    {α β : Type} [Zero α] [Zero β] {orbitCount m projectionCount : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (projection :
      Fin orbitCount → Fin projectionCount → (Fin m → α) → β)
    (h_zero_projection :
      ∀ orbit, AllZero (packet orbit) →
        ∀ i, projection orbit i (packet orbit) = 0)
    (chosen : Fin orbitCount → Fin projectionCount)
    (h_projection_nonzero :
      ∀ orbit, projection orbit (chosen orbit) (packet orbit) ≠ 0) :
    GlobalContentGood packet := by
  intro orbit
  exact projection_family_certificate_content
    (packet orbit) (projection orbit)
    (h_zero_projection orbit) (chosen orbit)
    (h_projection_nonzero orbit)

theorem no_harmful_from_projection_certificates
    {α β : Type} [Zero α] [Zero β] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (projection : Fin orbitCount → (Fin m → α) → β)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_zero_projection :
      ∀ orbit, AllZero (packet orbit) →
        projection orbit (packet orbit) = 0)
    (h_projection_nonzero :
      ∀ orbit, projection orbit (packet orbit) ≠ 0) :
    ∀ orbit, ¬ harmful orbit := by
  have h_content : GlobalContentGood packet :=
    global_content_from_projections packet projection
      h_zero_projection h_projection_nonzero
  exact global_content_no_harmful harmful packet
    h_harmful_all_zero h_content

theorem bezout_content_certificate
    {α : Type} [Zero α] [One α] {m : Nat}
    (packet : Fin m → α)
    (combine : (Fin m → α) → α)
    (h_zero_combine : AllZero packet → combine packet = 0)
    (h_combine_one : combine packet = 1)
    (h_zero_ne_one : (0 : α) ≠ 1) :
    PacketContentGood packet := by
  intro hzero
  have h0 : combine packet = 0 := h_zero_combine hzero
  have h01 : (0 : α) = 1 := Eq.trans h0.symm h_combine_one
  exact h_zero_ne_one h01

theorem global_content_from_bezout
    {α : Type} [Zero α] [One α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (combine : Fin orbitCount → (Fin m → α) → α)
    (h_zero_combine :
      ∀ orbit, AllZero (packet orbit) →
        combine orbit (packet orbit) = 0)
    (h_combine_one :
      ∀ orbit, combine orbit (packet orbit) = 1)
    (h_zero_ne_one : (0 : α) ≠ 1) :
    GlobalContentGood packet := by
  intro orbit
  exact bezout_content_certificate (packet orbit) (combine orbit)
    (h_zero_combine orbit) (h_combine_one orbit) h_zero_ne_one

theorem no_harmful_from_global_bezout
    {α : Type} [Zero α] [One α] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (combine : Fin orbitCount → (Fin m → α) → α)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_zero_combine :
      ∀ orbit, AllZero (packet orbit) →
        combine orbit (packet orbit) = 0)
    (h_combine_one :
      ∀ orbit, combine orbit (packet orbit) = 1)
    (h_zero_ne_one : (0 : α) ≠ 1) :
    ∀ orbit, ¬ harmful orbit := by
  have h_content : GlobalContentGood packet :=
    global_content_from_bezout packet combine
      h_zero_combine h_combine_one h_zero_ne_one
  exact global_content_no_harmful harmful packet
    h_harmful_all_zero h_content

end P24.GlobalContentGate
