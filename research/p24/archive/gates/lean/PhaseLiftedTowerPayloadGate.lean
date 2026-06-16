/-!
Finite payload accounting for the phase-lifted p24 tower route.

This file does not prove the arithmetic producer theorem.  It checks the
finite bookkeeping around the surviving selected-chain certificate surface and
keeps it separate from an h-scale class-table enumeration.
-/

namespace P24.PhaseLiftedTowerPayloadGate

inductive PayloadShape where
  | selectedChain
  | fullRelativeTable
  | fullClassTable
deriving DecidableEq

def p24SqrtFloor : Nat := 1000000000000
def p24TopDegree : Nat := 2
def p24Layer157Degree : Nat := 157
def p24Layer211Degree : Nat := 211
def p24QuotientDegree : Nat := 66254
def p24RecoveryDegree : Nat := 3107441
def p24ClassNumber : Nat := 205880396014

def p24FormalMPlusNSlots : Nat := p24QuotientDegree + p24RecoveryDegree
def p24InformativeChildPhaseSlots : Nat :=
  (p24Layer157Degree - 1) + (p24Layer211Degree - 1)
def p24ForcedChildTraceSlots : Nat := 2
def p24RelativeMorphismSlots : Nat :=
  p24TopDegree * p24Layer157Degree +
    (p24TopDegree * p24Layer157Degree) * p24Layer211Degree
def p24KummerNormalFormSlots : Nat :=
  p24TopDegree + p24ForcedChildTraceSlots +
    p24InformativeChildPhaseSlots + p24RecoveryDegree

def payloadSlots : PayloadShape -> Nat
  | PayloadShape.selectedChain =>
      p24TopDegree + p24Layer157Degree + p24Layer211Degree +
        p24RecoveryDegree
  | PayloadShape.fullRelativeTable =>
      p24TopDegree + p24TopDegree * p24Layer157Degree +
        (p24TopDegree * p24Layer157Degree) * p24Layer211Degree +
        p24RecoveryDegree
  | PayloadShape.fullClassTable =>
      p24ClassNumber

def classSetEnumerating : PayloadShape -> Bool
  | PayloadShape.selectedChain => false
  | PayloadShape.fullRelativeTable => false
  | PayloadShape.fullClassTable => true

abbrev classSetFree (shape : PayloadShape) : Prop :=
  classSetEnumerating shape = false

abbrev beatsFixedSqrt (shape : PayloadShape) : Prop :=
  payloadSlots shape < p24SqrtFloor

abbrev acceptableFiniteSurface (shape : PayloadShape) : Prop :=
  classSetFree shape ∧ beatsFixedSqrt shape

abbrev classSetFreeProducerContract
    (shape : PayloadShape)
    (producerSound : Prop) : Prop :=
  acceptableFiniteSurface shape ∧ producerSound

theorem selectedChain_slots_value :
    payloadSlots PayloadShape.selectedChain = 3107811 := by
  decide

theorem fullRelativeTable_slots_value :
    payloadSlots PayloadShape.fullRelativeTable = 3174011 := by
  decide

theorem formalMPlusN_slots_value :
    p24FormalMPlusNSlots = 3173695 := by
  decide

theorem informativeChildPhase_slots_value :
    p24InformativeChildPhaseSlots = 366 := by
  decide

theorem relativeMorphism_slots_value :
    p24RelativeMorphismSlots = 66568 := by
  decide

theorem relativeMorphism_slots_subsqrt :
    p24RelativeMorphismSlots < p24SqrtFloor := by
  decide

theorem fullRelativeTable_decomposes_as_morphism_plus_top_recovery :
    payloadSlots PayloadShape.fullRelativeTable =
      p24TopDegree + p24RelativeMorphismSlots + p24RecoveryDegree := by
  decide

theorem kummerNormalForm_slots_value :
    p24KummerNormalFormSlots = 3107811 := by
  decide

theorem selectedChain_eq_kummerNormalForm :
    payloadSlots PayloadShape.selectedChain = p24KummerNormalFormSlots := by
  decide

theorem selectedChain_slots_lt_formalMPlusN :
    payloadSlots PayloadShape.selectedChain < p24FormalMPlusNSlots := by
  decide

theorem formalMPlusN_slots_lt_fullRelativeTable :
    p24FormalMPlusNSlots < payloadSlots PayloadShape.fullRelativeTable := by
  decide

theorem selectedChain_slots_subsqrt :
    beatsFixedSqrt PayloadShape.selectedChain := by
  decide

theorem fullRelativeTable_slots_subsqrt :
    beatsFixedSqrt PayloadShape.fullRelativeTable := by
  decide

theorem selectedChain_classSetFree :
    classSetFree PayloadShape.selectedChain := by
  decide

theorem fullRelativeTable_classSetFree :
    classSetFree PayloadShape.fullRelativeTable := by
  decide

theorem selectedChain_acceptable :
    acceptableFiniteSurface PayloadShape.selectedChain := by
  constructor
  · exact selectedChain_classSetFree
  · exact selectedChain_slots_subsqrt

theorem fullRelativeTable_acceptable :
    acceptableFiniteSurface PayloadShape.fullRelativeTable := by
  constructor
  · exact fullRelativeTable_classSetFree
  · exact fullRelativeTable_slots_subsqrt

theorem fullClassTable_slots_fixed_subsqrt :
    beatsFixedSqrt PayloadShape.fullClassTable := by
  decide

theorem fullClassTable_not_classSetFree :
    ¬ classSetFree PayloadShape.fullClassTable := by
  decide

theorem fullClassTable_rejected_even_if_fixed_subsqrt :
    beatsFixedSqrt PayloadShape.fullClassTable ∧
      ¬ classSetFree PayloadShape.fullClassTable := by
  constructor
  · exact fullClassTable_slots_fixed_subsqrt
  · exact fullClassTable_not_classSetFree

theorem selectedChain_contract_from_sound
    (producerSound : Prop)
    (h_sound : producerSound) :
    classSetFreeProducerContract PayloadShape.selectedChain producerSound := by
  exact ⟨selectedChain_acceptable, h_sound⟩

theorem fullRelativeTable_contract_from_sound
    (producerSound : Prop)
    (h_sound : producerSound) :
    classSetFreeProducerContract PayloadShape.fullRelativeTable producerSound := by
  exact ⟨fullRelativeTable_acceptable, h_sound⟩

end P24.PhaseLiftedTowerPayloadGate
