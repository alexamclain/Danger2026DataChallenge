/-!
Finite gate for the CRT-axis matrix-tree factorization obstruction.

The computational toy in
`p24/axis_crt_matrix_tree_factorization_toy.py` finds pairs of surviving
Cauchy-Binet bases with the same combined edge multiset but different
coefficient products.  This file checks the small logical step behind that
audit:

* any ordinary edge-weight factorization `c(B) = C * prod_{e in B} a_e`
  forces equal coefficient products on such pair-sum witnesses;
* therefore one unequal product witness rules out that kind of matrix-tree
  compression.

The arithmetic witness values are produced externally by the finite-field
script.  Lean records only the implication being used.
-/

namespace P24.MatrixTreeFactorizationObstructionGate

def EdgeFactorization {Basis Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (coeff : Basis → Scalar)
    (scale : Scalar)
    (edgeProduct : Basis → Scalar) : Prop :=
  ∀ basis, coeff basis = mul scale (edgeProduct basis)

def ScaledPairSumProductInvariant {Basis Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (sameEdgeMultiset : Basis → Basis → Basis → Basis → Prop)
    (scale : Scalar)
    (edgeProduct : Basis → Scalar) : Prop :=
  ∀ B₁ B₂ B₃ B₄,
    sameEdgeMultiset B₁ B₂ B₃ B₄ →
      mul (mul scale (edgeProduct B₁)) (mul scale (edgeProduct B₂)) =
        mul (mul scale (edgeProduct B₃)) (mul scale (edgeProduct B₄))

theorem edge_factorization_implies_pair_sum_relation
    {Basis Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (coeff : Basis → Scalar)
    (scale : Scalar)
    (edgeProduct : Basis → Scalar)
    (sameEdgeMultiset : Basis → Basis → Basis → Basis → Prop)
    (h_factor : EdgeFactorization mul coeff scale edgeProduct)
    (h_pair :
      ScaledPairSumProductInvariant mul sameEdgeMultiset scale edgeProduct)
    {B₁ B₂ B₃ B₄ : Basis}
    (h_same : sameEdgeMultiset B₁ B₂ B₃ B₄) :
    mul (coeff B₁) (coeff B₂) = mul (coeff B₃) (coeff B₄) := by
  rw [h_factor B₁, h_factor B₂, h_factor B₃, h_factor B₄]
  exact h_pair B₁ B₂ B₃ B₄ h_same

theorem no_edge_factorization_from_pair_sum_witness
    {Basis Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (coeff : Basis → Scalar)
    (scale : Scalar)
    (edgeProduct : Basis → Scalar)
    (sameEdgeMultiset : Basis → Basis → Basis → Basis → Prop)
    (h_pair :
      ScaledPairSumProductInvariant mul sameEdgeMultiset scale edgeProduct)
    {B₁ B₂ B₃ B₄ : Basis}
    (h_same : sameEdgeMultiset B₁ B₂ B₃ B₄)
    (h_witness :
      mul (coeff B₁) (coeff B₂) ≠ mul (coeff B₃) (coeff B₄)) :
    ¬ EdgeFactorization mul coeff scale edgeProduct := by
  intro h_factor
  exact h_witness
    (edge_factorization_implies_pair_sum_relation
      mul coeff scale edgeProduct sameEdgeMultiset h_factor h_pair h_same)

theorem nat_edge_factorization_implies_pair_sum_relation
    {Basis : Type}
    (coeff : Basis → Nat)
    (scale : Nat)
    (edgeProduct : Basis → Nat)
    (sameEdgeMultiset : Basis → Basis → Basis → Basis → Prop)
    (h_factor : EdgeFactorization Nat.mul coeff scale edgeProduct)
    {B₁ B₂ B₃ B₄ : Basis}
    (_h_same : sameEdgeMultiset B₁ B₂ B₃ B₄)
    (h_pair :
      edgeProduct B₁ * edgeProduct B₂ =
        edgeProduct B₃ * edgeProduct B₄) :
    coeff B₁ * coeff B₂ = coeff B₃ * coeff B₄ := by
  rw [h_factor B₁, h_factor B₂, h_factor B₃, h_factor B₄]
  calc
    scale * edgeProduct B₁ * (scale * edgeProduct B₂)
        = scale * scale * (edgeProduct B₁ * edgeProduct B₂) := by
            ac_rfl
    _ = scale * scale * (edgeProduct B₃ * edgeProduct B₄) := by
            rw [h_pair]
    _ = scale * edgeProduct B₃ * (scale * edgeProduct B₄) := by
            ac_rfl

theorem m6_full_coeff_witness_products_differ :
    (12 : Nat) ≠ 10 := by
  decide

theorem m10_full_coeff_witness_products_differ :
    (12 : Nat) ≠ 10 := by
  decide

theorem m15_full_coeff_witness_products_differ :
    (28 : Nat) ≠ 8 := by
  decide

theorem m30_full_coeff_witness_products_differ :
    (54 : Nat) ≠ 9 := by
  decide

end P24.MatrixTreeFactorizationObstructionGate
