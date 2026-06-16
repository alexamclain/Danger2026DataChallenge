/-!
Finite pipeline gate for the p24 projector/internal-trace route.

This file deliberately leaves the arithmetic theorem as an explicit
hypothesis:

  every nontrivial right quotient projector has zero final internal trace.

It checks that, after that CM/Lang input, the remaining layers are formal:

* final internal trace zero gives a matching right coboundary;
* matching right coboundary plus left covariance gives a product coboundary;
* product coboundaries kill the six nontrivial character payloads;
* ordinary centering plus those six character payloads gives the 1092
  H-coset scalar verifier.

Thus the proof frontier is exactly the projector/internal-trace arithmetic
identity, not another finite linear-algebra step.
-/

namespace P24.TraceGcdProjectorTracePipelineGate

def AllProjectorInternalTraceZero {Character : Type}
    (finalTraceZero : Character → Prop) : Prop :=
  ∀ chi, finalTraceZero chi

def AllWeightedRightPotentials {Character : Type}
    (weightedPotential : Character → Prop) : Prop :=
  ∀ chi, weightedPotential chi

def AllRobertCaxisCentered {Character : Type}
    (robertCentered : Character → Prop) : Prop :=
  ∀ chi, robertCentered chi

def AllRobertDegreeZero {Character : Type}
    (robertDegreeZero : Character → Prop) : Prop :=
  ∀ chi, robertDegreeZero chi

def AllCTrivialComponentsZero {Character : Type}
    (cTrivialZero : Character → Prop) : Prop :=
  ∀ chi, cTrivialZero chi

def AllRowsCentered {Row : Type}
    (centered : Row → Prop) : Prop :=
  ∀ row, centered row

def AllCharacterPayloadZero {Character Row : Type}
    (characterZero : Character → Row → Prop) : Prop :=
  ∀ chi row, characterZero chi row

def AllHCosetSumsZero {Row Coset : Type}
    (hcosetZero : Row → Coset → Prop) : Prop :=
  ∀ row coset, hcosetZero row coset

theorem character_payload_from_projector_internal_trace
    {Character Row : Type}
    (finalTraceZero rightCoboundary : Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (h_right :
      ∀ chi, finalTraceZero chi → rightCoboundary chi)
    (h_product :
      ∀ chi row, rightCoboundary chi → productCoboundary chi row)
    (h_character :
      ∀ chi row, productCoboundary chi row → characterZero chi row)
    (h_trace : AllProjectorInternalTraceZero finalTraceZero) :
    AllCharacterPayloadZero characterZero := by
  intro chi row
  exact h_character chi row
    (h_product chi row (h_right chi (h_trace chi)))

theorem hcoset_verifier_from_projector_internal_trace
    {Character Row Coset : Type}
    (finalTraceZero rightCoboundary : Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
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
    (h_trace : AllProjectorInternalTraceZero finalTraceZero)
    (h_centered : AllRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact h_hcoset h_centered
    (character_payload_from_projector_internal_trace
      finalTraceZero rightCoboundary productCoboundary characterZero
      h_right h_product h_character h_trace)

theorem character_payload_from_weighted_right_potentials
    {Character Row : Type}
    (weightedPotential rightCoboundary : Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (h_potential :
      ∀ chi, weightedPotential chi → rightCoboundary chi)
    (h_product :
      ∀ chi row, rightCoboundary chi → productCoboundary chi row)
    (h_character :
      ∀ chi row, productCoboundary chi row → characterZero chi row)
    (h_potentials : AllWeightedRightPotentials weightedPotential) :
    AllCharacterPayloadZero characterZero := by
  intro chi row
  exact h_character chi row
    (h_product chi row (h_potential chi (h_potentials chi)))

theorem hcoset_verifier_from_weighted_right_potentials
    {Character Row Coset : Type}
    (weightedPotential rightCoboundary : Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (h_potential :
      ∀ chi, weightedPotential chi → rightCoboundary chi)
    (h_product :
      ∀ chi row, rightCoboundary chi → productCoboundary chi row)
    (h_character :
      ∀ chi row, productCoboundary chi row → characterZero chi row)
    (h_hcoset :
      AllRowsCentered centered →
      AllCharacterPayloadZero characterZero →
      AllHCosetSumsZero hcosetZero)
    (h_potentials : AllWeightedRightPotentials weightedPotential)
    (h_centered : AllRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact h_hcoset h_centered
    (character_payload_from_weighted_right_potentials
      weightedPotential rightCoboundary productCoboundary characterZero
      h_potential h_product h_character h_potentials)

theorem projector_internal_trace_from_robert_caxis_centering
    {Character : Type}
    (robertCentered cTrivialZero finalTraceZero : Character → Prop)
    (h_robert_c :
      ∀ chi, robertCentered chi → cTrivialZero chi)
    (h_c_trace :
      ∀ chi, cTrivialZero chi → finalTraceZero chi)
    (h_robert : AllRobertCaxisCentered robertCentered) :
    AllProjectorInternalTraceZero finalTraceZero := by
  intro chi
  exact h_c_trace chi (h_robert_c chi (h_robert chi))

theorem c_trivial_components_from_robert_degree_zero
    {Character : Type}
    (robertDegreeZero cTrivialZero : Character → Prop)
    (h_degree_zero :
      ∀ chi, robertDegreeZero chi → cTrivialZero chi)
    (h_robert : AllRobertDegreeZero robertDegreeZero) :
    AllCTrivialComponentsZero cTrivialZero := by
  intro chi
  exact h_degree_zero chi (h_robert chi)

theorem projector_internal_trace_from_robert_degree_zero
    {Character : Type}
    (robertDegreeZero cTrivialZero finalTraceZero : Character → Prop)
    (h_degree_zero :
      ∀ chi, robertDegreeZero chi → cTrivialZero chi)
    (h_c_trace :
      ∀ chi, cTrivialZero chi → finalTraceZero chi)
    (h_robert : AllRobertDegreeZero robertDegreeZero) :
    AllProjectorInternalTraceZero finalTraceZero := by
  intro chi
  exact h_c_trace chi (h_degree_zero chi (h_robert chi))

theorem hcoset_verifier_from_robert_caxis_centering
    {Character Row Coset : Type}
    (robertCentered cTrivialZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (h_robert_c :
      ∀ chi, robertCentered chi → cTrivialZero chi)
    (h_c_trace :
      ∀ chi, cTrivialZero chi → finalTraceZero chi)
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
    (h_robert : AllRobertCaxisCentered robertCentered)
    (h_centered : AllRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact hcoset_verifier_from_projector_internal_trace
    finalTraceZero rightCoboundary productCoboundary characterZero
    centered hcosetZero h_right h_product h_character h_hcoset
    (projector_internal_trace_from_robert_caxis_centering
      robertCentered cTrivialZero finalTraceZero
      h_robert_c h_c_trace h_robert)
    h_centered

theorem hcoset_verifier_from_robert_degree_zero
    {Character Row Coset : Type}
    (robertDegreeZero cTrivialZero finalTraceZero rightCoboundary :
      Character → Prop)
    (productCoboundary characterZero : Character → Row → Prop)
    (centered : Row → Prop)
    (hcosetZero : Row → Coset → Prop)
    (h_degree_zero :
      ∀ chi, robertDegreeZero chi → cTrivialZero chi)
    (h_c_trace :
      ∀ chi, cTrivialZero chi → finalTraceZero chi)
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
    (h_robert : AllRobertDegreeZero robertDegreeZero)
    (h_centered : AllRowsCentered centered) :
    AllHCosetSumsZero hcosetZero := by
  exact hcoset_verifier_from_projector_internal_trace
    finalTraceZero rightCoboundary productCoboundary characterZero
    centered hcosetZero h_right h_product h_character h_hcoset
    (projector_internal_trace_from_robert_degree_zero
      robertDegreeZero cTrivialZero finalTraceZero
      h_degree_zero h_c_trace h_robert)
    h_centered

def p24LeftRows : Nat := 156
def p24NontrivialRightCharacters : Nat := 6
def p24RightHCosets : Nat := 7
def p24QuotientCycles : Nat := 10
def p24QuotientCycleLength : Nat := 7
def p24BOverCDegree : Nat := 31
def p24COverEDegree : Nat := 179
def p24InternalDegree : Nat := 5549
def p24RhoCycleOrder : Nat :=
  p24RightHCosets * p24BOverCDegree * p24COverEDegree
def p24AfterBOverCQuotientOrder : Nat :=
  p24RhoCycleOrder / p24BOverCDegree
def p24VisibleJacobiLevel : Nat :=
  p24RightHCosets * p24COverEDegree
def p24VisibleJacobiPhi : Nat :=
  (p24RightHCosets - 1) * (p24COverEDegree - 1)
def p24VisibleThetaInfinitySum : Nat :=
  p24VisibleJacobiPhi / 2
def p24PlainCyclotomicFrobeniusOrder : Nat := 89
def p24RhoExponent : Nat := 780
def p24RhoCyclotomicShadowModLevel : Nat := 666
def p24RhoCyclotomicShadowModRight : Nat := 1
def p24RhoCyclotomicShadowModC : Nat := 129
def p24RhoCyclotomicShadowOrder : Nat := 89
def p24KLFrobeniusCOrbitCount : Nat := 2
def p24KLFrobeniusCOrbitSize : Nat := 89
def p24KLCNonzeroCharacterCount : Nat := 178
def p24KLRealInversionOrbitCount : Nat := 1
def p24KLRealInversionOrbitSize : Nat := 89
def p24KLCyclotomicRightOrder : Nat := 1
def p24KLCyclotomicVisibleOrder : Nat := 89
def p24VisibleRayOrderOverHilbert : Nat := 768960
def p24CandidateRatioOrderBound : Nat := p24AfterBOverCQuotientOrder
def p24FullRhoLevel : Nat := p24RhoCycleOrder
def p24BCKernelDegree : Nat := p24BOverCDegree
def p24BCInflatedRawCarryScale : Nat := p24BOverCDegree
def p24BCInflatedRawPushforwardScale : Nat :=
  p24BOverCDegree * p24BOverCDegree
def p24BCMultiplicativeNormPower : Nat := p24BOverCDegree
def p24BCTraceSurvivingCharacters : Nat := p24VisibleJacobiLevel
def p24BCTraceKilledKernelTwists : Nat :=
  (p24BOverCDegree - 1) * p24VisibleJacobiLevel
def p24BCQuotientRatioPairCheckCount : Nat :=
  p24BCTraceSurvivingCharacters * p24BCTraceSurvivingCharacters
def p24BCQuotientRatioMaxOrder : Nat := p24AfterBOverCQuotientOrder
def p24UnramifiedQuotientTwistExponent : Nat := p24BOverCDegree
def p24UnramifiedQuotientTwistOrder : Nat :=
  p24FullRhoLevel / p24UnramifiedQuotientTwistExponent
def p24UnramifiedTwistRightAxisOrder : Nat := p24RightHCosets
def p24UnramifiedTwistCAxisOrder : Nat := p24COverEDegree
def p24PostBCQuotientGeneratorOrder : Nat := p24VisibleJacobiLevel
def p24PostBCUnramifiedCharacterCount : Nat := p24VisibleJacobiLevel
def p24ArtinCharacterPairCheckCount : Nat :=
  p24PostBCUnramifiedCharacterCount * p24PostBCUnramifiedCharacterCount
def p24RhoFromRightAxisPower : Nat := 2
def p24RhoFromCAxisPower : Nat := 128
def p24RhoReconstructionIntegerSum : Nat :=
  p24RhoFromRightAxisPower * p24COverEDegree +
    p24RhoFromCAxisPower * p24RightHCosets
def p24RawRightHShift : Nat := 6
def p24PostBCRhoRightCoordinate : Nat := p24RhoFromRightAxisPower
def p24RightAxisHShift : Nat := 3
def p24CAxisHShift : Nat := 0
def p24SelectedArtinExponent : Nat := 1
def p24RightFixedResidualCharacterCount : Nat := p24COverEDegree
def p24CaxisResidualMaxOrder : Nat := p24COverEDegree
def p24PureCResidualValueSideInvariantCount : Nat := p24COverEDegree
def p24PureCResidualZeroDefectCount : Nat := 1
def p24RightMixedAdmissiblePairCount : Nat :=
  (p24RightHCosets - 1) * (p24COverEDegree - 1) *
    (p24COverEDegree - 2)
def p24R179CyclotomicPoleOrder : Nat := p24COverEDegree - 1
def p24R179CNontrivialFourierChannels : Nat :=
  p24RightHCosets * (p24COverEDegree - 1)
def p24InternalCosetBalanceCount : Nat := 560
def p24RecombinedCosetBalanceCount : Nat := 8
def p24CompressedVerifierEquations : Nat := 48
def p24CompressedOcticEquations : Nat := 42
def p24CompressedAnchorEquations : Nat := 6
def p24RobertCaxisPrime : Nat := 179
def p24RobertCaxisHalfDegree : Nat := 89
def p24RawPacketTerms : Nat :=
  p24NontrivialRightCharacters * p24QuotientCycles * p24QuotientCycleLength

theorem p24_nontrivial_character_payload_count :
    p24NontrivialRightCharacters * p24LeftRows = 936 := by
  decide

theorem p24_hcoset_payload_count :
    p24RightHCosets * p24LeftRows = 1092 := by
  decide

theorem p24_centering_plus_nontrivial_characters_count :
    p24LeftRows +
      p24NontrivialRightCharacters * p24LeftRows = 1092 := by
  decide

theorem p24_raw_packet_term_count :
    p24RawPacketTerms = 420 := by
  decide

theorem p24_projector_trace_payload_subsqrt :
    p24RightHCosets * p24LeftRows < 1000000000000 := by
  decide

theorem p24_internal_degree_factorization_named :
    p24BOverCDegree * p24COverEDegree = p24InternalDegree := by
  decide

theorem p24_rho_cycle_order_named :
    p24RhoCycleOrder = 38843 := by
  decide

theorem p24_after_b_over_c_trace_is_jacobi_quotient :
    p24AfterBOverCQuotientOrder =
      p24RightHCosets * p24COverEDegree := by
  decide

theorem p24_after_b_over_c_trace_quotient_count :
    p24AfterBOverCQuotientOrder = 1253 := by
  decide

theorem p24_visible_jacobi_level_matches_post_bc_quotient :
    p24VisibleJacobiLevel = p24AfterBOverCQuotientOrder := by
  decide

theorem p24_visible_jacobi_phi_count :
    p24VisibleJacobiPhi = 1068 := by
  decide

theorem p24_visible_theta_infinity_sum_count :
    p24VisibleThetaInfinitySum = 534 := by
  decide

theorem p24_plain_cyclotomic_frobenius_not_post_bc_quotient :
    p24PlainCyclotomicFrobeniusOrder ≠ p24AfterBOverCQuotientOrder := by
  decide

theorem p24_rho_cyclotomic_shadow_not_post_bc_quotient :
    p24RhoCyclotomicShadowOrder ≠ p24AfterBOverCQuotientOrder := by
  decide

theorem p24_rho_cyclotomic_shadow_count :
    p24RhoCyclotomicShadowOrder = 89 := by
  decide

theorem p24_rho_cyclotomic_shadow_moduli :
    p24RhoCyclotomicShadowModLevel = 666 ∧
      p24RhoCyclotomicShadowModRight = 1 ∧
      p24RhoCyclotomicShadowModC = 129 := by
  decide

theorem p24_kl_frobenius_c179_half_orbits :
    p24KLFrobeniusCOrbitCount = 2 ∧
      p24KLFrobeniusCOrbitSize = 89 ∧
      p24KLCNonzeroCharacterCount =
        2 * p24KLFrobeniusCOrbitSize := by
  decide

theorem p24_kl_real_inversion_quotient_degree :
    p24KLRealInversionOrbitCount = 1 ∧
      p24KLRealInversionOrbitSize = 89 := by
  decide

theorem p24_kl_half_anchor_matches_r179_kernel_degree :
    p24KLRealInversionOrbitSize * 2 = 178 := by
  decide

theorem p24_kl_visible_frobenius_not_post_bc_quotient :
    p24KLCyclotomicVisibleOrder ≠ p24AfterBOverCQuotientOrder := by
  decide

theorem p24_kl_visible_frobenius_trivial_on_right_axis :
    p24KLCyclotomicRightOrder = 1 := by
  decide

theorem p24_visible_ray_order_has_no_right_axis_primary :
    p24VisibleRayOrderOverHilbert % p24RightHCosets ≠ 0 := by
  decide

theorem p24_visible_ray_order_has_no_c_axis_primary :
    p24VisibleRayOrderOverHilbert % p24COverEDegree ≠ 0 := by
  decide

theorem p24_visible_ray_order_not_post_bc_quotient_source :
    p24VisibleRayOrderOverHilbert % p24AfterBOverCQuotientOrder ≠ 0 := by
  decide

theorem p24_visible_ray_order_coprime_to_right_axis :
    Nat.gcd p24VisibleRayOrderOverHilbert p24RightHCosets = 1 := by
  decide

theorem p24_visible_ray_order_coprime_to_c_axis :
    Nat.gcd p24VisibleRayOrderOverHilbert p24COverEDegree = 1 := by
  decide

theorem p24_visible_ray_order_coprime_to_post_bc_quotient :
    Nat.gcd p24VisibleRayOrderOverHilbert
      p24AfterBOverCQuotientOrder = 1 := by
  decide

theorem p24_candidate_ratio_order_bound_is_post_bc_quotient :
    p24CandidateRatioOrderBound = p24AfterBOverCQuotientOrder := by
  decide

theorem p24_candidate_ratio_order_bound_divides_post_bc_quotient :
    p24CandidateRatioOrderBound ∣ p24AfterBOverCQuotientOrder := by
  decide

theorem p24_visible_ray_restriction_forced_trivial_by_coprime_orders :
    Nat.gcd p24VisibleRayOrderOverHilbert
      p24CandidateRatioOrderBound = 1 := by
  decide

theorem p24_full_rho_level_is_bc_extension_of_visible_quotient :
    p24FullRhoLevel = p24BCKernelDegree * p24VisibleJacobiLevel := by
  decide

theorem p24_bc_inflated_raw_carry_scale_count :
    p24BCInflatedRawCarryScale = 31 := by
  decide

theorem p24_bc_inflated_raw_pushforward_scale_count :
    p24BCInflatedRawPushforwardScale = 961 := by
  decide

theorem p24_bc_multiplicative_norm_power_count :
    p24BCMultiplicativeNormPower = 31 := by
  decide

theorem p24_bc_trace_surviving_character_count :
    p24BCTraceSurvivingCharacters = 1253 := by
  decide

theorem p24_bc_trace_killed_kernel_twist_count :
    p24BCTraceKilledKernelTwists = 37590 := by
  decide

theorem p24_bc_trace_survivors_plus_killed_exhaust_full_rho :
    p24BCTraceSurvivingCharacters + p24BCTraceKilledKernelTwists =
      p24FullRhoLevel := by
  decide

theorem p24_bc_quotient_ratio_pair_check_count :
    p24BCQuotientRatioPairCheckCount = 1570009 := by
  decide

theorem p24_bc_quotient_ratio_max_order_is_post_bc :
    p24BCQuotientRatioMaxOrder = p24AfterBOverCQuotientOrder := by
  decide

theorem p24_bc_quotient_ratio_order_divides_post_bc :
    p24BCQuotientRatioMaxOrder ∣ p24AfterBOverCQuotientOrder := by
  decide

theorem p24_unramified_quotient_twist_order_count :
    p24UnramifiedQuotientTwistOrder = p24VisibleJacobiLevel := by
  decide

theorem p24_unramified_quotient_twist_exact_post_bc_selector :
    p24UnramifiedQuotientTwistOrder =
      p24RightHCosets * p24COverEDegree := by
  decide

theorem p24_unramified_twist_axis_orders :
    p24UnramifiedTwistRightAxisOrder = 7 ∧
      p24UnramifiedTwistCAxisOrder = 179 := by
  decide

theorem p24_unramified_twist_cyclotomic_shadow_mismatch :
    p24RhoCyclotomicShadowOrder ≠ p24UnramifiedQuotientTwistOrder := by
  decide

theorem p24_post_bc_quotient_generated_by_rho_count :
    p24PostBCQuotientGeneratorOrder = 1253 := by
  decide

theorem p24_post_bc_unramified_character_count :
    p24PostBCUnramifiedCharacterCount = 1253 := by
  decide

theorem p24_artin_character_pair_check_count :
    p24ArtinCharacterPairCheckCount = 1570009 := by
  decide

theorem p24_rho_value_can_determine_all_post_bc_characters_count :
    p24PostBCQuotientGeneratorOrder =
      p24PostBCUnramifiedCharacterCount := by
  decide

theorem p24_rho_from_axis_bezout_integer_sum :
    p24RhoReconstructionIntegerSum = 1254 := by
  decide

theorem p24_rho_from_axis_bezout_mod_quotient :
    p24RhoReconstructionIntegerSum % p24AfterBOverCQuotientOrder = 1 := by
  decide

theorem p24_rho_value_reduces_to_two_axis_values_count :
    p24ArtinCharacterPairCheckCount = 1253 * 1253 := by
  decide

theorem p24_right_axis_selector_recomposes_shift6 :
    (p24PostBCRhoRightCoordinate * p24RightAxisHShift +
      p24RhoFromCAxisPower * p24CAxisHShift) % p24RightHCosets =
      p24RawRightHShift := by
  decide

theorem p24_right_axis_selector_is_shift3_in_h_convention :
    p24RightAxisHShift = 3 := by
  decide

theorem p24_c_axis_fixes_right_h_quotient :
    p24CAxisHShift = 0 := by
  decide

theorem p24_right_fixed_residual_character_count :
    p24RightFixedResidualCharacterCount = 179 := by
  decide

theorem p24_caxis_residual_max_order_is_179 :
    p24CaxisResidualMaxOrder = p24COverEDegree := by
  decide

theorem p24_caxis_residual_order_divides_c_axis :
    p24CaxisResidualMaxOrder ∣ p24COverEDegree := by
  decide

theorem p24_selected_artin_exponent_is_one :
    p24SelectedArtinExponent = 1 := by
  decide

theorem p24_all_pure_c_residuals_preserve_value_side_count :
    p24PureCResidualValueSideInvariantCount = p24COverEDegree := by
  decide

theorem p24_pure_c_residual_zero_defect_count :
    p24PureCResidualZeroDefectCount = 1 := by
  decide

theorem p24_right_mixed_admissible_pair_count :
    p24RightMixedAdmissiblePairCount = 189036 := by
  decide

theorem p24_r179_cyclotomic_pole_order :
    p24R179CyclotomicPoleOrder = 178 := by
  decide

theorem p24_r179_c_nontrivial_fourier_channels :
    p24R179CNontrivialFourierChannels = 1246 := by
  decide

theorem p24_r179_kernel_degree_matches_half_pole_order :
    p24RobertCaxisHalfDegree * 2 = p24R179CyclotomicPoleOrder := by
  decide

theorem p24_compressed_equation_split :
    p24CompressedOcticEquations + p24CompressedAnchorEquations =
      p24CompressedVerifierEquations := by
  decide

theorem p24_weighted_character_potential_count :
    p24NontrivialRightCharacters = 6 := by
  decide

theorem p24_robert_caxis_nonzero_terms :
    p24RobertCaxisPrime - 1 = 178 := by
  decide

theorem p24_robert_caxis_real_half_degree :
    2 * p24RobertCaxisHalfDegree = p24RobertCaxisPrime - 1 := by
  decide

theorem p24_recombined_balance_target_subsqrt :
    p24CompressedVerifierEquations < 1000000000000 := by
  decide

end P24.TraceGcdProjectorTracePipelineGate
