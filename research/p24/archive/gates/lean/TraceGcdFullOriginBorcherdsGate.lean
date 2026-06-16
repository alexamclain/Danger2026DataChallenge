/-!
Finite gate for the full-origin Borcherds bridge in the trace-GCD route.

The full-origin route is useful only if a closed automorphic/Fitting product
`psiFull` is proved to compute the actual full-origin determinant norm up to
p-units.  This file records the finite implication after that arithmetic
input is supplied:

* zero local intersection makes `psiFull` a p-unit;
* p-unit comparison transfers this to the actual full-origin norm;
* the full-origin norm detects zero of the reduced right product;
* the reduced right product detects every translated Chow/Schubert zero;
* therefore the selected trace-GCD row is good.

No determinant, Chow form, class field, or Borcherds product is constructed
here.  This is the proof plumbing that the missing arithmetic theorem must
instantiate.
-/

namespace P24.TraceGcdFullOriginBorcherdsGate

def TransfersPUnit {α : Type} (source target : α) (PUnit : α → Prop) :
    Prop :=
  PUnit source → PUnit target

def GlobalLocalIntersectionFormula {α LocalData : Type}
    (psi : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData) : Prop :=
  LocalIntersectionZero localData → PUnit psi

def ChowDetectsBad {Index α : Type} [Zero α]
    (chow : Index → α)
    (Bad : Index → Prop) : Prop :=
  ∀ t, Bad t → chow t = 0

def RightProductDetectsChowZeros {Index α : Type} [Zero α]
    (chow : Index → α)
    (rightProduct : α) : Prop :=
  ∀ t, chow t = 0 → rightProduct = 0

def FullNormDetectsRightProductZero {α : Type} [Zero α]
    (rightProduct fullNorm : α) : Prop :=
  rightProduct = 0 → fullNorm = 0

theorem full_norm_punit_from_borcherds_local_intersection
    {α LocalData : Type}
    (psiFull fullNorm : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_formula :
      GlobalLocalIntersectionFormula psiFull PUnit
        LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psiFull fullNorm PUnit)
    (h_zero : LocalIntersectionZero localData) :
    PUnit fullNorm :=
  h_compare (h_formula h_zero)

theorem right_product_nonzero_from_full_origin_borcherds
    {α LocalData : Type} [Zero α]
    (psiFull fullNorm rightProduct : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_formula :
      GlobalLocalIntersectionFormula psiFull PUnit
        LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psiFull fullNorm PUnit)
    (h_zero : LocalIntersectionZero localData)
    (h_full_detects :
      FullNormDetectsRightProductZero rightProduct fullNorm) :
    rightProduct ≠ 0 := by
  intro h_right_zero
  have h_full_punit : PUnit fullNorm :=
    full_norm_punit_from_borcherds_local_intersection
      psiFull fullNorm PUnit LocalIntersectionZero localData
      h_formula h_compare h_zero
  have h_full_nonzero : fullNorm ≠ 0 :=
    h_punit_nonzero fullNorm h_full_punit
  exact h_full_nonzero (h_full_detects h_right_zero)

theorem no_chow_zero_from_full_origin_borcherds
    {Index α LocalData : Type} [Zero α]
    (chow : Index → α)
    (psiFull fullNorm rightProduct : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_right_detects :
      RightProductDetectsChowZeros chow rightProduct)
    (h_formula :
      GlobalLocalIntersectionFormula psiFull PUnit
        LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psiFull fullNorm PUnit)
    (h_zero : LocalIntersectionZero localData)
    (h_full_detects :
      FullNormDetectsRightProductZero rightProduct fullNorm) :
    ∀ t, chow t ≠ 0 := by
  intro t h_chow_zero
  have h_right_nonzero : rightProduct ≠ 0 :=
    right_product_nonzero_from_full_origin_borcherds
      psiFull fullNorm rightProduct PUnit LocalIntersectionZero localData
      h_punit_nonzero h_formula h_compare h_zero h_full_detects
  exact h_right_nonzero (h_right_detects t h_chow_zero)

theorem no_bad_from_full_origin_borcherds
    {Index α LocalData : Type} [Zero α]
    (chow : Index → α)
    (Bad : Index → Prop)
    (psiFull fullNorm rightProduct : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_right_detects :
      RightProductDetectsChowZeros chow rightProduct)
    (h_formula :
      GlobalLocalIntersectionFormula psiFull PUnit
        LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psiFull fullNorm PUnit)
    (h_zero : LocalIntersectionZero localData)
    (h_full_detects :
      FullNormDetectsRightProductZero rightProduct fullNorm) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_chow_nonzero : chow t ≠ 0 :=
    no_chow_zero_from_full_origin_borcherds
      chow psiFull fullNorm rightProduct PUnit LocalIntersectionZero
      localData h_punit_nonzero h_right_detects h_formula h_compare h_zero
      h_full_detects t
  exact h_chow_nonzero (h_bad_chow t h_bad)

theorem selected_good_from_full_origin_borcherds
    {Index α LocalData : Type} [Zero α]
    (chow : Index → α)
    (Bad Good : Index → Prop)
    (selected : Index)
    (psiFull fullNorm rightProduct : α)
    (PUnit : α → Prop)
    (LocalIntersectionZero : LocalData → Prop)
    (localData : LocalData)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_bad_chow : ChowDetectsBad chow Bad)
    (h_right_detects :
      RightProductDetectsChowZeros chow rightProduct)
    (h_formula :
      GlobalLocalIntersectionFormula psiFull PUnit
        LocalIntersectionZero localData)
    (h_compare : TransfersPUnit psiFull fullNorm PUnit)
    (h_zero : LocalIntersectionZero localData)
    (h_full_detects :
      FullNormDetectsRightProductZero rightProduct fullNorm)
    (h_no_bad_good : ∀ t, ¬ Bad t → Good t) :
    Good selected := by
  exact h_no_bad_good selected
    (no_bad_from_full_origin_borcherds
      chow Bad psiFull fullNorm rightProduct PUnit LocalIntersectionZero
      localData h_punit_nonzero h_bad_chow h_right_detects h_formula
      h_compare h_zero h_full_detects selected)

theorem p24_full_origin_borcherds_payload_subsqrt :
    2 < 1000000000000 := by
  decide

end P24.TraceGcdFullOriginBorcherdsGate
