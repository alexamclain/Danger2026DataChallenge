/-!
Finite gate for the trace-pairing/subspace-polynomial bridge.

The arithmetic data supply selected leading Lang/Fitting coordinates

    c_1,...,c_d in L.

There are two finite ways to detect whether these coordinates span `L`:

* the trace-pairing matrix
      B_ij = Tr(lambda_j * c_i)
  has nonzero determinant;
* the incremental subspace-polynomial residual product
      prod_i Norm(P_{i-1}(c_i))
  is nonzero.

This file does not construct traces, determinants, norms, or subspace
polynomials.  It records the finite handoff: once both quantities detect the
same full-span proposition, a p-unit residual product proves the trace-GCD
determinant is nonzero and rules out the associated bad-lambda event.
-/

namespace P24.TraceGcdTracePairingSubspaceBridgeGate

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def TracePairingDetectsSpan {Scalar : Type} [Zero Scalar]
    (traceDet : Scalar)
    (FullSpan : Prop) : Prop :=
  traceDet ≠ 0 ↔ FullSpan

def ResidualProductDetectsSpan {Scalar : Type} [Zero Scalar]
    (residualProduct : Scalar)
    (FullSpan : Prop) : Prop :=
  residualProduct ≠ 0 ↔ FullSpan

def SameSpanDetectors {Scalar : Type} [Zero Scalar]
    (traceDet residualProduct : Scalar)
    (FullSpan : Prop) : Prop :=
  TracePairingDetectsSpan traceDet FullSpan ∧
    ResidualProductDetectsSpan residualProduct FullSpan

def BadForcesTraceDetZero {Scalar : Type} [Zero Scalar]
    (Bad : Prop)
    (traceDet : Scalar) : Prop :=
  Bad → traceDet = 0

theorem trace_det_nonzero_iff_residual_product_nonzero
    {Scalar : Type} [Zero Scalar]
    (traceDet residualProduct : Scalar)
    (FullSpan : Prop)
    (h_bridge : SameSpanDetectors traceDet residualProduct FullSpan) :
    traceDet ≠ 0 ↔ residualProduct ≠ 0 := by
  constructor
  · intro h_trace
    exact h_bridge.2.2 (h_bridge.1.1 h_trace)
  · intro h_residual
    exact h_bridge.1.2 (h_bridge.2.1 h_residual)

theorem trace_det_nonzero_from_residual_product_nonzero
    {Scalar : Type} [Zero Scalar]
    (traceDet residualProduct : Scalar)
    (FullSpan : Prop)
    (h_bridge : SameSpanDetectors traceDet residualProduct FullSpan)
    (h_residual_nonzero : residualProduct ≠ 0) :
    traceDet ≠ 0 :=
  (trace_det_nonzero_iff_residual_product_nonzero
    traceDet residualProduct FullSpan h_bridge).2 h_residual_nonzero

theorem residual_product_nonzero_from_trace_det_nonzero
    {Scalar : Type} [Zero Scalar]
    (traceDet residualProduct : Scalar)
    (FullSpan : Prop)
    (h_bridge : SameSpanDetectors traceDet residualProduct FullSpan)
    (h_trace_nonzero : traceDet ≠ 0) :
    residualProduct ≠ 0 :=
  (trace_det_nonzero_iff_residual_product_nonzero
    traceDet residualProduct FullSpan h_bridge).1 h_trace_nonzero

theorem trace_det_nonzero_from_residual_punit
    {Scalar : Type} [Zero Scalar]
    (traceDet residualProduct residualInv : Scalar)
    (FullSpan : Prop)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_bridge : SameSpanDetectors traceDet residualProduct FullSpan)
    (h_payload : UnitPayload residualProduct residualInv UnitRel) :
    traceDet ≠ 0 :=
  trace_det_nonzero_from_residual_product_nonzero
    traceDet residualProduct FullSpan h_bridge
    (h_unit_nonzero residualProduct residualInv h_payload)

theorem no_bad_from_residual_punit
    {Scalar : Type} [Zero Scalar]
    (Bad : Prop)
    (traceDet residualProduct residualInv : Scalar)
    (FullSpan : Prop)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_bridge : SameSpanDetectors traceDet residualProduct FullSpan)
    (h_bad_zero : BadForcesTraceDetZero Bad traceDet)
    (h_payload : UnitPayload residualProduct residualInv UnitRel) :
    ¬ Bad := by
  intro h_bad
  have h_trace_nonzero : traceDet ≠ 0 :=
    trace_det_nonzero_from_residual_punit
      traceDet residualProduct residualInv FullSpan UnitRel
      h_unit_nonzero h_bridge h_payload
  exact h_trace_nonzero (h_bad_zero h_bad)

theorem no_bad_from_trace_det_punit
    {Scalar : Type} [Zero Scalar]
    (Bad : Prop)
    (traceDet traceInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_bad_zero : BadForcesTraceDetZero Bad traceDet)
    (h_payload : UnitPayload traceDet traceInv UnitRel) :
    ¬ Bad := by
  intro h_bad
  have h_trace_nonzero : traceDet ≠ 0 :=
    h_unit_nonzero traceDet traceInv h_payload
  exact h_trace_nonzero (h_bad_zero h_bad)

theorem p24_leading_dimension_split :
    4 * 35 + 16 = 156 := by
  decide

theorem p24_trace_pairing_bridge_payload_subsqrt :
    2 < 1000000000000 := by
  decide

end P24.TraceGcdTracePairingSubspaceBridgeGate
