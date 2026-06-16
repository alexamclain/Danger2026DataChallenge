/-!
Finite gate for tensor-factor equivariance of the leading trace-frame
determinant.

The arithmetic input is external: Frobenius transport across scalar-extension
tensor factors must carry the fixed leading determinant to a p-unit multiple
of its conjugate.  This file records only the zero/nonzero implication needed
to compress many tensor-factor p-unit targets to one representative target.
-/

namespace P24.TraceFrameTensorFactorEquivarianceGate

theorem all_factor_leads_nonzero_from_representative
    {α : Type} [Zero α] {factorCount : Nat}
    (factorLead : Fin factorCount → α)
    (representative : Fin factorCount)
    (h_transport_nonzero :
      ∀ factor, factorLead representative ≠ 0 → factorLead factor ≠ 0)
    (h_representative_nonzero : factorLead representative ≠ 0) :
    ∀ factor, factorLead factor ≠ 0 := by
  intro factor
  exact h_transport_nonzero factor h_representative_nonzero

theorem representative_lead_nonzero_from_norm
    {α : Type} [Zero α]
    (representativeLead representativeNorm : α)
    (h_zero_forces_norm_zero :
      representativeLead = 0 → representativeNorm = 0)
    (h_norm_nonzero : representativeNorm ≠ 0) :
    representativeLead ≠ 0 := by
  intro h_zero
  exact h_norm_nonzero (h_zero_forces_norm_zero h_zero)

theorem all_factor_leads_nonzero_from_representative_norm
    {α : Type} [Zero α] {factorCount : Nat}
    (factorLead : Fin factorCount → α)
    (representative : Fin factorCount)
    (representativeNorm : α)
    (h_transport_nonzero :
      ∀ factor, factorLead representative ≠ 0 → factorLead factor ≠ 0)
    (h_zero_forces_norm_zero :
      factorLead representative = 0 → representativeNorm = 0)
    (h_norm_nonzero : representativeNorm ≠ 0) :
    ∀ factor, factorLead factor ≠ 0 := by
  exact all_factor_leads_nonzero_from_representative
    factorLead representative h_transport_nonzero
    (representative_lead_nonzero_from_norm
      (factorLead representative) representativeNorm
      h_zero_forces_norm_zero h_norm_nonzero)

theorem all_trace_frames_good_from_representative_norm
    {α : Type} [Zero α] {factorCount : Nat}
    (factorLead : Fin factorCount → α)
    (representative : Fin factorCount)
    (representativeNorm : α)
    (TraceFrameGood : Fin factorCount → Prop)
    (h_transport_nonzero :
      ∀ factor, factorLead representative ≠ 0 → factorLead factor ≠ 0)
    (h_zero_forces_norm_zero :
      factorLead representative = 0 → representativeNorm = 0)
    (h_norm_nonzero : representativeNorm ≠ 0)
    (h_lead_good :
      ∀ factor, factorLead factor ≠ 0 → TraceFrameGood factor) :
    ∀ factor, TraceFrameGood factor := by
  intro factor
  exact h_lead_good factor
    (all_factor_leads_nonzero_from_representative_norm
      factorLead representative representativeNorm
      h_transport_nonzero h_zero_forces_norm_zero h_norm_nonzero factor)

end P24.TraceFrameTensorFactorEquivarianceGate
