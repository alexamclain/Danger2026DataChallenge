/-!
Finite handoff gate for the p24 affine quotient-profile reformulation.

The arithmetic theorem remains external.  This file records the formal shape:

* the direct recombined payload is the `6 * 8 = 48` family saying each
  nonzero relative coset has the same nontrivial right profile as
  `|<p>|` copies of the selected child;
* equivalently, each quotient column differs from that selected-child profile
  by a right-constant offset;
* the older `42 + 6` mixed-spectrum/anchor split is just the Fourier
  decomposition of that same affine profile identity.
-/

namespace P24.TraceGcdAffineProfileGate

def RightConstant {RightCoset Value : Type}
    (profile : RightCoset → Value) : Prop :=
  ∃ gamma, ∀ right, profile right = gamma

def AllAffineOffsets {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value) : Prop :=
  ∀ relative, RightConstant (difference relative)

def AllDirectPayload {RelativeCoset : Type}
    (direct : RelativeCoset → Prop) : Prop :=
  ∀ relative, direct relative

def AllMixedZero {RightChar RelativeChar : Type}
    (mixed : RightChar → RelativeChar → Prop) : Prop :=
  ∀ chi lambda, mixed chi lambda

def AllAnchorZero {RightChar : Type}
    (anchor : RightChar → Prop) : Prop :=
  ∀ chi, anchor chi

theorem direct_payload_from_affine_offsets
    {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (direct : RelativeCoset → Prop)
    (h_affine_implies_direct :
      AllAffineOffsets difference → AllDirectPayload direct)
    (h_affine : AllAffineOffsets difference) :
    AllDirectPayload direct := by
  exact h_affine_implies_direct h_affine

theorem affine_offsets_from_direct_payload
    {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (direct : RelativeCoset → Prop)
    (h_direct_implies_affine :
      AllDirectPayload direct → AllAffineOffsets difference)
    (h_direct : AllDirectPayload direct) :
    AllAffineOffsets difference := by
  exact h_direct_implies_affine h_direct

theorem affine_iff_direct_payload
    {RightCoset RelativeCoset Value : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (direct : RelativeCoset → Prop)
    (h_affine_implies_direct :
      AllAffineOffsets difference → AllDirectPayload direct)
    (h_direct_implies_affine :
      AllDirectPayload direct → AllAffineOffsets difference) :
    AllAffineOffsets difference ↔ AllDirectPayload direct := by
  constructor
  · exact h_affine_implies_direct
  · exact h_direct_implies_affine

theorem affine_iff_mixed_plus_anchor
    {RightCoset RelativeCoset Value RightChar RelativeChar : Type}
    (difference : RelativeCoset → RightCoset → Value)
    (mixed : RightChar → RelativeChar → Prop)
    (anchor : RightChar → Prop)
    (h_affine_implies_split :
      AllAffineOffsets difference → AllMixedZero mixed ∧ AllAnchorZero anchor)
    (h_split_implies_affine :
      AllMixedZero mixed → AllAnchorZero anchor → AllAffineOffsets difference) :
    AllAffineOffsets difference ↔ (AllMixedZero mixed ∧ AllAnchorZero anchor) := by
  constructor
  · intro h_affine
    exact h_affine_implies_split h_affine
  · intro h_split
    exact h_split_implies_affine h_split.1 h_split.2

def p24RightNontrivialCharacters : Nat := 6
def p24RelativeCosets : Nat := 8
def p24RelativeNontrivialCharacters : Nat := 7

def p24AffineDirectEquations : Nat :=
  p24RightNontrivialCharacters * p24RelativeCosets

def p24MixedEquations : Nat :=
  p24RightNontrivialCharacters * p24RelativeNontrivialCharacters

def p24AnchorEquations : Nat :=
  p24RightNontrivialCharacters

theorem p24_affine_direct_equation_count :
    p24AffineDirectEquations = 48 := by
  decide

theorem p24_mixed_plus_anchor_equation_count :
    p24MixedEquations + p24AnchorEquations = 48 := by
  decide

theorem p24_mixed_equation_count :
    p24MixedEquations = 42 := by
  decide

theorem p24_anchor_equation_count :
    p24AnchorEquations = 6 := by
  decide

end P24.TraceGcdAffineProfileGate
