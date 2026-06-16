/-!
Finite gate for symmetry-aligned paired tails.

In the p24 paired leading-erasure certificate, a shared four-block prefix
leaves a small residual source.  If a conjugation symmetry preserves that
prefix and swaps the two omitted tail blocks, then the two tail injectivity
checks are equivalent.  This file records only that finite implication; the
arithmetic work is proving that the CM mixed periods satisfy the symmetry
hypotheses for the `v -> -v` orbit pairing.
-/

namespace P24.ConjugateTailGate

def PrefixZero {Source PrefixCoord PrefixValue : Type} [Zero PrefixValue]
    (prefixMap : Source → PrefixCoord → PrefixValue)
    (x : Source) : Prop :=
  ∀ coord, prefixMap x coord = 0

def TailZero {Source TailCoord TailValue : Type} [Zero TailValue]
    (tailMap : Source → TailCoord → TailValue)
    (x : Source) : Prop :=
  ∀ coord, tailMap x coord = 0

def TailInjectiveOnPrefix
    {Source PrefixCoord PrefixValue TailCoord TailValue : Type}
    [Zero Source] [Zero PrefixValue] [Zero TailValue]
    (prefixMap : Source → PrefixCoord → PrefixValue)
    (tailMap : Source → TailCoord → TailValue) : Prop :=
  ∀ x, PrefixZero prefixMap x → TailZero tailMap x → x = 0

theorem conjugate_tail_injective
    {Source PrefixCoord PrefixValue TailACoord TailBCoord TailValue : Type}
    [Zero Source] [Zero PrefixValue] [Zero TailValue]
    (prefixMap : Source → PrefixCoord → PrefixValue)
    (tailA : Source → TailACoord → TailValue)
    (tailB : Source → TailBCoord → TailValue)
    (conj deconj : Source → Source)
    (h_right_inverse : ∀ y, conj (deconj y) = y)
    (h_conj_zero : conj 0 = 0)
    (h_prefix :
      ∀ y, PrefixZero prefixMap y → PrefixZero prefixMap (deconj y))
    (h_tail :
      ∀ y, TailZero tailB y → TailZero tailA (deconj y))
    (h_tailA : TailInjectiveOnPrefix prefixMap tailA) :
    TailInjectiveOnPrefix prefixMap tailB := by
  intro y h_prefix_y h_tail_y
  have h_deconj_zero : deconj y = 0 :=
    h_tailA (deconj y) (h_prefix y h_prefix_y) (h_tail y h_tail_y)
  calc
    y = conj (deconj y) := (h_right_inverse y).symm
    _ = conj 0 := by rw [h_deconj_zero]
    _ = 0 := h_conj_zero

theorem conjugate_tail_equivalence
    {Source PrefixCoord PrefixValue TailACoord TailBCoord TailValue : Type}
    [Zero Source] [Zero PrefixValue] [Zero TailValue]
    (prefixMap : Source → PrefixCoord → PrefixValue)
    (tailA : Source → TailACoord → TailValue)
    (tailB : Source → TailBCoord → TailValue)
    (conjAB conjBA : Source → Source)
    (h_AB_right_inverse : ∀ y, conjAB (conjBA y) = y)
    (h_BA_right_inverse : ∀ y, conjBA (conjAB y) = y)
    (h_AB_zero : conjAB 0 = 0)
    (h_BA_zero : conjBA 0 = 0)
    (h_prefix_AB :
      ∀ y, PrefixZero prefixMap y → PrefixZero prefixMap (conjBA y))
    (h_prefix_BA :
      ∀ y, PrefixZero prefixMap y → PrefixZero prefixMap (conjAB y))
    (h_tail_AB :
      ∀ y, TailZero tailB y → TailZero tailA (conjBA y))
    (h_tail_BA :
      ∀ y, TailZero tailA y → TailZero tailB (conjAB y)) :
    TailInjectiveOnPrefix prefixMap tailA ↔
      TailInjectiveOnPrefix prefixMap tailB := by
  constructor
  · exact conjugate_tail_injective
      prefixMap tailA tailB conjAB conjBA
      h_AB_right_inverse h_AB_zero h_prefix_AB h_tail_AB
  · exact conjugate_tail_injective
      prefixMap tailB tailA conjBA conjAB
      h_BA_right_inverse h_BA_zero h_prefix_BA h_tail_BA

end P24.ConjugateTailGate
