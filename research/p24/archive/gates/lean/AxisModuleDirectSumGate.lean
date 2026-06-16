/-!
Finite direct-sum gate for the p24 axis-module theorem.

This file deliberately uses only Lean core.  It does not prove the CM
nonvanishing theorem.  It checks the formal step suggested by the p24
module decomposition:

* decompose the axis source into four pieces
  constant + 2-axis + 157-axis + 211-axis;
* evaluate each piece into the packet field;
* if each component has trivial kernel and the four image subspaces are
  direct, then the combined axis evaluation is injective.

For p24 the missing arithmetic input is the selected-prime directness of
these four images inside each degree-388430 H-character packet field.
-/

namespace P24.AxisModuleDirectSumGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

structure Axis4 (Const Axis2 Axis157 Axis211 : Type) where
  const : Const
  axis2 : Axis2
  axis157 : Axis157
  axis211 : Axis211

namespace Axis4

def zero
    {Const Axis2 Axis157 Axis211 : Type}
    [Zero Const] [Zero Axis2] [Zero Axis157] [Zero Axis211] :
    Axis4 Const Axis2 Axis157 Axis211 :=
  { const := 0, axis2 := 0, axis157 := 0, axis211 := 0 }

def diff
    {Const Axis2 Axis157 Axis211 : Type}
    (diffConst : Const → Const → Const)
    (diff2 : Axis2 → Axis2 → Axis2)
    (diff157 : Axis157 → Axis157 → Axis157)
    (diff211 : Axis211 → Axis211 → Axis211)
    (left right : Axis4 Const Axis2 Axis157 Axis211) :
    Axis4 Const Axis2 Axis157 Axis211 :=
  {
    const := diffConst left.const right.const
    axis2 := diff2 left.axis2 right.axis2
    axis157 := diff157 left.axis157 right.axis157
    axis211 := diff211 left.axis211 right.axis211
  }

def eval
    {Const Axis2 Axis157 Axis211 PacketField : Type}
    (sum4 :
      PacketField → PacketField → PacketField → PacketField → PacketField)
    (evalConst : Const → PacketField)
    (eval2 : Axis2 → PacketField)
    (eval157 : Axis157 → PacketField)
    (eval211 : Axis211 → PacketField)
    (weight : Axis4 Const Axis2 Axis157 Axis211) :
    PacketField :=
  sum4
    (evalConst weight.const)
    (eval2 weight.axis2)
    (eval157 weight.axis157)
    (eval211 weight.axis211)

end Axis4

theorem axis4_kernel_trivial_from_direct_components
    {Const Axis2 Axis157 Axis211 PacketField : Type}
    [Zero Const] [Zero Axis2] [Zero Axis157] [Zero Axis211]
    [Zero PacketField]
    (sum4 :
      PacketField → PacketField → PacketField → PacketField → PacketField)
    (evalConst : Const → PacketField)
    (eval2 : Axis2 → PacketField)
    (eval157 : Axis157 → PacketField)
    (eval211 : Axis211 → PacketField)
    (h_sum_direct :
      ∀ v0 v2 v157 v211,
        sum4 v0 v2 v157 v211 = 0 →
          v0 = 0 ∧ v2 = 0 ∧ v157 = 0 ∧ v211 = 0)
    (h_const_kernel : ∀ value, evalConst value = 0 → value = 0)
    (h_2_kernel : ∀ value, eval2 value = 0 → value = 0)
    (h_157_kernel : ∀ value, eval157 value = 0 → value = 0)
    (h_211_kernel : ∀ value, eval211 value = 0 → value = 0) :
    ∀ weight : Axis4 Const Axis2 Axis157 Axis211,
      Axis4.eval sum4 evalConst eval2 eval157 eval211 weight = 0 →
        weight = Axis4.zero := by
  intro weight h_eval_zero
  cases weight with
  | mk const axis2 axis157 axis211 =>
      have h_parts :
          evalConst const = 0 ∧
          eval2 axis2 = 0 ∧
          eval157 axis157 = 0 ∧
          eval211 axis211 = 0 :=
        h_sum_direct
          (evalConst const)
          (eval2 axis2)
          (eval157 axis157)
          (eval211 axis211)
          h_eval_zero
      have h_const : const = 0 := h_const_kernel const h_parts.1
      have h_axis2 : axis2 = 0 := h_2_kernel axis2 h_parts.2.1
      have h_axis157 : axis157 = 0 :=
        h_157_kernel axis157 h_parts.2.2.1
      have h_axis211 : axis211 = 0 :=
        h_211_kernel axis211 h_parts.2.2.2
      cases h_const
      cases h_axis2
      cases h_axis157
      cases h_axis211
      rfl

theorem axis4_injective_from_direct_components
    {Const Axis2 Axis157 Axis211 PacketField : Type}
    [Zero Const] [Zero Axis2] [Zero Axis157] [Zero Axis211]
    [Zero PacketField]
    (diffConst : Const → Const → Const)
    (diff2 : Axis2 → Axis2 → Axis2)
    (diff157 : Axis157 → Axis157 → Axis157)
    (diff211 : Axis211 → Axis211 → Axis211)
    (packetDiff : PacketField → PacketField → PacketField)
    (sum4 :
      PacketField → PacketField → PacketField → PacketField → PacketField)
    (evalConst : Const → PacketField)
    (eval2 : Axis2 → PacketField)
    (eval157 : Axis157 → PacketField)
    (eval211 : Axis211 → PacketField)
    (h_eval_diff :
      ∀ left right,
        Axis4.eval sum4 evalConst eval2 eval157 eval211
          (Axis4.diff diffConst diff2 diff157 diff211 left right) =
            packetDiff
              (Axis4.eval sum4 evalConst eval2 eval157 eval211 left)
              (Axis4.eval sum4 evalConst eval2 eval157 eval211 right))
    (h_diff_eq_zero :
      ∀ left right,
        Axis4.diff diffConst diff2 diff157 diff211 left right =
          Axis4.zero →
            left = right)
    (h_packet_diff_self :
      ∀ value : PacketField, packetDiff value value = 0)
    (h_sum_direct :
      ∀ v0 v2 v157 v211,
        sum4 v0 v2 v157 v211 = 0 →
          v0 = 0 ∧ v2 = 0 ∧ v157 = 0 ∧ v211 = 0)
    (h_const_kernel : ∀ value, evalConst value = 0 → value = 0)
    (h_2_kernel : ∀ value, eval2 value = 0 → value = 0)
    (h_157_kernel : ∀ value, eval157 value = 0 → value = 0)
    (h_211_kernel : ∀ value, eval211 value = 0 → value = 0) :
    Injective (Axis4.eval sum4 evalConst eval2 eval157 eval211) := by
  intro left right h_eval_eq
  apply h_diff_eq_zero left right
  apply axis4_kernel_trivial_from_direct_components
    sum4 evalConst eval2 eval157 eval211
    h_sum_direct h_const_kernel h_2_kernel h_157_kernel h_211_kernel
  calc
    Axis4.eval sum4 evalConst eval2 eval157 eval211
        (Axis4.diff diffConst diff2 diff157 diff211 left right)
        =
          packetDiff
            (Axis4.eval sum4 evalConst eval2 eval157 eval211 left)
            (Axis4.eval sum4 evalConst eval2 eval157 eval211 right) :=
              h_eval_diff left right
    _ =
          packetDiff
            (Axis4.eval sum4 evalConst eval2 eval157 eval211 right)
            (Axis4.eval sum4 evalConst eval2 eval157 eval211 right) := by
              rw [h_eval_eq]
    _ = 0 :=
              h_packet_diff_self
                (Axis4.eval sum4 evalConst eval2 eval157 eval211 right)

end P24.AxisModuleDirectSumGate
