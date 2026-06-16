/-!
Finite handoff gate: the p24 reduced-anchor `179` kernel is not an
`F_p`-rational final-curve isogeny object.

The Python gate computes the arithmetic data.  This Lean file records the
resulting finite contract for the proof notes.
-/

namespace P24.TraceGcdReducedAnchorKernelFinalCurveGuardrail

structure FinalCurveTorsionGuardrail where
  cDividesFinalCurveOrder : Prop
  cFrobeniusDiscriminantSquare : Prop
  auxiliaryKernelTarget : Prop

def NotFinalCurveRationalKernel (gate : FinalCurveTorsionGuardrail) : Prop :=
  ¬ gate.cDividesFinalCurveOrder ∧
  ¬ gate.cFrobeniusDiscriminantSquare ∧
  gate.auxiliaryKernelTarget

theorem auxiliary_target_from_no_final_curve_kernel
    (gate : FinalCurveTorsionGuardrail)
    (h_gate : NotFinalCurveRationalKernel gate) :
    gate.auxiliaryKernelTarget ∧
    ¬ gate.cDividesFinalCurveOrder ∧
    ¬ gate.cFrobeniusDiscriminantSquare := by
  rcases h_gate with ⟨h_not_divides, h_not_square, h_aux⟩
  exact ⟨h_aux, h_not_divides, h_not_square⟩

def p24C : Nat := 179
def p24SelectedOrderOddPartModC : Nat := 56
def p24FrobeniusDiscriminantModC : Nat := 176
def p24MuCFieldDegreeOverFp : Nat := 89

theorem p24_c_not_dividing_selected_order_mod_value :
    p24SelectedOrderOddPartModC = 56 := by
  decide

theorem p24_frobenius_discriminant_mod_c :
    p24FrobeniusDiscriminantModC = 176 := by
  decide

theorem p24_mu_c_field_degree_over_fp :
    p24MuCFieldDegreeOverFp = 89 := by
  decide

end P24.TraceGcdReducedAnchorKernelFinalCurveGuardrail
