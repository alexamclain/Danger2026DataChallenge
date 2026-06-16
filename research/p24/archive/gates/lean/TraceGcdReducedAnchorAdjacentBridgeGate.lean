/-!
Finite handoff gate for the reduced-anchor / adjacent-anchor bridge.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate.py

checks the explicit cyclic calculation.  This Lean file records the contract:

* the reduced Jacobi anchor has a `C/E`-trivial row-sum slice;
* that slice has all six nonfixed right-projector channels;
* adjacent difference is invertible on those six channels;
* therefore the old adjacent-anchor target is precisely cancellation of the
  reduced anchor's `b=0` leak, not a separate arithmetic theorem.

The CM/Lang producer remains external: it must still realize the full
punctured right-zero row, not merely this row-sum slice.
-/

namespace P24.TraceGcdReducedAnchorAdjacentBridgeGate

structure ReducedAnchorFingerprint where
  fullPuncturedRightZeroRow : Prop
  cTrivialRowSumSlice : Prop
  rowSumHasAllSixNonfixedRightChannels : Prop

def SatisfiesReducedAnchorFingerprint
    (anchor : ReducedAnchorFingerprint) : Prop :=
  anchor.fullPuncturedRightZeroRow ∧
  anchor.cTrivialRowSumSlice ∧
  anchor.rowSumHasAllSixNonfixedRightChannels

structure AdjacentBridge where
  adjacentAnchorSeesCTrivialSlice : Prop
  rightDifferenceInvertibleOnNonfixedSlice : Prop
  oppositeRawB0LeakCancels : Prop

def SatisfiesAdjacentBridge
    (bridge : AdjacentBridge) : Prop :=
  bridge.adjacentAnchorSeesCTrivialSlice ∧
  bridge.rightDifferenceInvertibleOnNonfixedSlice ∧
  bridge.oppositeRawB0LeakCancels

structure OldAdjacentAnchorTarget where
  nonfixedRightProjectorsCancel : Prop

def SatisfiesOldAdjacentAnchorTarget
    (target : OldAdjacentAnchorTarget) : Prop :=
  target.nonfixedRightProjectorsCancel

theorem old_adjacent_target_from_reduced_anchor_b0_cancellation
    (anchor : ReducedAnchorFingerprint)
    (bridge : AdjacentBridge)
    (target : OldAdjacentAnchorTarget)
    (h_handoff :
      anchor.cTrivialRowSumSlice →
      anchor.rowSumHasAllSixNonfixedRightChannels →
      bridge.adjacentAnchorSeesCTrivialSlice →
      bridge.rightDifferenceInvertibleOnNonfixedSlice →
      bridge.oppositeRawB0LeakCancels →
      target.nonfixedRightProjectorsCancel)
    (h_anchor : SatisfiesReducedAnchorFingerprint anchor)
    (h_bridge : SatisfiesAdjacentBridge bridge) :
    SatisfiesOldAdjacentAnchorTarget target := by
  rcases h_anchor with
    ⟨_h_full_row, h_row_sum, h_six_channels⟩
  rcases h_bridge with
    ⟨h_adjacent_sees, h_invertible, h_cancel⟩
  exact h_handoff
    h_row_sum h_six_channels h_adjacent_sees h_invertible h_cancel

theorem full_anchor_realization_is_still_required
    (anchor : ReducedAnchorFingerprint)
    (h_anchor : SatisfiesReducedAnchorFingerprint anchor) :
    anchor.fullPuncturedRightZeroRow := by
  exact h_anchor.left

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def p24ReducedAnchorRowSumCoefficient : Nat := p24COverEDegree - 1
def p24NonfixedRightProjectorCount : Nat := p24RightQuotientDegree - 1
def p24HarnessTaskCountAfterBridge : Nat := 221

theorem p24_reduced_anchor_row_sum_coefficient :
    p24ReducedAnchorRowSumCoefficient = 178 := by
  decide

theorem p24_nonfixed_right_projector_count :
    p24NonfixedRightProjectorCount = 6 := by
  decide

theorem p24_bridge_harness_task_count :
    p24HarnessTaskCountAfterBridge = 221 := by
  decide

end P24.TraceGcdReducedAnchorAdjacentBridgeGate
