/-!
Finite gate for the residual-tail trace-frame certificate.

After the first trace-frame blocks, the p24 leading Plucker coordinate reduces
to a residual-kernel test:

  prefix coordinates vanish
  selected tail coordinates vanish
  --------------------------------
  the axis weight is zero.

This file checks only the abstract implication from that residual-tail
avoidance statement to injectivity of the selected leading coordinate map.
The arithmetic input remains the p24 p-unit/nonvanishing theorem for the
actual CM residual tail determinant.
-/

namespace P24.TraceFrameResidualTailGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

structure SelectedCoordinates (Prefix TailHead : Type) where
  pref : Prefix
  tailHead : TailHead

theorem selected_injective_from_residual_tail_avoidance
    {Source Factor Prefix TailHead : Type}
    [Zero Source] [Zero Prefix] [Zero TailHead]
    (eval : Source → Factor)
    (sourceDiff : Source → Source → Source)
    (factorDiff : Factor → Factor → Factor)
    (pref : Factor → Prefix)
    (tailHead : Factor → TailHead)
    (h_eval_diff :
      ∀ left right,
        eval (sourceDiff left right) =
          factorDiff (eval left) (eval right))
    (h_source_diff_zero :
      ∀ left right, sourceDiff left right = 0 → left = right)
    (h_prefix_diff_zero :
      ∀ left right,
        pref left = pref right →
          pref (factorDiff left right) = 0)
    (h_tail_diff_zero :
      ∀ left right,
        tailHead left = tailHead right →
          tailHead (factorDiff left right) = 0)
    (h_residual_tail_avoidance :
      ∀ source,
        pref (eval source) = 0 →
          tailHead (eval source) = 0 →
            source = 0) :
    Injective
      (fun source : Source =>
        (SelectedCoordinates.mk
          (pref (eval source))
          (tailHead (eval source)) :
            SelectedCoordinates Prefix TailHead)) := by
  intro left right h_selected_eq
  apply h_source_diff_zero left right
  apply h_residual_tail_avoidance
  · calc
      pref (eval (sourceDiff left right))
          =
            pref (factorDiff (eval left) (eval right)) := by
              rw [h_eval_diff left right]
      _ = 0 := by
            apply h_prefix_diff_zero
            exact congrArg SelectedCoordinates.pref h_selected_eq
  · calc
      tailHead (eval (sourceDiff left right))
          =
            tailHead (factorDiff (eval left) (eval right)) := by
              rw [h_eval_diff left right]
      _ = 0 := by
            apply h_tail_diff_zero
            exact congrArg SelectedCoordinates.tailHead h_selected_eq

theorem factor_injective_from_selected_coordinates
    {Source Factor Prefix TailHead : Type}
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (tailHead : Factor → TailHead)
    (h_selected_injective :
      Injective
        (fun source : Source =>
          (SelectedCoordinates.mk
            (pref (eval source))
            (tailHead (eval source)) :
              SelectedCoordinates Prefix TailHead))) :
    Injective eval := by
  intro left right h_eval_eq
  apply h_selected_injective
  exact congrArg
    (fun value =>
      (SelectedCoordinates.mk
        (pref value)
        (tailHead value) :
          SelectedCoordinates Prefix TailHead))
    h_eval_eq

def DisjointZero {C : Type} [Zero C] (U T : C → Prop) : Prop :=
  ∀ value, U value → T value → value = 0

def KernelIs {C Ann : Type} [Zero Ann] (ann : C → Ann) (T : C → Prop) : Prop :=
  ∀ value, ann value = 0 ↔ T value

def TrivialKernelOn {C Ann : Type} [Zero C] [Zero Ann]
    (ann : C → Ann) (U : C → Prop) : Prop :=
  ∀ value, U value → ann value = 0 → value = 0

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def CommonKernelTrivial {C Ann : Type} [Zero C] [Zero Ann]
    (annU annT : C → Ann) : Prop :=
  ∀ value, annU value = 0 → annT value = 0 → value = 0

def LinearizedResultantCriterion {C Ann Scalar : Type}
    [Zero C] [Zero Ann] [Zero Scalar]
    (annU annT : C → Ann)
    (resultant : Scalar) : Prop :=
  resultant ≠ 0 → CommonKernelTrivial annU annT

def SelectedTailOperatorCriterion
    {Source Factor Prefix C Ann Scalar : Type}
    [Zero Source] [Zero Prefix] [Zero Ann] [Zero Scalar]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (tailCoeff : Factor → C)
    (annTail : C → Ann)
    (resultant : Scalar) : Prop :=
  resultant ≠ 0 →
    ∀ source,
      pref (eval source) = 0 →
        annTail (tailCoeff (eval source)) = 0 →
          source = 0

theorem disjoint_from_annihilator_trivial_on_U
    {C Ann : Type} [Zero C] [Zero Ann]
    (ann : C → Ann)
    (U T : C → Prop)
    (h_kernel : KernelIs ann T)
    (h_trivial : TrivialKernelOn ann U) :
    DisjointZero U T := by
  intro value h_U h_T
  exact h_trivial value h_U ((h_kernel value).2 h_T)

theorem common_kernel_trivial_from_resultant_punit
    {C Ann Scalar : Type} [Zero C] [Zero Ann] [Zero Scalar]
    (annU annT : C → Ann)
    (resultant resultantInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_resultant :
      LinearizedResultantCriterion annU annT resultant)
    (h_payload :
      UnitPayload resultant resultantInv UnitRel) :
    CommonKernelTrivial annU annT :=
  h_resultant (h_unit_nonzero resultant resultantInv h_payload)

theorem disjoint_from_linearized_resultant_punit
    {C Ann Scalar : Type} [Zero C] [Zero Ann] [Zero Scalar]
    (annU annT : C → Ann)
    (U T : C → Prop)
    (resultant resultantInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_kernel_U : KernelIs annU U)
    (h_kernel_T : KernelIs annT T)
    (h_resultant :
      LinearizedResultantCriterion annU annT resultant)
    (h_payload :
      UnitPayload resultant resultantInv UnitRel) :
    DisjointZero U T := by
  intro value h_U h_T
  exact
    common_kernel_trivial_from_resultant_punit
      annU annT resultant resultantInv UnitRel
      h_unit_nonzero h_resultant h_payload value
      ((h_kernel_U value).2 h_U)
      ((h_kernel_T value).2 h_T)

theorem residual_tail_avoidance_from_disjoint_tail_subspaces
    {Source Factor Prefix C : Type}
    [Zero Source] [Zero Prefix] [Zero C]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (tailCoeff : Factor → C)
    (tailHeadZero : Factor → Prop)
    (U T : C → Prop)
    (h_tail_in_U :
      ∀ source,
        pref (eval source) = 0 →
          U (tailCoeff (eval source)))
    (h_tail_head_into_T :
      ∀ source,
        tailHeadZero (eval source) →
          T (tailCoeff (eval source)))
    (h_disjoint : DisjointZero U T)
    (h_tail_coeff_zero_to_source_zero :
      ∀ source,
        pref (eval source) = 0 →
          tailCoeff (eval source) = 0 →
            source = 0) :
    ∀ source,
      pref (eval source) = 0 →
        tailHeadZero (eval source) →
          source = 0 := by
  intro source h_pref h_tail
  apply h_tail_coeff_zero_to_source_zero source h_pref
  apply h_disjoint
  · exact h_tail_in_U source h_pref
  · exact h_tail_head_into_T source h_tail

theorem residual_tail_avoidance_from_annihilator_gate
    {Source Factor Prefix C Ann : Type}
    [Zero Source] [Zero Prefix] [Zero C] [Zero Ann]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (tailCoeff : Factor → C)
    (tailHeadZero : Factor → Prop)
    (annTail : C → Ann)
    (U T : C → Prop)
    (h_kernel : KernelIs annTail T)
    (h_trivial : TrivialKernelOn annTail U)
    (h_tail_in_U :
      ∀ source,
        pref (eval source) = 0 →
          U (tailCoeff (eval source)))
    (h_tail_head_into_T :
      ∀ source,
        tailHeadZero (eval source) →
          T (tailCoeff (eval source)))
    (h_tail_coeff_zero_to_source_zero :
      ∀ source,
        pref (eval source) = 0 →
          tailCoeff (eval source) = 0 →
            source = 0) :
    ∀ source,
      pref (eval source) = 0 →
        tailHeadZero (eval source) →
          source = 0 := by
  apply residual_tail_avoidance_from_disjoint_tail_subspaces
    eval pref tailCoeff tailHeadZero U T
  · exact h_tail_in_U
  · exact h_tail_head_into_T
  · exact disjoint_from_annihilator_trivial_on_U
      annTail U T h_kernel h_trivial
  · exact h_tail_coeff_zero_to_source_zero

theorem residual_tail_avoidance_from_selected_tail_operator_punit
    {Source Factor Prefix C Ann Scalar : Type}
    [Zero Source] [Zero Prefix] [Zero Ann] [Zero Scalar]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (tailCoeff : Factor → C)
    (tailHeadZero : Factor → Prop)
    (annTail : C → Ann)
    (resultant resultantInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_tail_head_annihilates :
      ∀ factor,
        tailHeadZero factor →
          annTail (tailCoeff factor) = 0)
    (h_resultant :
      SelectedTailOperatorCriterion
        eval pref tailCoeff annTail resultant)
    (h_payload :
      UnitPayload resultant resultantInv UnitRel) :
    ∀ source,
      pref (eval source) = 0 →
        tailHeadZero (eval source) →
          source = 0 := by
  intro source h_pref h_tail
  exact h_resultant
    (h_unit_nonzero resultant resultantInv h_payload)
    source h_pref
    (h_tail_head_annihilates (eval source) h_tail)

theorem residual_tail_avoidance_from_linearized_resultant_punit
    {Source Factor Prefix C Ann Scalar : Type}
    [Zero Source] [Zero Prefix] [Zero C] [Zero Ann] [Zero Scalar]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (tailCoeff : Factor → C)
    (tailHeadZero : Factor → Prop)
    (annU annT : C → Ann)
    (U T : C → Prop)
    (resultant resultantInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_kernel_U : KernelIs annU U)
    (h_kernel_T : KernelIs annT T)
    (h_resultant :
      LinearizedResultantCriterion annU annT resultant)
    (h_payload :
      UnitPayload resultant resultantInv UnitRel)
    (h_tail_in_U :
      ∀ source,
        pref (eval source) = 0 →
          U (tailCoeff (eval source)))
    (h_tail_head_into_T :
      ∀ source,
        tailHeadZero (eval source) →
          T (tailCoeff (eval source)))
    (h_tail_coeff_zero_to_source_zero :
      ∀ source,
        pref (eval source) = 0 →
          tailCoeff (eval source) = 0 →
            source = 0) :
    ∀ source,
      pref (eval source) = 0 →
        tailHeadZero (eval source) →
          source = 0 := by
  apply residual_tail_avoidance_from_disjoint_tail_subspaces
    eval pref tailCoeff tailHeadZero U T
  · exact h_tail_in_U
  · exact h_tail_head_into_T
  · exact disjoint_from_linearized_resultant_punit
      annU annT U T resultant resultantInv UnitRel
      h_unit_nonzero h_kernel_U h_kernel_T h_resultant h_payload
  · exact h_tail_coeff_zero_to_source_zero

end P24.TraceFrameResidualTailGate
