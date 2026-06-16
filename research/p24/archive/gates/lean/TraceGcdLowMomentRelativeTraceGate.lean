/-!
Finite handoff for the low-moment relative-trace constructor target.

The Python toy verifies the identity in an embedded CM tower:
child power sums are relative traces of powers of the fine quotient-period
element.  This Lean gate records the downstream contract: constructing the
selected relative traces plus sparse-relation avoidance is sufficient to use
the low-moment selector in place of a full child polynomial.
-/

namespace P24.TraceGcdLowMomentRelativeTraceGate

structure SelectedRelativeTraces where
  traceCount : Nat
  constructedIntrinsically : Prop

structure SparseMomentAvoidance where
  tracesSelectChild : Prop

def RelativeTraceSelectorReady
    (traces : SelectedRelativeTraces)
    (avoidance : SparseMomentAvoidance) : Prop :=
  traces.constructedIntrinsically ∧
  avoidance.tracesSelectChild

theorem child_selection_from_relative_traces
    (traces : SelectedRelativeTraces)
    (avoidance : SparseMomentAvoidance)
    (h_ready : RelativeTraceSelectorReady traces avoidance) :
    traces.constructedIntrinsically ∧ avoidance.tracesSelectChild := by
  exact h_ready

def p24FirstLayerRelativeTraces : Nat := 4
def p24SecondLayerRelativeTraces : Nat := 26
def p24SelectedPathRelativeTraces : Nat :=
  p24FirstLayerRelativeTraces + p24SecondLayerRelativeTraces

def p24ParentFieldTraceCoefficients : Nat :=
  2 * p24FirstLayerRelativeTraces + 314 * p24SecondLayerRelativeTraces

theorem p24_selected_path_relative_traces :
    p24SelectedPathRelativeTraces = 30 := by
  decide

theorem p24_parent_field_trace_coefficients :
    p24ParentFieldTraceCoefficients = 8172 := by
  decide

end P24.TraceGcdLowMomentRelativeTraceGate
