/-!
Finite gate for the residual-product prefix/tail split.

For the p24 representative residual product, the selected coordinates split as

    156 = 4*35 + 16.

The full residual product factors as a prefix product times a quotient-tail
product.  This file records only the finite handoff: if that split preserves
p-units, then prefix and tail p-units imply the full residual p-unit, which
then feeds the trace-pairing/subspace bridge.
-/

namespace P24.TraceGcdResidualPrefixTailGate

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def SplitUnitLaw {Scalar : Type}
    (pfx tail full : Scalar)
    (PUnit : Scalar → Prop) : Prop :=
  PUnit pfx → PUnit tail → PUnit full

def SplitZeroLaw {Scalar : Type} [Zero Scalar]
    (pfx tail full : Scalar) : Prop :=
  full ≠ 0 ↔ pfx ≠ 0 ∧ tail ≠ 0

theorem full_punit_from_prefix_tail_punits
    {Scalar : Type}
    (pfx tail full : Scalar)
    (PUnit : Scalar → Prop)
    (h_split : SplitUnitLaw pfx tail full PUnit)
    (h_pfx : PUnit pfx)
    (h_tail : PUnit tail) :
    PUnit full :=
  h_split h_pfx h_tail

theorem full_nonzero_from_prefix_tail_nonzero
    {Scalar : Type} [Zero Scalar]
    (pfx tail full : Scalar)
    (h_split : SplitZeroLaw pfx tail full)
    (h_pfx : pfx ≠ 0)
    (h_tail : tail ≠ 0) :
    full ≠ 0 :=
  h_split.2 ⟨h_pfx, h_tail⟩

theorem prefix_tail_nonzero_from_full_nonzero
    {Scalar : Type} [Zero Scalar]
    (pfx tail full : Scalar)
    (h_split : SplitZeroLaw pfx tail full)
    (h_full : full ≠ 0) :
    pfx ≠ 0 ∧ tail ≠ 0 :=
  h_split.1 h_full

theorem full_payload_from_prefix_tail_payloads
    {Scalar : Type}
    (pfx pfxInv tail tailInv full : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (PUnit : Scalar → Prop)
    (h_unitrel_punit :
      ∀ value inverse, UnitRel value inverse → PUnit value)
    (h_split : SplitUnitLaw pfx tail full PUnit)
    (h_pfx_payload : UnitPayload pfx pfxInv UnitRel)
    (h_tail_payload : UnitPayload tail tailInv UnitRel) :
    PUnit full :=
  full_punit_from_prefix_tail_punits pfx tail full PUnit h_split
    (h_unitrel_punit pfx pfxInv h_pfx_payload)
    (h_unitrel_punit tail tailInv h_tail_payload)

theorem p24_prefix_tail_dimension_split :
    4 * 35 + 16 = 156 := by
  decide

theorem p24_prefix_tail_payload_subsqrt :
    4 < 1000000000000 := by
  decide

end P24.TraceGcdResidualPrefixTailGate
