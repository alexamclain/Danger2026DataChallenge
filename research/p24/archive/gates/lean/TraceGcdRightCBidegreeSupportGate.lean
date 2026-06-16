/-!
Finite handoff gate for the p24 right/C bidegree support target.

After B/C trace, final C/E trace zero for each nontrivial right projector is
equivalent to saying the bidegrees

  right nontrivial x C-trivial

vanish.  The arithmetic theorem remains external: the actual weighted
CM/Lang packet must avoid those forbidden bidegrees.
-/

namespace P24.TraceGcdRightCBidegreeSupportGate

def AllFinalTraceZero {RightChar : Type}
    (finalTraceZero : RightChar → Prop) : Prop :=
  ∀ rightChar, finalTraceZero rightChar

def AllForbiddenBidegreesZero {RightChar : Type}
    (forbiddenBidegreeZero : RightChar → Prop) : Prop :=
  ∀ rightChar, forbiddenBidegreeZero rightChar

theorem final_trace_zero_iff_forbidden_bidegrees_zero
    {RightChar : Type}
    (finalTraceZero forbiddenBidegreeZero : RightChar → Prop)
    (h_to_bidegree :
      ∀ rightChar, finalTraceZero rightChar → forbiddenBidegreeZero rightChar)
    (h_from_bidegree :
      ∀ rightChar, forbiddenBidegreeZero rightChar → finalTraceZero rightChar) :
    AllFinalTraceZero finalTraceZero ↔
      AllForbiddenBidegreesZero forbiddenBidegreeZero := by
  constructor
  · intro h_final rightChar
    exact h_to_bidegree rightChar (h_final rightChar)
  · intro h_bidegree rightChar
    exact h_from_bidegree rightChar (h_bidegree rightChar)

def p24RightQuotientDegree : Nat := 7
def p24COverEDegree : Nat := 179
def toyCOverEDegree : Nat := 5
def p24ForbiddenBidegreeCount : Nat := 6

theorem p24_no_nontrivial_hom_C7_to_C179 :
    Nat.gcd p24RightQuotientDegree p24COverEDegree = 1 := by
  decide

theorem toy_no_nontrivial_hom_C7_to_C5 :
    Nat.gcd p24RightQuotientDegree toyCOverEDegree = 1 := by
  decide

theorem p24_forbidden_bidegree_count :
    p24ForbiddenBidegreeCount = 6 := by
  decide

end P24.TraceGcdRightCBidegreeSupportGate
