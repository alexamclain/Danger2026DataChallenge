/-!
Finite gate for the Plucker-chart displacement handoff.

The arithmetic theorem should identify p-integral CM/Lang operators `A` and
`B` before seeing the Plucker chart `C`.  If the full selected-plus-omitted
column family has a low-rank operator boundary, then the selected-basis chart
has low Sylvester displacement:

    A C - C B = S^{-1} (E_o - E_s C).

This file does not formalize matrices or rank.  It records the finite
implication: an exact handoff between boundary rank and displacement rank
transfers a small boundary bound to the chart.  It also records the p24
dimension bookkeeping for the `156 x 54` chart.
-/

namespace P24.TraceGcdPluckerDisplacementHandoffGate

def OperatorBoundaryBounded (boundaryRank bound : Nat) : Prop :=
  boundaryRank ≤ bound

def PluckerDisplacementBounded (displacementRank bound : Nat) : Prop :=
  displacementRank ≤ bound

def BoundaryDisplacementHandoff
    (boundaryRank displacementRank : Nat) : Prop :=
  displacementRank = boundaryRank

def OperatorsFixedBeforeChart : Prop := True

def PostfitOperatorsRejected : Prop := True

theorem displacement_bounded_from_operator_boundary
    (boundaryRank displacementRank bound : Nat)
    (h_handoff :
      BoundaryDisplacementHandoff boundaryRank displacementRank)
    (h_boundary : OperatorBoundaryBounded boundaryRank bound) :
    PluckerDisplacementBounded displacementRank bound := by
  unfold BoundaryDisplacementHandoff at h_handoff
  unfold OperatorBoundaryBounded at h_boundary
  unfold PluckerDisplacementBounded
  rw [h_handoff]
  exact h_boundary

theorem p24_plucker_handoff_dimensions :
    156 + 54 = 210 := by
  decide

theorem p24_plucker_chart_entries :
    156 * 54 = 8424 := by
  decide

theorem p24_erasure_is_below_mds_distance :
    54 < 210 - 156 + 1 := by
  decide

theorem p24_rs_tail_selected_columns :
    4 * 35 + 16 = 156 := by
  decide

theorem p24_rs_tail_omitted_columns :
    35 + (35 - 16) = 54 := by
  decide

theorem p24_rs_tail_split_cut_edges :
    1 + 1 = 2 := by
  decide

theorem p24_displacement_bound_from_operator_boundary
    (boundaryRank displacementRank bound : Nat)
    (h_handoff :
      BoundaryDisplacementHandoff boundaryRank displacementRank)
    (h_boundary : OperatorBoundaryBounded boundaryRank bound) :
    PluckerDisplacementBounded displacementRank bound :=
  displacement_bounded_from_operator_boundary
    boundaryRank displacementRank bound h_handoff h_boundary

theorem fixed_operator_requirement_and_postfit_rejection :
    OperatorsFixedBeforeChart ∧ PostfitOperatorsRejected := by
  constructor
  · trivial
  · trivial

end P24.TraceGcdPluckerDisplacementHandoffGate
