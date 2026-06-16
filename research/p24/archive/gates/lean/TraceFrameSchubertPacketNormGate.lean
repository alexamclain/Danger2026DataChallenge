/-!
Finite gate for the trace-frame Schubert packet-norm package.

The arithmetic theorem should produce four equivariant decomposition-field
elements whose eight residues are the packet Schubert determinants

  Delta_A, Delta_B, Delta_AB, Delta_tail.

This file checks only the finite bookkeeping:

* if a global packet norm is nonzero, none of its packet residues is zero;
* if the four packet residues are nonzero, the packet trace-frame certificate
  is good;
* if the packet trace-frame certificate is good, the harmful packet event is
  impossible.

The class-field construction of the four global norms is external to Lean.
-/

namespace P24.TraceFrameSchubertPacketNormGate

structure PacketDeltas (α : Type) (orbitCount : Nat) where
  deltaA : Fin orbitCount → α
  deltaB : Fin orbitCount → α
  deltaAB : Fin orbitCount → α
  deltaTail : Fin orbitCount → α

structure GlobalNorms (α : Type) where
  xiA : α
  xiB : α
  xiAB : α
  xiTail : α

def PacketSchubertGood {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketDeltas α orbitCount)
    (orbit : Fin orbitCount) : Prop :=
  deltas.deltaA orbit ≠ 0 ∧
  deltas.deltaB orbit ≠ 0 ∧
  deltas.deltaAB orbit ≠ 0 ∧
  deltas.deltaTail orbit ≠ 0

theorem packet_schubert_good_from_global_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketDeltas α orbitCount)
    (norms : GlobalNorms α)
    (h_any_zero_A :
      (∃ orbit, deltas.deltaA orbit = 0) → norms.xiA = 0)
    (h_any_zero_B :
      (∃ orbit, deltas.deltaB orbit = 0) → norms.xiB = 0)
    (h_any_zero_AB :
      (∃ orbit, deltas.deltaAB orbit = 0) → norms.xiAB = 0)
    (h_any_zero_tail :
      (∃ orbit, deltas.deltaTail orbit = 0) → norms.xiTail = 0)
    (h_xiA : norms.xiA ≠ 0)
    (h_xiB : norms.xiB ≠ 0)
    (h_xiAB : norms.xiAB ≠ 0)
    (h_xiTail : norms.xiTail ≠ 0) :
    ∀ orbit, PacketSchubertGood deltas orbit := by
  intro orbit
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro hzero
    exact h_xiA (h_any_zero_A ⟨orbit, hzero⟩)
  · intro hzero
    exact h_xiB (h_any_zero_B ⟨orbit, hzero⟩)
  · intro hzero
    exact h_xiAB (h_any_zero_AB ⟨orbit, hzero⟩)
  · intro hzero
    exact h_xiTail (h_any_zero_tail ⟨orbit, hzero⟩)

theorem all_trace_frames_good_from_global_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketDeltas α orbitCount)
    (norms : GlobalNorms α)
    (TraceFrameGood : Fin orbitCount → Prop)
    (h_packet_good_trace :
      ∀ orbit, PacketSchubertGood deltas orbit → TraceFrameGood orbit)
    (h_any_zero_A :
      (∃ orbit, deltas.deltaA orbit = 0) → norms.xiA = 0)
    (h_any_zero_B :
      (∃ orbit, deltas.deltaB orbit = 0) → norms.xiB = 0)
    (h_any_zero_AB :
      (∃ orbit, deltas.deltaAB orbit = 0) → norms.xiAB = 0)
    (h_any_zero_tail :
      (∃ orbit, deltas.deltaTail orbit = 0) → norms.xiTail = 0)
    (h_xiA : norms.xiA ≠ 0)
    (h_xiB : norms.xiB ≠ 0)
    (h_xiAB : norms.xiAB ≠ 0)
    (h_xiTail : norms.xiTail ≠ 0) :
    ∀ orbit, TraceFrameGood orbit := by
  intro orbit
  apply h_packet_good_trace
  exact packet_schubert_good_from_global_norms
    deltas norms h_any_zero_A h_any_zero_B h_any_zero_AB
    h_any_zero_tail h_xiA h_xiB h_xiAB h_xiTail orbit

theorem no_harmful_packets_from_global_schubert_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketDeltas α orbitCount)
    (norms : GlobalNorms α)
    (TraceFrameGood Harmful : Fin orbitCount → Prop)
    (h_packet_good_trace :
      ∀ orbit, PacketSchubertGood deltas orbit → TraceFrameGood orbit)
    (h_trace_no_harmful :
      ∀ orbit, TraceFrameGood orbit → ¬ Harmful orbit)
    (h_any_zero_A :
      (∃ orbit, deltas.deltaA orbit = 0) → norms.xiA = 0)
    (h_any_zero_B :
      (∃ orbit, deltas.deltaB orbit = 0) → norms.xiB = 0)
    (h_any_zero_AB :
      (∃ orbit, deltas.deltaAB orbit = 0) → norms.xiAB = 0)
    (h_any_zero_tail :
      (∃ orbit, deltas.deltaTail orbit = 0) → norms.xiTail = 0)
    (h_xiA : norms.xiA ≠ 0)
    (h_xiB : norms.xiB ≠ 0)
    (h_xiAB : norms.xiAB ≠ 0)
    (h_xiTail : norms.xiTail ≠ 0) :
    ∀ orbit, ¬ Harmful orbit := by
  intro orbit
  apply h_trace_no_harmful
  exact all_trace_frames_good_from_global_norms
    deltas norms TraceFrameGood h_packet_good_trace
    h_any_zero_A h_any_zero_B h_any_zero_AB h_any_zero_tail
    h_xiA h_xiB h_xiAB h_xiTail orbit

end P24.TraceFrameSchubertPacketNormGate
