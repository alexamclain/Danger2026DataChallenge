/-!
Finite gate for the p24 right-axis anchor descent target.

The arithmetic input is external: for the internally traced `G_chi` right
profile, one still has to prove the `rho=p^780` covariance relation and the
anchor fixedness.  This file records only the seven-coset implication:

  Y_{c+6} = rho(Y_c) for c mod 7
  rho(Y_0) = Y_0
  --------------------------------
  Y_0 = Y_1 = ... = Y_6.

This is the formal core behind the Python right-axis covariance/descent gate.
-/

namespace P24.TraceGcdRightAxisAnchorDescentGate

def AllEqual7 {V : Type} (y0 y1 y2 y3 y4 y5 y6 : V) : Prop :=
  y1 = y0 ∧ y2 = y0 ∧ y3 = y0 ∧ y4 = y0 ∧ y5 = y0 ∧ y6 = y0

theorem all_equal_from_shift6_covariance_and_anchor
    {V : Type}
    (rho : V → V)
    (y0 y1 y2 y3 y4 y5 y6 : V)
    (h_anchor : rho y0 = y0)
    (h0 : y6 = rho y0)
    (_h1 : y0 = rho y1)
    (h2 : y1 = rho y2)
    (h3 : y2 = rho y3)
    (h4 : y3 = rho y4)
    (h5 : y4 = rho y5)
    (h6 : y5 = rho y6) :
    AllEqual7 y0 y1 y2 y3 y4 y5 y6 := by
  have hy6 : y6 = y0 := by
    rw [h0, h_anchor]
  have hy5 : y5 = y0 := by
    rw [h6, hy6, h_anchor]
  have hy4 : y4 = y0 := by
    rw [h5, hy5, h_anchor]
  have hy3 : y3 = y0 := by
    rw [h4, hy4, h_anchor]
  have hy2 : y2 = y0 := by
    rw [h3, hy3, h_anchor]
  have hy1 : y1 = y0 := by
    rw [h2, hy2, h_anchor]
  exact ⟨hy1, hy2, hy3, hy4, hy5, hy6⟩

theorem anchor_from_all_equal_and_shift6_covariance
    {V : Type}
    (rho : V → V)
    (y0 y1 y2 y3 y4 y5 y6 : V)
    (h_equal : AllEqual7 y0 y1 y2 y3 y4 y5 y6)
    (h0 : y6 = rho y0) :
    rho y0 = y0 := by
  exact h0 ▸ h_equal.2.2.2.2.2

theorem all_equal_iff_anchor_under_shift6_covariance
    {V : Type}
    (rho : V → V)
    (y0 y1 y2 y3 y4 y5 y6 : V)
    (h0 : y6 = rho y0)
    (h1 : y0 = rho y1)
    (h2 : y1 = rho y2)
    (h3 : y2 = rho y3)
    (h4 : y3 = rho y4)
    (h5 : y4 = rho y5)
    (h6 : y5 = rho y6) :
    AllEqual7 y0 y1 y2 y3 y4 y5 y6 ↔ rho y0 = y0 := by
  constructor
  · intro h_equal
    exact anchor_from_all_equal_and_shift6_covariance
      rho y0 y1 y2 y3 y4 y5 y6 h_equal h0
  · intro h_anchor
    exact all_equal_from_shift6_covariance_and_anchor
      rho y0 y1 y2 y3 y4 y5 y6
      h_anchor h0 h1 h2 h3 h4 h5 h6

theorem p24_rho_fixed_E_degree :
    156 * 5 = 780 := by
  decide

theorem p24_right_axis_payload_count :
    156 + 6 * 156 = 1092 := by
  decide

theorem p24_internal_degree_factorization :
    31 * 179 = 5549 := by
  decide

end P24.TraceGcdRightAxisAnchorDescentGate
