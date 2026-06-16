/-!
Finite handoff gate for the auxiliary Kummer descent version of the
degenerate-anchor theorem.

The Python gate

  p24/trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate.py

checks the exponent arithmetic behind the statement:

* separate base-field row-sum and R_c residual factors need not exist;
* after adjoining beta with beta^c = s, the two slices split;
* their product descends to the base selected correction;
* the selected correction forces the R_c exponent e=1.

The remaining arithmetic input is to construct the corresponding p-integral
CM/Lang auxiliary extension, norm, or divisor realization for p24.
-/

namespace P24.TraceGcdAnchorKummerDescentGate

structure KummerAnchorSplit where
  betaCEqualsSelectedScalar : Prop
  rowSumSliceDefinedOverKummer : Prop
  cyclotomicResidualDefinedOverKummer : Prop
  separateSlicesAreNonbase : Prop

def SatisfiesKummerAnchorSplit
    (split : KummerAnchorSplit) : Prop :=
  split.betaCEqualsSelectedScalar ∧
  split.rowSumSliceDefinedOverKummer ∧
  split.cyclotomicResidualDefinedOverKummer ∧
  split.separateSlicesAreNonbase

structure KummerDescentProduct where
  productDescendsToBase : Prop
  productMatchesSelectedAnchorCorrection : Prop
  cyclotomicResidualExponentIsOne : Prop
  signNormalizationChosen : Prop

def SatisfiesKummerDescentProduct
    (product : KummerDescentProduct) : Prop :=
  product.productDescendsToBase ∧
  product.productMatchesSelectedAnchorCorrection ∧
  product.cyclotomicResidualExponentIsOne ∧
  product.signNormalizationChosen

structure PIntegralCMLangAnchor where
  pIntegralAuxiliaryRealization : Prop
  normOrDivisorDescent : Prop

def SatisfiesPIntegralCMLangAnchor
    (anchor : PIntegralCMLangAnchor) : Prop :=
  anchor.pIntegralAuxiliaryRealization ∧
  anchor.normOrDivisorDescent

structure FullSelectedAnchorCorrection where
  realizesSelectedAnchorCorrection : Prop

def SatisfiesFullSelectedAnchorCorrection
    (target : FullSelectedAnchorCorrection) : Prop :=
  target.realizesSelectedAnchorCorrection

theorem selected_anchor_from_kummer_cm_lang_descent
    (split : KummerAnchorSplit)
    (product : KummerDescentProduct)
    (anchor : PIntegralCMLangAnchor)
    (target : FullSelectedAnchorCorrection)
    (h_handoff :
      split.betaCEqualsSelectedScalar →
      split.rowSumSliceDefinedOverKummer →
      split.cyclotomicResidualDefinedOverKummer →
      split.separateSlicesAreNonbase →
      product.productDescendsToBase →
      product.productMatchesSelectedAnchorCorrection →
      product.cyclotomicResidualExponentIsOne →
      product.signNormalizationChosen →
      anchor.pIntegralAuxiliaryRealization →
      anchor.normOrDivisorDescent →
      target.realizesSelectedAnchorCorrection)
    (h_split : SatisfiesKummerAnchorSplit split)
    (h_product : SatisfiesKummerDescentProduct product)
    (h_anchor : SatisfiesPIntegralCMLangAnchor anchor) :
    SatisfiesFullSelectedAnchorCorrection target := by
  rcases h_split with
    ⟨h_beta, h_row, h_residual, h_nonbase⟩
  rcases h_product with
    ⟨h_descends, h_matches, h_e_one, h_sign⟩
  rcases h_anchor with
    ⟨h_integral, h_norm⟩
  exact h_handoff
    h_beta h_row h_residual h_nonbase
    h_descends h_matches h_e_one h_sign
    h_integral h_norm

def p24KummerAuxiliaryDegree : Nat := 179
def p24RightQuotientDegree : Nat := 7
def p24CyclotomicResidualExponent : Nat := 1
def p24ResidualFourierChannels : Nat :=
  p24RightQuotientDegree * (p24KummerAuxiliaryDegree - 1)

theorem p24_kummer_auxiliary_degree :
    p24KummerAuxiliaryDegree = 179 := by
  decide

theorem p24_cyclotomic_residual_exponent :
    p24CyclotomicResidualExponent = 1 := by
  decide

theorem p24_residual_fourier_channels :
    p24ResidualFourierChannels = 1246 := by
  decide

end P24.TraceGcdAnchorKummerDescentGate
