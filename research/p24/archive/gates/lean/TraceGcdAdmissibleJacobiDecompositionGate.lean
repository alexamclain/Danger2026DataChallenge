/-!
Finite handoff gate for the p24 admissible Jacobi-carry theorem.

The arithmetic input remains external:

  each nontrivial right projector of the selected weighted CM/Lang packet,
  after B/C trace, lies in the admissible C-axis Jacobi-carry span.

This file checks only the formal implication into the existing verifier
pipeline.  It also records the corrected rank bookkeeping: the termwise-safe
admissible span has p24 rank 621, while the broader C-axis family has rank
625 but includes leaky directions that require a separate cancellation input.
-/

namespace P24.TraceGcdAdmissibleJacobiDecompositionGate

def AllAdmissibleDecomposed {Character : Type}
    (inAdmissibleSpan : Character → Prop) : Prop :=
  ∀ chi, inAdmissibleSpan chi

def AllBroadDecomposedWithLeakCancellation {Character : Type}
    (inBroadSpan leakCancelled : Character → Prop) : Prop :=
  ∀ chi, inBroadSpan chi ∧ leakCancelled chi

def AllForbiddenBidegreesZero {Character : Type}
    (forbiddenBidegreeZero : Character → Prop) : Prop :=
  ∀ chi, forbiddenBidegreeZero chi

def AllProjectorInternalTraceZero {Character : Type}
    (finalTraceZero : Character → Prop) : Prop :=
  ∀ chi, finalTraceZero chi

def AllRowsCentered {Row : Type}
    (centered : Row → Prop) : Prop :=
  ∀ row, centered row

def AllCharacterPayloadZero {Character Row : Type}
    (characterZero : Character → Row → Prop) : Prop :=
  ∀ chi row, characterZero chi row

def AllHCosetSumsZero {Row Coset : Type}
    (hcosetZero : Row → Coset → Prop) : Prop :=
  ∀ row coset, hcosetZero row coset

theorem forbidden_from_admissible_decomposition
    {Character : Type}
    (inAdmissibleSpan forbiddenBidegreeZero : Character → Prop)
    (h_admissible_support :
      ∀ chi, inAdmissibleSpan chi → forbiddenBidegreeZero chi)
    (h_decomposition : AllAdmissibleDecomposed inAdmissibleSpan) :
    AllForbiddenBidegreesZero forbiddenBidegreeZero := by
  intro chi
  exact h_admissible_support chi (h_decomposition chi)

theorem forbidden_from_broad_decomposition_with_leak_cancellation
    {Character : Type}
    (inBroadSpan leakCancelled forbiddenBidegreeZero : Character → Prop)
    (h_broad_support :
      ∀ chi, inBroadSpan chi → leakCancelled chi → forbiddenBidegreeZero chi)
    (h_decomposition :
      AllBroadDecomposedWithLeakCancellation inBroadSpan leakCancelled) :
    AllForbiddenBidegreesZero forbiddenBidegreeZero := by
  intro chi
  exact h_broad_support chi (h_decomposition chi).1 (h_decomposition chi).2

theorem final_trace_from_admissible_decomposition
    {Character : Type}
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero : Character → Prop)
    (h_admissible_support :
      ∀ chi, inAdmissibleSpan chi → forbiddenBidegreeZero chi)
    (h_final :
      ∀ chi, forbiddenBidegreeZero chi → finalTraceZero chi)
    (h_decomposition : AllAdmissibleDecomposed inAdmissibleSpan) :
    AllProjectorInternalTraceZero finalTraceZero := by
  intro chi
  exact h_final chi
    (h_admissible_support chi (h_decomposition chi))

theorem character_payload_from_admissible_decomposition
    {Character Row : Type}
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (h_admissible_support :
      ∀ chi, inAdmissibleSpan chi → forbiddenBidegreeZero chi)
    (h_final :
      ∀ chi, forbiddenBidegreeZero chi → finalTraceZero chi)
    (h_right :
      ∀ chi, finalTraceZero chi → rightCoboundary chi)
    (h_product :
      ∀ chi row, rightCoboundary chi → productCoboundary chi row)
    (h_character :
      ∀ chi row, productCoboundary chi row → characterZero chi row)
    (h_decomposition : AllAdmissibleDecomposed inAdmissibleSpan) :
    AllCharacterPayloadZero characterZero := by
  intro chi row
  exact h_character chi row
    (h_product chi row
      (h_right chi
        (h_final chi
          (h_admissible_support chi (h_decomposition chi)))))

theorem hcoset_verifier_from_admissible_decomposition
    {Character Row Coset : Type}
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (h_admissible_support :
      ∀ chi, inAdmissibleSpan chi → forbiddenBidegreeZero chi)
    (h_final :
      ∀ chi, forbiddenBidegreeZero chi → finalTraceZero chi)
    (h_right :
      ∀ chi, finalTraceZero chi → rightCoboundary chi)
    (h_product :
      ∀ chi row, rightCoboundary chi → productCoboundary chi row)
    (h_character :
      ∀ chi row, productCoboundary chi row → characterZero chi row)
    (h_hcoset :
      AllRowsCentered centered →
      AllCharacterPayloadZero characterZero →
      AllHCosetSumsZero hcosetZero)
    (h_decomposition : AllAdmissibleDecomposed inAdmissibleSpan)
    (h_centered : AllRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact h_hcoset h_centered
    (character_payload_from_admissible_decomposition
      inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary
      productCoboundary characterZero h_admissible_support h_final
      h_right h_product h_character h_decomposition)

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def p24AdmissibleCaxisCarryRank : Nat := 621
def p24BroadCaxisCarryRank : Nat := 625
def p24NoForbiddenBidegreeDim : Nat := 1247
def p24OriginNormalizedNoForbiddenDim : Nat := 1246
def p24ConjugateCPairCount : Nat := 89
def p24LeftRows : Nat := 156
def p24RightHCosets : Nat := 7
def p24NontrivialRightCharacters : Nat := 6

theorem p24_admissible_rank_formula :
    p24RightQuotientDegree * ((p24COverEDegree - 1) / 2) - 2 =
      p24AdmissibleCaxisCarryRank := by
  decide

theorem p24_broad_rank_formula :
    p24RightQuotientDegree * ((p24COverEDegree - 1) / 2) + 2 =
      p24BroadCaxisCarryRank := by
  decide

theorem p24_broad_minus_admissible_rank :
    p24BroadCaxisCarryRank - p24AdmissibleCaxisCarryRank = 4 := by
  decide

theorem p24_conjugate_c_pair_count :
    (p24COverEDegree - 1) / 2 = p24ConjugateCPairCount := by
  decide

theorem p24_admissible_spectral_rank_formula :
    1 + p24RightQuotientDegree * (p24ConjugateCPairCount - 1) + 4 =
      p24AdmissibleCaxisCarryRank := by
  decide

theorem p24_admissible_span_strictly_smaller_than_no_forbidden :
    p24AdmissibleCaxisCarryRank < p24OriginNormalizedNoForbiddenDim := by
  decide

theorem p24_hcoset_verifier_count :
    p24RightHCosets * p24LeftRows = 1092 := by
  decide

theorem p24_centering_plus_nontrivial_character_count :
    p24LeftRows + p24NontrivialRightCharacters * p24LeftRows = 1092 := by
  decide

theorem p24_hcoset_verifier_subsqrt :
    p24RightHCosets * p24LeftRows < 1000000000000 := by
  decide

end P24.TraceGcdAdmissibleJacobiDecompositionGate
