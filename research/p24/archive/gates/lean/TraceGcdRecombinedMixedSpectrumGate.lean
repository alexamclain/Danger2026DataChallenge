/-!
Finite handoff gate for the p24 recombined mixed-spectrum target.

The arithmetic theorem is external: for the actual trace-GCD weighted
CM/Lang packet, the six right order-7 characters should have zero mixed
relative-octic spectrum and zero section-aware anchors.

This file records the formal contract:

* a finite Fourier split turns mixed spectrum plus anchor vanishings into the
  eight recombined balance equations for each right character;
* conversely, the inverse split can recover those two families from the eight
  balances;
* the p24 counts are `42 + 6 = 48`, with `54` compressed values if the `c_0`
  anchors are carried alongside the eight coset sums.
-/

namespace P24.TraceGcdRecombinedMixedSpectrumGate

def AllMixedOcticZero {RightChar OcticChar : Type}
    (mixedZero : RightChar → OcticChar → Prop) : Prop :=
  ∀ chi lambda, mixedZero chi lambda

def AllAnchorZero {RightChar : Type}
    (anchorZero : RightChar → Prop) : Prop :=
  ∀ chi, anchorZero chi

def AllRecombinedBalances {RightChar Coset : Type}
    (balance : RightChar → Coset → Prop) : Prop :=
  ∀ chi coset, balance chi coset

theorem recombined_balances_from_mixed_spectrum_and_anchors
    {RightChar OcticChar Coset : Type}
    (mixedZero : RightChar → OcticChar → Prop)
    (anchorZero : RightChar → Prop)
    (balance : RightChar → Coset → Prop)
    (h_split :
      AllMixedOcticZero mixedZero →
      AllAnchorZero anchorZero →
      AllRecombinedBalances balance)
    (h_mixed : AllMixedOcticZero mixedZero)
    (h_anchor : AllAnchorZero anchorZero) :
    AllRecombinedBalances balance := by
  exact h_split h_mixed h_anchor

theorem mixed_spectrum_and_anchors_from_recombined_balances
    {RightChar OcticChar Coset : Type}
    (mixedZero : RightChar → OcticChar → Prop)
    (anchorZero : RightChar → Prop)
    (balance : RightChar → Coset → Prop)
    (h_inverse :
      AllRecombinedBalances balance →
      AllMixedOcticZero mixedZero ∧ AllAnchorZero anchorZero)
    (h_balance : AllRecombinedBalances balance) :
    AllMixedOcticZero mixedZero ∧ AllAnchorZero anchorZero := by
  exact h_inverse h_balance

theorem recombined_balance_iff_mixed_spectrum_plus_anchor
    {RightChar OcticChar Coset : Type}
    (mixedZero : RightChar → OcticChar → Prop)
    (anchorZero : RightChar → Prop)
    (balance : RightChar → Coset → Prop)
    (h_split :
      AllMixedOcticZero mixedZero →
      AllAnchorZero anchorZero →
      AllRecombinedBalances balance)
    (h_inverse :
      AllRecombinedBalances balance →
      AllMixedOcticZero mixedZero ∧ AllAnchorZero anchorZero) :
    AllRecombinedBalances balance ↔
      (AllMixedOcticZero mixedZero ∧ AllAnchorZero anchorZero) := by
  constructor
  · intro h_balance
    exact h_inverse h_balance
  · intro h_pair
    exact h_split h_pair.1 h_pair.2

def p24RightNontrivialCharacters : Nat := 6
def p24RelativeNontrivialOcticCharacters : Nat := 7
def p24RelativeCosets : Nat := 8
def p24EIdempotentsPerFpPacket : Nat := 70
def p24InternalCosetsPerEIdempotent : Nat := 560
def p24InternalTraceSubgroupOrder : Nat := 5549
def p24RecombinedTraceSubgroupOrder : Nat := 388430
def p24CompressedValuesPerRightCharacterWithC0 : Nat := 9
def p24SqrtFloor : Nat := 1000000000000

def p24MixedOcticEquations : Nat :=
  p24RightNontrivialCharacters * p24RelativeNontrivialOcticCharacters

def p24AnchorEquations : Nat :=
  p24RightNontrivialCharacters

def p24RecombinedEquations : Nat :=
  p24RightNontrivialCharacters * p24RelativeCosets

def p24CompressedValuesWithC0 : Nat :=
  p24RightNontrivialCharacters * p24CompressedValuesPerRightCharacterWithC0

theorem p24_mixed_octic_equation_count :
    p24MixedOcticEquations = 42 := by
  decide

theorem p24_anchor_equation_count :
    p24AnchorEquations = 6 := by
  decide

theorem p24_recombined_equation_count :
    p24RecombinedEquations = 48 := by
  decide

theorem p24_split_equation_count :
    p24MixedOcticEquations + p24AnchorEquations =
      p24RecombinedEquations := by
  decide

theorem p24_compressed_values_with_c0_count :
    p24CompressedValuesWithC0 = 54 := by
  decide

theorem p24_internal_cosets_recombine_to_relative_cosets :
    p24InternalCosetsPerEIdempotent =
      p24EIdempotentsPerFpPacket * p24RelativeCosets := by
  decide

theorem p24_recombined_trace_order_from_internal_trace_order :
    p24RecombinedTraceSubgroupOrder =
      p24EIdempotentsPerFpPacket * p24InternalTraceSubgroupOrder := by
  decide

theorem p24_recombined_equations_subsqrt :
    p24RecombinedEquations < p24SqrtFloor := by
  decide

end P24.TraceGcdRecombinedMixedSpectrumGate
