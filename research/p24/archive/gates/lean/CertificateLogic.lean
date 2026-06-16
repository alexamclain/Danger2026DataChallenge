/-!
Certificate logic for the p24 relative-resolvent program.

This file intentionally uses only Lean core.  It formalizes the small finite
logic that sits around the still-open arithmetic theorem:

* an invertible finite transform preserves all-zero vectors;
* a content/Bezout certificate rules out an all-zero packet;
* a nonzero scalar energy rules out an all-zero packet whenever harmful
  vanishing is known to force that scalar to be zero.

The CM/class-field work is the proof that the p24 objects instantiate these
abstract predicates.
-/

namespace P24.CertificateLogic

def AllZero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u = 0

theorem allZero_ext {α : Type} [Zero α] {m : Nat}
    {v w : Fin m → α} (hvw : ∀ u, v u = w u)
    (hz : AllZero v) :
    AllZero w := by
  intro u
  rw [← hvw u]
  exact hz u

theorem transform_all_zero_iff {α β : Type} [Zero α] [Zero β] {m : Nat}
    (encode : (Fin m → α) → (Fin m → β))
    (decode : (Fin m → β) → (Fin m → α))
    (v : Fin m → α)
    (h_encode_zero : AllZero v → AllZero (encode v))
    (h_decode_zero : ∀ w, AllZero w → AllZero (decode w))
    (h_left_inverse : ∀ u, decode (encode v) u = v u) :
    AllZero (encode v) ↔ AllZero v := by
  constructor
  · intro henc u
    rw [← h_left_inverse u]
    exact h_decode_zero (encode v) henc u
  · intro hv
    exact h_encode_zero hv

theorem coordinate_certificate_no_harmful {α : Type} [Zero α] {m : Nat}
    (v : Fin m → α)
    (u : Fin m)
    (hu : v u ≠ 0) :
    ¬ AllZero v := by
  intro hz
  exact hu (hz u)

theorem content_certificate_no_harmful {α : Type} [Zero α] [One α] {m : Nat}
    (v : Fin m → α)
    (combine : (Fin m → α) → α)
    (h_combine_zero : AllZero v → combine v = 0)
    (h_certificate : combine v = 1)
    (h_zero_ne_one : (0 : α) ≠ 1) :
    ¬ AllZero v := by
  intro hz
  have h0 : combine v = 0 := h_combine_zero hz
  have h01 : (0 : α) = 1 := Eq.trans h0.symm h_certificate
  exact h_zero_ne_one h01

theorem product_certificate_no_harmful {α : Type} [Zero α] {m : Nat}
    (v : Fin m → α)
    (product : (Fin m → α) → α)
    (h_product_zero : AllZero v → product v = 0)
    (h_product_nonzero : product v ≠ 0) :
    ¬ AllZero v := by
  intro hz
  exact h_product_nonzero (h_product_zero hz)

theorem energy_certificate_no_harmful {α : Type} [Zero α] {m : Nat}
    (v : Fin m → α)
    (energy : α)
    (h_energy_zero : AllZero v → energy = 0)
    (h_energy_nonzero : energy ≠ 0) :
    ¬ AllZero v := by
  intro hz
  exact h_energy_nonzero (h_energy_zero hz)

theorem harmful_implies_energy_zero_contrapositive
    {α : Type} [Zero α] {m : Nat}
    (harmful : Prop)
    (v : Fin m → α)
    (energy : α)
    (h_harmful_all_zero : harmful → AllZero v)
    (h_energy_zero : AllZero v → energy = 0)
    (h_energy_nonzero : energy ≠ 0) :
    ¬ harmful := by
  intro hh
  exact h_energy_nonzero (h_energy_zero (h_harmful_all_zero hh))

theorem content_packet_no_harmful
    {α : Type} [Zero α] [One α] {m : Nat}
    (harmful : Prop)
    (packet : Fin m → α)
    (combine : (Fin m → α) → α)
    (h_harmful_all_zero : harmful → AllZero packet)
    (h_combine_zero : AllZero packet → combine packet = 0)
    (h_certificate : combine packet = 1)
    (h_zero_ne_one : (0 : α) ≠ 1) :
    ¬ harmful := by
  intro hh
  have hz : AllZero packet := h_harmful_all_zero hh
  exact content_certificate_no_harmful packet combine h_combine_zero
    h_certificate h_zero_ne_one hz

theorem all_packets_no_harmful_from_content
    {α : Type} [Zero α] [One α] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (combine : Fin orbitCount → (Fin m → α) → α)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_combine_zero :
      ∀ orbit, AllZero (packet orbit) → combine orbit (packet orbit) = 0)
    (h_certificate :
      ∀ orbit, combine orbit (packet orbit) = 1)
    (h_zero_ne_one : (0 : α) ≠ 1) :
    ∀ orbit, ¬ harmful orbit := by
  intro orbit
  exact content_packet_no_harmful (harmful orbit) (packet orbit)
    (combine orbit) (h_harmful_all_zero orbit)
    (h_combine_zero orbit) (h_certificate orbit) h_zero_ne_one

theorem all_packets_no_harmful_from_energy
    {α : Type} [Zero α] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (energy : Fin orbitCount → α)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_energy_zero :
      ∀ orbit, AllZero (packet orbit) → energy orbit = 0)
    (h_energy_nonzero :
      ∀ orbit, energy orbit ≠ 0) :
    ∀ orbit, ¬ harmful orbit := by
  intro orbit
  exact harmful_implies_energy_zero_contrapositive
    (harmful orbit) (packet orbit) (energy orbit)
    (h_harmful_all_zero orbit) (h_energy_zero orbit)
    (h_energy_nonzero orbit)

theorem packet_norms_nonzero_from_global_norm
    {α : Type} [Zero α] {orbitCount : Nat}
    (packetNorm : Fin orbitCount → α)
    (globalNorm : α)
    (h_any_zero : (∃ orbit, packetNorm orbit = 0) → globalNorm = 0)
    (h_global_nonzero : globalNorm ≠ 0) :
    ∀ orbit, packetNorm orbit ≠ 0 := by
  intro orbit hzero
  exact h_global_nonzero (h_any_zero ⟨orbit, hzero⟩)

theorem all_packets_no_harmful_from_global_norm
    {α : Type} [Zero α] {orbitCount : Nat}
    (harmful : Fin orbitCount → Prop)
    (packetNorm : Fin orbitCount → α)
    (globalNorm : α)
    (h_harmful_norm_zero :
      ∀ orbit, harmful orbit → packetNorm orbit = 0)
    (h_any_zero : (∃ orbit, packetNorm orbit = 0) → globalNorm = 0)
    (h_global_nonzero : globalNorm ≠ 0) :
    ∀ orbit, ¬ harmful orbit := by
  intro orbit hh
  have hnorm_nonzero :
      ∀ orbit, packetNorm orbit ≠ 0 :=
    packet_norms_nonzero_from_global_norm packetNorm globalNorm
      h_any_zero h_global_nonzero
  exact hnorm_nonzero orbit (h_harmful_norm_zero orbit hh)

end P24.CertificateLogic
