/-!
Finite gate for the centered-marginal cyclic consecutive-arc product.

The arithmetic input is the open p24 theorem:

  every cyclic right-window determinant Delta_C(t), t mod 211, is nonzero,
  equivalently the seven Frobenius-orbit products are p-units.

This file only checks the finite implication and the relevant p24 dimensions.
-/

namespace P24.CenteredArcProductGate

def p24AmbientDim : Nat := 211
def p24CenteredAmbientDim : Nat := 210
def p24RowDim : Nat := 156
def p24PlateauLength : Nat := 157
def p24PlateauConstraints : Nat := p24PlateauLength - 1
def p24PlateauSubspaceDim : Nat := p24AmbientDim - p24PlateauConstraints
def p24CenteredPlateauSubspaceDim : Nat := p24AmbientDim - p24PlateauLength
def p24WindowCount : Nat := 211
def p24NonzeroOrbitCount : Nat := 6
def p24NonzeroOrbitSize : Nat := 35
def p24OrbitCount : Nat := 1 + p24NonzeroOrbitCount
def p24ComplementSupportBound : Nat := p24AmbientDim - p24PlateauLength
def p24UncertaintyThreshold : Nat := p24AmbientDim + 1
def p24UncertaintyFrequencyFloor : Nat :=
  p24UncertaintyThreshold - p24ComplementSupportBound

def ConsecutiveArc {windowCount : Nat} (good : Fin windowCount → Prop) : Prop :=
  ∀ t, good t

def OrbitProductCertificate {orbitCount : Nat}
    (orbitGood : Fin orbitCount → Prop) : Prop :=
  ∀ orbit, orbitGood orbit

def OrbitCovers {windowCount orbitCount : Nat}
    (orbitOf : Fin windowCount → Fin orbitCount)
    (orbitGood : Fin orbitCount → Prop)
    (good : Fin windowCount → Prop) : Prop :=
  ∀ t, orbitGood (orbitOf t) → good t

def SelectedWindowGood {windowCount : Nat}
    (good : Fin windowCount → Prop)
    (selected : Fin windowCount) : Prop :=
  good selected

def DifferenceMinorPUnit (minorRank fieldDim : Nat) : Prop :=
  minorRank = fieldDim

def MixedMarginalFullRank (matrixRank fieldDim : Nat) : Prop :=
  fieldDim ≤ matrixRank

theorem p24_plateau_constraints_value :
    p24PlateauConstraints = 156 := by
  decide

theorem p24_plateau_subspace_dim_value :
    p24PlateauSubspaceDim = 55 := by
  decide

theorem p24_complementary_dimensions :
    p24RowDim + p24PlateauSubspaceDim = p24AmbientDim := by
  decide

theorem p24_centered_ambient_dim_value :
    p24CenteredAmbientDim = 210 := by
  decide

theorem p24_centered_plateau_subspace_dim_value :
    p24CenteredPlateauSubspaceDim = 54 := by
  decide

theorem p24_centered_complementary_dimensions :
    p24RowDim + p24CenteredPlateauSubspaceDim = p24CenteredAmbientDim := by
  decide

theorem p24_orbit_partition_count :
    1 + p24NonzeroOrbitCount * p24NonzeroOrbitSize = p24WindowCount := by
  decide

theorem p24_orbit_count_value :
    p24OrbitCount = 7 := by
  decide

theorem p24_complement_support_bound_value :
    p24ComplementSupportBound = 54 := by
  decide

theorem p24_uncertainty_frequency_floor_value :
    p24UncertaintyFrequencyFloor = 158 := by
  decide

theorem arc_from_orbit_products {windowCount orbitCount : Nat}
    (good : Fin windowCount → Prop)
    (orbitGood : Fin orbitCount → Prop)
    (orbitOf : Fin windowCount → Fin orbitCount)
    (h_orbits : OrbitProductCertificate orbitGood)
    (h_cover : OrbitCovers orbitOf orbitGood good) :
    ConsecutiveArc good := by
  intro t
  exact h_cover t (h_orbits (orbitOf t))

theorem selected_from_arc {windowCount : Nat}
    (good : Fin windowCount → Prop)
    (selected : Fin windowCount)
    (h_arc : ConsecutiveArc good) :
    SelectedWindowGood good selected := by
  exact h_arc selected

theorem mixed_rank_from_selected_difference_minor
    (minorRank matrixRank fieldDim : Nat)
    (h_minor : DifferenceMinorPUnit minorRank fieldDim)
    (h_minor_in_matrix : minorRank ≤ matrixRank) :
    MixedMarginalFullRank matrixRank fieldDim := by
  rw [MixedMarginalFullRank]
  rw [DifferenceMinorPUnit] at h_minor
  rw [← h_minor]
  exact h_minor_in_matrix

theorem selected_minor_from_orbit_products {windowCount orbitCount : Nat}
    (good : Fin windowCount → Prop)
    (orbitGood : Fin orbitCount → Prop)
    (orbitOf : Fin windowCount → Fin orbitCount)
    (selected : Fin windowCount)
    (h_orbits : OrbitProductCertificate orbitGood)
    (h_cover : OrbitCovers orbitOf orbitGood good) :
    SelectedWindowGood good selected :=
  selected_from_arc good selected
    (arc_from_orbit_products good orbitGood orbitOf h_orbits h_cover)

end P24.CenteredArcProductGate
