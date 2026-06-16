/-!
Finite gate for the CRT marginal-annihilator theorem.

After the Fourier/CRT reduction, the p24 trace-frame target is a statement
about one constant vector and the marginal-difference spaces

    Delta_c = span {M_a - M_0}.

This file checks only the abstract implication:

* if the selected marginal images are direct in the top-coefficient
  coordinate space;
* and each selected source component has trivial top-coefficient kernel;
* then the combined top-coefficient map is injective.

The arithmetic input remains the p24 CM theorem proving those directness and
kernel assumptions for the actual marginal packet sums.
-/

namespace P24.CrtMarginalAnnihilatorGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

structure Marginal3 (Const DeltaA DeltaB : Type) where
  const : Const
  deltaA : DeltaA
  deltaB : DeltaB

namespace Marginal3

def zero
    {Const DeltaA DeltaB : Type}
    [Zero Const] [Zero DeltaA] [Zero DeltaB] :
    Marginal3 Const DeltaA DeltaB :=
  { const := 0, deltaA := 0, deltaB := 0 }

def diff
    {Const DeltaA DeltaB : Type}
    (diffConst : Const → Const → Const)
    (diffA : DeltaA → DeltaA → DeltaA)
    (diffB : DeltaB → DeltaB → DeltaB)
    (left right : Marginal3 Const DeltaA DeltaB) :
    Marginal3 Const DeltaA DeltaB :=
  {
    const := diffConst left.const right.const
    deltaA := diffA left.deltaA right.deltaA
    deltaB := diffB left.deltaB right.deltaB
  }

def eval
    {Const DeltaA DeltaB Coordinates : Type}
    (sum3 : Coordinates → Coordinates → Coordinates → Coordinates)
    (evalConst : Const → Coordinates)
    (evalA : DeltaA → Coordinates)
    (evalB : DeltaB → Coordinates)
    (weight : Marginal3 Const DeltaA DeltaB) :
    Coordinates :=
  sum3
    (evalConst weight.const)
    (evalA weight.deltaA)
    (evalB weight.deltaB)

end Marginal3

structure Marginal4 (Const DeltaA DeltaB DeltaC : Type) where
  const : Const
  deltaA : DeltaA
  deltaB : DeltaB
  deltaC : DeltaC

namespace Marginal4

def zero
    {Const DeltaA DeltaB DeltaC : Type}
    [Zero Const] [Zero DeltaA] [Zero DeltaB] [Zero DeltaC] :
    Marginal4 Const DeltaA DeltaB DeltaC :=
  { const := 0, deltaA := 0, deltaB := 0, deltaC := 0 }

def diff
    {Const DeltaA DeltaB DeltaC : Type}
    (diffConst : Const → Const → Const)
    (diffA : DeltaA → DeltaA → DeltaA)
    (diffB : DeltaB → DeltaB → DeltaB)
    (diffC : DeltaC → DeltaC → DeltaC)
    (left right : Marginal4 Const DeltaA DeltaB DeltaC) :
    Marginal4 Const DeltaA DeltaB DeltaC :=
  {
    const := diffConst left.const right.const
    deltaA := diffA left.deltaA right.deltaA
    deltaB := diffB left.deltaB right.deltaB
    deltaC := diffC left.deltaC right.deltaC
  }

def eval
    {Const DeltaA DeltaB DeltaC Coordinates : Type}
    (sum4 :
      Coordinates → Coordinates → Coordinates → Coordinates → Coordinates)
    (evalConst : Const → Coordinates)
    (evalA : DeltaA → Coordinates)
    (evalB : DeltaB → Coordinates)
    (evalC : DeltaC → Coordinates)
    (weight : Marginal4 Const DeltaA DeltaB DeltaC) :
    Coordinates :=
  sum4
    (evalConst weight.const)
    (evalA weight.deltaA)
    (evalB weight.deltaB)
    (evalC weight.deltaC)

end Marginal4

theorem marginal3_kernel_trivial_from_directness
    {Const DeltaA DeltaB Coordinates : Type}
    [Zero Const] [Zero DeltaA] [Zero DeltaB] [Zero Coordinates]
    (sum3 : Coordinates → Coordinates → Coordinates → Coordinates)
    (evalConst : Const → Coordinates)
    (evalA : DeltaA → Coordinates)
    (evalB : DeltaB → Coordinates)
    (h_sum_direct :
      ∀ v0 vA vB,
        sum3 v0 vA vB = 0 → v0 = 0 ∧ vA = 0 ∧ vB = 0)
    (h_const_kernel : ∀ value, evalConst value = 0 → value = 0)
    (h_A_kernel : ∀ value, evalA value = 0 → value = 0)
    (h_B_kernel : ∀ value, evalB value = 0 → value = 0) :
    ∀ weight : Marginal3 Const DeltaA DeltaB,
      Marginal3.eval sum3 evalConst evalA evalB weight = 0 →
        weight = Marginal3.zero := by
  intro weight h_eval_zero
  cases weight with
  | mk const deltaA deltaB =>
      have h_parts :
          evalConst const = 0 ∧ evalA deltaA = 0 ∧ evalB deltaB = 0 :=
        h_sum_direct
          (evalConst const)
          (evalA deltaA)
          (evalB deltaB)
          h_eval_zero
      have h_const : const = 0 := h_const_kernel const h_parts.1
      have h_deltaA : deltaA = 0 := h_A_kernel deltaA h_parts.2.1
      have h_deltaB : deltaB = 0 := h_B_kernel deltaB h_parts.2.2
      cases h_const
      cases h_deltaA
      cases h_deltaB
      rfl

theorem marginal4_kernel_trivial_from_directness
    {Const DeltaA DeltaB DeltaC Coordinates : Type}
    [Zero Const] [Zero DeltaA] [Zero DeltaB] [Zero DeltaC]
    [Zero Coordinates]
    (sum4 :
      Coordinates → Coordinates → Coordinates → Coordinates → Coordinates)
    (evalConst : Const → Coordinates)
    (evalA : DeltaA → Coordinates)
    (evalB : DeltaB → Coordinates)
    (evalC : DeltaC → Coordinates)
    (h_sum_direct :
      ∀ v0 vA vB vC,
        sum4 v0 vA vB vC = 0 →
          v0 = 0 ∧ vA = 0 ∧ vB = 0 ∧ vC = 0)
    (h_const_kernel : ∀ value, evalConst value = 0 → value = 0)
    (h_A_kernel : ∀ value, evalA value = 0 → value = 0)
    (h_B_kernel : ∀ value, evalB value = 0 → value = 0)
    (h_C_kernel : ∀ value, evalC value = 0 → value = 0) :
    ∀ weight : Marginal4 Const DeltaA DeltaB DeltaC,
      Marginal4.eval sum4 evalConst evalA evalB evalC weight = 0 →
        weight = Marginal4.zero := by
  intro weight h_eval_zero
  cases weight with
  | mk const deltaA deltaB deltaC =>
      have h_parts :
          evalConst const = 0 ∧
          evalA deltaA = 0 ∧
          evalB deltaB = 0 ∧
          evalC deltaC = 0 :=
        h_sum_direct
          (evalConst const)
          (evalA deltaA)
          (evalB deltaB)
          (evalC deltaC)
          h_eval_zero
      have h_const : const = 0 := h_const_kernel const h_parts.1
      have h_deltaA : deltaA = 0 := h_A_kernel deltaA h_parts.2.1
      have h_deltaB : deltaB = 0 := h_B_kernel deltaB h_parts.2.2.1
      have h_deltaC : deltaC = 0 := h_C_kernel deltaC h_parts.2.2.2
      cases h_const
      cases h_deltaA
      cases h_deltaB
      cases h_deltaC
      rfl

theorem marginal4_injective_from_directness
    {Const DeltaA DeltaB DeltaC Coordinates : Type}
    [Zero Const] [Zero DeltaA] [Zero DeltaB] [Zero DeltaC]
    [Zero Coordinates]
    (diffConst : Const → Const → Const)
    (diffA : DeltaA → DeltaA → DeltaA)
    (diffB : DeltaB → DeltaB → DeltaB)
    (diffC : DeltaC → DeltaC → DeltaC)
    (coordinateDiff : Coordinates → Coordinates → Coordinates)
    (sum4 :
      Coordinates → Coordinates → Coordinates → Coordinates → Coordinates)
    (evalConst : Const → Coordinates)
    (evalA : DeltaA → Coordinates)
    (evalB : DeltaB → Coordinates)
    (evalC : DeltaC → Coordinates)
    (h_eval_diff :
      ∀ left right,
        Marginal4.eval sum4 evalConst evalA evalB evalC
          (Marginal4.diff diffConst diffA diffB diffC left right) =
            coordinateDiff
              (Marginal4.eval sum4 evalConst evalA evalB evalC left)
              (Marginal4.eval sum4 evalConst evalA evalB evalC right))
    (h_diff_eq_zero :
      ∀ left right,
        Marginal4.diff diffConst diffA diffB diffC left right =
          Marginal4.zero →
            left = right)
    (h_coordinate_diff_self :
      ∀ value : Coordinates, coordinateDiff value value = 0)
    (h_sum_direct :
      ∀ v0 vA vB vC,
        sum4 v0 vA vB vC = 0 →
          v0 = 0 ∧ vA = 0 ∧ vB = 0 ∧ vC = 0)
    (h_const_kernel : ∀ value, evalConst value = 0 → value = 0)
    (h_A_kernel : ∀ value, evalA value = 0 → value = 0)
    (h_B_kernel : ∀ value, evalB value = 0 → value = 0)
    (h_C_kernel : ∀ value, evalC value = 0 → value = 0) :
    Injective (Marginal4.eval sum4 evalConst evalA evalB evalC) := by
  intro left right h_eval_eq
  apply h_diff_eq_zero left right
  apply marginal4_kernel_trivial_from_directness
    sum4 evalConst evalA evalB evalC
    h_sum_direct h_const_kernel h_A_kernel h_B_kernel h_C_kernel
  calc
    Marginal4.eval sum4 evalConst evalA evalB evalC
        (Marginal4.diff diffConst diffA diffB diffC left right)
        =
          coordinateDiff
            (Marginal4.eval sum4 evalConst evalA evalB evalC left)
            (Marginal4.eval sum4 evalConst evalA evalB evalC right) :=
              h_eval_diff left right
    _ =
          coordinateDiff
            (Marginal4.eval sum4 evalConst evalA evalB evalC right)
            (Marginal4.eval sum4 evalConst evalA evalB evalC right) := by
              rw [h_eval_eq]
    _ = 0 :=
              h_coordinate_diff_self
                (Marginal4.eval sum4 evalConst evalA evalB evalC right)

end P24.CrtMarginalAnnihilatorGate
