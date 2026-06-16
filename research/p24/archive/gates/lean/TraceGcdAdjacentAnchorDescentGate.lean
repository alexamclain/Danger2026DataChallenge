/-!
Finite handoff gate for the p24 adjacent-trace anchor descent target.

The arithmetic theorem remains external.  This file records the formal
replacement of the remaining anchor condition by six nontrivial rho-projector
vanishings on the single trace value

  T_0 = Tr(P_0(zeta_n)).

Together with covariance and telescoping, that anchor descent is the final
formal input needed for the 48 compressed right-difference equations.
-/

namespace P24.TraceGcdAdjacentAnchorDescentGate

def AnchorDescended {Value : Type}
    (rho : Value → Value)
    (anchor : Value) : Prop :=
  rho anchor = anchor

def NontrivialProjectorsZero {Value : Type} [Zero Value]
    (projector : Nat → Value → Value)
    (anchor : Value) : Prop :=
  ∀ k, 1 ≤ k → k ≤ 6 → projector k anchor = 0

def ProjectorCriterion {Value : Type} [Zero Value]
    (rho : Value → Value)
    (projector : Nat → Value → Value) : Prop :=
  ∀ anchor,
    AnchorDescended rho anchor ↔ NontrivialProjectorsZero projector anchor

theorem anchor_descended_from_projector_vanishings
    {Value : Type} [Zero Value]
    (rho : Value → Value)
    (projector : Nat → Value → Value)
    (anchor : Value)
    (h_criterion : ProjectorCriterion rho projector)
    (h_projectors : NontrivialProjectorsZero projector anchor) :
    AnchorDescended rho anchor := by
  exact (h_criterion anchor).2 h_projectors

theorem projector_vanishings_from_anchor_descended
    {Value : Type} [Zero Value]
    (rho : Value → Value)
    (projector : Nat → Value → Value)
    (anchor : Value)
    (h_criterion : ProjectorCriterion rho projector)
    (h_anchor : AnchorDescended rho anchor) :
    NontrivialProjectorsZero projector anchor := by
  exact (h_criterion anchor).1 h_anchor

def ShiftCovariant {Index Value : Type}
    (shift : Index → Index)
    (rho : Value → Value)
    (traceValue : Index → Value) : Prop :=
  ∀ index, traceValue (shift index) = rho (traceValue index)

def AllZero {Index Value : Type} [Zero Value]
    (traceValue : Index → Value) : Prop :=
  ∀ index, traceValue index = 0

theorem all_zero_from_covariance_projector_anchor_and_telescope
    {Index Value : Type} [Zero Value]
    (shift : Index → Index)
    (rho : Value → Value)
    (projector : Nat → Value → Value)
    (anchorIndex : Index)
    (traceValue : Index → Value)
    (telescope : Prop)
    (h_covariant : ShiftCovariant shift rho traceValue)
    (h_projectors : NontrivialProjectorsZero projector (traceValue anchorIndex))
    (h_criterion : ProjectorCriterion rho projector)
    (h_telescope : telescope)
    (h_cov_anchor_telescope_implies_zero :
      ShiftCovariant shift rho traceValue →
      AnchorDescended rho (traceValue anchorIndex) →
      telescope →
      AllZero traceValue) :
    AllZero traceValue := by
  exact h_cov_anchor_telescope_implies_zero
    h_covariant
    ((h_criterion (traceValue anchorIndex)).2 h_projectors)
    h_telescope

def p24RawHcosetEquations : Nat := 156 * 7
def p24CompressedRightDifferenceEquations : Nat := 6 * 8
def p24SingleAdjacentAnchorProjectors : Nat := 6

theorem p24_raw_hcoset_equation_count :
    p24RawHcosetEquations = 1092 := by
  decide

theorem p24_compressed_right_difference_equation_count :
    p24CompressedRightDifferenceEquations = 48 := by
  decide

theorem p24_single_adjacent_anchor_projector_count :
    p24SingleAdjacentAnchorProjectors = 6 := by
  decide

end P24.TraceGcdAdjacentAnchorDescentGate
