/-!
Finite gate for a hypothetical dual-sparse uncertainty proof.

The p24 trace-GCD bad event has two support avatars in nearby formulations:

* representative leading erasure: a 54-coordinate support in right/Lang
  frequency coordinates;
* centered plateau difference: a 54-edge support after cyclic differencing.

If a single nonzero bad parameter could be shown to satisfy both bounds in a
prime cyclic Fourier pair, Tao/Chebotarev uncertainty with threshold `212`
would rule it out immediately.  This file records only that finite
implication and the p24 arithmetic counts.  It does not prove the missing
bridge identifying the two sparse avatars for the actual CM trace family.
-/

namespace P24.TraceGcdDualSparseBridgeGate

def UncertaintyBound {Param : Type}
    (Nonzero : Param → Prop)
    (timeSupport frequencySupport : Param → Nat)
    (threshold : Nat) : Prop :=
  ∀ param, Nonzero param →
    threshold ≤ timeSupport param + frequencySupport param

def SupportBound {Param : Type}
    (P : Param → Prop)
    (support : Param → Nat)
    (bound : Nat) : Prop :=
  ∀ param, P param → support param ≤ bound

def BadWithDualSparseBridge {Param : Type}
    (Bad Nonzero HasTimeSparse HasFrequencySparse : Param → Prop) : Prop :=
  ∃ param,
    Bad param ∧ Nonzero param ∧
      HasTimeSparse param ∧ HasFrequencySparse param

theorem no_bad_from_dual_sparse_uncertainty
    {Param : Type}
    (Bad Nonzero HasTimeSparse HasFrequencySparse : Param → Prop)
    (timeSupport frequencySupport : Param → Nat)
    (timeBound frequencyBound threshold : Nat)
    (h_uncertainty :
      UncertaintyBound Nonzero timeSupport frequencySupport threshold)
    (h_time :
      SupportBound HasTimeSparse timeSupport timeBound)
    (h_frequency :
      SupportBound HasFrequencySparse frequencySupport frequencyBound)
    (h_gap : timeBound + frequencyBound < threshold) :
    ¬ BadWithDualSparseBridge Bad Nonzero HasTimeSparse HasFrequencySparse := by
  intro h_bad
  rcases h_bad with ⟨param, _h_bad, h_nonzero, h_time_sparse, h_freq_sparse⟩
  have h_threshold :
      threshold ≤ timeSupport param + frequencySupport param :=
    h_uncertainty param h_nonzero
  have h_time_le : timeSupport param ≤ timeBound :=
    h_time param h_time_sparse
  have h_freq_le : frequencySupport param ≤ frequencyBound :=
    h_frequency param h_freq_sparse
  have h_sum_le :
      timeSupport param + frequencySupport param ≤
        timeBound + frequencyBound :=
    Nat.add_le_add h_time_le h_freq_le
  have h_threshold_le_bound : threshold ≤ timeBound + frequencyBound :=
    Nat.le_trans h_threshold h_sum_le
  have h_bound_lt_bound : timeBound + frequencyBound < timeBound + frequencyBound :=
    Nat.lt_of_lt_of_le h_gap h_threshold_le_bound
  exact Nat.lt_irrefl (timeBound + frequencyBound) h_bound_lt_bound

theorem p24_leading_erasure_support :
    35 + 19 = 54 := by
  decide

theorem p24_plateau_difference_support :
    211 - 157 = 54 := by
  decide

theorem p24_dual_sparse_uncertainty_gap :
    54 + 54 < 212 := by
  decide

theorem p24_plain_plateau_uncertainty_leaves_room :
    54 + 158 = 212 := by
  decide

theorem p24_frequency_complement_after_four_blocks :
    210 - 4 * 35 = 70 := by
  decide

theorem p24_prefix_uncertainty_gap_stronger_if_time_sparse :
    54 + 70 < 212 := by
  decide

theorem no_p24_bad_from_dual_sparse_bridge
    {Param : Type}
    (Bad Nonzero HasTimeSparse HasFrequencySparse : Param → Prop)
    (timeSupport frequencySupport : Param → Nat)
    (h_uncertainty :
      UncertaintyBound Nonzero timeSupport frequencySupport 212)
    (h_time :
      SupportBound HasTimeSparse timeSupport 54)
    (h_frequency :
      SupportBound HasFrequencySparse frequencySupport 54) :
    ¬ BadWithDualSparseBridge Bad Nonzero HasTimeSparse HasFrequencySparse :=
  no_bad_from_dual_sparse_uncertainty
    Bad Nonzero HasTimeSparse HasFrequencySparse
    timeSupport frequencySupport 54 54 212
    h_uncertainty h_time h_frequency
    p24_dual_sparse_uncertainty_gap

end P24.TraceGcdDualSparseBridgeGate
