/-!
Finite gate for the centered-profile Moore certificate.

The arithmetic candidate is a p-unit Moore determinant for centered profile
values

    G_s^0 in L = F_p(mu_157).

This file checks only the finite implication chain:

* a leading profile Moore p-unit gives full profile span;
* an equivalent full-square trace-Gram p-unit gives the same result;
* an equivalent base-field inversion-Gram p-unit gives the same result;
* an equivalent dropped-row base minor p-unit gives the same result;
* a leading square minor of the centered difference marginal gives the mixed
  rank directly;
* full profile span plus the profile/marginal rank dictionary gives the mixed
  centered marginal rank theorem;
* a contained normal Frobenius orbit is another sufficient way to get full
  profile span.
-/

namespace P24.CenteredProfileGate

def FullSpan (rank fieldDim : Nat) : Prop :=
  fieldDim ≤ rank

def LeadingMoorePUnit (leadingRank fieldDim : Nat) : Prop :=
  leadingRank = fieldDim

def TraceGramPUnit (gramRank fieldDim : Nat) : Prop :=
  gramRank = fieldDim

def BaseFieldGramPUnit (baseGramRank fieldDim : Nat) : Prop :=
  baseGramRank = fieldDim

def BaseFieldMinorPUnit (minorRank fieldDim : Nat) : Prop :=
  minorRank = fieldDim

def MixedMarginalFullRank (matrixRank fieldDim : Nat) : Prop :=
  fieldDim ≤ matrixRank

def DifferenceMinorPUnit (minorRank fieldDim : Nat) : Prop :=
  minorRank = fieldDim

def NormalOrbit (orbitRank fieldDim : Nat) : Prop :=
  orbitRank = fieldDim

def OrbitContainedInProfile (orbitRank profileRank : Nat) : Prop :=
  orbitRank ≤ profileRank

theorem full_span_from_leading_moore
    (profileRank leadingRank fieldDim : Nat)
    (h_leading : LeadingMoorePUnit leadingRank fieldDim)
    (h_leading_in_profile : leadingRank ≤ profileRank) :
    FullSpan profileRank fieldDim := by
  rw [FullSpan]
  rw [LeadingMoorePUnit] at h_leading
  rw [← h_leading]
  exact h_leading_in_profile

theorem mixed_rank_from_profile_span
    (profileRank matrixRank fieldDim : Nat)
    (h_profile : FullSpan profileRank fieldDim)
    (h_rank_dictionary : matrixRank = profileRank) :
    MixedMarginalFullRank matrixRank fieldDim := by
  rw [MixedMarginalFullRank, h_rank_dictionary]
  exact h_profile

theorem mixed_rank_from_leading_moore
    (profileRank leadingRank matrixRank fieldDim : Nat)
    (h_leading : LeadingMoorePUnit leadingRank fieldDim)
    (h_leading_in_profile : leadingRank ≤ profileRank)
    (h_rank_dictionary : matrixRank = profileRank) :
    MixedMarginalFullRank matrixRank fieldDim :=
  mixed_rank_from_profile_span profileRank matrixRank fieldDim
    (full_span_from_leading_moore
      profileRank leadingRank fieldDim h_leading h_leading_in_profile)
    h_rank_dictionary

theorem mixed_rank_from_difference_minor
    (minorRank matrixRank fieldDim : Nat)
    (h_minor : DifferenceMinorPUnit minorRank fieldDim)
    (h_minor_in_matrix : minorRank ≤ matrixRank) :
    MixedMarginalFullRank matrixRank fieldDim := by
  rw [MixedMarginalFullRank]
  rw [DifferenceMinorPUnit] at h_minor
  rw [← h_minor]
  exact h_minor_in_matrix

theorem leading_moore_from_trace_gram
    (leadingRank gramRank fieldDim : Nat)
    (h_gram : TraceGramPUnit gramRank fieldDim)
    (h_square_gram_equiv : leadingRank = gramRank) :
    LeadingMoorePUnit leadingRank fieldDim := by
  rw [LeadingMoorePUnit]
  rw [TraceGramPUnit] at h_gram
  rw [h_square_gram_equiv]
  exact h_gram

theorem mixed_rank_from_trace_gram
    (profileRank leadingRank gramRank matrixRank fieldDim : Nat)
    (h_gram : TraceGramPUnit gramRank fieldDim)
    (h_square_gram_equiv : leadingRank = gramRank)
    (h_leading_in_profile : leadingRank ≤ profileRank)
    (h_rank_dictionary : matrixRank = profileRank) :
    MixedMarginalFullRank matrixRank fieldDim :=
  mixed_rank_from_leading_moore
    profileRank leadingRank matrixRank fieldDim
    (leading_moore_from_trace_gram
      leadingRank gramRank fieldDim h_gram h_square_gram_equiv)
    h_leading_in_profile
    h_rank_dictionary

theorem trace_gram_from_base_field_gram
    (gramRank baseGramRank fieldDim : Nat)
    (h_base : BaseFieldGramPUnit baseGramRank fieldDim)
    (h_base_gram_equiv : gramRank = baseGramRank) :
    TraceGramPUnit gramRank fieldDim := by
  rw [TraceGramPUnit]
  rw [BaseFieldGramPUnit] at h_base
  rw [h_base_gram_equiv]
  exact h_base

theorem mixed_rank_from_base_field_gram
    (profileRank leadingRank gramRank baseGramRank matrixRank fieldDim : Nat)
    (h_base : BaseFieldGramPUnit baseGramRank fieldDim)
    (h_base_gram_equiv : gramRank = baseGramRank)
    (h_square_gram_equiv : leadingRank = gramRank)
    (h_leading_in_profile : leadingRank ≤ profileRank)
    (h_rank_dictionary : matrixRank = profileRank) :
    MixedMarginalFullRank matrixRank fieldDim :=
  mixed_rank_from_trace_gram
    profileRank leadingRank gramRank matrixRank fieldDim
    (trace_gram_from_base_field_gram
      gramRank baseGramRank fieldDim h_base h_base_gram_equiv)
    h_square_gram_equiv
    h_leading_in_profile
    h_rank_dictionary

theorem base_field_gram_from_minor
    (baseGramRank minorRank fieldDim : Nat)
    (h_minor : BaseFieldMinorPUnit minorRank fieldDim)
    (h_minor_gram_equiv : baseGramRank = minorRank) :
    BaseFieldGramPUnit baseGramRank fieldDim := by
  rw [BaseFieldGramPUnit]
  rw [BaseFieldMinorPUnit] at h_minor
  rw [h_minor_gram_equiv]
  exact h_minor

theorem mixed_rank_from_base_field_minor
    (profileRank leadingRank gramRank baseGramRank minorRank matrixRank fieldDim : Nat)
    (h_minor : BaseFieldMinorPUnit minorRank fieldDim)
    (h_minor_gram_equiv : baseGramRank = minorRank)
    (h_base_gram_equiv : gramRank = baseGramRank)
    (h_square_gram_equiv : leadingRank = gramRank)
    (h_leading_in_profile : leadingRank ≤ profileRank)
    (h_rank_dictionary : matrixRank = profileRank) :
    MixedMarginalFullRank matrixRank fieldDim :=
  mixed_rank_from_base_field_gram
    profileRank leadingRank gramRank baseGramRank matrixRank fieldDim
    (base_field_gram_from_minor
      baseGramRank minorRank fieldDim h_minor h_minor_gram_equiv)
    h_base_gram_equiv
    h_square_gram_equiv
    h_leading_in_profile
    h_rank_dictionary

theorem full_span_from_contained_normal_orbit
    (profileRank orbitRank fieldDim : Nat)
    (h_normal : NormalOrbit orbitRank fieldDim)
    (h_contained : OrbitContainedInProfile orbitRank profileRank) :
    FullSpan profileRank fieldDim := by
  rw [FullSpan]
  rw [NormalOrbit] at h_normal
  rw [OrbitContainedInProfile] at h_contained
  rw [← h_normal]
  exact h_contained

theorem mixed_rank_from_contained_normal_orbit
    (profileRank orbitRank matrixRank fieldDim : Nat)
    (h_normal : NormalOrbit orbitRank fieldDim)
    (h_contained : OrbitContainedInProfile orbitRank profileRank)
    (h_rank_dictionary : matrixRank = profileRank) :
    MixedMarginalFullRank matrixRank fieldDim :=
  mixed_rank_from_profile_span profileRank matrixRank fieldDim
    (full_span_from_contained_normal_orbit
      profileRank orbitRank fieldDim h_normal h_contained)
    h_rank_dictionary

end P24.CenteredProfileGate
