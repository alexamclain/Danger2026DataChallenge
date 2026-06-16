/-!
Finite gate for the fixed-frequency order-7 augmentation route.

The arithmetic theorem still has to prove the order-7 augmentation identity
for the actual p24 CM/Lang packet.  This file records only the finite
handoff:

* order-7 augmentation plus the negation covariance gives the seven
  fixed-frequency tail-in-prefix relations;
* tail-in-prefix plus prefix Plucker p-units makes every fixed frequency
  ordinary, so there are no fixed defect lines;
* no fixed defects reduce Frobenius-stable size-16 defect supports from
  1260 candidates to the 35 pure moving-orbit candidates.

No CM periods, resolvents, Gaussian sums, or local intersection theory are
formalized here.
-/

namespace P24.TraceGcdFixedFrequencyOrder7Gate

def Order7Augmentation (nontrivialZeroes quotientCharacters : Nat) : Prop :=
  nontrivialZeroes = quotientCharacters

def NegationCovariance (holds : Bool) : Prop :=
  holds = true

def DenominatorUnit (holds : Bool) : Prop :=
  holds = true

def FixedTailRelations (relations fixedCount : Nat) : Prop :=
  relations = fixedCount

def PrefixPluckerUnits (units fixedCount : Nat) : Prop :=
  units = fixedCount

def FixedOrdinaryFrequencies (ordinary fixedCount : Nat) : Prop :=
  ordinary = fixedCount

def NoFixedDefects (fixedDefects : Nat) : Prop :=
  fixedDefects = 0

def StableSupportReduction
    (before after pureMoving mixed : Nat) : Prop :=
  before = pureMoving + mixed ∧ after = pureMoving

def Order7SyzygyHandoff
    (nontrivialZeroes quotientCharacters fixedCount relations : Nat)
    (negation denominator : Bool) : Prop :=
  Order7Augmentation nontrivialZeroes quotientCharacters ->
  NegationCovariance negation ->
  DenominatorUnit denominator ->
  quotientCharacters = fixedCount - 1 ->
  FixedTailRelations relations fixedCount

theorem fixed_tail_relations_from_order7_augmentation
    (nontrivialZeroes quotientCharacters fixedCount relations : Nat)
    (negation denominator : Bool)
    (h_handoff :
      Order7SyzygyHandoff nontrivialZeroes quotientCharacters fixedCount
        relations negation denominator)
    (h_aug : Order7Augmentation nontrivialZeroes quotientCharacters)
    (h_neg : NegationCovariance negation)
    (h_unit : DenominatorUnit denominator)
    (h_count : quotientCharacters = fixedCount - 1) :
    FixedTailRelations relations fixedCount :=
  h_handoff h_aug h_neg h_unit h_count

theorem fixed_ordinaries_from_tail_relations_and_prefix_units
    (relations prefixUnits fixedCount ordinary : Nat)
    (h_relations : FixedTailRelations relations fixedCount)
    (h_prefix : PrefixPluckerUnits prefixUnits fixedCount)
    (h_ordinary : ordinary = Nat.min relations prefixUnits) :
    FixedOrdinaryFrequencies ordinary fixedCount := by
  unfold FixedTailRelations at h_relations
  unfold PrefixPluckerUnits at h_prefix
  unfold FixedOrdinaryFrequencies
  rw [h_ordinary, h_relations, h_prefix]
  exact Nat.min_self fixedCount

theorem no_fixed_defects_from_fixed_ordinaries
    (ordinary fixedCount fixedDefects : Nat)
    (h_ordinary : FixedOrdinaryFrequencies ordinary fixedCount)
    (h_defects : fixedDefects = fixedCount - ordinary) :
    NoFixedDefects fixedDefects := by
  unfold FixedOrdinaryFrequencies at h_ordinary
  unfold NoFixedDefects
  rw [h_defects, h_ordinary]
  exact Nat.sub_self fixedCount

theorem stable_supports_reduce_to_pure_moving
    (before after pureMoving mixed : Nat)
    (h_reduce : StableSupportReduction before after pureMoving mixed) :
    after = pureMoving := by
  exact h_reduce.2

theorem p24_order7_nontrivial_character_count :
    7 - 1 = 6 := by
  decide

theorem p24_fixed_frequency_count :
    7 = 7 := by
  decide

theorem p24_stable_support_accounting :
    StableSupportReduction 1260 35 35 1225 := by
  unfold StableSupportReduction
  decide

theorem p24_no_fixed_defect_reduces_supports_to_35 :
    stable_supports_reduce_to_pure_moving 1260 35 35 1225
      p24_stable_support_accounting = rfl := by
  rfl

theorem p24_reduced_support_count_certificate :
    ∃ after,
      after = 35 ∧ StableSupportReduction 1260 after 35 1225 := by
  exact ⟨35, rfl, p24_stable_support_accounting⟩

theorem p24_fixed_ordinaries_from_order7_payload
    (relations ordinary : Nat)
    (h_handoff : Order7SyzygyHandoff 6 6 7 relations true true)
    (h_prefix : PrefixPluckerUnits 7 7)
    (h_ordinary : ordinary = Nat.min relations 7) :
    FixedOrdinaryFrequencies ordinary 7 := by
  have h_relations : FixedTailRelations relations 7 :=
    fixed_tail_relations_from_order7_augmentation
      6 6 7 relations true true h_handoff rfl rfl rfl rfl
  exact fixed_ordinaries_from_tail_relations_and_prefix_units
    relations 7 7 ordinary h_relations h_prefix h_ordinary

theorem p24_no_fixed_defects_from_order7_payload
    (relations ordinary fixedDefects : Nat)
    (h_handoff : Order7SyzygyHandoff 6 6 7 relations true true)
    (h_prefix : PrefixPluckerUnits 7 7)
    (h_ordinary_min : ordinary = Nat.min relations 7)
    (h_defects : fixedDefects = 7 - ordinary) :
    NoFixedDefects fixedDefects := by
  have h_ordinary : FixedOrdinaryFrequencies ordinary 7 :=
    p24_fixed_ordinaries_from_order7_payload
      relations ordinary h_handoff h_prefix h_ordinary_min
  exact no_fixed_defects_from_fixed_ordinaries
    ordinary 7 fixedDefects h_ordinary h_defects

end P24.TraceGcdFixedFrequencyOrder7Gate
