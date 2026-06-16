/-!
Finite gate for the centered full-origin Borcherds bridge.

The arithmetic input would be a closed phase-aware product `psiFull` whose CM
value is a p-unit multiple of the full-origin centered Chow product.  The
origin action then makes this full-origin product a p-unit multiple of a power
of the 211-term right product.

This file checks only the finite handoff:

* zero local intersection gives `psiFull` a p-unit;
* p-unit comparison transfers to the full-origin norm;
* full-origin norm nonzero forces the right product nonzero;
* right product nonzero excludes every translated centered Chow zero.
-/

namespace P24.CenteredFullOriginBorcherdsGate

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

def p24M : Nat := 66254
def p24N : Nat := 3107441
def p24Right : Nat := 211
def p24MOverRight : Nat := p24M / p24Right
def p24FullOriginExponent : Nat := p24N * p24MOverRight

theorem p24_m_over_right_value :
    p24MOverRight = 314 := by
  decide

theorem p24_full_origin_exponent_value :
    p24FullOriginExponent = 975736474 := by
  decide

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

theorem p24_centered_full_origin_borcherds_payload_subsqrt :
    2 < 1000000000000 := by
  decide

end P24.CenteredFullOriginBorcherdsGate
