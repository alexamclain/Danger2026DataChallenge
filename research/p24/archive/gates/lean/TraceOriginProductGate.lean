/-!
Finite gate for the trace-gcd origin-product reduction.

The arithmetic theorem should prove a nonzero product over the reduced right
origin cycle.  This file records only the finite implication:

* if every right-cycle factor is good, and
* origin covariance maps each origin to its right-cycle factor,

then the selected origin is good, and in fact every origin is good.

The scalar version at the bottom records the stronger interface used by the
trace-GCD origin-resultant target: a nonzero product detects nonzero
right-component factors, and p-unit covariance transports those factors to
the selected tail-on-kernel determinant.
-/

namespace P24.TraceOriginProductGate

def OriginCovariance
    {Origin Right : Type}
    (toRight : Origin → Right)
    (GoodOrigin : Origin → Prop)
    (GoodRight : Right → Prop) : Prop :=
  ∀ origin, GoodRight (toRight origin) → GoodOrigin origin

def RightProductCertificate
    {Right : Type}
    (GoodRight : Right → Prop) : Prop :=
  ∀ right, GoodRight right

theorem selected_origin_from_right_product
    {Origin Right : Type}
    (toRight : Origin → Right)
    (GoodOrigin : Origin → Prop)
    (GoodRight : Right → Prop)
    (selected : Origin)
    (h_cov : OriginCovariance toRight GoodOrigin GoodRight)
    (h_product : RightProductCertificate GoodRight) :
    GoodOrigin selected := by
  exact h_cov selected (h_product (toRight selected))

theorem all_origins_from_right_product
    {Origin Right : Type}
    (toRight : Origin → Right)
    (GoodOrigin : Origin → Prop)
    (GoodRight : Right → Prop)
    (h_cov : OriginCovariance toRight GoodOrigin GoodRight)
    (h_product : RightProductCertificate GoodRight) :
    ∀ origin, GoodOrigin origin := by
  intro origin
  exact h_cov origin (h_product (toRight origin))

theorem selected_trace_gcd_from_product_and_covariance
    {Origin Right : Type}
    (toRight : Origin → Right)
    (TraceGcdGood : Origin → Prop)
    (RightFactorGood : Right → Prop)
    (selected : Origin)
    (h_cov : ∀ origin,
      RightFactorGood (toRight origin) → TraceGcdGood origin)
    (h_product : ∀ right, RightFactorGood right) :
    TraceGcdGood selected := by
  exact selected_origin_from_right_product
    toRight TraceGcdGood RightFactorGood selected h_cov h_product

def ProductDetectsZeros {Right Scalar : Type} [Zero Scalar]
    (F : Right → Scalar)
    (originProduct : Scalar) : Prop :=
  (∃ t, F t = 0) → originProduct = 0

def DeterminantCovarianceNonzero
    {Origin Right Scalar : Type} [Zero Scalar]
    (toRight : Origin → Right)
    (F : Right → Scalar)
    (Delta : Origin → Scalar) : Prop :=
  ∀ origin, F (toRight origin) ≠ 0 → Delta origin ≠ 0

theorem all_right_factors_nonzero_from_product
    {Right Scalar : Type} [Zero Scalar]
    (F : Right → Scalar)
    (originProduct : Scalar)
    (h_detects : ProductDetectsZeros F originProduct)
    (h_product : originProduct ≠ 0) :
    ∀ t, F t ≠ 0 := by
  intro t h_zero
  exact h_product (h_detects ⟨t, h_zero⟩)

theorem all_origin_determinants_nonzero_from_product
    {Origin Right Scalar : Type} [Zero Scalar]
    (toRight : Origin → Right)
    (F : Right → Scalar)
    (Delta : Origin → Scalar)
    (originProduct : Scalar)
    (h_detects : ProductDetectsZeros F originProduct)
    (h_product : originProduct ≠ 0)
    (h_covariance : DeterminantCovarianceNonzero toRight F Delta) :
    ∀ origin, Delta origin ≠ 0 := by
  intro origin
  apply h_covariance
  exact all_right_factors_nonzero_from_product
    F originProduct h_detects h_product (toRight origin)

theorem selected_origin_determinant_nonzero_from_product
    {Origin Right Scalar : Type} [Zero Scalar]
    (toRight : Origin → Right)
    (F : Right → Scalar)
    (Delta : Origin → Scalar)
    (originProduct : Scalar)
    (selected : Origin)
    (h_detects : ProductDetectsZeros F originProduct)
    (h_product : originProduct ≠ 0)
    (h_covariance : DeterminantCovarianceNonzero toRight F Delta) :
    Delta selected ≠ 0 := by
  exact all_origin_determinants_nonzero_from_product
    toRight F Delta originProduct h_detects h_product h_covariance selected

end P24.TraceOriginProductGate
