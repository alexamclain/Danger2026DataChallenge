/-!
Finite handoff gate for adjacent-anchor cyclic divisibility.

The Python gate

  p24/trace_gcd_fixed_frequency_p24_adjacent_anchor_cyclic_divisibility_gate.py

checks the finite algebra:

* one adjacent anchor `T0` is rho-fixed iff its six nontrivial order-7
  projectors vanish;
* equivalently, the degree `< 7` cyclic coordinate polynomial of `T0` is
  divisible by `Phi_7(y)=1+y+...+y^6`.

This records the proof contract for the p24 producer.  The arithmetic input is
still construction of the selected CM/Lang adjacent-trace anchor.
-/

namespace P24.TraceGcdAdjacentAnchorCyclicDivisibilityGate

structure AdjacentAnchor where
  rhoFixed : Prop
  nontrivialProjectorsZero : Prop
  phi7Divisible : Prop

def SatisfiesCyclicDivisibilityCriterion (anchor : AdjacentAnchor) : Prop :=
  (anchor.rhoFixed ↔ anchor.nontrivialProjectorsZero) ∧
  (anchor.nontrivialProjectorsZero ↔ anchor.phi7Divisible)

theorem rho_fixed_from_phi7_divisibility
    (anchor : AdjacentAnchor)
    (h : SatisfiesCyclicDivisibilityCriterion anchor)
    (h_phi : anchor.phi7Divisible) :
    anchor.rhoFixed := by
  exact h.1.mpr (h.2.mpr h_phi)

theorem phi7_divisibility_from_rho_fixed
    (anchor : AdjacentAnchor)
    (h : SatisfiesCyclicDivisibilityCriterion anchor)
    (h_fixed : anchor.rhoFixed) :
    anchor.phi7Divisible := by
  exact h.2.mp (h.1.mp h_fixed)

structure P24AdjacentAnchorCyclicTarget where
  rhoOrder : Nat
  nontrivialProjectorCount : Nat
  cyclicRemainderDegree : Nat
  compressedRightDifferenceEquations : Nat

def p24Target : P24AdjacentAnchorCyclicTarget where
  rhoOrder := 7
  nontrivialProjectorCount := 6
  cyclicRemainderDegree := 6
  compressedRightDifferenceEquations := 48

theorem p24_adjacent_anchor_cyclic_target_numbers :
    p24Target.rhoOrder = 7 ∧
    p24Target.nontrivialProjectorCount = 6 ∧
    p24Target.cyclicRemainderDegree = 6 ∧
    p24Target.compressedRightDifferenceEquations = 48 := by
  decide

end P24.TraceGcdAdjacentAnchorCyclicDivisibilityGate
