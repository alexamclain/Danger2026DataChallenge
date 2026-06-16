/-!
Finite gate for the representative dual obstruction.

For the representative p24 row, the bad event is a nonzero source element
whose four full prefix blocks vanish and whose tail projection also vanishes.
This file records the logic connecting that bad-lambda statement to prefix
kernel plus tail injectivity.
-/

namespace P24.RepresentativeDualObstructionGate

def PrefixZero {Source Prefix Value : Type} [Zero Value]
    (prefixMap : Source → Prefix → Value)
    (x : Source) : Prop :=
  ∀ pref, prefixMap x pref = 0

def TailZero {Source Tail Value : Type} [Zero Value]
    (tailMap : Source → Tail → Value)
    (x : Source) : Prop :=
  ∀ tail, tailMap x tail = 0

def NoRepresentativeBad
    {Source Prefix Tail PrefixValue TailValue : Type}
    [Zero Source] [Zero PrefixValue] [Zero TailValue]
    (prefixMap : Source → Prefix → PrefixValue)
    (tailMap : Source → Tail → TailValue) : Prop :=
  ∀ x, PrefixZero prefixMap x → TailZero tailMap x → x = 0

def TailInjectiveOnPrefixKernel
    {Source Prefix Tail PrefixValue TailValue : Type}
    [Zero Source] [Zero PrefixValue] [Zero TailValue]
    (prefixMap : Source → Prefix → PrefixValue)
    (tailMap : Source → Tail → TailValue) : Prop :=
  ∀ x, PrefixZero prefixMap x → TailZero tailMap x → x = 0

theorem no_bad_iff_tail_injective_on_prefix_kernel
    {Source Prefix Tail PrefixValue TailValue : Type}
    [Zero Source] [Zero PrefixValue] [Zero TailValue]
    (prefixMap : Source → Prefix → PrefixValue)
    (tailMap : Source → Tail → TailValue) :
    NoRepresentativeBad prefixMap tailMap ↔
      TailInjectiveOnPrefixKernel prefixMap tailMap := by
  rfl

def LeadingSeparates
    {Source Coord Value : Type} [Zero Source] [Zero Value]
    (coordMap : Source → Coord → Value) : Prop :=
  ∀ x, x ≠ 0 → ∃ coord, coordMap x coord ≠ 0

theorem leading_separates_from_no_bad
    {Source Prefix Tail Coord PrefixValue TailValue CoordValue : Type}
    [Zero Source] [Zero PrefixValue] [Zero TailValue] [Zero CoordValue]
    (prefixMap : Source → Prefix → PrefixValue)
    (tailMap : Source → Tail → TailValue)
    (coordMap : Source → Coord → CoordValue)
    (h_no_bad : NoRepresentativeBad prefixMap tailMap)
    (h_coord_zero_to_prefix_tail_zero :
      ∀ x, (∀ coord, coordMap x coord = 0) →
        PrefixZero prefixMap x ∧ TailZero tailMap x) :
    LeadingSeparates coordMap := by
  intro x h_nonzero
  by_cases h_exists : ∃ coord, coordMap x coord ≠ 0
  · exact h_exists
  · have h_all_zero : ∀ coord, coordMap x coord = 0 := by
      intro coord
      by_cases h_value : coordMap x coord = 0
      · exact h_value
      · exact False.elim (h_exists ⟨coord, h_value⟩)
    rcases h_coord_zero_to_prefix_tail_zero x h_all_zero with
      ⟨h_prefix, h_tail⟩
    exact False.elim (h_nonzero (h_no_bad x h_prefix h_tail))

end P24.RepresentativeDualObstructionGate
