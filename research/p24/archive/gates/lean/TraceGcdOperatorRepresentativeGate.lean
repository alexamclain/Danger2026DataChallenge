/-!
End-to-end finite gate for the trace-GCD one-operator certificate.

The smallest current verifier payload for the mixed representative route is

  Norm_trace, Norm_trace^{-1}

where `Norm_trace` is intended to be the determinant/resultant/operator norm
of the actual trace-GCD determinant sequence

  Delta(t) = det(P V_t A),    t mod 211.

This file records only the finite implication:

* the operator norm is a p-unit, hence nonzero;
* the honest operator norm detects any zero in the actual Delta sequence;
* therefore the selected representative determinant is nonzero;
* the selected row is good;
* right-unit equivariance propagates row-goodness to all six deletion rows;
* delete-one separation and the support-to-rank handoff give the mixed rank
  certificate.

No CM periods, determinants, operator norms, or p-adic unit theorem are
constructed here.
-/

namespace P24.TraceGcdOperatorRepresentativeGate

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def OperatorNormDetectsZero {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (norm : Scalar) : Prop :=
  (∃ t, Delta t = 0) → norm = 0

def AllSixRowsGood {Row : Type}
    (GoodRow : Row → Prop)
    (r1 r2 r3 r4 r5 r6 : Row) : Prop :=
  GoodRow r1 ∧ GoodRow r2 ∧ GoodRow r3 ∧
    GoodRow r4 ∧ GoodRow r5 ∧ GoodRow r6

def DeleteOneSeparates {Lambda RightOrbit Value : Type}
    [Zero Lambda] [Zero Value]
    (traceMap : Lambda → RightOrbit → Value) : Prop :=
  ∀ deleted lambda, lambda ≠ 0 →
    ∃ orbit, orbit ≠ deleted ∧ traceMap lambda orbit ≠ 0

def SupportAtLeastTwo {Lambda RightOrbit Value : Type}
    [Zero Lambda] [Zero Value]
    (traceMap : Lambda → RightOrbit → Value) : Prop :=
  ∀ lambda, lambda ≠ 0 →
    ∃ orbit₁ orbit₂,
      orbit₁ ≠ orbit₂ ∧
      traceMap lambda orbit₁ ≠ 0 ∧
      traceMap lambda orbit₂ ≠ 0

theorem deltas_nonzero_from_operator_norm_unit
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (norm normInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : OperatorNormDetectsZero Delta norm)
    (h_payload : UnitPayload norm normInv UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_norm_nonzero : norm ≠ 0 :=
    h_unit_nonzero norm normInv h_payload
  exact h_norm_nonzero (h_detects ⟨t, h_delta_zero⟩)

theorem all_six_rows_from_selected_delta
    {Index Row Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (GoodRow : Row → Prop)
    (selected : Index)
    (r1 r2 r3 r4 r5 r6 : Row)
    (norm normInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : OperatorNormDetectsZero Delta norm)
    (h_delta_to_row1 : Delta selected ≠ 0 → GoodRow r1)
    (h12 : GoodRow r1 → GoodRow r2)
    (h23 : GoodRow r2 → GoodRow r3)
    (h34 : GoodRow r3 → GoodRow r4)
    (h45 : GoodRow r4 → GoodRow r5)
    (h56 : GoodRow r5 → GoodRow r6)
    (_h61 : GoodRow r6 → GoodRow r1)
    (h_payload : UnitPayload norm normInv UnitRel) :
    AllSixRowsGood GoodRow r1 r2 r3 r4 r5 r6 := by
  have h_delta_selected : Delta selected ≠ 0 :=
    deltas_nonzero_from_operator_norm_unit
      Delta norm normInv UnitRel h_unit_nonzero h_detects h_payload selected
  have h1 : GoodRow r1 := h_delta_to_row1 h_delta_selected
  have h2 : GoodRow r2 := h12 h1
  have h3 : GoodRow r3 := h23 h2
  have h4 : GoodRow r4 := h34 h3
  have h5 : GoodRow r5 := h45 h4
  have h6 : GoodRow r6 := h56 h5
  exact ⟨h1, h2, h3, h4, h5, h6⟩

theorem support_at_least_two_from_delete_one
    {Lambda RightOrbit Value : Type}
    [Zero Lambda] [Zero Value] [Inhabited RightOrbit]
    (traceMap : Lambda → RightOrbit → Value)
    (h_delete : DeleteOneSeparates traceMap) :
    SupportAtLeastTwo traceMap := by
  intro lambda h_nonzero
  let deleted : RightOrbit := default
  rcases h_delete deleted lambda h_nonzero with
    ⟨orbit₀, _h_orbit₀_not_deleted, h_orbit₀_nonzero⟩
  rcases h_delete orbit₀ lambda h_nonzero with
    ⟨orbit₁, h_orbit₁_ne_orbit₀, h_orbit₁_nonzero⟩
  exact ⟨orbit₀, orbit₁, h_orbit₁_ne_orbit₀.symm,
    h_orbit₀_nonzero, h_orbit₁_nonzero⟩

theorem operator_norm_to_mixed_rank
    {Index Row Lambda RightOrbit Value Scalar Cert : Type}
    [Zero Lambda] [Zero Value] [Zero Scalar] [Inhabited RightOrbit]
    (Delta : Index → Scalar)
    (GoodRow : Row → Prop)
    (traceMap : Lambda → RightOrbit → Value)
    (RankGood : Cert → Prop)
    (cert : Cert)
    (selected : Index)
    (r1 r2 r3 r4 r5 r6 : Row)
    (norm normInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects : OperatorNormDetectsZero Delta norm)
    (h_delta_to_row1 : Delta selected ≠ 0 → GoodRow r1)
    (h12 : GoodRow r1 → GoodRow r2)
    (h23 : GoodRow r2 → GoodRow r3)
    (h34 : GoodRow r3 → GoodRow r4)
    (h45 : GoodRow r4 → GoodRow r5)
    (h56 : GoodRow r5 → GoodRow r6)
    (h61 : GoodRow r6 → GoodRow r1)
    (h_rows_to_delete :
      AllSixRowsGood GoodRow r1 r2 r3 r4 r5 r6 →
        DeleteOneSeparates traceMap)
    (h_support_to_rank :
      SupportAtLeastTwo traceMap → RankGood cert)
    (h_payload : UnitPayload norm normInv UnitRel) :
    RankGood cert := by
  have h_rows : AllSixRowsGood GoodRow r1 r2 r3 r4 r5 r6 :=
    all_six_rows_from_selected_delta
      Delta GoodRow selected r1 r2 r3 r4 r5 r6 norm normInv UnitRel
      h_unit_nonzero h_detects h_delta_to_row1 h12 h23 h34 h45 h56 h61
      h_payload
  exact h_support_to_rank
    (support_at_least_two_from_delete_one traceMap
      (h_rows_to_delete h_rows))

theorem p24_operator_payload_subsqrt :
    2 < 1000000000000 := by
  decide

theorem p24_decomposed_degree_subsqrt :
    66254 + 3107441 < 1000000000000 := by
  decide

end P24.TraceGcdOperatorRepresentativeGate
