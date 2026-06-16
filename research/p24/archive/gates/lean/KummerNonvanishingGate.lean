/-!
Finite gate for Kummer nonvanishing payloads.

For a cyclic prime relative layer, a primitive relative trace `T` may be
replaced by a Kummer power `K=T^r`.  This file does not formalize powers.  It
records the finite interface needed by the p24 trace-GCD route:

* if a zero trace forces the corresponding Kummer payload to vanish, and
* the Kummer payload is nonzero,
* then the trace is nonzero.

Together with an evaluation/trace identification, this turns Kummer p-units
into nonzero cyclic evaluations.
-/

namespace P24.KummerNonvanishingGate

def PowerDetectsTraceZero {Index Scalar : Type} [Zero Scalar]
    (trace kummer : Index → Scalar) : Prop :=
  ∀ i, trace i = 0 → kummer i = 0

def EvaluationsMatchTraces {EvalIndex TraceIndex Value : Type}
    (toTrace : EvalIndex → TraceIndex)
    (eval : EvalIndex → Value)
    (trace : TraceIndex → Value) : Prop :=
  ∀ i, eval i = trace (toTrace i)

theorem traces_nonzero_from_kummer
    {Index Scalar : Type} [Zero Scalar]
    (trace kummer : Index → Scalar)
    (h_detects : PowerDetectsTraceZero trace kummer)
    (h_kummer_nonzero : ∀ i, kummer i ≠ 0) :
    ∀ i, trace i ≠ 0 := by
  intro i h_trace_zero
  exact h_kummer_nonzero i (h_detects i h_trace_zero)

theorem evaluations_nonzero_from_kummer
    {EvalIndex TraceIndex Scalar : Type} [Zero Scalar]
    (toTrace : EvalIndex → TraceIndex)
    (eval : EvalIndex → Scalar)
    (trace kummer : TraceIndex → Scalar)
    (h_match : EvaluationsMatchTraces toTrace eval trace)
    (h_detects : PowerDetectsTraceZero trace kummer)
    (h_kummer_nonzero : ∀ i, kummer i ≠ 0) :
    ∀ i, eval i ≠ 0 := by
  intro i h_eval_zero
  have h_trace_nonzero :
      trace (toTrace i) ≠ 0 :=
    traces_nonzero_from_kummer trace kummer h_detects
      h_kummer_nonzero (toTrace i)
  exact h_trace_nonzero (by
    rw [← h_match i]
    exact h_eval_zero)

theorem selected_good_from_kummer
    {EvalIndex TraceIndex Scalar : Type} [Zero Scalar]
    (toTrace : EvalIndex → TraceIndex)
    (eval : EvalIndex → Scalar)
    (trace kummer : TraceIndex → Scalar)
    (Good : EvalIndex → Prop)
    (selected : EvalIndex)
    (h_match : EvaluationsMatchTraces toTrace eval trace)
    (h_detects : PowerDetectsTraceZero trace kummer)
    (h_kummer_nonzero : ∀ i, kummer i ≠ 0)
    (h_eval_to_good : ∀ i, eval i ≠ 0 → Good i) :
    Good selected := by
  exact h_eval_to_good selected
    (evaluations_nonzero_from_kummer toTrace eval trace kummer
      h_match h_detects h_kummer_nonzero selected)

end P24.KummerNonvanishingGate
