/-!
Finite gate for the mixed subspace-polynomial certificate.

The arithmetic input is that the monic `p`-linearized annihilator of the 210
trace-dual mixed coordinates has `p`-degree `156`, equivalently it is the full
field polynomial `X^(p^156)-X`.

This file only checks the finite logic:

* subspace-polynomial degree equals the coordinate span rank;
* absence of an annihilator of degree below the field dimension implies full
  span.
-/

namespace P24.MixedSubspacePolynomialGate

def FullSpan (rank fieldDim : Nat) : Prop :=
  fieldDim ≤ rank

def NoSmallAnnihilator (annDegree fieldDim : Nat) : Prop :=
  ¬ annDegree < fieldDim

theorem full_span_from_no_small_annihilator
    (rank annDegree fieldDim : Nat)
    (h_degree_rank : annDegree = rank)
    (h_no_small : NoSmallAnnihilator annDegree fieldDim) :
    FullSpan rank fieldDim := by
  have h_le : fieldDim ≤ annDegree := Nat.le_of_not_gt h_no_small
  simpa [FullSpan, h_degree_rank] using h_le

theorem no_small_annihilator_from_full_degree
    (annDegree fieldDim : Nat)
    (h_full_degree : annDegree = fieldDim) :
    NoSmallAnnihilator annDegree fieldDim := by
  intro h_small
  cases h_full_degree
  exact Nat.lt_irrefl annDegree h_small

theorem full_span_from_full_annihilator_degree
    (rank annDegree fieldDim : Nat)
    (h_degree_rank : annDegree = rank)
    (h_full_degree : annDegree = fieldDim) :
    FullSpan rank fieldDim :=
  full_span_from_no_small_annihilator
    rank annDegree fieldDim h_degree_rank
    (no_small_annihilator_from_full_degree annDegree fieldDim h_full_degree)

theorem full_span_from_prefix_tail
    (leadingRank prefixRank tailAug prefixDim tailDim fieldDim : Nat)
    (h_leading : leadingRank = prefixRank + tailAug)
    (h_field : fieldDim = prefixDim + tailDim)
    (h_prefix : prefixRank = prefixDim)
    (h_tail : tailAug = tailDim) :
    FullSpan leadingRank fieldDim := by
  rw [FullSpan, h_leading, h_field, h_prefix, h_tail]
  exact Nat.le_refl _

theorem p24_representative_full_span_from_prefix_tail
    (leadingRank prefixRank tailAug : Nat)
    (h_leading : leadingRank = prefixRank + tailAug)
    (h_prefix : prefixRank = 4 * 35)
    (h_tail : tailAug = 16) :
    FullSpan leadingRank 156 :=
  full_span_from_prefix_tail
    leadingRank prefixRank tailAug (4 * 35) 16 156
    h_leading (by decide) h_prefix h_tail

end P24.MixedSubspacePolynomialGate
