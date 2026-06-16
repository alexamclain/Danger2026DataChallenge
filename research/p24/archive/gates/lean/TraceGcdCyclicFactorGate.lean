/-!
Finite gate for factorwise cyclic-algebra trace-GCD certificates.

The trace-GCD determinant sequence is indexed by right roots

    Delta t = det(P V_t A).

A base-field polynomial interpolating printed determinant values is unsafe
unless the values are Frobenius-compatible.  The safe algebraic certificate is
factorwise only after the arithmetic producer supplies the actual descended or
twisted orbit-algebra residue of the actual determinant section, together with
a Bezout/unit witness in that orbit algebra.

This file keeps only the finite logic:

* each index `t` belongs to a factor/orbit;
* if `Delta t = 0`, the actual residue in that factor cannot be a unit;
* the certificate supplies a unit witness for every factor;
* therefore no `Delta t` is zero.
-/

namespace P24.TraceGcdCyclicFactorGate

def FactorUnitPayload {Factor Quotient : Type}
    (residue inverse : Factor → Quotient)
    (UnitRel : Quotient → Quotient → Prop) : Prop :=
  ∀ factor, UnitRel (residue factor) (inverse factor)

def ZeroEvalForcesNonunit
    {Index Factor Scalar Quotient : Type} [Zero Scalar]
    (factorOf : Index → Factor)
    (Delta : Index → Scalar)
    (residue : Factor → Quotient)
    (UnitRel : Quotient → Quotient → Prop) : Prop :=
  ∀ t inverse, Delta t = 0 →
    ¬ UnitRel (residue (factorOf t)) inverse

theorem values_nonzero_from_factor_units
    {Index Factor Scalar Quotient : Type} [Zero Scalar]
    (factorOf : Index → Factor)
    (Delta : Index → Scalar)
    (residue inverse : Factor → Quotient)
    (UnitRel : Quotient → Quotient → Prop)
    (h_zero_nonunit :
      ZeroEvalForcesNonunit factorOf Delta residue UnitRel)
    (h_payload : FactorUnitPayload residue inverse UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_not_unit :
      ¬ UnitRel (residue (factorOf t)) (inverse (factorOf t)) :=
    h_zero_nonunit t (inverse (factorOf t)) h_delta_zero
  exact h_not_unit (h_payload (factorOf t))

theorem selected_good_from_factor_units
    {Index Factor Scalar Quotient : Type} [Zero Scalar]
    (factorOf : Index → Factor)
    (Delta : Index → Scalar)
    (residue inverse : Factor → Quotient)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Quotient → Quotient → Prop)
    (h_zero_nonunit :
      ZeroEvalForcesNonunit factorOf Delta residue UnitRel)
    (h_payload : FactorUnitPayload residue inverse UnitRel)
    (h_delta_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_delta_to_good selected
    (values_nonzero_from_factor_units factorOf Delta residue inverse UnitRel
      h_zero_nonunit h_payload selected)

end P24.TraceGcdCyclicFactorGate
