/-!
Finite handoff gate for the reduced-anchor C-slice decomposition.

The Python gate

  p24/trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate.py

checks the explicit Fourier calculation.  This Lean file records the contract:

* the reduced anchor splits into a `C/E`-trivial row-sum slice and a
  `C/E`-nontrivial residual;
* the old adjacent-anchor theorem sees only the trivial slice;
* the residual is invisible to that theorem and still has to be realized by
  the selected CM/Lang degenerate-anchor unit.
-/

namespace P24.TraceGcdReducedAnchorSliceDecompositionGate

structure ReducedAnchorSliceDecomposition where
  reconstructsFullPuncturedRow : Prop
  cTrivialSliceHasB0Profile : Prop
  cNontrivialSliceHasNoB0Profile : Prop
  cNontrivialSliceHasNonzeroCProfile : Prop
  cNontrivialSliceHasZeroRowSums : Prop

def SatisfiesSliceDecomposition
    (decomp : ReducedAnchorSliceDecomposition) : Prop :=
  decomp.reconstructsFullPuncturedRow ∧
  decomp.cTrivialSliceHasB0Profile ∧
  decomp.cNontrivialSliceHasNoB0Profile ∧
  decomp.cNontrivialSliceHasNonzeroCProfile ∧
  decomp.cNontrivialSliceHasZeroRowSums

structure AdjacentAnchorVisibility where
  seesCTrivialSlice : Prop
  doesNotSeeCNontrivialSlice : Prop

def SatisfiesAdjacentAnchorVisibility
    (visibility : AdjacentAnchorVisibility) : Prop :=
  visibility.seesCTrivialSlice ∧
  visibility.doesNotSeeCNontrivialSlice

structure RemainingCMUnitTarget where
  mustRealizeCNontrivialResidual : Prop
  mustRealizeFullPuncturedRow : Prop

def SatisfiesRemainingCMUnitTarget
    (target : RemainingCMUnitTarget) : Prop :=
  target.mustRealizeCNontrivialResidual ∧
  target.mustRealizeFullPuncturedRow

theorem remaining_unit_target_from_slice_decomposition
    (decomp : ReducedAnchorSliceDecomposition)
    (visibility : AdjacentAnchorVisibility)
    (target : RemainingCMUnitTarget)
    (h_handoff :
      decomp.reconstructsFullPuncturedRow →
      decomp.cNontrivialSliceHasNoB0Profile →
      decomp.cNontrivialSliceHasNonzeroCProfile →
      decomp.cNontrivialSliceHasZeroRowSums →
      visibility.seesCTrivialSlice →
      visibility.doesNotSeeCNontrivialSlice →
      target.mustRealizeCNontrivialResidual ∧
        target.mustRealizeFullPuncturedRow)
    (h_decomp : SatisfiesSliceDecomposition decomp)
    (h_visibility : SatisfiesAdjacentAnchorVisibility visibility) :
    SatisfiesRemainingCMUnitTarget target := by
  rcases h_decomp with
    ⟨h_reconstructs, _h_triv, h_no_b0, h_nonzero_c, h_zero_rows⟩
  rcases h_visibility with ⟨h_sees, h_not_seen⟩
  exact h_handoff
    h_reconstructs h_no_b0 h_nonzero_c h_zero_rows h_sees h_not_seen

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def p24OldAdjacentB0Channels : Nat := p24RightQuotientDegree - 1
def p24RemainingCNontrivialChannels : Nat :=
  p24RightQuotientDegree * (p24COverEDegree - 1)
def p24HarnessTaskCountAfterSliceGate : Nat := 223

theorem p24_old_adjacent_b0_channels :
    p24OldAdjacentB0Channels = 6 := by
  decide

theorem p24_remaining_c_nontrivial_channels :
    p24RemainingCNontrivialChannels = 1246 := by
  decide

theorem p24_slice_gate_harness_task_count :
    p24HarnessTaskCountAfterSliceGate = 223 := by
  decide

end P24.TraceGcdReducedAnchorSliceDecompositionGate
