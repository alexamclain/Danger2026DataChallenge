/-!
Finite handoff gate for the p24 adjacent right-difference trace target.

The arithmetic theorem remains external.  This file records the contract:

* each adjacent right-coset difference defines a relative polynomial `P_i`;
* Gaussian-period inversion identifies balance on the eight relative `<p>`
  cosets with trace zero of `P_i(zeta_n)` to the degree-8 decomposition field;
* seven adjacent differences give `56` redundant equations, with `48`
  independent equations after the cyclic dependency.
-/

namespace P24.TraceGcdRightDifferenceTraceGate

def AllAdjacentTraceZero {RightDiff : Type}
    (traceZero : RightDiff → Prop) : Prop :=
  ∀ rightDiff, traceZero rightDiff

def AllAdjacentCosetBalanced {RightDiff RelativeCoset : Type}
    (balanced : RightDiff → RelativeCoset → Prop) : Prop :=
  ∀ rightDiff relative, balanced rightDiff relative

theorem adjacent_balance_from_trace_zero
    {RightDiff RelativeCoset : Type}
    (traceZero : RightDiff → Prop)
    (balanced : RightDiff → RelativeCoset → Prop)
    (h_trace_implies_balance :
      AllAdjacentTraceZero traceZero → AllAdjacentCosetBalanced balanced)
    (h_trace : AllAdjacentTraceZero traceZero) :
    AllAdjacentCosetBalanced balanced := by
  exact h_trace_implies_balance h_trace

theorem adjacent_trace_zero_from_balance
    {RightDiff RelativeCoset : Type}
    (traceZero : RightDiff → Prop)
    (balanced : RightDiff → RelativeCoset → Prop)
    (h_balance_implies_trace :
      AllAdjacentCosetBalanced balanced → AllAdjacentTraceZero traceZero)
    (h_balance : AllAdjacentCosetBalanced balanced) :
    AllAdjacentTraceZero traceZero := by
  exact h_balance_implies_trace h_balance

theorem adjacent_trace_zero_iff_balance
    {RightDiff RelativeCoset : Type}
    (traceZero : RightDiff → Prop)
    (balanced : RightDiff → RelativeCoset → Prop)
    (h_trace_implies_balance :
      AllAdjacentTraceZero traceZero → AllAdjacentCosetBalanced balanced)
    (h_balance_implies_trace :
      AllAdjacentCosetBalanced balanced → AllAdjacentTraceZero traceZero) :
    AllAdjacentTraceZero traceZero ↔ AllAdjacentCosetBalanced balanced := by
  constructor
  · exact h_trace_implies_balance
  · exact h_balance_implies_trace

def p24RightDifferences : Nat := 7
def p24IndependentRightDifferences : Nat := 6
def p24RelativeCosets : Nat := 8

def p24RedundantAdjacentTraceEquations : Nat :=
  p24RightDifferences * p24RelativeCosets

def p24IndependentAdjacentTraceEquations : Nat :=
  p24IndependentRightDifferences * p24RelativeCosets

theorem p24_redundant_adjacent_trace_equation_count :
    p24RedundantAdjacentTraceEquations = 56 := by
  decide

theorem p24_independent_adjacent_trace_equation_count :
    p24IndependentAdjacentTraceEquations = 48 := by
  decide

end P24.TraceGcdRightDifferenceTraceGate
