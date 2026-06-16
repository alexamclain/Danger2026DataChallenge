/-!
Finite gate for the full prefix-plus-tail coinvariant target.

The arithmetic theorem should construct the p-integral square map

    Phi_full : O_R^4 ⊕ C_tail -> E/(tau_R - 1)E

where `rank O_R = 35`, `rank C_tail = 16`, and the target has rank `156`.
If its determinant is a p-unit, then the full `140+16` trace-GCD map has full
rank.  This is the fixed-orbit linearized-resultant input without choosing a
prefix-kernel basis.

Lean records only the finite dimension handoff.
-/

namespace P24.TraceGcdFullCoinvariantTailGate

def SquareCoinvariantUnit
    (rank sourceDim targetDim : Nat) : Prop :=
  rank = sourceDim ∧ sourceDim = targetDim

def FullTraceGcdRank (rank ambientDim : Nat) : Prop :=
  rank = ambientDim

def KernelTrivial (kernelDim : Nat) : Prop :=
  kernelDim = 0

def KernelDimensionLaw
    (kernelDim ambientDim rank : Nat) : Prop :=
  kernelDim = ambientDim - rank

def FixedResultantUnit : Prop := True

def RsTailFixedMapUnit
    (rank sourceDim targetDim : Nat) : Prop :=
  rank = sourceDim ∧ sourceDim = targetDim

def RsTailAdjointSyndromeSurjective
    (rank sourceDualDim targetDim : Nat) : Prop :=
  rank = sourceDualDim ∧ sourceDualDim = targetDim

def RsTailMooreSchurSplitUnit
    (prefixRank prefixDim tailQuotientRank tailDim targetDim : Nat) : Prop :=
  prefixRank = prefixDim ∧
    tailQuotientRank = tailDim ∧
    prefixDim + tailDim = targetDim

def SemilinearCoreTrivial (coreDim : Nat) : Prop :=
  coreDim = 0

def FixedRelationKernelTrivial (kernelDim : Nat) : Prop :=
  kernelDim = 0

def Hilbert90CoreDescent (coreDim fixedKernelDim : Nat) : Prop :=
  (coreDim = 0) ↔ (fixedKernelDim = 0)

theorem full_rank_from_square_coinvariant_unit
    (rank sourceDim targetDim : Nat)
    (h_unit : SquareCoinvariantUnit rank sourceDim targetDim) :
    FullTraceGcdRank rank targetDim := by
  rcases h_unit with ⟨h_rank, h_square⟩
  unfold FullTraceGcdRank
  rw [h_rank, h_square]

theorem kernel_trivial_from_full_rank
    (kernelDim ambientDim rank : Nat)
    (h_kernel : KernelDimensionLaw kernelDim ambientDim rank)
    (h_full : FullTraceGcdRank rank ambientDim) :
    KernelTrivial kernelDim := by
  unfold KernelDimensionLaw at h_kernel
  unfold FullTraceGcdRank at h_full
  unfold KernelTrivial
  rw [h_kernel, h_full]
  exact Nat.sub_self ambientDim

theorem p24_full_coinvariant_dimensions :
    4 * 35 + 16 = 156 := by
  decide

theorem p24_full_rank_from_coinvariant_unit
    (rank : Nat)
    (h_unit : SquareCoinvariantUnit rank (4 * 35 + 16) 156) :
    FullTraceGcdRank rank 156 := by
  exact full_rank_from_square_coinvariant_unit
    rank (4 * 35 + 16) 156 h_unit

theorem p24_kernel_trivial_from_coinvariant_unit
    (rank kernelDim : Nat)
    (h_unit : SquareCoinvariantUnit rank (4 * 35 + 16) 156)
    (h_kernel : KernelDimensionLaw kernelDim 156 rank) :
    KernelTrivial kernelDim := by
  have h_full : FullTraceGcdRank rank 156 :=
    p24_full_rank_from_coinvariant_unit rank h_unit
  exact kernel_trivial_from_full_rank kernelDim 156 rank h_kernel h_full

theorem fixed_resultant_unit_from_coinvariant_unit
    (rank kernelDim : Nat)
    (h_unit : SquareCoinvariantUnit rank (4 * 35 + 16) 156)
    (h_kernel : KernelDimensionLaw kernelDim 156 rank)
    (h_trivial_to_unit : KernelTrivial kernelDim -> FixedResultantUnit) :
    FixedResultantUnit := by
  exact h_trivial_to_unit
    (p24_kernel_trivial_from_coinvariant_unit
      rank kernelDim h_unit h_kernel)

theorem p24_rs_tail_fixed_source_dimensions :
    28 + 4 * 28 + 16 = 156 := by
  decide

theorem p24_rs_tail_fixed_source_matches_square_source :
    28 + 4 * 28 + 16 = 4 * 35 + 16 := by
  decide

theorem p24_rs_tail_explicit_column_count :
    7 * 4 + (7 * 4) * 4 + 16 = 156 := by
  decide

theorem p24_rs_tail_explicit_columns_match_fixed_source :
    7 * 4 + (7 * 4) * 4 + 16 = 28 + 4 * 28 + 16 := by
  decide

theorem p24_rs_tail_adjoint_target_count :
    7 * 4 + (7 * 4) * 4 + 16 = 156 := by
  decide

theorem p24_rs_tail_moore_schur_split_count :
    (7 * 4 + (7 * 4) * 4) + 16 = 156 := by
  decide

theorem p24_rs_tail_prefix_coordinate_count :
    7 * 4 + (7 * 4) * 4 = 140 := by
  decide

theorem p24_rs_tail_full_fixed_source_count :
    6 * (7 + 7 * 4) = 210 := by
  decide

theorem p24_rs_tail_selected_block_count :
    4 * (7 + 7 * 4) + 16 = 156 := by
  decide

theorem p24_rs_tail_erasure_count :
    210 - 156 = 54 := by
  decide

theorem p24_rs_tail_selected_block_support_profile_subsets :
    2 ^ 5 - 1 = 31 := by
  decide

theorem p24_rs_tail_plucker_chart_entry_count :
    156 * (35 + 19) = 8424 := by
  decide

theorem rs_tail_fixed_map_unit_from_moore_schur_split
    (prefixRank tailQuotientRank : Nat)
    (h_split :
      RsTailMooreSchurSplitUnit prefixRank 140 tailQuotientRank 16 156) :
    RsTailFixedMapUnit (prefixRank + tailQuotientRank)
      (28 + 4 * 28 + 16) 156 := by
  rcases h_split with ⟨h_prefix, h_tail, h_total⟩
  unfold RsTailFixedMapUnit
  constructor
  · rw [h_prefix, h_tail]
  · decide

theorem rs_tail_fixed_map_unit_from_adjoint_syndrome
    (rank : Nat)
    (h_surj :
      RsTailAdjointSyndromeSurjective rank (28 + 4 * 28 + 16) 156) :
    RsTailFixedMapUnit rank (28 + 4 * 28 + 16) 156 := by
  exact h_surj

theorem square_coinvariant_unit_from_rs_tail_fixed_map_unit
    (rank : Nat)
    (h_unit : RsTailFixedMapUnit rank (28 + 4 * 28 + 16) 156) :
    SquareCoinvariantUnit rank (4 * 35 + 16) 156 := by
  rcases h_unit with ⟨h_rank, _h_square⟩
  unfold SquareCoinvariantUnit
  constructor
  · rw [h_rank]
  · decide

theorem p24_fixed_relation_kernel_trivial_from_rs_tail_unit
    (rank kernelDim : Nat)
    (h_unit : RsTailFixedMapUnit rank (28 + 4 * 28 + 16) 156)
    (h_kernel : KernelDimensionLaw kernelDim 156 rank) :
    FixedRelationKernelTrivial kernelDim := by
  have h_square : SquareCoinvariantUnit rank (4 * 35 + 16) 156 :=
    square_coinvariant_unit_from_rs_tail_fixed_map_unit rank h_unit
  have h_trivial : KernelTrivial kernelDim :=
    p24_kernel_trivial_from_coinvariant_unit rank kernelDim h_square h_kernel
  exact h_trivial

theorem semilinear_core_trivial_from_hilbert90_fixed_kernel
    (coreDim fixedKernelDim : Nat)
    (h_descent : Hilbert90CoreDescent coreDim fixedKernelDim)
    (h_fixed : FixedRelationKernelTrivial fixedKernelDim) :
    SemilinearCoreTrivial coreDim := by
  unfold SemilinearCoreTrivial
  unfold FixedRelationKernelTrivial at h_fixed
  unfold Hilbert90CoreDescent at h_descent
  exact h_descent.mpr h_fixed

theorem p24_semilinear_core_trivial_from_rs_tail_unit
    (rank fixedKernelDim coreDim : Nat)
    (h_unit : RsTailFixedMapUnit rank (28 + 4 * 28 + 16) 156)
    (h_kernel : KernelDimensionLaw fixedKernelDim 156 rank)
    (h_descent : Hilbert90CoreDescent coreDim fixedKernelDim) :
    SemilinearCoreTrivial coreDim := by
  exact semilinear_core_trivial_from_hilbert90_fixed_kernel
    coreDim fixedKernelDim h_descent
    (p24_fixed_relation_kernel_trivial_from_rs_tail_unit
      rank fixedKernelDim h_unit h_kernel)

theorem fixed_resultant_unit_from_rs_tail_fixed_map
    (rank kernelDim : Nat)
    (h_unit : RsTailFixedMapUnit rank (28 + 4 * 28 + 16) 156)
    (h_kernel : KernelDimensionLaw kernelDim 156 rank)
    (h_trivial_to_unit : KernelTrivial kernelDim -> FixedResultantUnit) :
    FixedResultantUnit := by
  have h_square : SquareCoinvariantUnit rank (4 * 35 + 16) 156 :=
    square_coinvariant_unit_from_rs_tail_fixed_map_unit rank h_unit
  exact fixed_resultant_unit_from_coinvariant_unit
    rank kernelDim h_square h_kernel h_trivial_to_unit

end P24.TraceGcdFullCoinvariantTailGate
