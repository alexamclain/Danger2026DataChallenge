/-!
Finite gate for the prefix-syndrome / tail-resultant bridge.

The latest p24 prefix theorem gives a `140`-coordinate syndrome/Moore p-unit.
That proves the prefix trace map is surjective, so its kernel inside
`L = F_p(mu_157)` has dimension `16`.  The representative fixed resultant is
then the separate assertion that the selected `16` tail coordinates inject on
that kernel.

This file records only the finite plumbing:

* prefix syndrome full rank gives the residual kernel dimension;
* tail rank equal to that residual dimension makes the common zero space
  trivial;
* prefix syndrome p-unit plus tail resultant p-unit rules out the same
  representative bad event.

No CM periods, traces, Moore determinants, resultants, or p-adic units are
constructed here.
-/

namespace P24.TraceGcdPrefixSyndromeResultantBridgeGate

def UnitPayload {Scalar : Type}
    (value inverse : Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitRel value inverse

def PrefixSyndromeSurjective (prefixRank targetDim : Nat) : Prop :=
  prefixRank = targetDim

def PrefixKernelDimension
    (kernelDim ambientDim prefixRank : Nat) : Prop :=
  prefixRank + kernelDim = ambientDim

def TailInjectiveOnKernel (kernelDim tailRankOnKernel : Nat) : Prop :=
  tailRankOnKernel = kernelDim

def CommonZeroDimension
    (commonZeroDim kernelDim tailRankOnKernel : Nat) : Prop :=
  commonZeroDim = kernelDim - tailRankOnKernel

def CommonZeroTrivial (commonZeroDim : Nat) : Prop :=
  commonZeroDim = 0

def PrefixPUnitDetectsSurjectivity {Scalar : Type} [Zero Scalar]
    (prefixValue : Scalar)
    (PrefixGood : Prop) : Prop :=
  prefixValue ≠ 0 → PrefixGood

def TailPUnitDetectsInjectivity {Scalar : Type} [Zero Scalar]
    (tailValue : Scalar)
    (TailGood : Prop) : Prop :=
  tailValue ≠ 0 → TailGood

def RepresentativeBadForcesFailure
    (Bad PrefixGood TailGood : Prop) : Prop :=
  Bad → ¬ (PrefixGood ∧ TailGood)

theorem kernel_dim_from_prefix_syndrome
    (kernelDim ambientDim prefixRank prefixDim residualDim : Nat)
    (h_kernel :
      PrefixKernelDimension kernelDim ambientDim prefixRank)
    (h_split : prefixDim + residualDim = ambientDim)
    (h_prefix :
      PrefixSyndromeSurjective prefixRank prefixDim) :
    kernelDim = residualDim := by
  rw [PrefixKernelDimension] at h_kernel
  rw [PrefixSyndromeSurjective] at h_prefix
  rw [h_prefix] at h_kernel
  have h_same : prefixDim + kernelDim = prefixDim + residualDim := by
    rw [h_kernel, h_split]
  exact Nat.add_left_cancel h_same

theorem common_zero_trivial_from_tail_injective
    (commonZeroDim kernelDim tailRankOnKernel : Nat)
    (h_common :
      CommonZeroDimension commonZeroDim kernelDim tailRankOnKernel)
    (h_tail :
      TailInjectiveOnKernel kernelDim tailRankOnKernel) :
    CommonZeroTrivial commonZeroDim := by
  rw [CommonZeroDimension] at h_common
  rw [TailInjectiveOnKernel] at h_tail
  rw [CommonZeroTrivial, h_common, h_tail]
  exact Nat.sub_self kernelDim

theorem p24_kernel_dim_from_prefix_syndrome
    (prefixRank kernelDim : Nat)
    (h_prefix : prefixRank = 140)
    (h_kernel : PrefixKernelDimension kernelDim 156 prefixRank) :
    kernelDim = 16 := by
  have h_prefix_good :
      PrefixSyndromeSurjective prefixRank 140 := h_prefix
  exact kernel_dim_from_prefix_syndrome
    kernelDim 156 prefixRank 140 16 h_kernel (by decide) h_prefix_good

theorem p24_common_zero_trivial_from_prefix_and_tail
    (commonZeroDim prefixRank kernelDim tailRankOnKernel : Nat)
    (h_prefix : prefixRank = 140)
    (h_kernel : PrefixKernelDimension kernelDim 156 prefixRank)
    (h_tail : tailRankOnKernel = 16)
    (h_common :
      CommonZeroDimension commonZeroDim kernelDim tailRankOnKernel) :
    CommonZeroTrivial commonZeroDim := by
  have h_kernel_dim : kernelDim = 16 :=
    p24_kernel_dim_from_prefix_syndrome
      prefixRank kernelDim h_prefix h_kernel
  have h_tail_good :
      TailInjectiveOnKernel kernelDim tailRankOnKernel := by
    rw [TailInjectiveOnKernel, h_tail, h_kernel_dim]
  exact common_zero_trivial_from_tail_injective
    commonZeroDim kernelDim tailRankOnKernel h_common h_tail_good

theorem no_representative_bad_from_prefix_tail_punits
    {Scalar : Type} [Zero Scalar]
    (Bad PrefixGood TailGood : Prop)
    (prefixValue prefixInv tailValue tailInv : Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_prefix_detects :
      PrefixPUnitDetectsSurjectivity prefixValue PrefixGood)
    (h_tail_detects :
      TailPUnitDetectsInjectivity tailValue TailGood)
    (h_bad_failure :
      RepresentativeBadForcesFailure Bad PrefixGood TailGood)
    (h_prefix_payload :
      UnitPayload prefixValue prefixInv UnitRel)
    (h_tail_payload :
      UnitPayload tailValue tailInv UnitRel) :
    ¬ Bad := by
  intro h_bad
  have h_prefix_nonzero : prefixValue ≠ 0 :=
    h_unit_nonzero prefixValue prefixInv h_prefix_payload
  have h_tail_nonzero : tailValue ≠ 0 :=
    h_unit_nonzero tailValue tailInv h_tail_payload
  have h_prefix_good : PrefixGood :=
    h_prefix_detects h_prefix_nonzero
  have h_tail_good : TailGood :=
    h_tail_detects h_tail_nonzero
  exact h_bad_failure h_bad ⟨h_prefix_good, h_tail_good⟩

theorem p24_prefix_syndrome_resultant_payload_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_prefix_syndrome_resultant_dimension_split :
    140 + 16 = 156 := by
  decide

end P24.TraceGcdPrefixSyndromeResultantBridgeGate
