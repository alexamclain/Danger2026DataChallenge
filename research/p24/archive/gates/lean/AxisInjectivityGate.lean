/-!
Finite gate for the L1 axis-support injectivity theorem.

This file uses only Lean core.  It does not prove that the p24 CM packet
evaluation map is injective.  It checks the finite logic behind the refined
target:

* the axis coefficient space contains the L1 coefficient function;
* a selected packet gives a linear/evaluation map from that axis space into
  the packet field;
* if that map is injective and L1 is not the zero coefficient function, then
  the selected L1 packet value is nonzero;
* if all-zero harmful packets force every axis evaluation to vanish, the
  nonzero L1 value rules out harmful vanishing.

For p24 the open arithmetic input is the injectivity of a 368-dimensional
base-field map into the degree-388430 Frobenius packet field.
-/

namespace P24.AxisInjectivityGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

def AllZero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u = 0

def PacketContentGood {α : Type} [Zero α] {m : Nat}
    (packet : Fin m → α) : Prop :=
  ¬ AllZero packet

def GlobalContentGood {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α) : Prop :=
  ∀ orbit, PacketContentGood (packet orbit)

theorem injective_eval_nonzero_of_weight_nonzero
    {Weight PacketField : Type} [Zero Weight] [Zero PacketField]
    (eval : Weight → PacketField)
    (h_eval_zero : eval 0 = 0)
    (h_injective : Injective eval)
    (weight : Weight)
    (h_weight_nonzero : weight ≠ 0) :
    eval weight ≠ 0 := by
  intro h_eval_weight_zero
  have h_same_eval : eval weight = eval 0 := by
    exact Eq.trans h_eval_weight_zero h_eval_zero.symm
  exact h_weight_nonzero (h_injective h_same_eval)

theorem l1_nonzero_from_axis_injectivity
    {Weight PacketField : Type} [Zero Weight] [Zero PacketField]
    (axisEval : Weight → PacketField)
    (l1Weight : Weight)
    (h_axis_zero : axisEval 0 = 0)
    (h_axis_injective : Injective axisEval)
    (h_l1_weight_nonzero : l1Weight ≠ 0) :
    axisEval l1Weight ≠ 0 :=
  injective_eval_nonzero_of_weight_nonzero axisEval
    h_axis_zero h_axis_injective l1Weight h_l1_weight_nonzero

theorem axis_injective_from_full_injective
    {AxisWeight FullWeight PacketField : Type}
    (embed : AxisWeight → FullWeight)
    (fullEval : FullWeight → PacketField)
    (axisEval : AxisWeight → PacketField)
    (h_axis_eval :
      ∀ weight, axisEval weight = fullEval (embed weight))
    (h_embed_injective : Injective embed)
    (h_full_injective : Injective fullEval) :
    Injective axisEval := by
  intro x y hxy
  have h_full :
      fullEval (embed x) = fullEval (embed y) := by
    exact Eq.trans (h_axis_eval x).symm
      (Eq.trans hxy (h_axis_eval y))
  exact h_embed_injective (h_full_injective h_full)

theorem injective_from_projected_eval
    {Weight PacketField CoordinateSpace : Type}
    (eval : Weight → PacketField)
    (project : PacketField → CoordinateSpace)
    (h_projected_injective : Injective (fun weight => project (eval weight))) :
    Injective eval := by
  intro x y h_eval
  exact h_projected_injective (congrArg project h_eval)

theorem kernel_trivial_from_pairing_separates
    {Weight PacketField Scalar Index : Type}
    [Zero Weight] [Zero PacketField] [Zero Scalar]
    (eval : Weight → PacketField)
    (test : Index → Weight)
    (pair : PacketField → PacketField → Scalar)
    (h_pair_zero_left : ∀ y, pair 0 y = 0)
    (h_separates :
      ∀ weight,
        (∀ i, pair (eval weight) (eval (test i)) = 0) →
          weight = 0) :
    ∀ weight, eval weight = 0 → weight = 0 := by
  intro weight h_eval_zero
  apply h_separates
  intro i
  rw [h_eval_zero]
  exact h_pair_zero_left (eval (test i))

theorem injective_from_kernel_trivial
    {Weight PacketField : Type}
    [Zero Weight] [Zero PacketField]
    (weightDiff : Weight → Weight → Weight)
    (packetDiff : PacketField → PacketField → PacketField)
    (eval : Weight → PacketField)
    (h_eval_diff :
      ∀ left right,
        eval (weightDiff left right) =
          packetDiff (eval left) (eval right))
    (h_diff_eq_zero :
      ∀ left right, weightDiff left right = 0 → left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_kernel_trivial :
      ∀ weight, eval weight = 0 → weight = 0) :
    Injective eval := by
  intro left right h_eval_eq
  exact h_diff_eq_zero left right (
    h_kernel_trivial (weightDiff left right) (
  calc
    eval (weightDiff left right)
        = packetDiff (eval left) (eval right) := h_eval_diff left right
    _ = packetDiff (eval right) (eval right) := by rw [h_eval_eq]
    _ = 0 := h_packet_diff_self (eval right)))

theorem injective_from_pairing_separates_kernel
    {Weight PacketField Scalar Index : Type}
    [Zero Weight] [Zero PacketField] [Zero Scalar]
    (weightDiff : Weight → Weight → Weight)
    (packetDiff : PacketField → PacketField → PacketField)
    (eval : Weight → PacketField)
    (test : Index → Weight)
    (pair : PacketField → PacketField → Scalar)
    (h_eval_diff :
      ∀ left right,
        eval (weightDiff left right) =
          packetDiff (eval left) (eval right))
    (h_diff_eq_zero :
      ∀ left right, weightDiff left right = 0 → left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_pair_zero_left : ∀ y, pair 0 y = 0)
    (h_separates :
      ∀ weight,
        (∀ i, pair (eval weight) (eval (test i)) = 0) →
          weight = 0) :
    Injective eval := by
  apply injective_from_kernel_trivial
    weightDiff packetDiff eval
    h_eval_diff h_diff_eq_zero h_packet_diff_self
  exact kernel_trivial_from_pairing_separates
    eval test pair h_pair_zero_left h_separates

theorem kernel_trivial_from_annihilator_avoidance
    {AxisWeight FullWeight PacketField : Type}
    [Zero AxisWeight] [Zero PacketField]
    (embedAxis : AxisWeight → FullWeight)
    (fullEval : FullWeight → PacketField)
    (axisEval : AxisWeight → PacketField)
    (Annihilator : FullWeight → Prop)
    (h_axis_eval :
      ∀ weight, axisEval weight = fullEval (embedAxis weight))
    (h_annihilator_of_zero :
      ∀ fullWeight, fullEval fullWeight = 0 →
        Annihilator fullWeight)
    (h_axis_avoids_annihilator :
      ∀ weight, Annihilator (embedAxis weight) → weight = 0) :
    ∀ weight, axisEval weight = 0 → weight = 0 := by
  intro weight h_axis_zero
  apply h_axis_avoids_annihilator
  apply h_annihilator_of_zero
  calc
    fullEval (embedAxis weight)
        = axisEval weight := (h_axis_eval weight).symm
    _ = 0 := h_axis_zero

theorem axis_injective_from_annihilator_avoidance
    {AxisWeight FullWeight PacketField : Type}
    [Zero AxisWeight] [Zero PacketField]
    (weightDiff : AxisWeight → AxisWeight → AxisWeight)
    (packetDiff : PacketField → PacketField → PacketField)
    (embedAxis : AxisWeight → FullWeight)
    (fullEval : FullWeight → PacketField)
    (axisEval : AxisWeight → PacketField)
    (Annihilator : FullWeight → Prop)
    (h_eval_diff :
      ∀ left right,
        axisEval (weightDiff left right) =
          packetDiff (axisEval left) (axisEval right))
    (h_diff_eq_zero :
      ∀ left right, weightDiff left right = 0 → left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_axis_eval :
      ∀ weight, axisEval weight = fullEval (embedAxis weight))
    (h_annihilator_of_zero :
      ∀ fullWeight, fullEval fullWeight = 0 →
        Annihilator fullWeight)
    (h_axis_avoids_annihilator :
      ∀ weight, Annihilator (embedAxis weight) → weight = 0) :
    Injective axisEval := by
  apply injective_from_kernel_trivial
    weightDiff packetDiff axisEval
    h_eval_diff h_diff_eq_zero h_packet_diff_self
  exact kernel_trivial_from_annihilator_avoidance
    embedAxis fullEval axisEval Annihilator
    h_axis_eval h_annihilator_of_zero h_axis_avoids_annihilator

theorem annihilator_avoidance_from_axis_injective
    {AxisWeight FullWeight PacketField : Type}
    [Zero AxisWeight] [Zero PacketField]
    (embedAxis : AxisWeight → FullWeight)
    (fullEval : FullWeight → PacketField)
    (axisEval : AxisWeight → PacketField)
    (Annihilator : FullWeight → Prop)
    (h_axis_eval :
      ∀ weight, axisEval weight = fullEval (embedAxis weight))
    (h_axis_zero : axisEval 0 = 0)
    (h_zero_of_annihilator :
      ∀ fullWeight, Annihilator fullWeight →
        fullEval fullWeight = 0)
    (h_axis_injective : Injective axisEval) :
    ∀ weight, Annihilator (embedAxis weight) → weight = 0 := by
  intro weight h_annihilator
  apply h_axis_injective
  calc
    axisEval weight
        = fullEval (embedAxis weight) := h_axis_eval weight
    _ = 0 := h_zero_of_annihilator (embedAxis weight) h_annihilator
    _ = axisEval 0 := h_axis_zero.symm

theorem axis_injective_iff_annihilator_avoidance
    {AxisWeight FullWeight PacketField : Type}
    [Zero AxisWeight] [Zero PacketField]
    (weightDiff : AxisWeight → AxisWeight → AxisWeight)
    (packetDiff : PacketField → PacketField → PacketField)
    (embedAxis : AxisWeight → FullWeight)
    (fullEval : FullWeight → PacketField)
    (axisEval : AxisWeight → PacketField)
    (Annihilator : FullWeight → Prop)
    (h_eval_diff :
      ∀ left right,
        axisEval (weightDiff left right) =
          packetDiff (axisEval left) (axisEval right))
    (h_diff_eq_zero :
      ∀ left right, weightDiff left right = 0 → left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_axis_eval :
      ∀ weight, axisEval weight = fullEval (embedAxis weight))
    (h_axis_zero : axisEval 0 = 0)
    (h_annihilator_of_zero :
      ∀ fullWeight, fullEval fullWeight = 0 →
        Annihilator fullWeight)
    (h_zero_of_annihilator :
      ∀ fullWeight, Annihilator fullWeight →
        fullEval fullWeight = 0) :
    Injective axisEval ↔
      ∀ weight, Annihilator (embedAxis weight) → weight = 0 := by
  constructor
  · intro h_axis_injective
    exact annihilator_avoidance_from_axis_injective
      embedAxis fullEval axisEval Annihilator
      h_axis_eval h_axis_zero h_zero_of_annihilator h_axis_injective
  · intro h_axis_avoids_annihilator
    exact axis_injective_from_annihilator_avoidance
      weightDiff packetDiff embedAxis fullEval axisEval Annihilator
      h_eval_diff h_diff_eq_zero h_packet_diff_self
      h_axis_eval h_annihilator_of_zero h_axis_avoids_annihilator

theorem component_action_injective_from_cancellable_scales
    {AxisWeight Index Component : Type}
    (coordinate : AxisWeight → Index → Component)
    (scale : Index → Component → Component)
    (h_coordinate_injective : Injective coordinate)
    (h_scale_injective : ∀ index, Injective (scale index)) :
    Injective (fun weight index => scale index (coordinate weight index)) := by
  intro left right h_scaled_eq
  apply h_coordinate_injective
  funext index
  apply h_scale_injective index
  exact congrFun h_scaled_eq index

theorem axis_injective_from_semisimple_component_scales
    {AxisWeight PacketField Index Component : Type}
    (axisEval : AxisWeight → PacketField)
    (project : PacketField → Index → Component)
    (coordinate : AxisWeight → Index → Component)
    (scale : Index → Component → Component)
    (h_project_eval :
      ∀ weight index,
        project (axisEval weight) index =
          scale index (coordinate weight index))
    (h_coordinate_injective : Injective coordinate)
    (h_scale_injective : ∀ index, Injective (scale index)) :
    Injective axisEval := by
  intro left right h_eval_eq
  have h_scaled_eq :
      (fun index => scale index (coordinate left index)) =
        (fun index => scale index (coordinate right index)) := by
    funext index
    calc
      scale index (coordinate left index)
          = project (axisEval left) index :=
              (h_project_eval left index).symm
      _ = project (axisEval right) index := by rw [h_eval_eq]
      _ = scale index (coordinate right index) :=
              h_project_eval right index
  exact component_action_injective_from_cancellable_scales
    coordinate scale h_coordinate_injective h_scale_injective h_scaled_eq

theorem base_kernel_trivial_from_tensor_factor
    {BaseWeight ExtendedWeight PacketField TensorFactor : Type}
    [Zero BaseWeight] [Zero ExtendedWeight] [Zero PacketField]
    [Zero TensorFactor]
    (baseEval : BaseWeight → PacketField)
    (extendWeight : BaseWeight → ExtendedWeight)
    (factorEval : ExtendedWeight → TensorFactor)
    (h_base_zero_to_factor_zero :
      ∀ weight, baseEval weight = 0 →
        factorEval (extendWeight weight) = 0)
    (h_extend_zero : extendWeight 0 = 0)
    (h_extend_injective : Injective extendWeight)
    (h_factor_kernel :
      ∀ extWeight, factorEval extWeight = 0 → extWeight = 0) :
    ∀ weight, baseEval weight = 0 → weight = 0 := by
  intro weight h_base_zero
  have h_factor_zero :
      factorEval (extendWeight weight) = 0 :=
    h_base_zero_to_factor_zero weight h_base_zero
  have h_ext_zero : extendWeight weight = 0 :=
    h_factor_kernel (extendWeight weight) h_factor_zero
  have h_same : extendWeight weight = extendWeight 0 := by
    exact Eq.trans h_ext_zero h_extend_zero.symm
  exact h_extend_injective h_same

theorem base_injective_from_tensor_factor
    {BaseWeight ExtendedWeight PacketField TensorFactor : Type}
    [Zero BaseWeight] [Zero ExtendedWeight] [Zero PacketField]
    [Zero TensorFactor]
    (weightDiff : BaseWeight → BaseWeight → BaseWeight)
    (packetDiff : PacketField → PacketField → PacketField)
    (baseEval : BaseWeight → PacketField)
    (extendWeight : BaseWeight → ExtendedWeight)
    (factorEval : ExtendedWeight → TensorFactor)
    (h_eval_diff :
      ∀ left right,
        baseEval (weightDiff left right) =
          packetDiff (baseEval left) (baseEval right))
    (h_diff_eq_zero :
      ∀ left right, weightDiff left right = 0 → left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_base_zero_to_factor_zero :
      ∀ weight, baseEval weight = 0 →
        factorEval (extendWeight weight) = 0)
    (h_extend_zero : extendWeight 0 = 0)
    (h_extend_injective : Injective extendWeight)
    (h_factor_kernel :
      ∀ extWeight, factorEval extWeight = 0 → extWeight = 0) :
    Injective baseEval := by
  apply injective_from_kernel_trivial
    weightDiff packetDiff baseEval
    h_eval_diff h_diff_eq_zero h_packet_diff_self
  exact base_kernel_trivial_from_tensor_factor
    baseEval extendWeight factorEval
    h_base_zero_to_factor_zero h_extend_zero h_extend_injective h_factor_kernel

theorem factor_kernel_trivial_from_coordinate_projection
    {ExtendedWeight TensorFactor Coordinates : Type}
    [Zero ExtendedWeight] [Zero TensorFactor]
    (factorEval : ExtendedWeight → TensorFactor)
    (coordinateProject : TensorFactor → Coordinates)
    (h_factor_zero : factorEval 0 = 0)
    (h_projected_injective :
      Injective (fun extWeight => coordinateProject (factorEval extWeight))) :
    ∀ extWeight, factorEval extWeight = 0 → extWeight = 0 := by
  intro extWeight h_zero
  apply h_projected_injective
  exact Eq.trans
    (congrArg coordinateProject h_zero)
    (congrArg coordinateProject h_factor_zero).symm

theorem base_injective_from_tensor_factor_coordinates
    {BaseWeight ExtendedWeight PacketField TensorFactor Coordinates : Type}
    [Zero BaseWeight] [Zero ExtendedWeight] [Zero PacketField]
    [Zero TensorFactor]
    (weightDiff : BaseWeight → BaseWeight → BaseWeight)
    (packetDiff : PacketField → PacketField → PacketField)
    (baseEval : BaseWeight → PacketField)
    (extendWeight : BaseWeight → ExtendedWeight)
    (factorEval : ExtendedWeight → TensorFactor)
    (coordinateProject : TensorFactor → Coordinates)
    (h_eval_diff :
      ∀ left right,
        baseEval (weightDiff left right) =
          packetDiff (baseEval left) (baseEval right))
    (h_diff_eq_zero :
      ∀ left right, weightDiff left right = 0 → left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_base_zero_to_factor_zero :
      ∀ weight, baseEval weight = 0 →
        factorEval (extendWeight weight) = 0)
    (h_extend_zero : extendWeight 0 = 0)
    (h_extend_injective : Injective extendWeight)
    (h_factor_zero : factorEval 0 = 0)
    (h_projected_injective :
      Injective (fun extWeight => coordinateProject (factorEval extWeight))) :
    Injective baseEval := by
  apply base_injective_from_tensor_factor
    weightDiff packetDiff baseEval extendWeight factorEval
    h_eval_diff h_diff_eq_zero h_packet_diff_self
    h_base_zero_to_factor_zero h_extend_zero h_extend_injective
  exact factor_kernel_trivial_from_coordinate_projection
    factorEval coordinateProject h_factor_zero h_projected_injective

theorem base_injective_from_tensor_factor_moore_coordinates
    {BaseWeight ExtendedWeight PacketField TensorFactor MooreCoordinates : Type}
    [Zero BaseWeight] [Zero ExtendedWeight] [Zero PacketField]
    [Zero TensorFactor]
    (weightDiff : BaseWeight → BaseWeight → BaseWeight)
    (packetDiff : PacketField → PacketField → PacketField)
    (baseEval : BaseWeight → PacketField)
    (extendWeight : BaseWeight → ExtendedWeight)
    (factorEval : ExtendedWeight → TensorFactor)
    (mooreProject : TensorFactor → MooreCoordinates)
    (h_eval_diff :
      ∀ left right,
        baseEval (weightDiff left right) =
          packetDiff (baseEval left) (baseEval right))
    (h_diff_eq_zero :
      ∀ left right, weightDiff left right = 0 → left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_base_zero_to_factor_zero :
      ∀ weight, baseEval weight = 0 →
        factorEval (extendWeight weight) = 0)
    (h_extend_zero : extendWeight 0 = 0)
    (h_extend_injective : Injective extendWeight)
    (h_factor_zero : factorEval 0 = 0)
    (h_moore_injective :
      Injective (fun extWeight => mooreProject (factorEval extWeight))) :
    Injective baseEval :=
  base_injective_from_tensor_factor_coordinates
    weightDiff packetDiff baseEval extendWeight factorEval mooreProject
    h_eval_diff h_diff_eq_zero h_packet_diff_self
    h_base_zero_to_factor_zero h_extend_zero h_extend_injective
    h_factor_zero h_moore_injective

theorem injective_iff_precompose_bijection
    {Source Target Value : Type}
    (toTarget : Source → Target)
    (fromTarget : Target → Source)
    (sourceEval : Source → Value)
    (targetEval : Target → Value)
    (h_source_eval :
      ∀ source, sourceEval source = targetEval (toTarget source))
    (h_left_inverse : ∀ source, fromTarget (toTarget source) = source)
    (h_right_inverse : ∀ target, toTarget (fromTarget target) = target) :
    Injective sourceEval ↔ Injective targetEval := by
  constructor
  · intro h_source_inj target1 target2 h_eval
    have h_source_eval_eq :
        sourceEval (fromTarget target1) =
          sourceEval (fromTarget target2) := by
      calc
        sourceEval (fromTarget target1)
            = targetEval (toTarget (fromTarget target1)) :=
                h_source_eval (fromTarget target1)
        _ = targetEval target1 := by rw [h_right_inverse target1]
        _ = targetEval target2 := h_eval
        _ = targetEval (toTarget (fromTarget target2)) := by
                rw [h_right_inverse target2]
        _ = sourceEval (fromTarget target2) :=
                (h_source_eval (fromTarget target2)).symm
    have h_from_eq : fromTarget target1 = fromTarget target2 :=
      h_source_inj h_source_eval_eq
    calc
      target1 = toTarget (fromTarget target1) := (h_right_inverse target1).symm
      _ = toTarget (fromTarget target2) := by rw [h_from_eq]
      _ = target2 := h_right_inverse target2
  · intro h_target_inj source1 source2 h_eval
    have h_target_eval_eq :
        targetEval (toTarget source1) =
          targetEval (toTarget source2) := by
      calc
        targetEval (toTarget source1)
            = sourceEval source1 := (h_source_eval source1).symm
        _ = sourceEval source2 := h_eval
        _ = targetEval (toTarget source2) := h_source_eval source2
    have h_to_eq : toTarget source1 = toTarget source2 :=
      h_target_inj h_target_eval_eq
    have h_from_eq :
        fromTarget (toTarget source1) = fromTarget (toTarget source2) := by
      rw [h_to_eq]
    calc
      source1 = fromTarget (toTarget source1) := (h_left_inverse source1).symm
      _ = fromTarget (toTarget source2) := h_from_eq
      _ = source2 := h_left_inverse source2

theorem packet_content_from_axis_injective_l1
    {α Weight PacketField : Type}
    [Zero α] [Zero Weight] [Zero PacketField] {m : Nat}
    (packet : Fin m → α)
    (axisEval : Weight → PacketField)
    (l1Weight : Weight)
    (h_all_zero_l1_zero :
      AllZero packet → axisEval l1Weight = 0)
    (h_axis_zero : axisEval 0 = 0)
    (h_axis_injective : Injective axisEval)
    (h_l1_weight_nonzero : l1Weight ≠ 0) :
    PacketContentGood packet := by
  intro h_packet_zero
  have h_l1_nonzero : axisEval l1Weight ≠ 0 :=
    l1_nonzero_from_axis_injectivity axisEval l1Weight
      h_axis_zero h_axis_injective h_l1_weight_nonzero
  exact h_l1_nonzero (h_all_zero_l1_zero h_packet_zero)

theorem global_content_from_axis_injective_l1
    {α Weight PacketField : Type}
    [Zero α] [Zero Weight] [Zero PacketField] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (axisEval : Fin orbitCount → Weight → PacketField)
    (l1Weight : Weight)
    (h_all_zero_l1_zero :
      ∀ orbit, AllZero (packet orbit) →
        axisEval orbit l1Weight = 0)
    (h_axis_zero :
      ∀ orbit, axisEval orbit 0 = 0)
    (h_axis_injective :
      ∀ orbit, Injective (axisEval orbit))
    (h_l1_weight_nonzero : l1Weight ≠ 0) :
    GlobalContentGood packet := by
  intro orbit
  exact packet_content_from_axis_injective_l1
    (packet orbit) (axisEval orbit) l1Weight
    (h_all_zero_l1_zero orbit) (h_axis_zero orbit)
    (h_axis_injective orbit) h_l1_weight_nonzero

theorem no_harmful_from_axis_injective_l1
    {α Weight PacketField : Type}
    [Zero α] [Zero Weight] [Zero PacketField] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (axisEval : Fin orbitCount → Weight → PacketField)
    (l1Weight : Weight)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_all_zero_l1_zero :
      ∀ orbit, AllZero (packet orbit) →
        axisEval orbit l1Weight = 0)
    (h_axis_zero :
      ∀ orbit, axisEval orbit 0 = 0)
    (h_axis_injective :
      ∀ orbit, Injective (axisEval orbit))
    (h_l1_weight_nonzero : l1Weight ≠ 0) :
    ∀ orbit, ¬ harmful orbit := by
  have h_content : GlobalContentGood packet :=
    global_content_from_axis_injective_l1
      packet axisEval l1Weight h_all_zero_l1_zero
      h_axis_zero h_axis_injective h_l1_weight_nonzero
  intro orbit hh
  exact h_content orbit (h_harmful_all_zero orbit hh)

def p24AxisDimension : Nat := 368

def p24PacketDegree : Nat := 388430

def p24PacketOrbitCount : Nat := 8

def p24KCharacterFieldDegree : Nat := 5460

def p24TensorFactorCountOverKCharacterField : Nat := 70

def p24TensorFactorDegreeOverKCharacterField : Nat := 5549

def p24AxisRankCoordinatesPerPacket : Nat :=
  p24AxisDimension * p24PacketDegree

def p24AxisRankCoordinatesAllPackets : Nat :=
  p24PacketOrbitCount * p24AxisRankCoordinatesPerPacket

def p24SqrtFloor : Nat := 1000000000000

def p24Order157OrbitDegreeOverFp : Nat := 156

def p24Order211OrbitDegreeOverFp : Nat := 35

def p24Order211ModuleCountOverFp : Nat := 6

def p24Order157SplitCountOverPacketField : Nat := 2

def p24Order157ModuleDimensionOverPacketField : Nat := 78

def p24Order211SplitCountOverPacketField : Nat := 210

def p24Order211ModuleDimensionOverPacketField : Nat := 1

def p24AxisModuleCountOverPacketField : Nat :=
  1 + 1 +
    p24Order157SplitCountOverPacketField +
    p24Order211SplitCountOverPacketField

theorem p24_axis_dimension :
    p24AxisDimension = 1 + 1 + 156 + 210 := by
  decide

theorem p24_axis_dimension_fits_packet_degree :
    p24AxisDimension < p24PacketDegree := by
  decide

theorem p24_packet_degree_tensor_factorization :
    p24PacketDegree =
      p24TensorFactorCountOverKCharacterField *
        p24TensorFactorDegreeOverKCharacterField := by
  decide

theorem p24_axis_dimension_fits_one_tensor_factor :
    p24AxisDimension < p24TensorFactorDegreeOverKCharacterField := by
  decide

theorem p24_axis_rank_coordinates_per_packet :
    p24AxisRankCoordinatesPerPacket = 142942240 := by
  decide

theorem p24_axis_rank_coordinates_all_packets :
    p24AxisRankCoordinatesAllPackets = 1143537920 := by
  decide

theorem p24_axis_rank_coordinates_all_packets_subsqrt :
    p24AxisRankCoordinatesAllPackets < p24SqrtFloor := by
  decide

theorem p24_order_211_base_module_dimension :
    p24Order211ModuleCountOverFp *
      p24Order211OrbitDegreeOverFp = 210 := by
  decide

theorem p24_axis_packet_field_module_count :
    p24AxisModuleCountOverPacketField = 214 := by
  decide

theorem p24_axis_packet_field_module_dimension :
    1 + 1 +
      p24Order157SplitCountOverPacketField *
        p24Order157ModuleDimensionOverPacketField +
      p24Order211SplitCountOverPacketField *
        p24Order211ModuleDimensionOverPacketField =
        p24AxisDimension := by
  decide

end P24.AxisInjectivityGate
