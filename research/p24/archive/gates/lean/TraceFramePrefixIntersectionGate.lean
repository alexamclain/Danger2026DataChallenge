/-!
Finite gate for the prefix-intersection split of the trace-frame theorem.

The p24 prefix theorem is:

  A = constant + 2-axis + 157-axis
  B = 211-axis
  rank Top_2(A+B) is maximal.

After component-normality, the prefix kernel is exactly the forced
intersection of Top_2(A) and Top_2(B).  This file does not formalize
dimension.  It records the finite implication once that kernel is given by a
parametrization:

  prefix-zero source -> kernelLift(i)
  tail kills only i=0
  kernelLift(0)=0
  -----------------------------
  prefix + tail coordinates are injective.

The arithmetic input remains the p-unit theorem proving the prefix
intersection parametrization and the residual-tail nonvanishing.
-/

namespace P24.TraceFramePrefixIntersectionGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

structure SelectedCoordinates (Prefix Tail : Type) where
  pref : Prefix
  tail : Tail

theorem prefix_not_injective_from_nonzero_kernel_lift
    {Source Inter Prefix : Type}
    [Zero Source] [Zero Prefix]
    (pref : Source → Prefix)
    (kernelLift : Inter → Source)
    (inter : Inter)
    (h_pref_zero : pref 0 = 0)
    (h_lift_pref_zero : pref (kernelLift inter) = 0)
    (h_lift_nonzero : kernelLift inter ≠ 0) :
    ¬ Injective pref := by
  intro h_injective
  have h_same_prefix : pref (kernelLift inter) = pref 0 := by
    rw [h_lift_pref_zero, h_pref_zero]
  exact h_lift_nonzero (h_injective h_same_prefix)

theorem residual_avoidance_from_prefix_kernel_param
    {Source Inter Prefix Tail : Type}
    [Zero Source] [Zero Inter] [Zero Prefix] [Zero Tail]
    (pref : Source → Prefix)
    (tail : Source → Tail)
    (kernelLift : Inter → Source)
    (h_prefix_kernel_param :
      ∀ source, pref source = 0 →
        ∃ inter, source = kernelLift inter)
    (h_tail_kernel_trivial :
      ∀ inter, tail (kernelLift inter) = 0 → inter = 0)
    (h_kernel_zero : kernelLift 0 = 0) :
    ∀ source, pref source = 0 → tail source = 0 → source = 0 := by
  intro source h_pref h_tail
  rcases h_prefix_kernel_param source h_pref with ⟨inter, h_source⟩
  have h_inter_zero : inter = 0 := by
    apply h_tail_kernel_trivial
    rw [← h_source]
    exact h_tail
  calc
    source = kernelLift inter := h_source
    _ = kernelLift 0 := by rw [h_inter_zero]
    _ = 0 := h_kernel_zero

theorem selected_injective_from_prefix_intersection
    {Source Inter Prefix Tail : Type}
    [Zero Source] [Zero Inter] [Zero Prefix] [Zero Tail]
    (sourceDiff : Source → Source → Source)
    (pref : Source → Prefix)
    (tail : Source → Tail)
    (kernelLift : Inter → Source)
    (h_source_diff_zero :
      ∀ left right, sourceDiff left right = 0 → left = right)
    (h_pref_diff_zero :
      ∀ left right,
        pref left = pref right → pref (sourceDiff left right) = 0)
    (h_tail_diff_zero :
      ∀ left right,
        tail left = tail right → tail (sourceDiff left right) = 0)
    (h_prefix_kernel_param :
      ∀ source, pref source = 0 →
        ∃ inter, source = kernelLift inter)
    (h_tail_kernel_trivial :
      ∀ inter, tail (kernelLift inter) = 0 → inter = 0)
    (h_kernel_zero : kernelLift 0 = 0) :
    Injective
      (fun source : Source =>
        (SelectedCoordinates.mk
          (pref source)
          (tail source) :
            SelectedCoordinates Prefix Tail)) := by
  intro left right h_selected
  apply h_source_diff_zero left right
  apply residual_avoidance_from_prefix_kernel_param
    pref tail kernelLift
    h_prefix_kernel_param h_tail_kernel_trivial h_kernel_zero
  · apply h_pref_diff_zero
    exact congrArg SelectedCoordinates.pref h_selected
  · apply h_tail_diff_zero
    exact congrArg SelectedCoordinates.tail h_selected

structure AxisSplit (A B : Type) where
  left : A
  right : B

def AxisSplit.zero {A B : Type} [Zero A] [Zero B] : AxisSplit A B :=
  { left := 0, right := 0 }

theorem axis_split_zero_from_parts
    {A B : Type} [Zero A] [Zero B]
    (value : AxisSplit A B)
    (h_left : value.left = 0)
    (h_right : value.right = 0) :
    value = AxisSplit.zero := by
  cases value with
  | mk left right =>
      cases h_left
      cases h_right
      rfl

theorem prefix_kernel_param_from_component_lifts
    {Source Inter A B Prefix : Type}
    [Zero Prefix]
    (make : A → B → Source)
    (leftLift : Inter → A)
    (rightLift : Inter → B)
    (pref : Source → Prefix)
    (h_prefix_kernel :
      ∀ source, pref source = 0 →
        ∃ inter, source = make (leftLift inter) (rightLift inter)) :
    ∀ source, pref source = 0 →
      ∃ inter, source = make (leftLift inter) (rightLift inter) := by
  exact h_prefix_kernel

end P24.TraceFramePrefixIntersectionGate
