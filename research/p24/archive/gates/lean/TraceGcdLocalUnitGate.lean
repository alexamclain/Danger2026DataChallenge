/-!
Finite gate for the trace-GCD local-unit proof target.

This joins two previously separate finite interfaces:

* the representative `140 + 16` linearized trace-gcd statement;
* the seven orbit block-cycle/Fitting unit payload.

Lean does not construct the CM periods, determinants, or p-adic units.  It
only records the finite implications that the arithmetic theorem must
instantiate for the p24 certificate.
-/

namespace P24.TraceGcdLocalUnitGate

def TraceGcdDegree (kernelDim tailRankOnKernel : Nat) : Nat :=
  kernelDim - tailRankOnKernel

def CommonZeroTrivial (commonZeroDim : Nat) : Prop :=
  commonZeroDim = 0

def PrefixKernelDimension
    (sourceDim prefixRank kernelDim : Nat) : Prop :=
  prefixRank + kernelDim = sourceDim

def TailLocalUnit
    (kernelDim tailRankOnKernel : Nat) : Prop :=
  kernelDim ≤ tailRankOnKernel

theorem common_zero_trivial_from_tail_local_unit
    (commonZeroDim kernelDim tailRankOnKernel : Nat)
    (h_common :
      commonZeroDim = TraceGcdDegree kernelDim tailRankOnKernel)
    (h_tail_unit : TailLocalUnit kernelDim tailRankOnKernel) :
    CommonZeroTrivial commonZeroDim := by
  simp [CommonZeroTrivial, TraceGcdDegree, h_common,
    Nat.sub_eq_zero_of_le h_tail_unit]

theorem p24_prefix_kernel_dimension :
    PrefixKernelDimension 156 (4 * 35) 16 := by
  simp [PrefixKernelDimension]

theorem p24_common_zero_trivial_from_tail_rank
    (commonZeroDim : Nat)
    (h_common : commonZeroDim = TraceGcdDegree 16 16) :
    CommonZeroTrivial commonZeroDim :=
  common_zero_trivial_from_tail_local_unit commonZeroDim 16 16
    h_common (Nat.le_refl 16)

theorem p24_leading_dimension_split :
    4 * 35 + 16 = 156 := by
  decide

theorem p24_support_gap :
    35 + 19 < 210 - 156 + 1 := by
  decide

theorem p24_block_cycle_sign_positive :
    (16 * (35 - 1)) % 2 = 0 := by
  decide

def UnitPayload {Index Scalar : Type}
    (value inverse : Index → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ i, UnitRel (value i) (inverse i)

def FittingNormDetectsDeltaZero {Index Orbit Scalar : Type}
    [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (blockNorm : Orbit → Scalar) : Prop :=
  ∀ t, Delta t = 0 → blockNorm (orbitOf t) = 0

theorem delta_nonzero_from_orbit_fitting_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (blockNorm blockNormInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects :
      FittingNormDetectsDeltaZero orbitOf Delta blockNorm)
    (h_payload :
      UnitPayload blockNorm blockNormInv UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_norm_nonzero : blockNorm (orbitOf t) ≠ 0 :=
    h_unit_nonzero (blockNorm (orbitOf t)) (blockNormInv (orbitOf t))
      (h_payload (orbitOf t))
  exact h_norm_nonzero (h_detects t h_delta_zero)

def RepresentativeGood {Index : Type}
    (Good : Index → Prop)
    (selected : Index) : Prop :=
  Good selected

theorem representative_good_from_orbit_fitting_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (blockNorm blockNormInv : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_detects :
      FittingNormDetectsDeltaZero orbitOf Delta blockNorm)
    (h_payload :
      UnitPayload blockNorm blockNormInv UnitRel)
    (h_delta_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    RepresentativeGood Good selected := by
  exact h_delta_to_good selected
    (delta_nonzero_from_orbit_fitting_units
      orbitOf Delta blockNorm blockNormInv UnitRel
      h_unit_nonzero h_detects h_payload selected)

def LocalBad {Index : Type} (BadAt : Index → Prop) : Prop :=
  ∃ t, BadAt t

theorem no_local_bad_from_delta_nonzero
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (BadAt : Index → Prop)
    (h_bad_to_zero : ∀ t, BadAt t → Delta t = 0)
    (h_delta_nonzero : ∀ t, Delta t ≠ 0) :
    ¬ LocalBad BadAt := by
  intro h_bad
  rcases h_bad with ⟨t, h_bad_at_t⟩
  exact h_delta_nonzero t (h_bad_to_zero t h_bad_at_t)

end P24.TraceGcdLocalUnitGate
