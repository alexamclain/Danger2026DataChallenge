/-!
Finite gate for the mixed trace-dual theorem candidate.

The arithmetic theorem now says that six relative traces

    lambda |-> (Tr_{E/R}(lambda * S_j))_j

separate every nonzero lambda in the left character field.  This file checks
the abstract finite logic connecting that separation statement to the
coordinate-span formulation.
-/

namespace P24.MixedTraceDualGate

def FamilySeparates {Lambda Index Scalar : Type} [Zero Lambda] [Zero Scalar]
    (pair : Lambda → Index → Scalar) : Prop :=
  ∀ lambda, lambda ≠ 0 → ∃ i, pair lambda i ≠ 0

def NoCommonTraceKernel {Lambda RightIndex RightValue : Type}
    [Zero Lambda] [Zero RightValue]
    (traceMap : Lambda → RightIndex → RightValue) : Prop :=
  ∀ lambda, lambda ≠ 0 → ∃ j, traceMap lambda j ≠ 0

theorem family_separates_from_no_common_trace_kernel
    {Lambda RightIndex RightValue : Type}
    [Zero Lambda] [Zero RightValue]
    (traceMap : Lambda → RightIndex → RightValue)
    (h_no_kernel : NoCommonTraceKernel traceMap) :
    FamilySeparates traceMap := by
  intro lambda h_nonzero
  exact h_no_kernel lambda h_nonzero

theorem no_common_trace_kernel_from_family_separates
    {Lambda RightIndex RightValue : Type}
    [Zero Lambda] [Zero RightValue]
    (traceMap : Lambda → RightIndex → RightValue)
    (h_separates : FamilySeparates traceMap) :
    NoCommonTraceKernel traceMap := by
  intro lambda h_nonzero
  exact h_separates lambda h_nonzero

theorem no_kernel_as_contrapositive
    {Lambda RightIndex RightValue : Type}
    [Zero Lambda] [Zero RightValue]
    (traceMap : Lambda → RightIndex → RightValue)
    (h_no_kernel : NoCommonTraceKernel traceMap)
    (lambda : Lambda)
    (h_all_zero : ∀ j, traceMap lambda j = 0) :
    lambda = 0 := by
  by_cases h_zero : lambda = 0
  · exact h_zero
  · rcases h_no_kernel lambda h_zero with ⟨j, h_value_nonzero⟩
    exact False.elim (h_value_nonzero (h_all_zero j))

end P24.MixedTraceDualGate
