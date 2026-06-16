/-!
Finite algebra gate for the p24 product-coboundary route.

The arithmetic input is external: for the raw p24 packet term

  T_{1,0,a} * R_{chi,-a}

one still has to construct the left covariance multiplier and the matching
right-resolvent potential from CM/Lang data.  This file records only the
formal product rule:

  sigma(A) = alpha • A
  B = sigma(V) - eta • V
  epsilon • (alpha^{-1} • X) = eta • X

imply

  A * B = sigma(alpha^{-1} • (A * V))
          - epsilon • (alpha^{-1} • (A * V)).

So a matching right-resolvent coboundary gives a raw product coboundary without
first proving trace zero or inverting Hilbert-90.
-/

namespace P24.TraceGcdProductCoboundaryGate

def TwistedCoboundary {K V : Type}
    (sigma : V → V) (scale : K → V → V) (sub : V → V → V)
    (epsilon : K) (potential : V) : V :=
  sub (sigma potential) (scale epsilon potential)

def Covariant {K V : Type}
    (sigma : V → V) (scale : K → V → V)
    (alpha : K) (value : V) : Prop :=
  sigma value = scale alpha value

def RightCoboundary {K V : Type}
    (sigma : V → V) (scale : K → V → V) (sub : V → V → V)
    (eta : K) (factor potential : V) : Prop :=
  factor = TwistedCoboundary sigma scale sub eta potential

theorem product_coboundary_from_left_covariance
    {K V : Type}
    (sigma : V → V)
    (prod : V → V → V)
    (scale : K → V → V)
    (sub : V → V → V)
    (alpha alphaInv epsilon eta : K)
    (left right rightPotential : V)
    (h_right :
      RightCoboundary sigma scale sub eta right rightPotential)
    (h_left_cov :
      Covariant sigma scale alpha left)
    (h_prod_sub :
      ∀ x y, prod left (sub x y) =
        sub (prod left x) (prod left y))
    (h_prod_scale_right :
      ∀ k x, prod left (scale k x) =
        scale k (prod left x))
    (h_sigma_scale :
      ∀ k x, sigma (scale k x) =
        scale k (sigma x))
    (h_sigma_prod :
      sigma (prod left rightPotential) =
        prod (sigma left) (sigma rightPotential))
    (h_prod_scale_left_alpha :
      ∀ x, prod (scale alpha left) x =
        scale alpha (prod left x))
    (h_unscale_alpha :
      ∀ x, scale alphaInv (scale alpha x) = x)
    (h_twist_match :
      ∀ x, scale epsilon (scale alphaInv x) =
        scale eta x) :
    prod left right =
      TwistedCoboundary sigma scale sub epsilon
        (scale alphaInv (prod left rightPotential)) := by
  unfold RightCoboundary at h_right
  unfold TwistedCoboundary at h_right
  unfold Covariant at h_left_cov
  unfold TwistedCoboundary
  rw [h_right]
  rw [h_prod_sub]
  rw [h_prod_scale_right]
  have h_first :
      prod left (sigma rightPotential) =
        sigma (scale alphaInv (prod left rightPotential)) := by
    calc
      prod left (sigma rightPotential)
          = scale alphaInv
              (scale alpha (prod left (sigma rightPotential))) :=
            (h_unscale_alpha (prod left (sigma rightPotential))).symm
      _ = scale alphaInv
              (prod (scale alpha left) (sigma rightPotential)) := by
            rw [← h_prod_scale_left_alpha (sigma rightPotential)]
      _ = scale alphaInv
              (prod (sigma left) (sigma rightPotential)) := by
            rw [← h_left_cov]
      _ = scale alphaInv (sigma (prod left rightPotential)) := by
            rw [← h_sigma_prod]
      _ = sigma (scale alphaInv (prod left rightPotential)) := by
            rw [h_sigma_scale]
  have h_second :
      scale eta (prod left rightPotential) =
        scale epsilon
          (scale alphaInv (prod left rightPotential)) :=
    (h_twist_match (prod left rightPotential)).symm
  rw [h_first, h_second]

theorem p24_product_packet_count :
    6 * 10 * 7 = 420 := by
  decide

theorem p24_character_payload_count :
    6 * 156 + 156 = 1092 := by
  decide

theorem p24_internal_trace_degree_factorization :
    31 * 179 = 5549 := by
  decide

end P24.TraceGcdProductCoboundaryGate
