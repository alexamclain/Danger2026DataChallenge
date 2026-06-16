/-!
Finite gate for trace-GCD block-cycle/Fitting norms.

The crossed-product orbit norm can be lifted from scalar weights

    Delta(t) = det(M_t)

to a block cyclic operator built from the actual tail-on-kernel maps `M_t`.
The arithmetic producer may then target a Fitting determinant of the block
operator directly.

Lean records only the finite implication:

* the named block norm equals the named orbit product;
* any zero determinant value zeros the orbit product;
* every block norm is nonzero;
* therefore every determinant value is nonzero.
-/

namespace P24.TraceGcdBlockCycleGate

def BlockNormMatchesProduct {Orbit Scalar : Type}
    (blockNorm orbitProduct : Orbit → Scalar) : Prop :=
  ∀ orbit, blockNorm orbit = orbitProduct orbit

def OrbitProductZeroOnValueZero {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (orbitProduct : Orbit → Scalar) : Prop :=
  ∀ t, Delta t = 0 → orbitProduct (orbitOf t) = 0

theorem orbit_products_nonzero_from_block_norms
    {Orbit Scalar : Type} [Zero Scalar]
    (blockNorm orbitProduct : Orbit → Scalar)
    (h_match : BlockNormMatchesProduct blockNorm orbitProduct)
    (h_block_nonzero : ∀ orbit, blockNorm orbit ≠ 0) :
    ∀ orbit, orbitProduct orbit ≠ 0 := by
  intro orbit h_zero
  exact h_block_nonzero orbit (by
    rw [h_match orbit]
    exact h_zero)

theorem values_nonzero_from_block_norms
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (blockNorm orbitProduct : Orbit → Scalar)
    (h_match : BlockNormMatchesProduct blockNorm orbitProduct)
    (h_zero_factor :
      OrbitProductZeroOnValueZero orbitOf Delta orbitProduct)
    (h_block_nonzero : ∀ orbit, blockNorm orbit ≠ 0) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_orbit_zero : orbitProduct (orbitOf t) = 0 :=
    h_zero_factor t h_delta_zero
  exact
    (orbit_products_nonzero_from_block_norms
      blockNorm orbitProduct h_match h_block_nonzero (orbitOf t))
    h_orbit_zero

theorem selected_good_from_block_norms
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (blockNorm orbitProduct : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (h_match : BlockNormMatchesProduct blockNorm orbitProduct)
    (h_zero_factor :
      OrbitProductZeroOnValueZero orbitOf Delta orbitProduct)
    (h_block_nonzero : ∀ orbit, blockNorm orbit ≠ 0)
    (h_delta_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_delta_to_good selected
    (values_nonzero_from_block_norms orbitOf Delta blockNorm orbitProduct
      h_match h_zero_factor h_block_nonzero selected)

def LocalBad {Index : Type} (BadAt : Index → Prop) : Prop :=
  ∃ t, BadAt t

def OrbitBlockBad {Orbit : Type} (BlockBad : Orbit → Prop) : Prop :=
  ∃ orbit, BlockBad orbit

def BlockBadForcesLocalBad {Index Orbit : Type}
    (orbitOf : Index → Orbit)
    (BlockBad : Orbit → Prop)
    (BadAt : Index → Prop) : Prop :=
  ∀ orbit, BlockBad orbit → ∃ t, orbitOf t = orbit ∧ BadAt t

theorem no_orbit_block_bad_from_no_local_bad
    {Index Orbit : Type}
    (orbitOf : Index → Orbit)
    (BlockBad : Orbit → Prop)
    (BadAt : Index → Prop)
    (h_sound : BlockBadForcesLocalBad orbitOf BlockBad BadAt)
    (h_no_local_bad : ∀ t, ¬ BadAt t) :
    ∀ orbit, ¬ BlockBad orbit := by
  intro orbit h_block_bad
  rcases h_sound orbit h_block_bad with ⟨t, _h_orbit, h_bad_at_t⟩
  exact h_no_local_bad t h_bad_at_t

theorem no_global_block_bad_from_no_local_bad
    {Index Orbit : Type}
    (orbitOf : Index → Orbit)
    (BlockBad : Orbit → Prop)
    (BadAt : Index → Prop)
    (h_sound : BlockBadForcesLocalBad orbitOf BlockBad BadAt)
    (h_no_local_bad : ∀ t, ¬ BadAt t) :
    ¬ OrbitBlockBad BlockBad := by
  intro h_global_bad
  rcases h_global_bad with ⟨orbit, h_block_bad⟩
  exact
    (no_orbit_block_bad_from_no_local_bad
      orbitOf BlockBad BadAt h_sound h_no_local_bad orbit)
    h_block_bad

end P24.TraceGcdBlockCycleGate
