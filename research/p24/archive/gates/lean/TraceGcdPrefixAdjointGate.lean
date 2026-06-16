/-!
Finite gate for the trace-GCD prefix adjoint theorem.

The arithmetic input is the relative-trace adjoint rank equality for the
four selected prefix blocks:

    rank(A_B) = rank(A_B^*).

For p24, `A_B : L -> R^4`, `dim L = 156`, and `dim R^4 = 4*35 = 140`.
This file records only the finite handoff:

* prefix rank 140 is the same as adjoint injectivity on the 140-dimensional
  adjoint domain;
* once prefix rank is 140, the prefix kernel has dimension 16.
-/

namespace P24.TraceGcdPrefixAdjointGate

def PrefixSurjective (prefixRank codomainDim : Nat) : Prop :=
  prefixRank = codomainDim

def AdjointInjective (adjointRank adjointDomainDim : Nat) : Prop :=
  adjointRank = adjointDomainDim

def KernelDimensionLaw
    (kernelDim leftDim prefixRank : Nat) : Prop :=
  kernelDim = leftDim - prefixRank

theorem adjoint_injective_from_prefix_surjective
    (prefixRank adjointRank codomainDim : Nat)
    (h_rank : prefixRank = adjointRank)
    (h_prefix : PrefixSurjective prefixRank codomainDim) :
    AdjointInjective adjointRank codomainDim := by
  rw [PrefixSurjective] at h_prefix
  rw [AdjointInjective]
  rw [← h_rank]
  exact h_prefix

theorem prefix_surjective_from_adjoint_injective
    (prefixRank adjointRank codomainDim : Nat)
    (h_rank : prefixRank = adjointRank)
    (h_adj : AdjointInjective adjointRank codomainDim) :
    PrefixSurjective prefixRank codomainDim := by
  rw [AdjointInjective] at h_adj
  rw [PrefixSurjective]
  rw [h_rank]
  exact h_adj

theorem kernel_dim_from_prefix_rank
    (kernelDim leftDim prefixRank codomainDim residualDim : Nat)
    (h_kernel : KernelDimensionLaw kernelDim leftDim prefixRank)
    (h_left : leftDim = codomainDim + residualDim)
    (h_prefix : PrefixSurjective prefixRank codomainDim) :
    kernelDim = residualDim := by
  rw [KernelDimensionLaw] at h_kernel
  rw [PrefixSurjective] at h_prefix
  rw [h_kernel, h_left, h_prefix]
  exact Nat.add_sub_cancel_left codomainDim residualDim

theorem p24_prefix_adjoint_injective_from_rank_match
    (prefixRank adjointRank : Nat)
    (h_rank : prefixRank = adjointRank)
    (h_prefix : prefixRank = 4 * 35) :
    AdjointInjective adjointRank 140 := by
  have h_prefix_surj : PrefixSurjective prefixRank (4 * 35) := h_prefix
  have h_adj := adjoint_injective_from_prefix_surjective
    prefixRank adjointRank (4 * 35) h_rank h_prefix_surj
  simpa using h_adj

theorem p24_prefix_kernel_dim
    (prefixRank kernelDim : Nat)
    (h_prefix : prefixRank = 4 * 35)
    (h_kernel : KernelDimensionLaw kernelDim 156 prefixRank) :
    kernelDim = 16 := by
  have h_prefix_surj : PrefixSurjective prefixRank (4 * 35) := h_prefix
  have h_dim := kernel_dim_from_prefix_rank
    kernelDim 156 prefixRank (4 * 35) 16
    h_kernel (by decide) h_prefix_surj
  simpa using h_dim

theorem p24_prefix_tail_dimension_split :
    4 * 35 + 16 = 156 := by
  decide

end P24.TraceGcdPrefixAdjointGate
