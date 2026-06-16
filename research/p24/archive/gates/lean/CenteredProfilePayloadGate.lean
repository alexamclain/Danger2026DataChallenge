/-!
Finite payload accounting for the centered-profile mixed-rank route.

The arithmetic input is still a p-unit theorem for the actual p24 centered
Hermitian marginal.  This file only checks the finite sizes of the verifier
surfaces that would follow from such a theorem.
-/

namespace P24.CenteredProfilePayloadGate

def p24SqrtFloor : Nat := 1000000000000
def p24LeftDim : Nat := 156
def p24RightNonzero : Nat := 210
def p24RightFull : Nat := 211
def p24RightOrbitCount : Nat := 7

def centeredMatrixEntries : Nat := p24LeftDim * p24RightNonzero
def leadingMinorEntries : Nat := p24LeftDim * p24LeftDim
def explicitMatrixRankWitnessEntries : Nat :=
  centeredMatrixEntries + leadingMinorEntries
def determinantScalarPayload : Nat := 2
def rightPointwiseProductPayload : Nat := 2 * p24RightFull
def rightOrbitNormPayload : Nat := 2 * p24RightOrbitCount

theorem centeredMatrixEntries_value :
    centeredMatrixEntries = 32760 := by
  decide

theorem leadingMinorEntries_value :
    leadingMinorEntries = 24336 := by
  decide

theorem explicitMatrixRankWitnessEntries_value :
    explicitMatrixRankWitnessEntries = 57096 := by
  decide

theorem determinantScalarPayload_value :
    determinantScalarPayload = 2 := by
  decide

theorem rightPointwiseProductPayload_value :
    rightPointwiseProductPayload = 422 := by
  decide

theorem rightOrbitNormPayload_value :
    rightOrbitNormPayload = 14 := by
  decide

theorem centeredMatrixEntries_subsqrt :
    centeredMatrixEntries < p24SqrtFloor := by
  decide

theorem leadingMinorEntries_subsqrt :
    leadingMinorEntries < p24SqrtFloor := by
  decide

theorem explicitMatrixRankWitnessEntries_subsqrt :
    explicitMatrixRankWitnessEntries < p24SqrtFloor := by
  decide

theorem determinantScalarPayload_subsqrt :
    determinantScalarPayload < p24SqrtFloor := by
  decide

theorem rightPointwiseProductPayload_subsqrt :
    rightPointwiseProductPayload < p24SqrtFloor := by
  decide

theorem rightOrbitNormPayload_subsqrt :
    rightOrbitNormPayload < p24SqrtFloor := by
  decide

theorem determinantPayload_lt_pointwisePayload :
    determinantScalarPayload < rightPointwiseProductPayload := by
  decide

theorem rightOrbitNormPayload_lt_pointwisePayload :
    rightOrbitNormPayload < rightPointwiseProductPayload := by
  decide

theorem explicitMatrixWitness_lt_selectedChain :
    explicitMatrixRankWitnessEntries < 3107811 := by
  decide

end P24.CenteredProfilePayloadGate
