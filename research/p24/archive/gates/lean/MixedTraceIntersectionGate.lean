/-!
Finite gate for the mixed trace-intersection theorem candidate.

The arithmetic theorem can be phrased as

    L ∩ W^perp = {0},

where W is the right-field span of the six mixed periods and the pairing is
the relative trace pairing.  This file checks the abstract logic:
if vanishing of all six pairings is equivalent to membership in W^perp, and
the intersection is trivial, then the six traces separate every nonzero
element of L.
-/

namespace P24.MixedTraceIntersectionGate

def InOrthogonal {Left Period Index Value : Type} [Zero Value]
    (pair : Left → Period → Value)
    (period : Index → Period)
    (lambda : Left) : Prop :=
  ∀ j, pair lambda (period j) = 0

def TrivialIntersection {Left : Type} [Zero Left]
    (inOrthogonal : Left → Prop) : Prop :=
  ∀ lambda, inOrthogonal lambda → lambda = 0

def Separates {Left Index Value : Type} [Zero Left] [Zero Value]
    (traceMap : Left → Index → Value) : Prop :=
  ∀ lambda, lambda ≠ 0 → ∃ j, traceMap lambda j ≠ 0

theorem separates_from_trivial_intersection
    {Left Period Index Value : Type} [Zero Left] [Zero Value]
    (pair : Left → Period → Value)
    (period : Index → Period)
    (h_trivial :
      TrivialIntersection (InOrthogonal pair period)) :
    Separates (fun lambda j => pair lambda (period j)) := by
  intro lambda h_nonzero
  by_cases h_sep : ∃ j, pair lambda (period j) ≠ 0
  · exact h_sep
  · have h_orth : InOrthogonal pair period lambda := by
      have h_orth_again : InOrthogonal pair period lambda := by
        intro j
        by_cases h_value : pair lambda (period j) = 0
        · exact h_value
        · exact False.elim (h_sep ⟨j, h_value⟩)
      exact h_orth_again
    have h_zero : lambda = 0 := h_trivial lambda h_orth
    exact False.elim (h_nonzero h_zero)

theorem trivial_intersection_from_separates
    {Left Period Index Value : Type} [Zero Left] [Zero Value]
    (pair : Left → Period → Value)
    (period : Index → Period)
    (h_separates :
      Separates (fun lambda j => pair lambda (period j))) :
    TrivialIntersection (InOrthogonal pair period) := by
  intro lambda h_orth
  by_cases h_zero : lambda = 0
  · exact h_zero
  · rcases h_separates lambda h_zero with ⟨j, h_nonzero_value⟩
    exact False.elim (h_nonzero_value (h_orth j))

end P24.MixedTraceIntersectionGate
