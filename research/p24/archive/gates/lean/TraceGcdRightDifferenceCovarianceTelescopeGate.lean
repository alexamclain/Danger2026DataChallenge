/-!
Finite handoff gate for the p24 right-difference covariance-telescope target.

The arithmetic theorem remains external.  This file records the formal shape:

* adjacent right-difference traces telescope;
* shift-6 covariance plus one descended anchor makes all seven trace values
  equal;
* equality plus telescoping and invertibility of 7 forces all trace values
  to vanish.
-/

namespace P24.TraceGcdRightDifferenceCovarianceTelescopeGate

def AllZero {Index Value : Type} [Zero Value]
    (traceValue : Index → Value) : Prop :=
  ∀ index, traceValue index = 0

def AllEqual {Index Value : Type}
    (traceValue : Index → Value) : Prop :=
  ∃ common, ∀ index, traceValue index = common

def ShiftCovariant {Index Value : Type}
    (shift : Index → Index)
    (rho : Value → Value)
    (traceValue : Index → Value) : Prop :=
  ∀ index, traceValue (shift index) = rho (traceValue index)

def AnchorDescended {Index Value : Type}
    (anchor : Index)
    (rho : Value → Value)
    (traceValue : Index → Value) : Prop :=
  rho (traceValue anchor) = traceValue anchor

def TelescopesToZero {Value : Type} [Zero Value]
    (_traceValues : Value) : Prop :=
  _traceValues = 0

theorem all_equal_from_covariance_and_anchor
    {Index Value : Type}
    (shift : Index → Index)
    (rho : Value → Value)
    (anchor : Index)
    (traceValue : Index → Value)
    (h_covariant : ShiftCovariant shift rho traceValue)
    (h_anchor : AnchorDescended anchor rho traceValue)
    (h_cov_anchor_implies_equal :
      ShiftCovariant shift rho traceValue →
      AnchorDescended anchor rho traceValue →
      AllEqual traceValue) :
    AllEqual traceValue := by
  exact h_cov_anchor_implies_equal h_covariant h_anchor

theorem all_zero_from_equal_and_telescope
    {Index Value : Type} [Zero Value]
    (traceValue : Index → Value)
    (h_equal : AllEqual traceValue)
    (telescope : Prop)
    (h_equal_telescope_implies_zero :
      AllEqual traceValue → telescope → AllZero traceValue)
    (h_telescope : telescope) :
    AllZero traceValue := by
  exact h_equal_telescope_implies_zero h_equal h_telescope

theorem all_zero_from_covariance_anchor_and_telescope
    {Index Value : Type} [Zero Value]
    (shift : Index → Index)
    (rho : Value → Value)
    (anchor : Index)
    (traceValue : Index → Value)
    (telescope : Prop)
    (h_covariant : ShiftCovariant shift rho traceValue)
    (h_anchor : AnchorDescended anchor rho traceValue)
    (h_cov_anchor_implies_equal :
      ShiftCovariant shift rho traceValue →
      AnchorDescended anchor rho traceValue →
      AllEqual traceValue)
    (h_equal_telescope_implies_zero :
      AllEqual traceValue → telescope → AllZero traceValue)
    (h_telescope : telescope) :
    AllZero traceValue := by
  exact h_equal_telescope_implies_zero
    (h_cov_anchor_implies_equal h_covariant h_anchor)
    h_telescope

def p24RightShift : Nat := 6
def p24RightQuotient : Nat := 7
def p24RelativeCosets : Nat := 8
def p24IndependentRightDifferences : Nat := 6

def p24RedundantAdjacentTraceEquations : Nat :=
  p24RightQuotient * p24RelativeCosets

def p24IndependentAdjacentTraceEquations : Nat :=
  p24IndependentRightDifferences * p24RelativeCosets

theorem p24_shift6_coprime_to_7 :
    Nat.gcd p24RightShift p24RightQuotient = 1 := by
  decide

theorem p24_redundant_adjacent_trace_equation_count :
    p24RedundantAdjacentTraceEquations = 56 := by
  decide

theorem p24_independent_adjacent_trace_equation_count :
    p24IndependentAdjacentTraceEquations = 48 := by
  decide

end P24.TraceGcdRightDifferenceCovarianceTelescopeGate
