/-!
Finite handoff gate for the p24 right-difference formulation.

The arithmetic theorem remains external.  This file records the contract:

* affine quotient-profile offsets imply the cyclic right-difference identity;
* the right-difference identity recovers the affine offsets by averaging;
* the redundant `7 * 8 = 56` cyclic-difference equations have the same
  independent count `6 * 8 = 48` as the recombined payload.
-/

namespace P24.TraceGcdRightDifferenceGate

def AllAffineOffsets {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value) : Prop :=
  ∀ relative, ∃ gamma, ∀ right, difference relative right = gamma

def AllRightDifferencesMatch {RightCoset RelativeCoset : Type}
    (rightDiffOk : RelativeCoset → RightCoset → Prop) : Prop :=
  ∀ relative right, rightDiffOk relative right

def AverageRecoversOffsets {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (_average : RelativeCoset → Value) : Prop :=
  ∀ relative, ∃ gamma, gamma = _average relative ∧
    ∀ right, difference relative right = gamma

theorem right_differences_from_affine_offsets
    {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (rightDiffOk : RelativeCoset → RightCoset → Prop)
    (h_affine_implies_difference :
      AllAffineOffsets difference → AllRightDifferencesMatch rightDiffOk)
    (h_affine : AllAffineOffsets difference) :
    AllRightDifferencesMatch rightDiffOk := by
  exact h_affine_implies_difference h_affine

theorem affine_offsets_from_right_differences
    {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (rightDiffOk : RelativeCoset → RightCoset → Prop)
    (h_difference_implies_affine :
      AllRightDifferencesMatch rightDiffOk → AllAffineOffsets difference)
    (h_difference : AllRightDifferencesMatch rightDiffOk) :
    AllAffineOffsets difference := by
  exact h_difference_implies_affine h_difference

theorem affine_iff_right_difference
    {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (rightDiffOk : RelativeCoset → RightCoset → Prop)
    (h_affine_implies_difference :
      AllAffineOffsets difference → AllRightDifferencesMatch rightDiffOk)
    (h_difference_implies_affine :
      AllRightDifferencesMatch rightDiffOk → AllAffineOffsets difference) :
    AllAffineOffsets difference ↔ AllRightDifferencesMatch rightDiffOk := by
  constructor
  · exact h_affine_implies_difference
  · exact h_difference_implies_affine

theorem average_recovery_from_right_differences
    {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (average : RelativeCoset → Value)
    (rightDiffOk : RelativeCoset → RightCoset → Prop)
    (h_difference_implies_average :
      AllRightDifferencesMatch rightDiffOk → AverageRecoversOffsets difference average)
    (h_difference : AllRightDifferencesMatch rightDiffOk) :
    AverageRecoversOffsets difference average := by
  exact h_difference_implies_average h_difference

def p24RightQuotient : Nat := 7
def p24RightIndependentCharacters : Nat := 6
def p24RelativeCosets : Nat := 8

def p24RedundantRightDifferenceEquations : Nat :=
  p24RightQuotient * p24RelativeCosets

def p24IndependentRightDifferenceEquations : Nat :=
  p24RightIndependentCharacters * p24RelativeCosets

theorem p24_redundant_right_difference_equation_count :
    p24RedundantRightDifferenceEquations = 56 := by
  decide

theorem p24_independent_right_difference_equation_count :
    p24IndependentRightDifferenceEquations = 48 := by
  decide

end P24.TraceGcdRightDifferenceGate
