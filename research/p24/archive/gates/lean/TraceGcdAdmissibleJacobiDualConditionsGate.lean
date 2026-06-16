/-!
Finite handoff gate for the p24 admissible Jacobi dual Fourier target.

The arithmetic input remains external:

  for each nontrivial right projector of the selected weighted CM/Lang packet,
  after B/C trace, its Fourier coefficients on C_7 x C_179 satisfy the four
  dual condition families recorded in
  `trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate.md`.

This file checks only the formal implication:

  four dual Fourier families
  => admissible C-axis Jacobi span
  => no forbidden bidegrees
  => final internal trace zero
  => matching right coboundary
  => product coboundary
  => 1092 H-coset verifier equations.

It also records the corrected p24 count:

  6 + 6*89 + 89 + 3 = 632 equations,
  7*179 - 632 = 621 admissible dimensions.
-/

namespace P24.TraceGcdAdmissibleJacobiDualConditionsGate

structure DualFourierFamilies where
  forbiddenCTrivialVanishes : Prop
  conjugatePairSkew : Prop
  rightTrivialPairSumsNormalized : Prop
  globalPairBalances : Prop

def SatisfiesFourDualFamilies (families : DualFourierFamilies) : Prop :=
  families.forbiddenCTrivialVanishes ∧
  families.conjugatePairSkew ∧
  families.rightTrivialPairSumsNormalized ∧
  families.globalPairBalances

def AllFourDualFamilies {Character : Type}
    (families : Character → DualFourierFamilies) : Prop :=
  ∀ chi, SatisfiesFourDualFamilies (families chi)

def AllAdmissibleDecomposed {Character : Type}
    (inAdmissibleSpan : Character → Prop) : Prop :=
  ∀ chi, inAdmissibleSpan chi

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

theorem admissible_decomposition_from_four_dual_families
    {Character : Type}
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan : Character → Prop)
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
    (h_four : AllFourDualFamilies families) :
    AllAdmissibleDecomposed inAdmissibleSpan := by
  intro chi
  exact h_dual_complete chi (h_four chi)

theorem forbidden_from_four_dual_families
    {Character : Type}
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero : Character → Prop)
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
    (h_admissible_support :
      ∀ chi, inAdmissibleSpan chi → forbiddenBidegreeZero chi)
    (h_four : AllFourDualFamilies families) :
    AllForbiddenBidegreesZero forbiddenBidegreeZero := by
  intro chi
  exact h_admissible_support chi
    (h_dual_complete chi (h_four chi))

theorem final_trace_from_four_dual_families
    {Character : Type}
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero : Character → Prop)
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
    (h_admissible_support :
      ∀ chi, inAdmissibleSpan chi → forbiddenBidegreeZero chi)
    (h_final :
      ∀ chi, forbiddenBidegreeZero chi → finalTraceZero chi)
    (h_four : AllFourDualFamilies families) :
    AllProjectorInternalTraceZero finalTraceZero := by
  intro chi
  exact h_final chi
    (h_admissible_support chi
      (h_dual_complete chi (h_four chi)))

theorem character_payload_from_four_dual_families
    {Character Row : Type}
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
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
    (h_four : AllFourDualFamilies families) :
    AllCharacterPayloadZero characterZero := by
  intro chi row
  exact h_character chi row
    (h_product chi row
      (h_right chi
        (h_final chi
          (h_admissible_support chi
            (h_dual_complete chi (h_four chi))))))

theorem hcoset_verifier_from_four_dual_families
    {Character Row Coset : Type}
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
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
    (h_four : AllFourDualFamilies families)
    (h_centered : AllRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact h_hcoset h_centered
    (character_payload_from_four_dual_families
      families inAdmissibleSpan forbiddenBidegreeZero finalTraceZero
      rightCoboundary productCoboundary characterZero h_dual_complete
      h_admissible_support h_final h_right h_product h_character h_four)

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def p24ConjugateCPairCount : Nat := 89
def p24ForbiddenCTrivialCount : Nat := 6
def p24ConjugateSkewCount : Nat := 6 * p24ConjugateCPairCount
def p24RightTrivialPairSumCount : Nat := p24ConjugateCPairCount
def p24GlobalPairBalanceCount : Nat := 3
def p24DualConditionCount : Nat := 632
def p24FourierAmbientDim : Nat := 1253
def p24DualSolutionDim : Nat := 621
def p24AdmissibleCaxisCarryRank : Nat := 621
def p24LeftRows : Nat := 156
def p24RightHCosets : Nat := 7
def p24NontrivialRightCharacters : Nat := 6

theorem p24_conjugate_c_pair_count :
    (p24COverEDegree - 1) / 2 = p24ConjugateCPairCount := by
  decide

theorem p24_fourier_ambient_dim_formula :
    p24RightQuotientDegree * p24COverEDegree = p24FourierAmbientDim := by
  decide

theorem p24_dual_condition_count_formula :
    p24ForbiddenCTrivialCount + p24ConjugateSkewCount +
      p24RightTrivialPairSumCount + p24GlobalPairBalanceCount =
        p24DualConditionCount := by
  decide

theorem p24_dual_condition_count_expanded :
    6 + 6 * 89 + 89 + 3 = p24DualConditionCount := by
  decide

theorem p24_dual_solution_dim_formula :
    p24FourierAmbientDim - p24DualConditionCount = p24DualSolutionDim := by
  decide

theorem p24_dual_solution_dim_matches_admissible_rank :
    p24DualSolutionDim = p24AdmissibleCaxisCarryRank := by
  decide

theorem p24_dual_rank_formula :
    p24RightQuotientDegree * p24COverEDegree -
      (6 + 6 * p24ConjugateCPairCount + p24ConjugateCPairCount + 3) =
        p24AdmissibleCaxisCarryRank := by
  decide

theorem p24_hcoset_verifier_count :
    p24RightHCosets * p24LeftRows = 1092 := by
  decide

theorem p24_centering_plus_nontrivial_character_count :
    p24LeftRows + p24NontrivialRightCharacters * p24LeftRows = 1092 := by
  decide

theorem p24_dual_conditions_subsqrt :
    p24DualConditionCount < 1000000000000 := by
  decide

theorem p24_hcoset_verifier_subsqrt :
    p24RightHCosets * p24LeftRows < 1000000000000 := by
  decide

end P24.TraceGcdAdmissibleJacobiDualConditionsGate
