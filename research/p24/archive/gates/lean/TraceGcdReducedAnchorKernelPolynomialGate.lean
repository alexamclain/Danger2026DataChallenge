/-!
Finite handoff gate for the kernel-polynomial realization of the reduced
anchor subgroup divisor.

For an odd cyclic subgroup `H` of order `c`, the monic kernel polynomial

  K_H(x) = product over `(H \ {O})/{+-1}` of `(x - x(Q))`

has divisor `sum_{Q in H, Q != O} [Q] - (c - 1)[O]`.  The Python gate checks
this on small finite elliptic curves and records the p24 counts.
-/

namespace P24.TraceGcdReducedAnchorKernelPolynomialGate

structure KernelPolynomial where
  rootPairsAreNonzeroSubgroupModuloSign : Prop
  degreeIsHalfNonzeroSubgroup : Prop
  divisorEqualsSubgroupResidual : Prop

def KernelPolynomialRealizesResidual
    (poly : KernelPolynomial) : Prop :=
  poly.rootPairsAreNonzeroSubgroupModuloSign ∧
  poly.degreeIsHalfNonzeroSubgroup ∧
  poly.divisorEqualsSubgroupResidual

structure VeluDenominator where
  squareOfKernelPolynomial : Prop

structure ProducerTarget where
  selectedCMLangKernelPolynomial : Prop
  pIntegralSpecialization : Prop
  avoidsClassEnumeration : Prop

def ProducerTargetReady
    (target : ProducerTarget) : Prop :=
  target.selectedCMLangKernelPolynomial ∧
  target.pIntegralSpecialization ∧
  target.avoidsClassEnumeration

theorem producer_from_kernel_polynomial_target
    (poly : KernelPolynomial)
    (velu : VeluDenominator)
    (target : ProducerTarget)
    (h_poly : KernelPolynomialRealizesResidual poly)
    (h_velu : velu.squareOfKernelPolynomial)
    (h_target : ProducerTargetReady target) :
    poly.divisorEqualsSubgroupResidual ∧
    velu.squareOfKernelPolynomial ∧
    target.selectedCMLangKernelPolynomial ∧
    target.pIntegralSpecialization ∧
    target.avoidsClassEnumeration := by
  rcases h_poly with ⟨_h_roots, _h_degree, h_divisor⟩
  rcases h_target with ⟨h_cm, h_integral, h_no_enum⟩
  exact ⟨h_divisor, h_velu, h_cm, h_integral, h_no_enum⟩

def p24C : Nat := 179
def p24KernelPolynomialDegree : Nat := (p24C - 1) / 2
def p24KernelDivisorPoleOrder : Nat := 2 * p24KernelPolynomialDegree
def p24VeluXDenominatorDegree : Nat := 2 * p24KernelPolynomialDegree

theorem p24_kernel_polynomial_degree :
    p24KernelPolynomialDegree = 89 := by
  decide

theorem p24_kernel_divisor_pole_order :
    p24KernelDivisorPoleOrder = 178 := by
  decide

theorem p24_velu_x_denominator_degree :
    p24VeluXDenominatorDegree = 178 := by
  decide

end P24.TraceGcdReducedAnchorKernelPolynomialGate
