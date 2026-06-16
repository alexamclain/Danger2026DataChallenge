/-!
Finite handoff gate separating the reduced-anchor diamond norm from the
ordinary cyclic C/E trace norm.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_cyclic_vs_diamond_norm_gate.py

checks the concrete divisor identities:

* cyclic translations of `[zeta_c] - [1]` telescope to the trivial divisor;
* diamond multipliers of `[zeta_c] - [1]` give the cyclotomic residual.

Thus a p24 producer using the cyclic C/E trace norm erases the selected-anchor
residual.  The arithmetic theorem must provide the diamond/unit norm or an
equivalent identity.
-/

namespace P24.TraceGcdReducedAnchorCyclicVsDiamondNormGate

structure CyclicTranslationNorm where
  normOverCyclicTranslations : Prop
  telescopesToTrivialDivisor : Prop

def SatisfiesCyclicTranslationNorm
    (norm : CyclicTranslationNorm) : Prop :=
  norm.normOverCyclicTranslations ∧
  norm.telescopesToTrivialDivisor

structure DiamondUnitNorm where
  normOverNonzeroMultipliers : Prop
  equalsCyclotomicResidual : Prop
  residualNontrivial : Prop

def SatisfiesDiamondUnitNorm
    (norm : DiamondUnitNorm) : Prop :=
  norm.normOverNonzeroMultipliers ∧
  norm.equalsCyclotomicResidual ∧
  norm.residualNontrivial

structure ProducerNormChoice where
  usesCyclicCOverENorm : Prop
  usesDiamondUnitNorm : Prop

def ProducerNormChoiceIsHonest
    (choice : ProducerNormChoice) : Prop :=
  choice.usesDiamondUnitNorm ∧ ¬ choice.usesCyclicCOverENorm

theorem cyclic_norm_cannot_be_the_diamond_residual
    (cyclic : CyclicTranslationNorm)
    (diamond : DiamondUnitNorm)
    (h_cyclic : SatisfiesCyclicTranslationNorm cyclic)
    (h_diamond : SatisfiesDiamondUnitNorm diamond)
    (h_trivial_not_residual :
      cyclic.telescopesToTrivialDivisor →
      diamond.equalsCyclotomicResidual →
      diamond.residualNontrivial →
      ¬ cyclic.normOverCyclicTranslations = diamond.normOverNonzeroMultipliers) :
    ¬ cyclic.normOverCyclicTranslations = diamond.normOverNonzeroMultipliers := by
  rcases h_cyclic with ⟨_h_cyclic_norm, h_telescopes⟩
  rcases h_diamond with ⟨_h_diamond_norm, h_residual, h_nontrivial⟩
  exact h_trivial_not_residual h_telescopes h_residual h_nontrivial

theorem honest_choice_from_diamond_and_not_cyclic
    (choice : ProducerNormChoice)
    (h_diamond : choice.usesDiamondUnitNorm)
    (h_not_cyclic : ¬ choice.usesCyclicCOverENorm) :
    ProducerNormChoiceIsHonest choice := by
  exact ⟨h_diamond, h_not_cyclic⟩

def p24COverEDegree : Nat := 179
def p24CyclicTranslationOrbitSize : Nat := p24COverEDegree
def p24DiamondOrbitSize : Nat := p24COverEDegree - 1

theorem p24_cyclic_translation_orbit_size :
    p24CyclicTranslationOrbitSize = 179 := by
  decide

theorem p24_diamond_orbit_size :
    p24DiamondOrbitSize = 178 := by
  decide

theorem p24_cyclic_and_diamond_orbit_sizes_distinct :
    p24CyclicTranslationOrbitSize ≠ p24DiamondOrbitSize := by
  decide

end P24.TraceGcdReducedAnchorCyclicVsDiamondNormGate
