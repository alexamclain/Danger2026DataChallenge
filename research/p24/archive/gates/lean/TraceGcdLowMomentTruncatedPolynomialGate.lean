/-!
Finite handoff for the truncated-polynomial form of low moments.

Newton identities identify the first `k` power sums with the first `k`
elementary coefficients whenever `1, ..., k` are units.  For p24, the first
coefficient `e1` is the parent period, so the producer can target the next
coefficients of the selected child polynomial.
-/

namespace P24.TraceGcdLowMomentTruncatedPolynomialGate

structure TruncatedChildPolynomialTarget where
  coefficientCountIncludingE1 : Nat
  e1KnownFromParent : Prop

def NewCoefficientCount (target : TruncatedChildPolynomialTarget) : Nat :=
  target.coefficientCountIncludingE1 - 1

def p24FirstLayerTarget : TruncatedChildPolynomialTarget where
  coefficientCountIncludingE1 := 4
  e1KnownFromParent := True

def p24SecondLayerTarget : TruncatedChildPolynomialTarget where
  coefficientCountIncludingE1 := 26
  e1KnownFromParent := True

def p24SelectorCoefficientConstraints : Nat :=
  p24FirstLayerTarget.coefficientCountIncludingE1 +
  p24SecondLayerTarget.coefficientCountIncludingE1

def p24NewProducerCoefficients : Nat :=
  NewCoefficientCount p24FirstLayerTarget +
  NewCoefficientCount p24SecondLayerTarget

def p24FirstLayerParentCount : Nat := 2

def p24SecondLayerParentCount : Nat := 314

def p24ParentFieldCoefficientSurface : Nat :=
  p24FirstLayerParentCount *
    p24FirstLayerTarget.coefficientCountIncludingE1 +
  p24SecondLayerParentCount *
    p24SecondLayerTarget.coefficientCountIncludingE1

def p24SqrtFloor : Nat := 1000000000000

theorem p24_selector_coefficient_constraints :
    p24SelectorCoefficientConstraints = 30 := by
  decide

theorem p24_new_producer_coefficients :
    p24NewProducerCoefficients = 28 := by
  decide

theorem p24_parent_field_coefficient_surface :
    p24ParentFieldCoefficientSurface = 8172 := by
  decide

theorem p24_parent_field_coefficient_surface_subsqrt :
    p24ParentFieldCoefficientSurface < p24SqrtFloor := by
  decide

theorem e1_known_first_layer :
    p24FirstLayerTarget.e1KnownFromParent := by
  trivial

theorem e1_known_second_layer :
    p24SecondLayerTarget.e1KnownFromParent := by
  trivial

end P24.TraceGcdLowMomentTruncatedPolynomialGate
