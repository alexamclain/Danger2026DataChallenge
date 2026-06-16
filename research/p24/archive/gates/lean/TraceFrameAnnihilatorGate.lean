/-!
Finite gate for trace-frame annihilator certificates.

The arithmetic target can be phrased as:

* the trace-frame kernel is contained in a fixed annihilator subspace;
* the projected axis image avoids that annihilator.

This file checks the abstract implication from those assumptions to
injectivity of the projected axis evaluation.
-/

namespace P24.TraceFrameAnnihilatorGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

theorem injective_from_trace_annihilator_avoidance
    {Source Factor TraceCoordinates : Type}
    [Zero Source] [Zero TraceCoordinates]
    (eval : Source → Factor)
    (sourceDiff : Source → Source → Source)
    (factorDiff : Factor → Factor → Factor)
    (traceFrame : Factor → TraceCoordinates)
    (Annihilator : Factor → Prop)
    (h_eval_diff :
      ∀ left right,
        eval (sourceDiff left right) =
          factorDiff (eval left) (eval right))
    (h_source_diff_zero :
      ∀ left right, sourceDiff left right = 0 → left = right)
    (h_trace_diff_zero :
      ∀ left right,
        traceFrame left = traceFrame right →
          traceFrame (factorDiff left right) = 0)
    (h_kernel_into_annihilator :
      ∀ value, traceFrame value = 0 → Annihilator value)
    (h_axis_avoids_annihilator :
      ∀ source, Annihilator (eval source) → source = 0) :
    Injective (fun source => traceFrame (eval source)) →
      Injective eval := by
  intro _ left right h_eval_eq
  apply h_source_diff_zero left right
  apply h_axis_avoids_annihilator
  apply h_kernel_into_annihilator
  calc
    traceFrame (eval (sourceDiff left right))
        =
          traceFrame (factorDiff (eval left) (eval right)) := by
            rw [h_eval_diff left right]
    _ = 0 := h_trace_diff_zero (eval left) (eval right) (by rw [h_eval_eq])

theorem trace_frame_injective_from_annihilator_avoidance
    {Source Factor TraceCoordinates : Type}
    [Zero Source] [Zero TraceCoordinates]
    (eval : Source → Factor)
    (sourceDiff : Source → Source → Source)
    (factorDiff : Factor → Factor → Factor)
    (traceFrame : Factor → TraceCoordinates)
    (Annihilator : Factor → Prop)
    (h_eval_diff :
      ∀ left right,
        eval (sourceDiff left right) =
          factorDiff (eval left) (eval right))
    (h_source_diff_zero :
      ∀ left right, sourceDiff left right = 0 → left = right)
    (h_trace_diff_zero :
      ∀ left right,
        traceFrame left = traceFrame right →
          traceFrame (factorDiff left right) = 0)
    (h_kernel_into_annihilator :
      ∀ value, traceFrame value = 0 → Annihilator value)
    (h_axis_avoids_annihilator :
      ∀ source, Annihilator (eval source) → source = 0) :
    Injective (fun source => traceFrame (eval source)) := by
  intro left right h_trace_eq
  apply h_source_diff_zero left right
  apply h_axis_avoids_annihilator
  apply h_kernel_into_annihilator
  calc
    traceFrame (eval (sourceDiff left right))
        =
          traceFrame (factorDiff (eval left) (eval right)) := by
            rw [h_eval_diff left right]
    _ = 0 := h_trace_diff_zero (eval left) (eval right) h_trace_eq

end P24.TraceFrameAnnihilatorGate
