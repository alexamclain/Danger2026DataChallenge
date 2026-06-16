/-!
Finite support gate for the trace-GCD prefix subcode formulation.

The metric prefix-Gram obstruction can be written as:

    there is a nonzero parameter lambda in the prefix span whose trace word
    vanishes on the 140 prefix coordinates.

If vanishing on the prefix forces the associated scalar word to be supported on
the 71-coordinate complement, then any parameter-level distance theorem

    nonzero prefix parameter -> support weight at least 72

rules out the obstruction.

The file also records the optional uncertainty route: if the same bad word had
time support at most 71 and Fourier support at most 140, prime cyclic
uncertainty with threshold 212 would rule it out.  The arithmetic burden is
proving the Fourier-support hypothesis for the actual trace-GCD family.
-/

namespace P24.PrefixSubcodeDistanceGate

def DistanceOnParams {Param : Type}
    (Active Nonzero : Param → Prop)
    (supportWeight : Param → Nat)
    (minDistance : Nat) : Prop :=
  ∀ param, Active param → Nonzero param →
    minDistance ≤ supportWeight param

def BadSupportBound {Param : Type}
    (Active Bad : Param → Prop)
    (supportWeight : Param → Nat)
    (badSupport : Nat) : Prop :=
  ∀ param, Active param → Bad param →
    supportWeight param ≤ badSupport

def PrefixErasureInjective {Param : Type}
    (Active Nonzero VanishesOnPrefix : Param → Prop) : Prop :=
  ∀ param, Active param → Nonzero param → ¬ VanishesOnPrefix param

theorem prefix_erasure_from_distance_gap
    {Param : Type}
    (Active Nonzero VanishesOnPrefix : Param → Prop)
    (supportWeight : Param → Nat)
    (minDistance complementSize : Nat)
    (h_distance :
      DistanceOnParams Active Nonzero supportWeight minDistance)
    (h_prefix_bound :
      BadSupportBound Active VanishesOnPrefix supportWeight complementSize)
    (h_gap : complementSize < minDistance) :
    PrefixErasureInjective Active Nonzero VanishesOnPrefix := by
  intro param h_active h_nonzero h_vanishes
  have h_min_le_support : minDistance ≤ supportWeight param :=
    h_distance param h_active h_nonzero
  have h_support_le_complement : supportWeight param ≤ complementSize :=
    h_prefix_bound param h_active h_vanishes
  have h_min_le_complement : minDistance ≤ complementSize :=
    Nat.le_trans h_min_le_support h_support_le_complement
  have h_complement_lt_complement : complementSize < complementSize :=
    Nat.lt_of_lt_of_le h_gap h_min_le_complement
  exact Nat.lt_irrefl complementSize h_complement_lt_complement

theorem p24_prime_prefix_complement_size :
    211 - 140 = 71 := by
  decide

theorem p24_nonzero_right_prefix_complement_size :
    210 - 140 = 70 := by
  decide

theorem p24_prime_prefix_distance_gap :
    71 < 72 := by
  decide

theorem p24_nonzero_right_prefix_distance_gap :
    70 < 71 := by
  decide

theorem p24_prime_prefix_erasure_from_distance_72
    {Param : Type}
    (Active Nonzero VanishesOnPrefix : Param → Prop)
    (supportWeight : Param → Nat)
    (h_distance :
      DistanceOnParams Active Nonzero supportWeight 72)
    (h_prefix_bound :
      BadSupportBound Active VanishesOnPrefix supportWeight 71) :
    PrefixErasureInjective Active Nonzero VanishesOnPrefix :=
  prefix_erasure_from_distance_gap
    Active Nonzero VanishesOnPrefix supportWeight 72 71
    h_distance h_prefix_bound p24_prime_prefix_distance_gap

theorem p24_nonzero_right_prefix_erasure_from_distance_71
    {Param : Type}
    (Active Nonzero VanishesOnPrefix : Param → Prop)
    (supportWeight : Param → Nat)
    (h_distance :
      DistanceOnParams Active Nonzero supportWeight 71)
    (h_prefix_bound :
      BadSupportBound Active VanishesOnPrefix supportWeight 70) :
    PrefixErasureInjective Active Nonzero VanishesOnPrefix :=
  prefix_erasure_from_distance_gap
    Active Nonzero VanishesOnPrefix supportWeight 71 70
    h_distance h_prefix_bound p24_nonzero_right_prefix_distance_gap

def UncertaintyBound {Param : Type}
    (Nonzero : Param → Prop)
    (timeSupport frequencySupport : Param → Nat)
    (threshold : Nat) : Prop :=
  ∀ param, Nonzero param →
    threshold ≤ timeSupport param + frequencySupport param

def SupportBound {Param : Type}
    (Bounded : Param → Prop)
    (weight : Param → Nat)
    (bound : Nat) : Prop :=
  ∀ param, Bounded param → weight param ≤ bound

def BadFromPrefixAndFrequency {Param : Type}
    (Active Nonzero VanishesOnPrefix HasPrefixFrequency : Param → Prop) : Prop :=
  ∃ param,
    Active param
    ∧ Nonzero param
    ∧ VanishesOnPrefix param
    ∧ HasPrefixFrequency param

theorem no_bad_from_uncertainty_gap
    {Param : Type}
    (Active Nonzero VanishesOnPrefix HasPrefixFrequency : Param → Prop)
    (timeSupport frequencySupport : Param → Nat)
    (timeBound frequencyBound threshold : Nat)
    (h_uncertainty :
      UncertaintyBound Nonzero timeSupport frequencySupport threshold)
    (h_time_bound :
      SupportBound VanishesOnPrefix timeSupport timeBound)
    (h_frequency_bound :
      SupportBound HasPrefixFrequency frequencySupport frequencyBound)
    (h_gap : timeBound + frequencyBound < threshold) :
    ¬ BadFromPrefixAndFrequency
      Active Nonzero VanishesOnPrefix HasPrefixFrequency := by
  intro h_bad
  rcases h_bad with
    ⟨param, _h_active, h_nonzero, h_vanishes, h_has_frequency⟩
  have h_threshold_le_sum :
      threshold ≤ timeSupport param + frequencySupport param :=
    h_uncertainty param h_nonzero
  have h_time_le : timeSupport param ≤ timeBound :=
    h_time_bound param h_vanishes
  have h_frequency_le : frequencySupport param ≤ frequencyBound :=
    h_frequency_bound param h_has_frequency
  have h_sum_le_bound :
      timeSupport param + frequencySupport param ≤
        timeBound + frequencyBound :=
    Nat.add_le_add h_time_le h_frequency_le
  have h_threshold_le_bound :
      threshold ≤ timeBound + frequencyBound :=
    Nat.le_trans h_threshold_le_sum h_sum_le_bound
  have h_bound_lt_bound :
      timeBound + frequencyBound < timeBound + frequencyBound :=
    Nat.lt_of_lt_of_le h_gap h_threshold_le_bound
  exact Nat.lt_irrefl (timeBound + frequencyBound) h_bound_lt_bound

theorem p24_prefix_uncertainty_gap :
    71 + 140 < 212 := by
  decide

theorem no_p24_prefix_bad_from_uncertainty
    {Param : Type}
    (Active Nonzero VanishesOnPrefix HasPrefixFrequency : Param → Prop)
    (timeSupport frequencySupport : Param → Nat)
    (h_uncertainty :
      UncertaintyBound Nonzero timeSupport frequencySupport 212)
    (h_time_bound :
      SupportBound VanishesOnPrefix timeSupport 71)
    (h_frequency_bound :
      SupportBound HasPrefixFrequency frequencySupport 140) :
    ¬ BadFromPrefixAndFrequency
      Active Nonzero VanishesOnPrefix HasPrefixFrequency :=
  no_bad_from_uncertainty_gap
    Active Nonzero VanishesOnPrefix HasPrefixFrequency
    timeSupport frequencySupport 71 140 212
    h_uncertainty h_time_bound h_frequency_bound
    p24_prefix_uncertainty_gap

end P24.PrefixSubcodeDistanceGate
