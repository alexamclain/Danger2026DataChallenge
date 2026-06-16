/-!
Finite gate for the norm-compressed trace-frame certificate.

This file combines the finite implications that are otherwise recorded in
separate gates:

* a nonzero degree-8 packet norm makes every H-packet representative leading
  determinant nonzero;
* tensor-factor equivariance transports that nonzero determinant to every
  scalar-extension tensor factor;
* the beta-orbit/tensor-factor indexing then covers every nonzero beta orbit.

The arithmetic inputs are external:

* construction of the determinant-line element whose degree-8 norm is supplied;
* proof that zero in any packet representative forces that norm to vanish;
* proof that tensor-factor transport is by p-units;
* proof that factorwise leading nonvanishing is the desired beta goodness.
-/

namespace P24.TraceFrameNormCompressedCertificateGate

def FactorwiseCertificate {Packet Factor : Type}
    (FactorGood : Packet → Factor → Prop) : Prop :=
  ∀ packet factor, FactorGood packet factor

def BetaOrbitCovered {BetaOrbit Packet Factor : Type}
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood : BetaOrbit → Prop) : Prop :=
  ∀ beta, FactorGood (packetOf beta) (factorOf beta) → BetaGood beta

def InversePayload {Scalar : Type} [Mul Scalar] [One Scalar]
    (value inverse : Scalar) : Prop :=
  value * inverse = 1

theorem nonzero_from_inverse_payload
    {Scalar : Type} [Zero Scalar] [One Scalar] [Mul Scalar]
    (value inverse : Scalar)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_payload : InversePayload value inverse) :
    value ≠ 0 := by
  intro h_value_zero
  exact h_one_ne_zero (by
    calc
      (1 : Scalar) = value * inverse := h_payload.symm
      _ = (0 : Scalar) * inverse := by rw [h_value_zero]
      _ = 0 := h_zero_mul inverse)

theorem representative_packet_leads_nonzero_from_degree8_norm
    {Packet Scalar : Type} [Zero Scalar]
    (representativeLead : Packet → Scalar)
    (degree8Norm : Scalar)
    (h_any_zero :
      (∃ packet, representativeLead packet = 0) → degree8Norm = 0)
    (h_norm_nonzero : degree8Norm ≠ 0) :
    ∀ packet, representativeLead packet ≠ 0 := by
  intro packet h_zero
  exact h_norm_nonzero (h_any_zero ⟨packet, h_zero⟩)

theorem factor_leads_nonzero_from_representative_transport
    {Packet Factor Scalar : Type} [Zero Scalar]
    (factorLead : Packet → Factor → Scalar)
    (representative : Factor)
    (representativeLead : Packet → Scalar)
    (h_rep :
      ∀ packet, factorLead packet representative = representativeLead packet)
    (h_transport :
      ∀ packet factor,
        factorLead packet representative ≠ 0 →
          factorLead packet factor ≠ 0)
    (h_rep_nonzero : ∀ packet, representativeLead packet ≠ 0) :
    ∀ packet factor, factorLead packet factor ≠ 0 := by
  intro packet factor
  apply h_transport packet factor
  rw [h_rep packet]
  exact h_rep_nonzero packet

theorem factorwise_good_from_degree8_norm
    {Packet Factor Scalar : Type} [Zero Scalar]
    (factorLead : Packet → Factor → Scalar)
    (representative : Factor)
    (representativeLead : Packet → Scalar)
    (degree8Norm : Scalar)
    (FactorGood : Packet → Factor → Prop)
    (h_rep :
      ∀ packet, factorLead packet representative = representativeLead packet)
    (h_any_zero :
      (∃ packet, representativeLead packet = 0) → degree8Norm = 0)
    (h_norm_nonzero : degree8Norm ≠ 0)
    (h_transport :
      ∀ packet factor,
        factorLead packet representative ≠ 0 →
          factorLead packet factor ≠ 0)
    (h_lead_good :
      ∀ packet factor, factorLead packet factor ≠ 0 →
        FactorGood packet factor) :
    FactorwiseCertificate FactorGood := by
  intro packet factor
  exact h_lead_good packet factor
    (factor_leads_nonzero_from_representative_transport
      factorLead representative representativeLead h_rep h_transport
      (representative_packet_leads_nonzero_from_degree8_norm
        representativeLead degree8Norm h_any_zero h_norm_nonzero)
      packet factor)

theorem all_beta_orbits_good_from_degree8_norm
    {BetaOrbit Packet Factor Scalar : Type} [Zero Scalar]
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (factorLead : Packet → Factor → Scalar)
    (representative : Factor)
    (representativeLead : Packet → Scalar)
    (degree8Norm : Scalar)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood : BetaOrbit → Prop)
    (h_rep :
      ∀ packet, factorLead packet representative = representativeLead packet)
    (h_any_zero :
      (∃ packet, representativeLead packet = 0) → degree8Norm = 0)
    (h_norm_nonzero : degree8Norm ≠ 0)
    (h_transport :
      ∀ packet factor,
        factorLead packet representative ≠ 0 →
          factorLead packet factor ≠ 0)
    (h_lead_good :
      ∀ packet factor, factorLead packet factor ≠ 0 →
        FactorGood packet factor)
    (h_beta_covered :
      BetaOrbitCovered packetOf factorOf FactorGood BetaGood) :
    ∀ beta, BetaGood beta := by
  intro beta
  apply h_beta_covered
  exact factorwise_good_from_degree8_norm
    factorLead representative representativeLead degree8Norm FactorGood
    h_rep h_any_zero h_norm_nonzero h_transport h_lead_good
    (packetOf beta) (factorOf beta)

theorem all_beta_orbits_good_from_degree8_inverse_payload
    {BetaOrbit Packet Factor Scalar : Type}
    [Zero Scalar] [One Scalar] [Mul Scalar]
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (factorLead : Packet → Factor → Scalar)
    (representative : Factor)
    (representativeLead : Packet → Scalar)
    (degree8Norm degree8NormInverse : Scalar)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood : BetaOrbit → Prop)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_payload : InversePayload degree8Norm degree8NormInverse)
    (h_rep :
      ∀ packet, factorLead packet representative = representativeLead packet)
    (h_any_zero :
      (∃ packet, representativeLead packet = 0) → degree8Norm = 0)
    (h_transport :
      ∀ packet factor,
        factorLead packet representative ≠ 0 →
          factorLead packet factor ≠ 0)
    (h_lead_good :
      ∀ packet factor, factorLead packet factor ≠ 0 →
        FactorGood packet factor)
    (h_beta_covered :
      BetaOrbitCovered packetOf factorOf FactorGood BetaGood) :
    ∀ beta, BetaGood beta := by
  apply all_beta_orbits_good_from_degree8_norm
    packetOf factorOf factorLead representative representativeLead
    degree8Norm FactorGood BetaGood
    h_rep h_any_zero
  · exact nonzero_from_inverse_payload
      degree8Norm degree8NormInverse h_zero_mul h_one_ne_zero h_payload
  · exact h_transport
  · exact h_lead_good
  · exact h_beta_covered

theorem no_harmful_beta_orbits_from_degree8_inverse_payload
    {BetaOrbit Packet Factor Scalar : Type}
    [Zero Scalar] [One Scalar] [Mul Scalar]
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (factorLead : Packet → Factor → Scalar)
    (representative : Factor)
    (representativeLead : Packet → Scalar)
    (degree8Norm degree8NormInverse : Scalar)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood Harmful : BetaOrbit → Prop)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_payload : InversePayload degree8Norm degree8NormInverse)
    (h_rep :
      ∀ packet, factorLead packet representative = representativeLead packet)
    (h_any_zero :
      (∃ packet, representativeLead packet = 0) → degree8Norm = 0)
    (h_transport :
      ∀ packet factor,
        factorLead packet representative ≠ 0 →
          factorLead packet factor ≠ 0)
    (h_lead_good :
      ∀ packet factor, factorLead packet factor ≠ 0 →
        FactorGood packet factor)
    (h_beta_covered :
      BetaOrbitCovered packetOf factorOf FactorGood BetaGood)
    (h_good_no_harmful :
      ∀ beta, BetaGood beta → ¬ Harmful beta) :
    ∀ beta, ¬ Harmful beta := by
  intro beta
  exact h_good_no_harmful beta
    (all_beta_orbits_good_from_degree8_inverse_payload
      packetOf factorOf factorLead representative representativeLead
      degree8Norm degree8NormInverse FactorGood BetaGood
      h_zero_mul h_one_ne_zero h_payload h_rep h_any_zero
      h_transport h_lead_good h_beta_covered beta)

theorem no_harmful_all_beta_orbits_from_zero_gate_and_nonzero_inverse_payload
    {ZeroOrbit NonzeroBetaOrbit Packet Factor Scalar : Type}
    [Zero Scalar] [One Scalar] [Mul Scalar]
    (packetOf : NonzeroBetaOrbit → Packet)
    (factorOf : NonzeroBetaOrbit → Factor)
    (factorLead : Packet → Factor → Scalar)
    (representative : Factor)
    (representativeLead : Packet → Scalar)
    (degree8Norm degree8NormInverse : Scalar)
    (FactorGood : Packet → Factor → Prop)
    (NonzeroBetaGood : NonzeroBetaOrbit → Prop)
    (ZeroHarmful : ZeroOrbit → Prop)
    (NonzeroHarmful : NonzeroBetaOrbit → Prop)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_payload : InversePayload degree8Norm degree8NormInverse)
    (h_rep :
      ∀ packet, factorLead packet representative = representativeLead packet)
    (h_any_zero :
      (∃ packet, representativeLead packet = 0) → degree8Norm = 0)
    (h_transport :
      ∀ packet factor,
        factorLead packet representative ≠ 0 →
          factorLead packet factor ≠ 0)
    (h_lead_good :
      ∀ packet factor, factorLead packet factor ≠ 0 →
        FactorGood packet factor)
    (h_beta_covered :
      BetaOrbitCovered packetOf factorOf FactorGood NonzeroBetaGood)
    (h_zero_no_harmful :
      ∀ zero, ¬ ZeroHarmful zero)
    (h_good_no_harmful :
      ∀ beta, NonzeroBetaGood beta → ¬ NonzeroHarmful beta) :
    ∀ beta : Sum ZeroOrbit NonzeroBetaOrbit,
      ¬ match beta with
        | Sum.inl zero => ZeroHarmful zero
        | Sum.inr nonzero => NonzeroHarmful nonzero := by
  intro beta
  cases beta with
  | inl zero =>
      exact h_zero_no_harmful zero
  | inr nonzero =>
      exact no_harmful_beta_orbits_from_degree8_inverse_payload
        packetOf factorOf factorLead representative representativeLead
        degree8Norm degree8NormInverse FactorGood NonzeroBetaGood
        NonzeroHarmful h_zero_mul h_one_ne_zero h_payload h_rep h_any_zero
        h_transport h_lead_good h_beta_covered h_good_no_harmful nonzero

theorem no_harmful_zero_orbits_from_inverse_payload
    {ZeroOrbit Scalar : Type} [Zero Scalar] [One Scalar] [Mul Scalar]
    (zeroValue zeroValueInverse : Scalar)
    (ZeroHarmful : ZeroOrbit → Prop)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_zero_payload : InversePayload zeroValue zeroValueInverse)
    (h_zero_harmful_forces_zero :
      ∀ zero, ZeroHarmful zero → zeroValue = 0) :
    ∀ zero, ¬ ZeroHarmful zero := by
  intro zero h_harmful
  exact (nonzero_from_inverse_payload
    zeroValue zeroValueInverse h_zero_mul h_one_ne_zero h_zero_payload)
    (h_zero_harmful_forces_zero zero h_harmful)

theorem no_harmful_all_beta_orbits_from_four_element_payload
    {ZeroOrbit NonzeroBetaOrbit Packet Factor Scalar : Type}
    [Zero Scalar] [One Scalar] [Mul Scalar]
    (packetOf : NonzeroBetaOrbit → Packet)
    (factorOf : NonzeroBetaOrbit → Factor)
    (factorLead : Packet → Factor → Scalar)
    (representative : Factor)
    (representativeLead : Packet → Scalar)
    (zeroValue zeroValueInverse : Scalar)
    (degree8Norm degree8NormInverse : Scalar)
    (FactorGood : Packet → Factor → Prop)
    (NonzeroBetaGood : NonzeroBetaOrbit → Prop)
    (ZeroHarmful : ZeroOrbit → Prop)
    (NonzeroHarmful : NonzeroBetaOrbit → Prop)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_zero_payload : InversePayload zeroValue zeroValueInverse)
    (h_degree8_payload :
      InversePayload degree8Norm degree8NormInverse)
    (h_zero_harmful_forces_zero :
      ∀ zero, ZeroHarmful zero → zeroValue = 0)
    (h_rep :
      ∀ packet, factorLead packet representative = representativeLead packet)
    (h_any_zero :
      (∃ packet, representativeLead packet = 0) → degree8Norm = 0)
    (h_transport :
      ∀ packet factor,
        factorLead packet representative ≠ 0 →
          factorLead packet factor ≠ 0)
    (h_lead_good :
      ∀ packet factor, factorLead packet factor ≠ 0 →
        FactorGood packet factor)
    (h_beta_covered :
      BetaOrbitCovered packetOf factorOf FactorGood NonzeroBetaGood)
    (h_good_no_harmful :
      ∀ beta, NonzeroBetaGood beta → ¬ NonzeroHarmful beta) :
    ∀ beta : Sum ZeroOrbit NonzeroBetaOrbit,
      ¬ match beta with
        | Sum.inl zero => ZeroHarmful zero
        | Sum.inr nonzero => NonzeroHarmful nonzero := by
  apply no_harmful_all_beta_orbits_from_zero_gate_and_nonzero_inverse_payload
    packetOf factorOf factorLead representative representativeLead
    degree8Norm degree8NormInverse FactorGood NonzeroBetaGood
    ZeroHarmful NonzeroHarmful h_zero_mul h_one_ne_zero
    h_degree8_payload h_rep h_any_zero h_transport h_lead_good
    h_beta_covered
  · exact no_harmful_zero_orbits_from_inverse_payload
      zeroValue zeroValueInverse ZeroHarmful
      h_zero_mul h_one_ne_zero h_zero_payload h_zero_harmful_forces_zero
  · exact h_good_no_harmful

def p24SqrtFloor : Nat := 1000000000000

def p24KCharacterFieldDegree : Nat := 5460

def p24HPacketCount : Nat := 8

def p24TensorFactorCountPerPacket : Nat := 70

def p24NonzeroBetaOrbitCount : Nat :=
  p24HPacketCount * p24TensorFactorCountPerPacket

def p24SubfieldDegreeOverE : Nat := 179

def p24SelectedTailHeadCoordinates : Nat := 10

def p24LeadingTraceFrameCoordinateCount : Nat :=
  p24SubfieldDegreeOverE +
    p24SubfieldDegreeOverE +
    p24SelectedTailHeadCoordinates

def p24AxisDimension : Nat := 368

def p24SingleLeadingMatrixEntriesPerPacketOverE : Nat :=
  p24AxisDimension * p24AxisDimension

def p24SingleLeadingAllPacketsEntriesOverE : Nat :=
  p24HPacketCount * p24SingleLeadingMatrixEntriesPerPacketOverE

def p24SingleLeadingAllPacketsFpSlots : Nat :=
  p24SingleLeadingAllPacketsEntriesOverE * p24KCharacterFieldDegree

def p24SingleLeadingAllFactorsEntriesOverE : Nat :=
  p24HPacketCount *
    p24TensorFactorCountPerPacket *
    p24SingleLeadingMatrixEntriesPerPacketOverE

def p24SingleLeadingAllFactorsFpSlots : Nat :=
  p24SingleLeadingAllFactorsEntriesOverE * p24KCharacterFieldDegree

def p24FactorizedEntriesPerPacketOverE : Nat :=
  158 * 158 + 210 * 210 + 200 * 200 + 10 * 10

def p24FactorizedOneFactorAllPacketsFpSlots : Nat :=
  p24HPacketCount *
    p24FactorizedEntriesPerPacketOverE *
    p24KCharacterFieldDegree

def p24FactorizedAllFactorsFpSlots : Nat :=
  p24HPacketCount *
    p24TensorFactorCountPerPacket *
    p24FactorizedEntriesPerPacketOverE *
    p24KCharacterFieldDegree

def p24NormCompressedPayloadEntriesOverE : Nat := 2

def p24NormCompressedPayloadFpSlots : Nat :=
  p24NormCompressedPayloadEntriesOverE * p24KCharacterFieldDegree

def p24FullBetaFourElementPayloadEntriesOverE : Nat := 4

def p24FullBetaFourElementPayloadFpSlots : Nat :=
  p24FullBetaFourElementPayloadEntriesOverE * p24KCharacterFieldDegree

def p24OrbitwiseNormPayloadEntriesOverE : Nat :=
  2 * p24NonzeroBetaOrbitCount

def p24OrbitwiseNormPayloadFpSlots : Nat :=
  p24OrbitwiseNormPayloadEntriesOverE * p24KCharacterFieldDegree

theorem p24_nonzero_beta_orbit_count :
    p24NonzeroBetaOrbitCount = 560 := by
  decide

theorem p24_leading_trace_frame_coordinate_count :
    p24LeadingTraceFrameCoordinateCount = p24AxisDimension := by
  decide

theorem p24_single_leading_matrix_entries_per_packet :
    p24SingleLeadingMatrixEntriesPerPacketOverE = 135424 := by
  decide

theorem p24_single_leading_all_packets_fp_slots :
    p24SingleLeadingAllPacketsFpSlots = 5915320320 := by
  decide

theorem p24_single_leading_all_packets_subsqrt :
    p24SingleLeadingAllPacketsFpSlots < p24SqrtFloor := by
  decide

theorem p24_single_leading_all_factors_fp_slots :
    p24SingleLeadingAllFactorsFpSlots = 414072422400 := by
  decide

theorem p24_single_leading_all_factors_subsqrt :
    p24SingleLeadingAllFactorsFpSlots < p24SqrtFloor := by
  decide

theorem p24_factorized_entries_per_packet :
    p24FactorizedEntriesPerPacketOverE = 109164 := by
  decide

theorem p24_factorized_one_factor_all_packets_fp_slots :
    p24FactorizedOneFactorAllPacketsFpSlots = 4768283520 := by
  decide

theorem p24_factorized_one_factor_subsqrt :
    p24FactorizedOneFactorAllPacketsFpSlots < p24SqrtFloor := by
  decide

theorem p24_factorized_all_factors_fp_slots :
    p24FactorizedAllFactorsFpSlots = 333779846400 := by
  decide

theorem p24_factorized_all_factors_subsqrt :
    p24FactorizedAllFactorsFpSlots < p24SqrtFloor := by
  decide

theorem p24_norm_compressed_payload_fp_slots :
    p24NormCompressedPayloadFpSlots = 10920 := by
  decide

theorem p24_norm_compressed_payload_subsqrt :
    p24NormCompressedPayloadFpSlots < p24SqrtFloor := by
  decide

theorem p24_full_beta_four_element_payload_fp_slots :
    p24FullBetaFourElementPayloadFpSlots = 21840 := by
  decide

theorem p24_full_beta_four_element_payload_subsqrt :
    p24FullBetaFourElementPayloadFpSlots < p24SqrtFloor := by
  decide

theorem p24_orbitwise_norm_payload_fp_slots :
    p24OrbitwiseNormPayloadFpSlots = 6115200 := by
  decide

theorem p24_orbitwise_norm_payload_subsqrt :
    p24OrbitwiseNormPayloadFpSlots < p24SqrtFloor := by
  decide

end P24.TraceFrameNormCompressedCertificateGate
