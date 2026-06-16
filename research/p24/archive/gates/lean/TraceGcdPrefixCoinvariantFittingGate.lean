/-!
Finite gate for the prefix coinvariant Fitting target.

The arithmetic theorem should construct the p-integral map

    Phi_B : O_R^4 -> E/(tau_R - 1)E

and prove that its maximal-minor ideal is a p-unit.  Since the source has
rank `4*35=140` and the target has rank `156`, this is a rectangular
Fitting statement: unit maximal minors imply rank 140 after reduction, and
then the dual prefix kernel in `L` has dimension 16.

This file records only that finite handoff.
-/

namespace P24.TraceGcdPrefixCoinvariantFittingGate

def MaximalMinorUnit (rank sourceDim : Nat) : Prop :=
  rank = sourceDim

def PrefixRankFull (prefixRank prefixDim : Nat) : Prop :=
  prefixRank = prefixDim

def ExpectedCokernelRank
    (cokernelRank targetDim sourceDim : Nat) : Prop :=
  cokernelRank = targetDim - sourceDim

def KernelDimensionLaw
    (kernelDim ambientDim prefixRank : Nat) : Prop :=
  kernelDim = ambientDim - prefixRank

theorem prefix_full_from_maximal_minor_unit
    (rank sourceDim : Nat)
    (h_unit : MaximalMinorUnit rank sourceDim) :
    PrefixRankFull rank sourceDim := by
  exact h_unit

theorem kernel_dim_from_prefix_full
    (kernelDim ambientDim prefixRank prefixDim residualDim : Nat)
    (h_kernel : KernelDimensionLaw kernelDim ambientDim prefixRank)
    (h_ambient : ambientDim = prefixDim + residualDim)
    (h_prefix : PrefixRankFull prefixRank prefixDim) :
    kernelDim = residualDim := by
  rw [KernelDimensionLaw] at h_kernel
  rw [PrefixRankFull] at h_prefix
  rw [h_kernel, h_ambient, h_prefix]
  exact Nat.add_sub_cancel_left prefixDim residualDim

theorem p24_prefix_rank_from_coinvariant_fitting
    (rank : Nat)
    (h_unit : MaximalMinorUnit rank (4 * 35)) :
    PrefixRankFull rank 140 := by
  have h_full := prefix_full_from_maximal_minor_unit rank (4 * 35) h_unit
  simpa using h_full

theorem p24_prefix_kernel_dim_from_coinvariant_fitting
    (rank kernelDim : Nat)
    (h_unit : MaximalMinorUnit rank (4 * 35))
    (h_kernel : KernelDimensionLaw kernelDim 156 rank) :
    kernelDim = 16 := by
  have h_prefix : PrefixRankFull rank (4 * 35) :=
    prefix_full_from_maximal_minor_unit rank (4 * 35) h_unit
  have h_dim := kernel_dim_from_prefix_full
    kernelDim 156 rank (4 * 35) 16
    h_kernel (by decide) h_prefix
  simpa using h_dim

theorem p24_prefix_coinvariant_dimensions :
    4 * 35 + 16 = 156 := by
  decide

theorem p24_expected_cokernel_rank :
    ExpectedCokernelRank 16 156 (4 * 35) := by
  unfold ExpectedCokernelRank
  decide

end P24.TraceGcdPrefixCoinvariantFittingGate
