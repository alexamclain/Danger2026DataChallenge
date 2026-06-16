/-!
Finite handoff gate for functorial covariance of adjacent right-difference
trace values.

The arithmetic theorem remains external.  This file records the formal shape:

* pointwise semilinear covariance of the evaluated adjacent polynomials;
* the relative multiplier lies inside the trace subgroup, so quotient trace
  coordinates are not permuted;
* therefore the adjacent decomposition-trace values satisfy the same
  shift-6 covariance used by the covariance-telescope gate.
-/

namespace P24.TraceGcdRightDifferenceTraceCovarianceFunctorialGate

def PointwiseSemilinearCovariant {RightIndex Exponent Value : Type}
    (shift : RightIndex → RightIndex)
    (multiplier : Exponent → Exponent)
    (rho : Value → Value)
    (valueAt : RightIndex → Exponent → Value) : Prop :=
  ∀ index exponent,
    valueAt (shift index) (multiplier exponent) = rho (valueAt index exponent)

def MultiplierFixesTraceCosets {Coset : Type}
    (cosetMap : Coset → Coset) : Prop :=
  ∀ coset, cosetMap coset = coset

def TraceCovariant {RightIndex Coset TraceValue : Type}
    (shift : RightIndex → RightIndex)
    (rho : TraceValue → TraceValue)
    (traceAt : RightIndex → Coset → TraceValue) : Prop :=
  ∀ index coset, traceAt (shift index) coset = rho (traceAt index coset)

theorem trace_covariance_from_pointwise_covariance_inside_trace_subgroup
    {RightIndex Exponent Value Coset TraceValue : Type}
    (shift : RightIndex → RightIndex)
    (multiplier : Exponent → Exponent)
    (rhoValue : Value → Value)
    (rhoTrace : TraceValue → TraceValue)
    (valueAt : RightIndex → Exponent → Value)
    (cosetMap : Coset → Coset)
    (traceAt : RightIndex → Coset → TraceValue)
    (h_pointwise :
      PointwiseSemilinearCovariant shift multiplier rhoValue valueAt)
    (h_inside : MultiplierFixesTraceCosets cosetMap)
    (h_functorial :
      PointwiseSemilinearCovariant shift multiplier rhoValue valueAt →
      MultiplierFixesTraceCosets cosetMap →
      TraceCovariant shift rhoTrace traceAt) :
    TraceCovariant shift rhoTrace traceAt := by
  exact h_functorial h_pointwise h_inside

def p24RightShift : Nat := 6
def p24RightQuotient : Nat := 7
def p24RelativeQuotient : Nat := 8

theorem p24_shift6_coprime_to_7 :
    Nat.gcd p24RightShift p24RightQuotient = 1 := by
  decide

theorem p24_relative_quotient_count :
    p24RelativeQuotient = 8 := by
  decide

end P24.TraceGcdRightDifferenceTraceCovarianceFunctorialGate
