/-!
Finite gate for the single leading trace-frame Plucker norm.

The factorized Schubert route names four p-units.  For descent, the safest
denominator-free object is often the full leading Plucker determinant itself.
This file checks the finite implication:

  global leading packet norm nonzero
    => every packet leading determinant is nonzero
    => every packet trace-frame certificate is good
    => no harmful packet collapse.

The arithmetic construction of the global leading determinant is external.
-/

namespace P24.TraceFrameLeadingNormGate

theorem packet_leads_nonzero_from_global_norm
    {α : Type} [Zero α] {orbitCount : Nat}
    (packetLead : Fin orbitCount → α)
    (globalLeadNorm : α)
    (h_any_zero :
      (∃ orbit, packetLead orbit = 0) → globalLeadNorm = 0)
    (h_global_nonzero : globalLeadNorm ≠ 0) :
    ∀ orbit, packetLead orbit ≠ 0 := by
  intro orbit hzero
  exact h_global_nonzero (h_any_zero ⟨orbit, hzero⟩)

theorem all_trace_frames_good_from_global_lead_norm
    {α : Type} [Zero α] {orbitCount : Nat}
    (packetLead : Fin orbitCount → α)
    (globalLeadNorm : α)
    (TraceFrameGood : Fin orbitCount → Prop)
    (h_lead_good :
      ∀ orbit, packetLead orbit ≠ 0 → TraceFrameGood orbit)
    (h_any_zero :
      (∃ orbit, packetLead orbit = 0) → globalLeadNorm = 0)
    (h_global_nonzero : globalLeadNorm ≠ 0) :
    ∀ orbit, TraceFrameGood orbit := by
  intro orbit
  exact h_lead_good orbit
    (packet_leads_nonzero_from_global_norm
      packetLead globalLeadNorm h_any_zero h_global_nonzero orbit)

theorem no_harmful_packets_from_global_lead_norm
    {α : Type} [Zero α] {orbitCount : Nat}
    (packetLead : Fin orbitCount → α)
    (globalLeadNorm : α)
    (TraceFrameGood Harmful : Fin orbitCount → Prop)
    (h_lead_good :
      ∀ orbit, packetLead orbit ≠ 0 → TraceFrameGood orbit)
    (h_trace_no_harmful :
      ∀ orbit, TraceFrameGood orbit → ¬ Harmful orbit)
    (h_any_zero :
      (∃ orbit, packetLead orbit = 0) → globalLeadNorm = 0)
    (h_global_nonzero : globalLeadNorm ≠ 0) :
    ∀ orbit, ¬ Harmful orbit := by
  intro orbit
  apply h_trace_no_harmful
  exact all_trace_frames_good_from_global_lead_norm
    packetLead globalLeadNorm TraceFrameGood h_lead_good
    h_any_zero h_global_nonzero orbit

end P24.TraceFrameLeadingNormGate
