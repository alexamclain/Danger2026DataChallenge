/-!
Finite handoff gate for the reduced-anchor cyclotomic divisor candidate.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate.py

checks the explicit finite calculation:

  c * h_nontriv = sum_{k != 0} [zeta_c^k] - (c - 1)[1].

For prime c this is the divisor of

  Phi_c(X) / (X - 1)^(c - 1).

This Lean file records the proof contract we need next: if the selected
CM/Lang degenerate-anchor unit specializes p-integrally to this principal
cyclotomic residual and also supplies the already identified row-sum slice,
then it realizes the full reduced-anchor target.
-/

namespace P24.TraceGcdReducedAnchorCyclotomicDivisorGate

structure CNontrivialResidual where
  clearsDenominatorByC : Prop
  integralDegreeZeroDivisor : Prop
  hasNoB0FourierProfile : Prop
  hasAllNontrivialCChannels : Prop

def SatisfiesCNontrivialResidual
    (residual : CNontrivialResidual) : Prop :=
  residual.clearsDenominatorByC ∧
  residual.integralDegreeZeroDivisor ∧
  residual.hasNoB0FourierProfile ∧
  residual.hasAllNontrivialCChannels

structure CyclotomicPrincipalDivisor where
  divisorIsPhiOverXMinusOnePower : Prop
  divisorMatchesClearedResidual : Prop
  degreeZero : Prop

def SatisfiesCyclotomicPrincipalDivisor
    (divisor : CyclotomicPrincipalDivisor) : Prop :=
  divisor.divisorIsPhiOverXMinusOnePower ∧
  divisor.divisorMatchesClearedResidual ∧
  divisor.degreeZero

structure SelectedCMLangSpecialization where
  pIntegralAtSelectedPrime : Prop
  realizesCyclotomicResidual : Prop
  realizesCTrivialRowSumSlice : Prop

def SatisfiesSelectedCMLangSpecialization
    (specialization : SelectedCMLangSpecialization) : Prop :=
  specialization.pIntegralAtSelectedPrime ∧
  specialization.realizesCyclotomicResidual ∧
  specialization.realizesCTrivialRowSumSlice

structure FullReducedAnchorTarget where
  realizesFullPuncturedRightZeroRow : Prop
  realizesB0RowSumSlice : Prop
  realizesCNontrivialResidual : Prop

def SatisfiesFullReducedAnchorTarget
    (target : FullReducedAnchorTarget) : Prop :=
  target.realizesFullPuncturedRightZeroRow ∧
  target.realizesB0RowSumSlice ∧
  target.realizesCNontrivialResidual

theorem full_anchor_target_from_cyclotomic_cm_lang_specialization
    (residual : CNontrivialResidual)
    (divisor : CyclotomicPrincipalDivisor)
    (specialization : SelectedCMLangSpecialization)
    (target : FullReducedAnchorTarget)
    (h_handoff :
      residual.clearsDenominatorByC →
      residual.integralDegreeZeroDivisor →
      residual.hasNoB0FourierProfile →
      residual.hasAllNontrivialCChannels →
      divisor.divisorIsPhiOverXMinusOnePower →
      divisor.divisorMatchesClearedResidual →
      divisor.degreeZero →
      specialization.pIntegralAtSelectedPrime →
      specialization.realizesCyclotomicResidual →
      specialization.realizesCTrivialRowSumSlice →
      target.realizesFullPuncturedRightZeroRow ∧
        target.realizesB0RowSumSlice ∧
        target.realizesCNontrivialResidual)
    (h_residual : SatisfiesCNontrivialResidual residual)
    (h_divisor : SatisfiesCyclotomicPrincipalDivisor divisor)
    (h_specialization :
      SatisfiesSelectedCMLangSpecialization specialization) :
    SatisfiesFullReducedAnchorTarget target := by
  rcases h_residual with
    ⟨h_clear, h_integral, h_no_b0, h_channels⟩
  rcases h_divisor with
    ⟨h_phi, h_matches, h_degree_zero⟩
  rcases h_specialization with
    ⟨h_p_integral, h_realizes_residual, h_realizes_b0⟩
  exact h_handoff
    h_clear h_integral h_no_b0 h_channels
    h_phi h_matches h_degree_zero
    h_p_integral h_realizes_residual h_realizes_b0

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def p24CyclotomicPoleOrder : Nat := p24COverEDegree - 1
def p24CNontrivialResidualChannels : Nat :=
  p24RightQuotientDegree * (p24COverEDegree - 1)

theorem p24_cyclotomic_pole_order :
    p24CyclotomicPoleOrder = 178 := by
  decide

theorem p24_c_nontrivial_residual_channels :
    p24CNontrivialResidualChannels = 1246 := by
  decide

end P24.TraceGcdReducedAnchorCyclotomicDivisorGate
