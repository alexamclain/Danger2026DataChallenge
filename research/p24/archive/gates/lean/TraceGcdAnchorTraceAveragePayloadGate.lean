/-!
Finite payload accounting for the p24 anchor trace-average route.

This file does not prove the CM/Lang producer theorem.  It checks that the
anchor verifier surfaces are sub-sqrt and keeps them separate from the
required honesty condition tying the supplied values to the embedded CM
trace-defect sums.
-/

namespace P24.TraceGcdAnchorTraceAveragePayloadGate

inductive AnchorPayloadShape where
  | defectHCosetSums
  | traceAveragePlusChildProfile
  | unauthenticatedEqualSums
deriving DecidableEq

def p24SqrtFloor : Nat := 1000000000000
def p24M : Nat := 66254
def p24DefectHCosetSlots : Nat := 7
def p24TraceAveragePlusChildSlots : Nat := 2 * p24M
def p24SelectedChainSlots : Nat := 3107811

def payloadSlots : AnchorPayloadShape -> Nat
  | AnchorPayloadShape.defectHCosetSums => p24DefectHCosetSlots
  | AnchorPayloadShape.traceAveragePlusChildProfile => p24TraceAveragePlusChildSlots
  | AnchorPayloadShape.unauthenticatedEqualSums => p24DefectHCosetSlots

def requiresProducerHonesty : AnchorPayloadShape -> Bool
  | AnchorPayloadShape.defectHCosetSums => true
  | AnchorPayloadShape.traceAveragePlusChildProfile => true
  | AnchorPayloadShape.unauthenticatedEqualSums => true

def producerSurfaceNamed : AnchorPayloadShape -> Bool
  | AnchorPayloadShape.defectHCosetSums => true
  | AnchorPayloadShape.traceAveragePlusChildProfile => true
  | AnchorPayloadShape.unauthenticatedEqualSums => false

abbrev beatsFixedSqrt (shape : AnchorPayloadShape) : Prop :=
  payloadSlots shape < p24SqrtFloor

abbrev authenticatedSurface (shape : AnchorPayloadShape) : Prop :=
  producerSurfaceNamed shape = true

abbrev anchorPayloadContract
    (shape : AnchorPayloadShape)
    (producerSound : Prop) : Prop :=
  beatsFixedSqrt shape ∧ authenticatedSurface shape ∧ producerSound

theorem defectHCoset_slots_value :
    payloadSlots AnchorPayloadShape.defectHCosetSums = 7 := by
  decide

theorem traceAveragePlusChild_slots_value :
    payloadSlots AnchorPayloadShape.traceAveragePlusChildProfile = 132508 := by
  decide

theorem traceAveragePlusChild_decomposes :
    p24TraceAveragePlusChildSlots = 2 * p24M := by
  decide

theorem defectHCoset_slots_subsqrt :
    beatsFixedSqrt AnchorPayloadShape.defectHCosetSums := by
  decide

theorem traceAveragePlusChild_slots_subsqrt :
    beatsFixedSqrt AnchorPayloadShape.traceAveragePlusChildProfile := by
  decide

theorem traceAveragePlusChild_smaller_than_selectedChain :
    payloadSlots AnchorPayloadShape.traceAveragePlusChildProfile <
      p24SelectedChainSlots := by
  decide

theorem defectHCoset_smaller_than_traceAveragePlusChild :
    payloadSlots AnchorPayloadShape.defectHCosetSums <
      payloadSlots AnchorPayloadShape.traceAveragePlusChildProfile := by
  decide

theorem defectHCoset_authenticated :
    authenticatedSurface AnchorPayloadShape.defectHCosetSums := by
  decide

theorem traceAveragePlusChild_authenticated :
    authenticatedSurface AnchorPayloadShape.traceAveragePlusChildProfile := by
  decide

theorem unauthenticatedEqualSums_not_authenticated :
    ¬ authenticatedSurface AnchorPayloadShape.unauthenticatedEqualSums := by
  decide

theorem defectHCoset_contract_from_sound
    (producerSound : Prop)
    (h_sound : producerSound) :
    anchorPayloadContract AnchorPayloadShape.defectHCosetSums producerSound := by
  exact ⟨defectHCoset_slots_subsqrt, defectHCoset_authenticated, h_sound⟩

theorem traceAveragePlusChild_contract_from_sound
    (producerSound : Prop)
    (h_sound : producerSound) :
    anchorPayloadContract AnchorPayloadShape.traceAveragePlusChildProfile
      producerSound := by
  exact
    ⟨traceAveragePlusChild_slots_subsqrt,
      traceAveragePlusChild_authenticated,
      h_sound⟩

end P24.TraceGcdAnchorTraceAveragePayloadGate
