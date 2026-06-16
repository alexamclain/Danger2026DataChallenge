/-!
Finite gate for determinant-line descent up to p-units.

The arithmetic theorem should show that each packet Schubert determinant is
the residue of a global determinant-line section, possibly after multiplying
by an explicit local p-unit.  This file records the finite consequence:

  global norm nonzero
    => every global residue is nonzero
    => every packet determinant is nonzero, because the residue differs only
       by a unit.

No class-field or determinant-line construction is formalized here.
-/

namespace P24.SchubertEquivariantDescentGate

structure DescendedResidues (α : Type) (orbitCount : Nat) where
  globalResidue : Fin orbitCount → α
  packetDelta : Fin orbitCount → α

def ZeroCompatible {α : Type} [Zero α] {orbitCount : Nat}
    (residues : DescendedResidues α orbitCount) : Prop :=
  ∀ orbit, residues.globalResidue orbit = 0 ↔ residues.packetDelta orbit = 0

theorem packet_deltas_nonzero_from_descended_norm
    {α : Type} [Zero α] {orbitCount : Nat}
    (residues : DescendedResidues α orbitCount)
    (globalNorm : α)
    (h_zero_compatible : ZeroCompatible residues)
    (h_any_global_residue_zero :
      (∃ orbit, residues.globalResidue orbit = 0) → globalNorm = 0)
    (h_global_norm_nonzero : globalNorm ≠ 0) :
    ∀ orbit, residues.packetDelta orbit ≠ 0 := by
  intro orbit h_packet_zero
  have h_global_zero : residues.globalResidue orbit = 0 :=
    (h_zero_compatible orbit).2 h_packet_zero
  exact h_global_norm_nonzero
    (h_any_global_residue_zero ⟨orbit, h_global_zero⟩)

structure FourDescendedResidues (α : Type) (orbitCount : Nat) where
  A : DescendedResidues α orbitCount
  B : DescendedResidues α orbitCount
  AB : DescendedResidues α orbitCount
  tail : DescendedResidues α orbitCount

structure FourNorms (α : Type) where
  A : α
  B : α
  AB : α
  tail : α

def FourPacketGood {α : Type} [Zero α] {orbitCount : Nat}
    (residues : FourDescendedResidues α orbitCount)
    (orbit : Fin orbitCount) : Prop :=
  residues.A.packetDelta orbit ≠ 0 ∧
  residues.B.packetDelta orbit ≠ 0 ∧
  residues.AB.packetDelta orbit ≠ 0 ∧
  residues.tail.packetDelta orbit ≠ 0

theorem four_packet_good_from_descended_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (residues : FourDescendedResidues α orbitCount)
    (norms : FourNorms α)
    (h_zero_A : ZeroCompatible residues.A)
    (h_zero_B : ZeroCompatible residues.B)
    (h_zero_AB : ZeroCompatible residues.AB)
    (h_zero_tail : ZeroCompatible residues.tail)
    (h_any_A :
      (∃ orbit, residues.A.globalResidue orbit = 0) → norms.A = 0)
    (h_any_B :
      (∃ orbit, residues.B.globalResidue orbit = 0) → norms.B = 0)
    (h_any_AB :
      (∃ orbit, residues.AB.globalResidue orbit = 0) → norms.AB = 0)
    (h_any_tail :
      (∃ orbit, residues.tail.globalResidue orbit = 0) → norms.tail = 0)
    (h_norm_A : norms.A ≠ 0)
    (h_norm_B : norms.B ≠ 0)
    (h_norm_AB : norms.AB ≠ 0)
    (h_norm_tail : norms.tail ≠ 0) :
    ∀ orbit, FourPacketGood residues orbit := by
  intro orbit
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact packet_deltas_nonzero_from_descended_norm
      residues.A norms.A h_zero_A h_any_A h_norm_A orbit
  · exact packet_deltas_nonzero_from_descended_norm
      residues.B norms.B h_zero_B h_any_B h_norm_B orbit
  · exact packet_deltas_nonzero_from_descended_norm
      residues.AB norms.AB h_zero_AB h_any_AB h_norm_AB orbit
  · exact packet_deltas_nonzero_from_descended_norm
      residues.tail norms.tail h_zero_tail h_any_tail h_norm_tail orbit

theorem no_harmful_from_descended_schubert_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (residues : FourDescendedResidues α orbitCount)
    (norms : FourNorms α)
    (TraceFrameGood Harmful : Fin orbitCount → Prop)
    (h_four_good_trace :
      ∀ orbit, FourPacketGood residues orbit → TraceFrameGood orbit)
    (h_trace_no_harmful :
      ∀ orbit, TraceFrameGood orbit → ¬ Harmful orbit)
    (h_zero_A : ZeroCompatible residues.A)
    (h_zero_B : ZeroCompatible residues.B)
    (h_zero_AB : ZeroCompatible residues.AB)
    (h_zero_tail : ZeroCompatible residues.tail)
    (h_any_A :
      (∃ orbit, residues.A.globalResidue orbit = 0) → norms.A = 0)
    (h_any_B :
      (∃ orbit, residues.B.globalResidue orbit = 0) → norms.B = 0)
    (h_any_AB :
      (∃ orbit, residues.AB.globalResidue orbit = 0) → norms.AB = 0)
    (h_any_tail :
      (∃ orbit, residues.tail.globalResidue orbit = 0) → norms.tail = 0)
    (h_norm_A : norms.A ≠ 0)
    (h_norm_B : norms.B ≠ 0)
    (h_norm_AB : norms.AB ≠ 0)
    (h_norm_tail : norms.tail ≠ 0) :
    ∀ orbit, ¬ Harmful orbit := by
  intro orbit
  apply h_trace_no_harmful
  apply h_four_good_trace
  exact four_packet_good_from_descended_norms
    residues norms h_zero_A h_zero_B h_zero_AB h_zero_tail
    h_any_A h_any_B h_any_AB h_any_tail
    h_norm_A h_norm_B h_norm_AB h_norm_tail orbit

end P24.SchubertEquivariantDescentGate
