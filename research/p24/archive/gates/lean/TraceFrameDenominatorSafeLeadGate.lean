/-!
Finite gate for the denominator-safe trace-frame Schubert package.

The local four-factor theorem names

  Delta_A, Delta_B, Delta_AB, Delta_tail.

For global decomposition-field descent, `Delta_tail` is denominator-sensitive
because it is naturally built from `ker Top_2`.  The safer package is:

  Delta_A, Delta_B, Delta_AB, Delta_lead.

This file checks only the finite bookkeeping:

* global packet norms for A, B, AB, and lead make every packet residue nonzero;
* in each packet, prefix nonvanishing plus leading nonvanishing implies the
  trace-frame certificate;
* hence no harmful packet event occurs.

The arithmetic construction of the global determinant-line sections is
external.
-/

namespace P24.TraceFrameDenominatorSafeLeadGate

structure PacketPrefixLeadDeltas (α : Type) (orbitCount : Nat) where
  deltaA : Fin orbitCount → α
  deltaB : Fin orbitCount → α
  deltaAB : Fin orbitCount → α
  deltaLead : Fin orbitCount → α

structure GlobalPrefixLeadNorms (α : Type) where
  xiA : α
  xiB : α
  xiAB : α
  xiLead : α

def PacketPrefixGood {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketPrefixLeadDeltas α orbitCount)
    (orbit : Fin orbitCount) : Prop :=
  deltas.deltaA orbit ≠ 0 ∧
  deltas.deltaB orbit ≠ 0 ∧
  deltas.deltaAB orbit ≠ 0

def PacketLeadGood {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketPrefixLeadDeltas α orbitCount)
    (orbit : Fin orbitCount) : Prop :=
  deltas.deltaLead orbit ≠ 0

theorem packet_prefix_lead_good_from_global_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketPrefixLeadDeltas α orbitCount)
    (norms : GlobalPrefixLeadNorms α)
    (h_any_zero_A :
      (∃ orbit, deltas.deltaA orbit = 0) → norms.xiA = 0)
    (h_any_zero_B :
      (∃ orbit, deltas.deltaB orbit = 0) → norms.xiB = 0)
    (h_any_zero_AB :
      (∃ orbit, deltas.deltaAB orbit = 0) → norms.xiAB = 0)
    (h_any_zero_lead :
      (∃ orbit, deltas.deltaLead orbit = 0) → norms.xiLead = 0)
    (h_xiA : norms.xiA ≠ 0)
    (h_xiB : norms.xiB ≠ 0)
    (h_xiAB : norms.xiAB ≠ 0)
    (h_xiLead : norms.xiLead ≠ 0) :
    ∀ orbit, PacketPrefixGood deltas orbit ∧ PacketLeadGood deltas orbit := by
  intro orbit
  refine ⟨?_, ?_⟩
  · refine ⟨?_, ?_, ?_⟩
    · intro hzero
      exact h_xiA (h_any_zero_A ⟨orbit, hzero⟩)
    · intro hzero
      exact h_xiB (h_any_zero_B ⟨orbit, hzero⟩)
    · intro hzero
      exact h_xiAB (h_any_zero_AB ⟨orbit, hzero⟩)
  · intro hzero
    exact h_xiLead (h_any_zero_lead ⟨orbit, hzero⟩)

theorem all_trace_frames_good_from_global_prefix_lead_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketPrefixLeadDeltas α orbitCount)
    (norms : GlobalPrefixLeadNorms α)
    (TraceFrameGood : Fin orbitCount → Prop)
    (h_prefix_lead_trace :
      ∀ orbit,
        PacketPrefixGood deltas orbit →
          PacketLeadGood deltas orbit →
            TraceFrameGood orbit)
    (h_any_zero_A :
      (∃ orbit, deltas.deltaA orbit = 0) → norms.xiA = 0)
    (h_any_zero_B :
      (∃ orbit, deltas.deltaB orbit = 0) → norms.xiB = 0)
    (h_any_zero_AB :
      (∃ orbit, deltas.deltaAB orbit = 0) → norms.xiAB = 0)
    (h_any_zero_lead :
      (∃ orbit, deltas.deltaLead orbit = 0) → norms.xiLead = 0)
    (h_xiA : norms.xiA ≠ 0)
    (h_xiB : norms.xiB ≠ 0)
    (h_xiAB : norms.xiAB ≠ 0)
    (h_xiLead : norms.xiLead ≠ 0) :
    ∀ orbit, TraceFrameGood orbit := by
  intro orbit
  have h_good :=
    packet_prefix_lead_good_from_global_norms
      deltas norms h_any_zero_A h_any_zero_B h_any_zero_AB
      h_any_zero_lead h_xiA h_xiB h_xiAB h_xiLead orbit
  exact h_prefix_lead_trace orbit h_good.1 h_good.2

theorem no_harmful_packets_from_global_prefix_lead_norms
    {α : Type} [Zero α] {orbitCount : Nat}
    (deltas : PacketPrefixLeadDeltas α orbitCount)
    (norms : GlobalPrefixLeadNorms α)
    (TraceFrameGood Harmful : Fin orbitCount → Prop)
    (h_prefix_lead_trace :
      ∀ orbit,
        PacketPrefixGood deltas orbit →
          PacketLeadGood deltas orbit →
            TraceFrameGood orbit)
    (h_trace_no_harmful :
      ∀ orbit, TraceFrameGood orbit → ¬ Harmful orbit)
    (h_any_zero_A :
      (∃ orbit, deltas.deltaA orbit = 0) → norms.xiA = 0)
    (h_any_zero_B :
      (∃ orbit, deltas.deltaB orbit = 0) → norms.xiB = 0)
    (h_any_zero_AB :
      (∃ orbit, deltas.deltaAB orbit = 0) → norms.xiAB = 0)
    (h_any_zero_lead :
      (∃ orbit, deltas.deltaLead orbit = 0) → norms.xiLead = 0)
    (h_xiA : norms.xiA ≠ 0)
    (h_xiB : norms.xiB ≠ 0)
    (h_xiAB : norms.xiAB ≠ 0)
    (h_xiLead : norms.xiLead ≠ 0) :
    ∀ orbit, ¬ Harmful orbit := by
  intro orbit
  apply h_trace_no_harmful
  exact all_trace_frames_good_from_global_prefix_lead_norms
    deltas norms TraceFrameGood h_prefix_lead_trace
    h_any_zero_A h_any_zero_B h_any_zero_AB h_any_zero_lead
    h_xiA h_xiB h_xiAB h_xiLead orbit

end P24.TraceFrameDenominatorSafeLeadGate
