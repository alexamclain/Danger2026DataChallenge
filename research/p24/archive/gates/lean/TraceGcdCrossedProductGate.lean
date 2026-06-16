/-!
Finite gate for trace-GCD crossed-product orbit norms.

For a Frobenius orbit `O`, the raw determinant values

    Delta(t), t in O

need not descend as ordinary base-field factor residues.  The safe finite
package is a crossed-product/reduced norm whose scalar value equals the orbit
product.  For p24 the nonzero orbit lengths are `35`, so the weighted-cycle
determinant has positive sign and can be absorbed into the named norm.

Lean checks only the finite implication:

* the named crossed norm equals the actual orbit product;
* any zero `Delta(t)` makes the orbit product zero;
* every crossed norm is nonzero;
* therefore every `Delta(t)` is nonzero.
-/

namespace P24.TraceGcdCrossedProductGate

def CrossedNormMatchesProduct {Orbit Scalar : Type}
    (crossedNorm orbitProduct : Orbit → Scalar) : Prop :=
  ∀ orbit, crossedNorm orbit = orbitProduct orbit

def OrbitProductZeroOnValueZero {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (orbitProduct : Orbit → Scalar) : Prop :=
  ∀ t, Delta t = 0 → orbitProduct (orbitOf t) = 0

theorem orbit_products_nonzero_from_crossed_norms
    {Orbit Scalar : Type} [Zero Scalar]
    (crossedNorm orbitProduct : Orbit → Scalar)
    (h_match : CrossedNormMatchesProduct crossedNorm orbitProduct)
    (h_crossed_nonzero : ∀ orbit, crossedNorm orbit ≠ 0) :
    ∀ orbit, orbitProduct orbit ≠ 0 := by
  intro orbit h_zero
  exact h_crossed_nonzero orbit (by
    rw [h_match orbit]
    exact h_zero)

theorem values_nonzero_from_crossed_norms
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (crossedNorm orbitProduct : Orbit → Scalar)
    (h_match : CrossedNormMatchesProduct crossedNorm orbitProduct)
    (h_zero_factor :
      OrbitProductZeroOnValueZero orbitOf Delta orbitProduct)
    (h_crossed_nonzero : ∀ orbit, crossedNorm orbit ≠ 0) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_orbit_product_zero : orbitProduct (orbitOf t) = 0 :=
    h_zero_factor t h_delta_zero
  exact
    (orbit_products_nonzero_from_crossed_norms
      crossedNorm orbitProduct h_match h_crossed_nonzero (orbitOf t))
    h_orbit_product_zero

theorem selected_good_from_crossed_norms
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (crossedNorm orbitProduct : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (h_match : CrossedNormMatchesProduct crossedNorm orbitProduct)
    (h_zero_factor :
      OrbitProductZeroOnValueZero orbitOf Delta orbitProduct)
    (h_crossed_nonzero : ∀ orbit, crossedNorm orbit ≠ 0)
    (h_delta_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_delta_to_good selected
    (values_nonzero_from_crossed_norms orbitOf Delta crossedNorm
      orbitProduct h_match h_zero_factor h_crossed_nonzero selected)

end P24.TraceGcdCrossedProductGate
