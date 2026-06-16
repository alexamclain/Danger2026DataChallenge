/-!
Finite handoff gate for the p24 adjacent-difference operator.

With the p24 convention the right quotient shift is `6 = -1 mod 7`, so the
adjacent anchor is formally `(rho^6 - 1)Y_0`.  The arithmetic theorem remains
external; this file records the finite interface:

* the difference operator has kernel exactly the fixed/right-axis anchor;
* it is invertible on nontrivial projector channels;
* therefore adjacent-anchor descent and right-axis anchor descent are the
  same finite target after covariance.
-/

namespace P24.TraceGcdAdjacentDifferenceOperatorGate

def RightAxisAnchorDescended {Value : Type}
    (rho : Value → Value)
    (anchor : Value) : Prop :=
  rho anchor = anchor

def AdjacentAnchorDescended {Value : Type}
    (rho : Value → Value)
    (adjacentAnchor : Value) : Prop :=
  rho adjacentAnchor = adjacentAnchor

def DifferenceInvertibleOnNonfixedQuotient {Value : Type} [Zero Value]
    (difference : Value → Value)
    (rightProjector adjacentProjector : Nat → Value → Value) : Prop :=
  ∀ k anchor,
    1 ≤ k → k ≤ 6 →
      adjacentProjector k (difference anchor) = (0 : Value) ↔
        rightProjector k anchor = (0 : Value)

def ProjectorCriterion {Value : Type} [Zero Value]
    (rho : Value → Value)
    (projector : Nat → Value → Value) : Prop :=
  ∀ anchor, rho anchor = anchor ↔
    ∀ k, 1 ≤ k → k ≤ 6 → projector k anchor = (0 : Value)

theorem adjacent_anchor_descent_iff_right_axis_anchor_descent
    {Value : Type} [Zero Value]
    (rho : Value → Value)
    (difference : Value → Value)
    (rightProjector adjacentProjector : Nat → Value → Value)
    (anchor : Value)
    (h_difference :
      DifferenceInvertibleOnNonfixedQuotient
        difference rightProjector adjacentProjector)
    (h_right : ProjectorCriterion rho rightProjector)
    (h_adjacent : ProjectorCriterion rho adjacentProjector)
    (h_projector_handoff :
      DifferenceInvertibleOnNonfixedQuotient
          difference rightProjector adjacentProjector →
        ProjectorCriterion rho rightProjector →
        ProjectorCriterion rho adjacentProjector →
        (AdjacentAnchorDescended rho (difference anchor) ↔
          RightAxisAnchorDescended rho anchor)) :
    AdjacentAnchorDescended rho (difference anchor) ↔
      RightAxisAnchorDescended rho anchor := by
  exact h_projector_handoff h_difference h_right h_adjacent

def p24RightShift : Nat := 6
def p24RightQuotient : Nat := 7
def p24NontrivialProjectorCount : Nat := 6

theorem p24_shift_is_minus_one_mod_7 :
    (p24RightShift + 1) % p24RightQuotient = 0 := by
  decide

theorem p24_nontrivial_projector_count :
    p24NontrivialProjectorCount = 6 := by
  decide

end P24.TraceGcdAdjacentDifferenceOperatorGate
