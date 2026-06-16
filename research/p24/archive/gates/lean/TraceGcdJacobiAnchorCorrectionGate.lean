/-!
Finite handoff gate for the Jacobi single-anchor correction.

The arithmetic input remains external:

  a literal or CM/Lang Jacobi-type packet satisfies a punctured
  Hasse-Davenport product formula away from the degenerate right-zero anchor,
  and the selected packet supplies the analogue of the normalization
  J(1,1)/(q-2).

The Python gate

  p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.py

checks this in small finite-field Jacobi-sum models.  This Lean file records
the finite contract:

  punctured pair-products and nonzero right-row ratios
  + single-anchor correction of the C-zero pair-product and right-zero ratio
  => full multiplicative producer identities
  => selected-defect value identities
  => admissible-span/verifier handoff.
-/

namespace P24.TraceGcdJacobiAnchorCorrectionGate

structure PuncturedHasseDavenport where
  offCZeroPairProductsConstant : Prop
  nonzeroRightRowsHaveCommonRatio : Prop

def SatisfiesPuncturedHasseDavenport
    (hd : PuncturedHasseDavenport) : Prop :=
  hd.offCZeroPairProductsConstant ∧
  hd.nonzeroRightRowsHaveCommonRatio

structure SingleAnchorCorrection where
  cZeroPairProductsConstantAfterCorrection : Prop
  rightZeroRowRatioMatchesAfterCorrection : Prop
  onlyOneAnchorValueChanged : Prop

def SatisfiesSingleAnchorCorrection
    (anchor : SingleAnchorCorrection) : Prop :=
  anchor.cZeroPairProductsConstantAfterCorrection ∧
  anchor.rightZeroRowRatioMatchesAfterCorrection ∧
  anchor.onlyOneAnchorValueChanged

structure MultiplicativeProducerIdentities where
  cZeroPairProductsConstant : Prop
  offCZeroPairProductsConstant : Prop
  selectedRowProductRatiosConstant : Prop

def SatisfiesMultiplicativeProducer
    (producer : MultiplicativeProducerIdentities) : Prop :=
  producer.cZeroPairProductsConstant ∧
  producer.offCZeroPairProductsConstant ∧
  producer.selectedRowProductRatiosConstant

structure SelectedDefectValueIdentities where
  cRowSumsIndependent : Prop
  cZeroFiberVanishes : Prop
  inversionComplementConstantOffCZero : Prop

def SatisfiesValueIdentities
    (ids : SelectedDefectValueIdentities) : Prop :=
  ids.cRowSumsIndependent ∧
  ids.cZeroFiberVanishes ∧
  ids.inversionComplementConstantOffCZero

def AllVerifierEquations {Row Coset : Type}
    (hcosetZero : Row → Coset → Prop) : Prop :=
  ∀ row coset, hcosetZero row coset

theorem multiplicative_producer_from_punctured_hd_and_anchor
    (hd : PuncturedHasseDavenport)
    (anchor : SingleAnchorCorrection)
    (producer : MultiplicativeProducerIdentities)
    (h_pair :
      hd.offCZeroPairProductsConstant →
      anchor.cZeroPairProductsConstantAfterCorrection →
      producer.offCZeroPairProductsConstant ∧
        producer.cZeroPairProductsConstant)
    (h_ratio :
      hd.nonzeroRightRowsHaveCommonRatio →
      anchor.rightZeroRowRatioMatchesAfterCorrection →
      producer.selectedRowProductRatiosConstant)
    (h_hd : SatisfiesPuncturedHasseDavenport hd)
    (h_anchor : SatisfiesSingleAnchorCorrection anchor) :
    SatisfiesMultiplicativeProducer producer := by
  rcases h_hd with ⟨h_off, h_nonzero_ratio⟩
  rcases h_anchor with ⟨h_czero, h_right_zero_ratio, _h_single⟩
  rcases h_pair h_off h_czero with ⟨h_off_producer, h_czero_producer⟩
  exact ⟨h_czero_producer, h_off_producer,
    h_ratio h_nonzero_ratio h_right_zero_ratio⟩

theorem value_identities_from_punctured_hd_anchor
    (hd : PuncturedHasseDavenport)
    (anchor : SingleAnchorCorrection)
    (producer : MultiplicativeProducerIdentities)
    (ids : SelectedDefectValueIdentities)
    (h_pair :
      hd.offCZeroPairProductsConstant →
      anchor.cZeroPairProductsConstantAfterCorrection →
      producer.offCZeroPairProductsConstant ∧
        producer.cZeroPairProductsConstant)
    (h_ratio :
      hd.nonzeroRightRowsHaveCommonRatio →
      anchor.rightZeroRowRatioMatchesAfterCorrection →
      producer.selectedRowProductRatiosConstant)
    (h_product_to_value :
      SatisfiesMultiplicativeProducer producer →
      SatisfiesValueIdentities ids)
    (h_hd : SatisfiesPuncturedHasseDavenport hd)
    (h_anchor : SatisfiesSingleAnchorCorrection anchor) :
    SatisfiesValueIdentities ids := by
  exact h_product_to_value
    (multiplicative_producer_from_punctured_hd_and_anchor
      hd anchor producer h_pair h_ratio h_hd h_anchor)

theorem verifier_from_punctured_hd_anchor
    {Row Coset : Type}
    (hd : PuncturedHasseDavenport)
    (anchor : SingleAnchorCorrection)
    (producer : MultiplicativeProducerIdentities)
    (ids : SelectedDefectValueIdentities)
    (hcosetZero : Row → Coset → Prop)
    (h_pair :
      hd.offCZeroPairProductsConstant →
      anchor.cZeroPairProductsConstantAfterCorrection →
      producer.offCZeroPairProductsConstant ∧
        producer.cZeroPairProductsConstant)
    (h_ratio :
      hd.nonzeroRightRowsHaveCommonRatio →
      anchor.rightZeroRowRatioMatchesAfterCorrection →
      producer.selectedRowProductRatiosConstant)
    (h_product_to_value :
      SatisfiesMultiplicativeProducer producer →
      SatisfiesValueIdentities ids)
    (h_value_to_verifier :
      SatisfiesValueIdentities ids →
      AllVerifierEquations hcosetZero)
    (h_hd : SatisfiesPuncturedHasseDavenport hd)
    (h_anchor : SatisfiesSingleAnchorCorrection anchor) :
    AllVerifierEquations hcosetZero := by
  exact h_value_to_verifier
    (value_identities_from_punctured_hd_anchor
      hd anchor producer ids h_pair h_ratio h_product_to_value h_hd h_anchor)

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def p24AnchorCorrectionExponent : Nat := p24COverEDegree - 1
def p24AnchorCorrectionSlots : Nat := 1
def p24LeftRows : Nat := 156
def p24RightHCosets : Nat := 7

theorem p24_anchor_correction_exponent :
    p24AnchorCorrectionExponent = 178 := by
  decide

theorem p24_single_anchor_is_constant_size :
    p24AnchorCorrectionSlots = 1 := by
  decide

theorem p24_hcoset_equation_count :
    p24LeftRows * p24RightHCosets = 1092 := by
  decide

theorem p24_anchor_is_smaller_than_hcoset_surface :
    p24AnchorCorrectionSlots < p24LeftRows * p24RightHCosets := by
  decide

end P24.TraceGcdJacobiAnchorCorrectionGate
