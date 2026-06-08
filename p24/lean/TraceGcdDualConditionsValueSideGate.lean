/-!
Finite handoff gate for the value-side form of the p24 dual Fourier target.

The arithmetic input remains external:

  after B/C trace, the selected weighted packet f on C_7 x C_179 has
  equal C-row sums, vanishes on the C-zero fiber, and has constant
  inversion-complement off that fiber.

The Python gate checks that these three value-side identities are equivalent
to the four dual Fourier families with lambda_179=-1/89.  This Lean file
records the formal handoff:

  value-side identities
  => four dual Fourier families
  => admissible span
  => verifier pipeline.
-/

namespace P24.TraceGcdDualConditionsValueSideGate

structure ValueSideIdentities where
  cRowSumsIndependent : Prop
  cZeroFiberVanishes : Prop
  inversionComplementConstantOffCZero : Prop

def SatisfiesValueSideIdentities (ids : ValueSideIdentities) : Prop :=
  ids.cRowSumsIndependent ∧
  ids.cZeroFiberVanishes ∧
  ids.inversionComplementConstantOffCZero

structure RobertProducerObligations where
  selectedDefectSubtraction : Prop
  degreeZeroAfterRightProjection : Prop
  inversionPairCompatibility : Prop

def SatisfiesRobertProducerObligations
    (obligations : RobertProducerObligations) : Prop :=
  obligations.selectedDefectSubtraction ∧
  obligations.degreeZeroAfterRightProjection ∧
  obligations.inversionPairCompatibility

def valueSideFromRobertProducer
    (obligations : RobertProducerObligations) : ValueSideIdentities where
  cRowSumsIndependent := obligations.degreeZeroAfterRightProjection
  cZeroFiberVanishes := obligations.selectedDefectSubtraction
  inversionComplementConstantOffCZero :=
    obligations.inversionPairCompatibility

structure ReducedJacobiCarryObligations where
  quotientCRowSumsIndependent : Prop
  quotientCZeroFiberVanishes : Prop
  quotientInversionComplementConstantOffCZero : Prop

def SatisfiesReducedJacobiCarryObligations
    (obligations : ReducedJacobiCarryObligations) : Prop :=
  obligations.quotientCRowSumsIndependent ∧
  obligations.quotientCZeroFiberVanishes ∧
  obligations.quotientInversionComplementConstantOffCZero

def valueSideFromReducedJacobiCarry
    (obligations : ReducedJacobiCarryObligations) : ValueSideIdentities where
  cRowSumsIndependent := obligations.quotientCRowSumsIndependent
  cZeroFiberVanishes := obligations.quotientCZeroFiberVanishes
  inversionComplementConstantOffCZero :=
    obligations.quotientInversionComplementConstantOffCZero

structure HeckeRatioLocalDataObligations where
  sameInfinityType : Prop
  sameFiniteLocalTypeOnKilledConductorPart : Prop
  killedLocalRayPartHasNoPostBCCharacterSupport : Prop
  ratioFactorsThroughUnramifiedPostBCQuotient : Prop

def SatisfiesHeckeRatioLocalDataObligations
    (obligations : HeckeRatioLocalDataObligations) : Prop :=
  obligations.sameInfinityType ∧
  obligations.sameFiniteLocalTypeOnKilledConductorPart ∧
  obligations.killedLocalRayPartHasNoPostBCCharacterSupport ∧
  obligations.ratioFactorsThroughUnramifiedPostBCQuotient

def ratioIsUnramifiedFiniteOrderFromLocalData
    (obligations : HeckeRatioLocalDataObligations) : Prop :=
  SatisfiesHeckeRatioLocalDataObligations obligations

structure HeckeRatioAxisValueObligations where
  ratioMatchesRightAxisSelector : Prop
  ratioMatchesCAxisSelector : Prop

def SatisfiesHeckeRatioAxisValueObligations
    (obligations : HeckeRatioAxisValueObligations) : Prop :=
  obligations.ratioMatchesRightAxisSelector ∧
  obligations.ratioMatchesCAxisSelector

def ratioMatchesSelectorOnRhoFromAxisValues
    (obligations : HeckeRatioAxisValueObligations) : Prop :=
  SatisfiesHeckeRatioAxisValueObligations obligations

structure HeckeRatioArtinCoordinateObligations where
  postBCQuotientGeneratedByRho : Prop
  localDataMakesRatioUnramifiedFiniteOrder :
    HeckeRatioLocalDataObligations
  axisValuesDetermineRatioOnRho : HeckeRatioAxisValueObligations

def SatisfiesHeckeRatioArtinCoordinateObligations
    (obligations : HeckeRatioArtinCoordinateObligations) : Prop :=
  obligations.postBCQuotientGeneratedByRho ∧
  ratioIsUnramifiedFiniteOrderFromLocalData
    obligations.localDataMakesRatioUnramifiedFiniteOrder ∧
  ratioMatchesSelectorOnRhoFromAxisValues
    obligations.axisValuesDetermineRatioOnRho

theorem hecke_ratio_unramified_finite_order_from_local_data
    (obligations : HeckeRatioLocalDataObligations)
    (h_local : SatisfiesHeckeRatioLocalDataObligations obligations) :
    ratioIsUnramifiedFiniteOrderFromLocalData obligations := by
  exact h_local

theorem ratio_matches_selector_on_rho_from_axis_values
    (obligations : HeckeRatioAxisValueObligations)
    (h_axis : SatisfiesHeckeRatioAxisValueObligations obligations) :
    ratioMatchesSelectorOnRhoFromAxisValues obligations := by
  exact h_axis

structure UnramifiedTwistedJacobiProducerObligations where
  unramifiedTwistSelectsPostBCQuotient : Prop
  heckeRatioGivesArtinCoordinatePullback :
    HeckeRatioArtinCoordinateObligations
  selectedTraceGcdEqualsTwistedJacobiPacket : Prop
  twistedReducedCarry : ReducedJacobiCarryObligations

def SatisfiesUnramifiedTwistedJacobiProducerObligations
    (obligations : UnramifiedTwistedJacobiProducerObligations) : Prop :=
  obligations.unramifiedTwistSelectsPostBCQuotient ∧
  SatisfiesHeckeRatioArtinCoordinateObligations
    obligations.heckeRatioGivesArtinCoordinatePullback ∧
  obligations.selectedTraceGcdEqualsTwistedJacobiPacket ∧
  SatisfiesReducedJacobiCarryObligations obligations.twistedReducedCarry

def reducedJacobiCarryFromUnramifiedTwistedJacobi
    (obligations : UnramifiedTwistedJacobiProducerObligations) :
    ReducedJacobiCarryObligations :=
  obligations.twistedReducedCarry

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

def AllValueSideIdentities {Character : Type}
    (ids : Character → ValueSideIdentities) : Prop :=
  ∀ chi, SatisfiesValueSideIdentities (ids chi)

def AllRobertProducerObligations {Character : Type}
    (obligations : Character → RobertProducerObligations) : Prop :=
  ∀ chi, SatisfiesRobertProducerObligations (obligations chi)

def AllReducedJacobiCarryObligations {Character : Type}
    (obligations : Character → ReducedJacobiCarryObligations) : Prop :=
  ∀ chi, SatisfiesReducedJacobiCarryObligations (obligations chi)

def AllUnramifiedTwistedJacobiProducerObligations {Character : Type}
    (obligations :
      Character → UnramifiedTwistedJacobiProducerObligations) : Prop :=
  ∀ chi, SatisfiesUnramifiedTwistedJacobiProducerObligations
    (obligations chi)

def AllFourDualFamilies {Character : Type}
    (families : Character → DualFourierFamilies) : Prop :=
  ∀ chi, SatisfiesFourDualFamilies (families chi)

def AllAdmissibleDecomposed {Character : Type}
    (inAdmissibleSpan : Character → Prop) : Prop :=
  ∀ chi, inAdmissibleSpan chi

def AllHCosetSumsZero {Row Coset : Type}
    (hcosetZero : Row → Coset → Prop) : Prop :=
  ∀ row coset, hcosetZero row coset

theorem value_side_from_robert_producer_obligations
    {Character : Type}
    (obligations : Character → RobertProducerObligations)
    (h_robert : AllRobertProducerObligations obligations) :
    AllValueSideIdentities
      (fun chi => valueSideFromRobertProducer (obligations chi)) := by
  intro chi
  rcases h_robert chi with ⟨h_selected, h_degree_zero, h_inversion⟩
  exact ⟨h_degree_zero, h_selected, h_inversion⟩

theorem value_side_from_reduced_jacobi_carry_obligations
    {Character : Type}
    (obligations : Character → ReducedJacobiCarryObligations)
    (h_carry : AllReducedJacobiCarryObligations obligations) :
    AllValueSideIdentities
      (fun chi => valueSideFromReducedJacobiCarry (obligations chi)) := by
  intro chi
  rcases h_carry chi with ⟨h_rows, h_zero, h_inversion⟩
  exact ⟨h_rows, h_zero, h_inversion⟩

theorem reduced_jacobi_carry_from_unramified_twisted_jacobi_obligations
    {Character : Type}
    (obligations :
      Character → UnramifiedTwistedJacobiProducerObligations)
    (h_twisted : AllUnramifiedTwistedJacobiProducerObligations obligations) :
    AllReducedJacobiCarryObligations
      (fun chi =>
        reducedJacobiCarryFromUnramifiedTwistedJacobi (obligations chi)) := by
  intro chi
  rcases h_twisted chi with
    ⟨_h_selector, _h_ratio, _h_identification, h_carry⟩
  exact h_carry

theorem value_side_from_unramified_twisted_jacobi_obligations
    {Character : Type}
    (obligations :
      Character → UnramifiedTwistedJacobiProducerObligations)
    (h_twisted : AllUnramifiedTwistedJacobiProducerObligations obligations) :
    AllValueSideIdentities
      (fun chi =>
        valueSideFromReducedJacobiCarry
          (reducedJacobiCarryFromUnramifiedTwistedJacobi
            (obligations chi))) := by
  exact value_side_from_reduced_jacobi_carry_obligations
    (fun chi =>
      reducedJacobiCarryFromUnramifiedTwistedJacobi (obligations chi))
    (reduced_jacobi_carry_from_unramified_twisted_jacobi_obligations
      obligations h_twisted)

theorem four_dual_families_from_value_side_identities
    {Character : Type}
    (ids : Character → ValueSideIdentities)
    (families : Character → DualFourierFamilies)
    (h_value_to_dual :
      ∀ chi, SatisfiesValueSideIdentities (ids chi) →
        SatisfiesFourDualFamilies (families chi))
    (h_value : AllValueSideIdentities ids) :
    AllFourDualFamilies families := by
  intro chi
  exact h_value_to_dual chi (h_value chi)

theorem four_dual_families_from_robert_producer_obligations
    {Character : Type}
    (obligations : Character → RobertProducerObligations)
    (families : Character → DualFourierFamilies)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromRobertProducer (obligations chi)) →
        SatisfiesFourDualFamilies (families chi))
    (h_robert : AllRobertProducerObligations obligations) :
    AllFourDualFamilies families := by
  exact four_dual_families_from_value_side_identities
    (fun chi => valueSideFromRobertProducer (obligations chi))
    families h_value_to_dual
    (value_side_from_robert_producer_obligations obligations h_robert)

theorem four_dual_families_from_reduced_jacobi_carry_obligations
    {Character : Type}
    (obligations : Character → ReducedJacobiCarryObligations)
    (families : Character → DualFourierFamilies)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromReducedJacobiCarry (obligations chi)) →
        SatisfiesFourDualFamilies (families chi))
    (h_carry : AllReducedJacobiCarryObligations obligations) :
    AllFourDualFamilies families := by
  exact four_dual_families_from_value_side_identities
    (fun chi => valueSideFromReducedJacobiCarry (obligations chi))
    families h_value_to_dual
    (value_side_from_reduced_jacobi_carry_obligations obligations h_carry)

theorem four_dual_families_from_unramified_twisted_jacobi_obligations
    {Character : Type}
    (obligations :
      Character → UnramifiedTwistedJacobiProducerObligations)
    (families : Character → DualFourierFamilies)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromReducedJacobiCarry
            (reducedJacobiCarryFromUnramifiedTwistedJacobi
              (obligations chi))) →
        SatisfiesFourDualFamilies (families chi))
    (h_twisted : AllUnramifiedTwistedJacobiProducerObligations obligations) :
    AllFourDualFamilies families := by
  exact four_dual_families_from_value_side_identities
    (fun chi =>
      valueSideFromReducedJacobiCarry
        (reducedJacobiCarryFromUnramifiedTwistedJacobi (obligations chi)))
    families h_value_to_dual
    (value_side_from_unramified_twisted_jacobi_obligations
      obligations h_twisted)

theorem admissible_decomposition_from_value_side_identities
    {Character : Type}
    (ids : Character → ValueSideIdentities)
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan : Character → Prop)
    (h_value_to_dual :
      ∀ chi, SatisfiesValueSideIdentities (ids chi) →
        SatisfiesFourDualFamilies (families chi))
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
    (h_value : AllValueSideIdentities ids) :
    AllAdmissibleDecomposed inAdmissibleSpan := by
  intro chi
  exact h_dual_complete chi (h_value_to_dual chi (h_value chi))

theorem admissible_decomposition_from_robert_producer_obligations
    {Character : Type}
    (obligations : Character → RobertProducerObligations)
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan : Character → Prop)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromRobertProducer (obligations chi)) →
        SatisfiesFourDualFamilies (families chi))
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
    (h_robert : AllRobertProducerObligations obligations) :
    AllAdmissibleDecomposed inAdmissibleSpan := by
  intro chi
  exact h_dual_complete chi
    (h_value_to_dual chi
      ((value_side_from_robert_producer_obligations obligations h_robert) chi))

theorem admissible_decomposition_from_reduced_jacobi_carry_obligations
    {Character : Type}
    (obligations : Character → ReducedJacobiCarryObligations)
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan : Character → Prop)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromReducedJacobiCarry (obligations chi)) →
        SatisfiesFourDualFamilies (families chi))
    (h_dual_complete :
      ∀ chi, SatisfiesFourDualFamilies (families chi) →
        inAdmissibleSpan chi)
    (h_carry : AllReducedJacobiCarryObligations obligations) :
    AllAdmissibleDecomposed inAdmissibleSpan := by
  intro chi
  exact h_dual_complete chi
    (h_value_to_dual chi
      ((value_side_from_reduced_jacobi_carry_obligations obligations h_carry) chi))

theorem hcoset_verifier_from_value_side_identities
    {Character Row Coset : Type}
    (ids : Character → ValueSideIdentities)
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (allRowsCentered : (Row → Prop) → Prop)
    (allCharacterPayloadZero : (Character → Row → Prop) → Prop)
    (h_value_to_dual :
      ∀ chi, SatisfiesValueSideIdentities (ids chi) →
        SatisfiesFourDualFamilies (families chi))
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
    (h_character_collect :
      (∀ chi row, characterZero chi row) →
        allCharacterPayloadZero characterZero)
    (h_hcoset :
      allRowsCentered centered →
      allCharacterPayloadZero characterZero →
      AllHCosetSumsZero hcosetZero)
    (h_value : AllValueSideIdentities ids)
    (h_centered : allRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  apply h_hcoset h_centered
  apply h_character_collect
  intro chi row
  exact h_character chi row
    (h_product chi row
      (h_right chi
        (h_final chi
          (h_admissible_support chi
            (h_dual_complete chi
              (h_value_to_dual chi (h_value chi)))))))

theorem hcoset_verifier_from_robert_producer_obligations
    {Character Row Coset : Type}
    (obligations : Character → RobertProducerObligations)
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (allRowsCentered : (Row → Prop) → Prop)
    (allCharacterPayloadZero : (Character → Row → Prop) → Prop)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromRobertProducer (obligations chi)) →
        SatisfiesFourDualFamilies (families chi))
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
    (h_character_collect :
      (∀ chi row, characterZero chi row) →
        allCharacterPayloadZero characterZero)
    (h_hcoset :
      allRowsCentered centered →
      allCharacterPayloadZero characterZero →
      AllHCosetSumsZero hcosetZero)
    (h_robert : AllRobertProducerObligations obligations)
    (h_centered : allRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact hcoset_verifier_from_value_side_identities
    (fun chi => valueSideFromRobertProducer (obligations chi))
    families inAdmissibleSpan forbiddenBidegreeZero finalTraceZero
    rightCoboundary productCoboundary characterZero centered hcosetZero
    allRowsCentered allCharacterPayloadZero h_value_to_dual h_dual_complete
    h_admissible_support h_final h_right h_product h_character
    h_character_collect h_hcoset
    (value_side_from_robert_producer_obligations obligations h_robert)
    h_centered

theorem hcoset_verifier_from_reduced_jacobi_carry_obligations
    {Character Row Coset : Type}
    (obligations : Character → ReducedJacobiCarryObligations)
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (allRowsCentered : (Row → Prop) → Prop)
    (allCharacterPayloadZero : (Character → Row → Prop) → Prop)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromReducedJacobiCarry (obligations chi)) →
        SatisfiesFourDualFamilies (families chi))
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
    (h_character_collect :
      (∀ chi row, characterZero chi row) →
        allCharacterPayloadZero characterZero)
    (h_hcoset :
      allRowsCentered centered →
      allCharacterPayloadZero characterZero →
      AllHCosetSumsZero hcosetZero)
    (h_carry : AllReducedJacobiCarryObligations obligations)
    (h_centered : allRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact hcoset_verifier_from_value_side_identities
    (fun chi => valueSideFromReducedJacobiCarry (obligations chi))
    families inAdmissibleSpan forbiddenBidegreeZero finalTraceZero
    rightCoboundary productCoboundary characterZero centered hcosetZero
    allRowsCentered allCharacterPayloadZero h_value_to_dual h_dual_complete
    h_admissible_support h_final h_right h_product h_character
    h_character_collect h_hcoset
    (value_side_from_reduced_jacobi_carry_obligations obligations h_carry)
    h_centered

theorem hcoset_verifier_from_unramified_twisted_jacobi_obligations
    {Character Row Coset : Type}
    (obligations :
      Character → UnramifiedTwistedJacobiProducerObligations)
    (families : Character → DualFourierFamilies)
    (inAdmissibleSpan forbiddenBidegreeZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (allRowsCentered : (Row → Prop) → Prop)
    (allCharacterPayloadZero : (Character → Row → Prop) → Prop)
    (h_value_to_dual :
      ∀ chi,
        SatisfiesValueSideIdentities
          (valueSideFromReducedJacobiCarry
            (reducedJacobiCarryFromUnramifiedTwistedJacobi
              (obligations chi))) →
        SatisfiesFourDualFamilies (families chi))
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
    (h_character_collect :
      (∀ chi row, characterZero chi row) →
        allCharacterPayloadZero characterZero)
    (h_hcoset :
      allRowsCentered centered →
      allCharacterPayloadZero characterZero →
      AllHCosetSumsZero hcosetZero)
    (h_twisted : AllUnramifiedTwistedJacobiProducerObligations obligations)
    (h_centered : allRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact hcoset_verifier_from_value_side_identities
    (fun chi =>
      valueSideFromReducedJacobiCarry
        (reducedJacobiCarryFromUnramifiedTwistedJacobi (obligations chi)))
    families inAdmissibleSpan forbiddenBidegreeZero finalTraceZero
    rightCoboundary productCoboundary characterZero centered hcosetZero
    allRowsCentered allCharacterPayloadZero h_value_to_dual h_dual_complete
    h_admissible_support h_final h_right h_product h_character
    h_character_collect h_hcoset
    (value_side_from_unramified_twisted_jacobi_obligations
      obligations h_twisted)
    h_centered

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def p24ConjugateCPairCount : Nat := 89
def p24DualConditionCount : Nat := 632
def p24FourierAmbientDim : Nat := 1253
def p24AdmissibleCaxisCarryRank : Nat := 621
def p24RightMixedReducedJacobiPairs : Nat :=
  (p24RightQuotientDegree - 1) *
    (p24COverEDegree - 1) * (p24COverEDegree - 2)
def p24LeftRows : Nat := 156
def p24RightHCosets : Nat := 7
def p24NontrivialRightCharacters : Nat := 6

theorem p24_value_side_lambda_numerator_denominator :
    2 * 89 = p24COverEDegree - 1 := by
  decide

theorem p24_dual_condition_count_expanded :
    6 + 6 * p24ConjugateCPairCount + p24ConjugateCPairCount + 3 =
      p24DualConditionCount := by
  decide

theorem p24_dual_solution_dim_matches_admissible_rank :
    p24FourierAmbientDim - p24DualConditionCount =
      p24AdmissibleCaxisCarryRank := by
  decide

theorem p24_right_mixed_reduced_jacobi_pair_count :
    p24RightMixedReducedJacobiPairs = 189036 := by
  decide

theorem p24_hcoset_verifier_count :
    p24RightHCosets * p24LeftRows = 1092 := by
  decide

theorem p24_centering_plus_nontrivial_character_count :
    p24LeftRows + p24NontrivialRightCharacters * p24LeftRows = 1092 := by
  decide

end P24.TraceGcdDualConditionsValueSideGate
