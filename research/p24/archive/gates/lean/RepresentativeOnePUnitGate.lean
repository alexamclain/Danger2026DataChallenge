/-!
Finite gate for the one-representative p-unit certificate surface.

The arithmetic input is the selected-prime p-unit theorem for one
representative leading Moore determinant

  L_rep = B_rep * T_rep.

Right-unit equivariance transports that representative row around the six
right Frobenius factors.  This file records the finite plumbing:

* one representative p-unit gives the first row-good statement;
* the unit cycle propagates row-goodness to all six deletion rows;
* all deletion rows good imply delete-one separation;
* delete-one separation implies right support at least two;
* support at least two is the finite mixed-rank handoff.

No class-field periods, Moore determinants, Lang bases, or p-adic unit
theorems are constructed here.
-/

namespace P24.RepresentativeOnePUnitGate

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def AllSixRowsGood {Row : Type}
    (GoodRow : Row → Prop)
    (r1 r2 r3 r4 r5 r6 : Row) : Prop :=
  GoodRow r1 ∧ GoodRow r2 ∧ GoodRow r3 ∧
    GoodRow r4 ∧ GoodRow r5 ∧ GoodRow r6

def DeleteOneSeparates {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value) : Prop :=
  ∀ deleted lambda, lambda ≠ 0 →
    ∃ orbit, orbit ≠ deleted ∧ traceMap lambda orbit ≠ 0

def SupportAtLeastTwo {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value) : Prop :=
  ∀ lambda, lambda ≠ 0 →
    ∃ orbit₁ orbit₂,
      orbit₁ ≠ orbit₂ ∧
      traceMap lambda orbit₁ ≠ 0 ∧
      traceMap lambda orbit₂ ≠ 0

theorem all_six_rows_from_representative_cycle
    {Row Scalar : Type}
    (GoodRow : Row → Prop)
    (r1 r2 r3 r4 r5 r6 : Row)
    (rep inv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_rep_to_row1 : UnitPayload rep inv UnitRel → GoodRow r1)
    (h12 : GoodRow r1 → GoodRow r2)
    (h23 : GoodRow r2 → GoodRow r3)
    (h34 : GoodRow r3 → GoodRow r4)
    (h45 : GoodRow r4 → GoodRow r5)
    (h56 : GoodRow r5 → GoodRow r6)
    (_h61 : GoodRow r6 → GoodRow r1)
    (h_payload : UnitPayload rep inv UnitRel) :
    AllSixRowsGood GoodRow r1 r2 r3 r4 r5 r6 := by
  have h1 : GoodRow r1 := h_rep_to_row1 h_payload
  have h2 : GoodRow r2 := h12 h1
  have h3 : GoodRow r3 := h23 h2
  have h4 : GoodRow r4 := h34 h3
  have h5 : GoodRow r5 := h45 h4
  have h6 : GoodRow r6 := h56 h5
  exact ⟨h1, h2, h3, h4, h5, h6⟩

theorem support_at_least_two_from_delete_one
    {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value] [Inhabited Orbit]
    (traceMap : Lambda → Orbit → Value)
    (h_delete : DeleteOneSeparates traceMap) :
    SupportAtLeastTwo traceMap := by
  intro lambda h_nonzero
  let deleted : Orbit := default
  rcases h_delete deleted lambda h_nonzero with
    ⟨orbit₀, _h_orbit₀_not_deleted, h_orbit₀_nonzero⟩
  rcases h_delete orbit₀ lambda h_nonzero with
    ⟨orbit₁, h_orbit₁_ne_orbit₀, h_orbit₁_nonzero⟩
  exact ⟨orbit₀, orbit₁, h_orbit₁_ne_orbit₀.symm,
    h_orbit₀_nonzero, h_orbit₁_nonzero⟩

theorem representative_punit_to_mixed_rank
    {Row Lambda Orbit Value Scalar Cert : Type}
    [Zero Lambda] [Zero Value] [Inhabited Orbit]
    (GoodRow : Row → Prop)
    (traceMap : Lambda → Orbit → Value)
    (RankGood : Cert → Prop)
    (cert : Cert)
    (r1 r2 r3 r4 r5 r6 : Row)
    (rep inv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_rep_to_row1 : UnitPayload rep inv UnitRel → GoodRow r1)
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
    (h_payload : UnitPayload rep inv UnitRel) :
    RankGood cert := by
  have h_rows : AllSixRowsGood GoodRow r1 r2 r3 r4 r5 r6 :=
    all_six_rows_from_representative_cycle
      GoodRow r1 r2 r3 r4 r5 r6 rep inv UnitRel h_rep_to_row1
      h12 h23 h34 h45 h56 h61 h_payload
  exact h_support_to_rank
    (support_at_least_two_from_delete_one traceMap
      (h_rows_to_delete h_rows))

theorem p24_representative_unit_payload_subsqrt :
    2 < 1000000000000 := by
  decide

end P24.RepresentativeOnePUnitGate
