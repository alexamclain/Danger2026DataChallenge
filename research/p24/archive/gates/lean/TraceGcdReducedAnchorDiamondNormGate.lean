/-!
Finite handoff gate for the reduced-anchor diamond norm identity.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate.py

checks that the denominator-cleared residual

  sum_{k != 0} [zeta_c^k] - (c - 1)[1]

is the diamond norm over `(Z/cZ)^*` of the single divisor `[zeta_c] - [1]`.
Equivalently, the corresponding rational function is

  Phi_c(X)/(X - 1)^(c - 1).

This is deliberately a diamond/unit norm, not the cyclic C/E trace norm.
-/

namespace P24.TraceGcdReducedAnchorDiamondNormGate

structure SingleDiamondFactor where
  divisorIsOnePointMinusBasepoint : Prop
  pIntegralSelectedCMLangFactor : Prop

def SatisfiesSingleDiamondFactor
    (factor : SingleDiamondFactor) : Prop :=
  factor.divisorIsOnePointMinusBasepoint ∧
  factor.pIntegralSelectedCMLangFactor

structure DiamondNormResidual where
  normOverNonzeroMultipliers : Prop
  equalsCyclotomicResidualDivisor : Prop
  equalsPhiOverXMinusOnePower : Prop
  notCyclicCETraceNorm : Prop

def SatisfiesDiamondNormResidual
    (residual : DiamondNormResidual) : Prop :=
  residual.normOverNonzeroMultipliers ∧
  residual.equalsCyclotomicResidualDivisor ∧
  residual.equalsPhiOverXMinusOnePower ∧
  residual.notCyclicCETraceNorm

structure KummerSignDescent where
  auxiliaryKummerDescent : Prop
  signNormalization : Prop

def SatisfiesKummerSignDescent
    (descent : KummerSignDescent) : Prop :=
  descent.auxiliaryKummerDescent ∧
  descent.signNormalization

structure SelectedAnchorProducer where
  realizesSelectedAnchor : Prop

def SatisfiesSelectedAnchorProducer
    (producer : SelectedAnchorProducer) : Prop :=
  producer.realizesSelectedAnchor

theorem selected_anchor_from_pintegral_diamond_norm_and_kummer_descent
    (factor : SingleDiamondFactor)
    (residual : DiamondNormResidual)
    (descent : KummerSignDescent)
    (producer : SelectedAnchorProducer)
    (h_handoff :
      factor.divisorIsOnePointMinusBasepoint →
      factor.pIntegralSelectedCMLangFactor →
      residual.normOverNonzeroMultipliers →
      residual.equalsCyclotomicResidualDivisor →
      residual.equalsPhiOverXMinusOnePower →
      residual.notCyclicCETraceNorm →
      descent.auxiliaryKummerDescent →
      descent.signNormalization →
      producer.realizesSelectedAnchor)
    (h_factor : SatisfiesSingleDiamondFactor factor)
    (h_residual : SatisfiesDiamondNormResidual residual)
    (h_descent : SatisfiesKummerSignDescent descent) :
    SatisfiesSelectedAnchorProducer producer := by
  rcases h_factor with ⟨h_one_point, h_integral⟩
  rcases h_residual with
    ⟨h_norm, h_divisor, h_phi, h_not_trace⟩
  rcases h_descent with ⟨h_kummer, h_sign⟩
  exact h_handoff
    h_one_point h_integral
    h_norm h_divisor h_phi h_not_trace
    h_kummer h_sign

def p24COverEDegree : Nat := 179
def p24RightQuotientDegree : Nat := 7
def p24DiamondNormOrbitSize : Nat := p24COverEDegree - 1
def p24ResidualFourierChannels : Nat :=
  p24RightQuotientDegree * (p24COverEDegree - 1)

theorem p24_diamond_norm_orbit_size :
    p24DiamondNormOrbitSize = 178 := by
  decide

theorem p24_residual_fourier_channels :
    p24ResidualFourierChannels = 1246 := by
  decide

end P24.TraceGcdReducedAnchorDiamondNormGate
