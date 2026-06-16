/-!
Finite handoff gate for generator-invariance of the reduced-anchor subgroup
kernel polynomial.

Once the selected order-`c` subgroup `H` is known, changing the generator of
`H` only permutes `H \ {O}`.  Thus the whole-subgroup kernel polynomial is a
single object, even though the oriented one-point divisors have `c-1`
diamond conjugates.
-/

namespace P24.TraceGcdReducedAnchorKernelGeneratorInvarianceGate

structure GeneratorInvariantKernel where
  generatorChangesPermuteNonzeroSubgroup : Prop
  kernelPolynomialDependsOnlyOnSubgroup : Prop

def KernelGeneratorInvariant (gate : GeneratorInvariantKernel) : Prop :=
  gate.generatorChangesPermuteNonzeroSubgroup ∧
  gate.kernelPolynomialDependsOnlyOnSubgroup

structure ConditionalSearchSurface where
  anchorSignChoices : Nat
  forcedKummerExponentChoices : Nat
  kernelPolynomialGeneratorOrbits : Nat

def ConditionalKernelCases (surface : ConditionalSearchSurface) : Nat :=
  surface.anchorSignChoices *
  surface.forcedKummerExponentChoices *
  surface.kernelPolynomialGeneratorOrbits

theorem conditional_surface_from_generator_invariance
    (gate : GeneratorInvariantKernel)
    (surface : ConditionalSearchSurface)
    (h_gate : KernelGeneratorInvariant gate)
    (h_signs : surface.anchorSignChoices = 2)
    (h_kummer : surface.forcedKummerExponentChoices = 1)
    (h_kernel : surface.kernelPolynomialGeneratorOrbits = 1) :
    ConditionalKernelCases surface = 2 ∧
    gate.kernelPolynomialDependsOnlyOnSubgroup := by
  rcases h_gate with ⟨_h_perm, h_depends⟩
  unfold ConditionalKernelCases
  rw [h_signs, h_kummer, h_kernel]
  exact ⟨by decide, h_depends⟩

def p24C : Nat := 179
def p24OrientedOnePointDiamondChoices : Nat := p24C - 1
def p24XCoordinateGeneratorPairs : Nat := (p24C - 1) / 2
def p24KernelPolynomialGeneratorOrbits : Nat := 1
def p24ConditionalKernelSearchCases : Nat := 2 * 1 * p24KernelPolynomialGeneratorOrbits

theorem p24_oriented_one_point_diamond_choices :
    p24OrientedOnePointDiamondChoices = 178 := by
  decide

theorem p24_x_coordinate_generator_pairs :
    p24XCoordinateGeneratorPairs = 89 := by
  decide

theorem p24_kernel_polynomial_generator_orbits :
    p24KernelPolynomialGeneratorOrbits = 1 := by
  decide

theorem p24_conditional_kernel_search_cases :
    p24ConditionalKernelSearchCases = 2 := by
  decide

end P24.TraceGcdReducedAnchorKernelGeneratorInvarianceGate
