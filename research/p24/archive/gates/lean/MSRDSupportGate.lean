/-!
Finite support gate for the MSRD/LRS import.

This file deliberately avoids formal coding theory.  It checks only the
finite implication needed by `p24/msrd_lrs_import_boundary.md`:

* if every nonzero codeword has support weight at least `minDistance`;
* and the representative bad event would force support weight at most
  `badSupport`;
* and `badSupport < minDistance`;
* then the representative bad event is impossible.

For the current p24 trace-frame formulation, the relative coefficient code
has `31` blocks of `E`-dimension `179` and axis dimension `368`.  An MSRD/LRS
import would give minimum distance

  31 * 179 - 368 + 1 = 5182,

while the bad low-relative-degree event is supported on at most

  28 * 179 = 5012

scalar `E`-coordinates.

The older `210 - 156 + 1` / `35 + 19` representative support count is kept
below as a smaller generic gate for earlier tensor-factor reductions.

This gate is metric-agnostic.  The p24 `35+19` count is valid for scalar
coordinate/Hamming support, or for a sum-rank model whose rank weight really
counts those erased scalar coordinates.  It is not valid for the coarse
six-right-block support, where every word has weight at most `6`.
-/

namespace P24.MSRDSupportGate

def DistanceAtLeast {Codeword : Type} [Zero Codeword]
    (supportWeight : Codeword → Nat) (minDistance : Nat) : Prop :=
  ∀ word, word ≠ 0 → minDistance ≤ supportWeight word

def BadSupportBound {Codeword : Type}
    (bad : Codeword → Prop) (supportWeight : Codeword → Nat)
    (badSupport : Nat) : Prop :=
  ∀ word, bad word → supportWeight word ≤ badSupport

def MaxSupportWeight {Codeword : Type}
    (supportWeight : Codeword → Nat) (maxWeight : Nat) : Prop :=
  ∀ word, supportWeight word ≤ maxWeight

theorem no_bad_from_distance_gap
    {Codeword : Type} [Zero Codeword]
    (bad : Codeword → Prop)
    (supportWeight : Codeword → Nat)
    (minDistance badSupport : Nat)
    (h_distance : DistanceAtLeast supportWeight minDistance)
    (h_bad_bound : BadSupportBound bad supportWeight badSupport)
    (h_gap : badSupport < minDistance) :
    ∀ word, word ≠ 0 → ¬ bad word := by
  intro word h_nonzero h_bad
  have h_min_le_weight : minDistance ≤ supportWeight word :=
    h_distance word h_nonzero
  have h_weight_le_bad : supportWeight word ≤ badSupport :=
    h_bad_bound word h_bad
  have h_min_le_bad : minDistance ≤ badSupport :=
    Nat.le_trans h_min_le_weight h_weight_le_bad
  have h_bad_lt_bad : badSupport < badSupport :=
    Nat.lt_of_lt_of_le h_gap h_min_le_bad
  exact Nat.lt_irrefl badSupport h_bad_lt_bad

theorem p24_bad_support_lt_msrd_distance :
    35 + 19 < 210 - 156 + 1 := by
  decide

theorem p24_six_block_support_lt_distance :
    6 < 210 - 156 + 1 := by
  decide

theorem no_p24_bad_from_msrd_distance
    {Codeword : Type} [Zero Codeword]
    (bad : Codeword → Prop)
    (supportWeight : Codeword → Nat)
    (h_distance : DistanceAtLeast supportWeight (210 - 156 + 1))
    (h_bad_bound : BadSupportBound bad supportWeight (35 + 19)) :
    ∀ word, word ≠ 0 → ¬ bad word :=
  no_bad_from_distance_gap bad supportWeight (210 - 156 + 1) (35 + 19)
    h_distance h_bad_bound p24_bad_support_lt_msrd_distance

theorem p24_trace_frame_bad_support_lt_msrd_distance :
    28 * 179 < 31 * 179 - 368 + 1 := by
  decide

theorem p24_trace_frame_needed_distance_slack :
    (31 * 179 - 368 + 1) - (28 * 179 + 1) = 169 := by
  decide

theorem no_p24_trace_frame_bad_from_msrd_distance
    {Codeword : Type} [Zero Codeword]
    (bad : Codeword → Prop)
    (supportWeight : Codeword → Nat)
    (h_distance : DistanceAtLeast supportWeight (31 * 179 - 368 + 1))
    (h_bad_bound : BadSupportBound bad supportWeight (28 * 179)) :
    ∀ word, word ≠ 0 → ¬ bad word :=
  no_bad_from_distance_gap bad supportWeight
    (31 * 179 - 368 + 1) (28 * 179)
    h_distance h_bad_bound p24_trace_frame_bad_support_lt_msrd_distance

theorem no_nonzero_word_if_distance_exceeds_max_weight
    {Codeword : Type} [Zero Codeword]
    (supportWeight : Codeword → Nat)
    (minDistance maxWeight : Nat)
    (h_distance : DistanceAtLeast supportWeight minDistance)
    (h_max : MaxSupportWeight supportWeight maxWeight)
    (h_gap : maxWeight < minDistance) :
    ∀ word : Codeword, word = 0 := by
  intro word
  by_cases h_zero : word = 0
  · exact h_zero
  · have h_min_le_weight : minDistance ≤ supportWeight word :=
      h_distance word h_zero
    have h_weight_le_max : supportWeight word ≤ maxWeight :=
      h_max word
    have h_min_le_max : minDistance ≤ maxWeight :=
      Nat.le_trans h_min_le_weight h_weight_le_max
    have h_max_lt_max : maxWeight < maxWeight :=
      Nat.lt_of_lt_of_le h_gap h_min_le_max
    exact False.elim (Nat.lt_irrefl maxWeight h_max_lt_max)

theorem no_nonzero_word_from_distance_55_and_six_block_support
    {Codeword : Type} [Zero Codeword]
    (supportWeight : Codeword → Nat)
    (h_distance : DistanceAtLeast supportWeight (210 - 156 + 1))
    (h_max : MaxSupportWeight supportWeight 6) :
    ∀ word : Codeword, word = 0 :=
  no_nonzero_word_if_distance_exceeds_max_weight
    supportWeight (210 - 156 + 1) 6
    h_distance h_max p24_six_block_support_lt_distance

end P24.MSRDSupportGate
