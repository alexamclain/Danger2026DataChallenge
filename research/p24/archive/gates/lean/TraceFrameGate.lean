/-!
Finite gate for twisted trace-frame certificates.

The new intermediate-field target replaces a coordinate projection from one
tensor factor by a short trace frame

    x ↦ (Tr(theta^0 x), ..., Tr(theta^(k-1) x)).

This file checks only the abstract implication: if that trace frame is
injective on the factor-projected axis evaluations, then the one-factor
projection, and therefore the tensor-extended axis evaluation, is injective.
-/

namespace P24.TraceFrameGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

theorem factor_injective_from_trace_frame
    {Source TensorAlgebra Factor TraceCoordinates : Type}
    (extEval : Source → TensorAlgebra)
    (factorProject : TensorAlgebra → Factor)
    (traceFrame : Factor → TraceCoordinates)
    (h_trace_frame_injective :
      Injective
        (fun source => traceFrame (factorProject (extEval source)))) :
    Injective (fun source => factorProject (extEval source)) := by
  intro left right h_factor
  apply h_trace_frame_injective
  exact congrArg traceFrame h_factor

theorem tensor_injective_from_trace_frame
    {Source TensorAlgebra Factor TraceCoordinates : Type}
    (extEval : Source → TensorAlgebra)
    (factorProject : TensorAlgebra → Factor)
    (traceFrame : Factor → TraceCoordinates)
    (h_trace_frame_injective :
      Injective
        (fun source => traceFrame (factorProject (extEval source)))) :
    Injective extEval := by
  intro left right h_eval
  have h_factor :
      factorProject (extEval left) = factorProject (extEval right) :=
    congrArg factorProject h_eval
  exact factor_injective_from_trace_frame
    extEval factorProject traceFrame h_trace_frame_injective h_factor

end P24.TraceFrameGate
