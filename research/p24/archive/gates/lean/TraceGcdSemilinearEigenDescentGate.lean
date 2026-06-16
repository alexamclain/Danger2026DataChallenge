/-!
Finite gate for the p24 semilinear factor-cycle cancellation target.

The arithmetic input is external: the actual CM packet product sum must satisfy
rho=p^780 covariance across the 70 E-tensor factors, and the same total must
descend to the rho-fixed left field L=F_p(mu_157).  This file records only the
abstract implication:

  fixed by rho + nontrivial rho-eigenvalue => zero.

No CM class-field construction or finite-field eigenspace computation is
formalized here.
-/

namespace P24.TraceGcdSemilinearEigenDescentGate

def FixedBy {V : Type} (sigma : V → V) (value : V) : Prop :=
  sigma value = value

def EigenFor {V : Type} (sigma twist : V → V) (value : V) : Prop :=
  sigma value = twist value

def FixedEigenspaceIntersectionZero {V : Type} [Zero V]
    (twist : V → V) : Prop :=
  ∀ value, twist value = value → value = 0

theorem zero_from_descent_and_nontrivial_eigen
    {V : Type} [Zero V]
    (sigma twist : V → V)
    (packetSum : V)
    (h_descends : FixedBy sigma packetSum)
    (h_eigen : EigenFor sigma twist packetSum)
    (h_intersection :
      FixedEigenspaceIntersectionZero twist) :
    packetSum = 0 := by
  apply h_intersection packetSum
  exact h_eigen.symm.trans h_descends

theorem all_character_sums_zero_from_descent_and_eigen
    {Character V : Type} [Zero V]
    (sigma : V → V)
    (twist : Character → V → V)
    (packetSum : Character → V)
    (h_descends :
      ∀ chi, FixedBy sigma (packetSum chi))
    (h_eigen :
      ∀ chi, EigenFor sigma (twist chi) (packetSum chi))
    (h_intersection :
      ∀ chi, FixedEigenspaceIntersectionZero (twist chi)) :
    ∀ chi, packetSum chi = 0 := by
  intro chi
  exact zero_from_descent_and_nontrivial_eigen
    sigma (twist chi) (packetSum chi)
    (h_descends chi) (h_eigen chi) (h_intersection chi)

theorem h_coset_equation_count :
    156 * 7 = 1092 := by
  decide

theorem p24_rho_order_on_E_numerology :
    780 * 7 = 5460 := by
  decide

theorem p24_factor_cycles_numerology :
    10 * 7 = 70 := by
  decide

theorem p24_certificate_surface_subsqrt_scale :
    4 < 1000000000000 := by
  decide

end P24.TraceGcdSemilinearEigenDescentGate
