/-!
Finite gate for a possible Borcherds/local-intersection proof of the
trace-frame leading p-unit.

This file deliberately does not formalize Borcherds products, valuations, or
CM cycles.  It records the finite implication a future arithmetic theorem
would have to supply:

* a phase-aware product/divisor value `borcherdsValue`;
* a comparison showing it equals the trace-frame leading norm up to p-units;
* a local-intersection formula proving `borcherdsValue` is a p-unit;
* therefore the trace-frame leading norm is a p-unit/nonzero, and the
  existing trace-frame gates apply.

The missing input remains arithmetic: construct the phase-aware divisor and
prove its selected-prime local intersection is zero.
-/

namespace P24.TraceFrameBorcherdsPUnitGate

def TransfersPUnit {α : Type} (source target : α) (PUnit : α → Prop) : Prop :=
  PUnit source → PUnit target

theorem leading_norm_punit_from_borcherds_comparison
    {α : Type}
    (borcherdsValue leadingNorm : α)
    (PUnit : α → Prop)
    (h_compare :
      TransfersPUnit borcherdsValue leadingNorm PUnit)
    (h_borcherds_punit : PUnit borcherdsValue) :
    PUnit leadingNorm :=
  h_compare h_borcherds_punit

theorem borcherds_punit_from_zero_local_intersection
    {α LocalData : Type}
    (borcherdsValue : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_local_formula :
      LocalIntersectionZero localData → PUnit borcherdsValue)
    (h_zero_intersection : LocalIntersectionZero localData) :
    PUnit borcherdsValue :=
  h_local_formula h_zero_intersection

theorem leading_norm_punit_from_local_intersection
    {α LocalData : Type}
    (borcherdsValue leadingNorm : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_local_formula :
      LocalIntersectionZero localData → PUnit borcherdsValue)
    (h_compare :
      TransfersPUnit borcherdsValue leadingNorm PUnit)
    (h_zero_intersection : LocalIntersectionZero localData) :
    PUnit leadingNorm :=
  leading_norm_punit_from_borcherds_comparison
    borcherdsValue leadingNorm PUnit h_compare
    (borcherds_punit_from_zero_local_intersection
      borcherdsValue PUnit LocalIntersectionZero localData
      h_local_formula h_zero_intersection)

theorem leading_norm_nonzero_from_punit
    {α : Type} [Zero α]
    (leadingNorm : α)
    (PUnit : α → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_leading_punit : PUnit leadingNorm) :
    leadingNorm ≠ 0 :=
  h_punit_nonzero leadingNorm h_leading_punit

theorem leading_norm_nonzero_from_borcherds_local_intersection
    {α LocalData : Type} [Zero α]
    (borcherdsValue leadingNorm : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_local_formula :
      LocalIntersectionZero localData → PUnit borcherdsValue)
    (h_compare :
      TransfersPUnit borcherdsValue leadingNorm PUnit)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_zero_intersection : LocalIntersectionZero localData) :
    leadingNorm ≠ 0 :=
  leading_norm_nonzero_from_punit leadingNorm PUnit h_punit_nonzero
    (leading_norm_punit_from_local_intersection
      borcherdsValue leadingNorm PUnit LocalIntersectionZero localData
      h_local_formula h_compare h_zero_intersection)

end P24.TraceFrameBorcherdsPUnitGate
