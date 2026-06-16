/-!
Finite gate for the Hermitian-orthogonal Plucker version of the centered
marginal determinant.

The arithmetic/linear-algebra identity isolated by the audit is:

  Delta_C(t) = sum_S u_S(t) v_S(t)

after choosing a p-integral Hermitian-orthogonal packet basis.  This file does
not construct that basis, the Plucker coordinates, or a p-adic valuation
argument.  It records the finite handoff:

* an exact orthogonal Plucker comparison transfers p-unitness from the diagonal
  pairing to the determinant;
* a local initial-dominance theorem is one possible producer of that p-unitness;
* determinant p-unitness excludes the centered Schubert bad event.
-/

namespace P24.CenteredHermitianPluckerGate

def OrthogonalPluckerComparison {Index Scalar : Type}
    (delta diagonalPairing : Index → Scalar) : Prop :=
  ∀ t, delta t = diagonalPairing t

def DiagonalPairingPUnitPayload {Index Scalar : Type}
    (diagonalPairing : Index → Scalar)
    (PUnit : Scalar → Prop) : Prop :=
  ∀ t, PUnit (diagonalPairing t)

def InitialDominanceProducer {Index Scalar : Type}
    (diagonalPairing initial higher : Index → Scalar)
    (PUnit Small : Scalar → Prop) : Prop :=
  ∀ t, PUnit (initial t) → Small (higher t) → PUnit (diagonalPairing t)

def InitialTermsPUnit {Index Scalar : Type}
    (initial : Index → Scalar)
    (PUnit : Scalar → Prop) : Prop :=
  ∀ t, PUnit (initial t)

def HigherTermsSmall {Index Scalar : Type}
    (higher : Index → Scalar)
    (Small : Scalar → Prop) : Prop :=
  ∀ t, Small (higher t)

def BadDetectedByDelta {Index Scalar : Type} [Zero Scalar]
    (delta : Index → Scalar)
    (Bad : Index → Prop) : Prop :=
  ∀ t, Bad t → delta t = 0

def GoodFromNoBad {Index : Type}
    (Bad Good : Index → Prop) : Prop :=
  ∀ t, ¬ Bad t → Good t

def ConsecutiveArc {Index : Type} (Good : Index → Prop) : Prop :=
  ∀ t, Good t

theorem diagonal_pairing_punits_from_initial_dominance
    {Index Scalar : Type}
    (diagonalPairing initial higher : Index → Scalar)
    (PUnit Small : Scalar → Prop)
    (h_producer :
      InitialDominanceProducer diagonalPairing initial higher PUnit Small)
    (h_initial : InitialTermsPUnit initial PUnit)
    (h_higher : HigherTermsSmall higher Small) :
    DiagonalPairingPUnitPayload diagonalPairing PUnit := by
  intro t
  exact h_producer t (h_initial t) (h_higher t)

theorem deltas_punit_from_diagonal_pairing_punits
    {Index Scalar : Type}
    (delta diagonalPairing : Index → Scalar)
    (PUnit : Scalar → Prop)
    (h_compare : OrthogonalPluckerComparison delta diagonalPairing)
    (h_payload : DiagonalPairingPUnitPayload diagonalPairing PUnit) :
    ∀ t, PUnit (delta t) := by
  intro t
  rw [h_compare t]
  exact h_payload t

theorem no_bad_from_diagonal_pairing_punits
    {Index Scalar : Type} [Zero Scalar]
    (delta diagonalPairing : Index → Scalar)
    (Bad : Index → Prop)
    (PUnit : Scalar → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_compare : OrthogonalPluckerComparison delta diagonalPairing)
    (h_bad_delta : BadDetectedByDelta delta Bad)
    (h_payload : DiagonalPairingPUnitPayload diagonalPairing PUnit) :
    ∀ t, ¬ Bad t := by
  intro t h_bad
  have h_delta_punit : PUnit (delta t) :=
    deltas_punit_from_diagonal_pairing_punits
      delta diagonalPairing PUnit h_compare h_payload t
  exact (h_punit_nonzero (delta t) h_delta_punit) (h_bad_delta t h_bad)

theorem consecutive_arc_from_diagonal_initial_dominance
    {Index Scalar : Type} [Zero Scalar]
    (delta diagonalPairing initial higher : Index → Scalar)
    (Bad Good : Index → Prop)
    (PUnit Small : Scalar → Prop)
    (h_punit_nonzero : ∀ value, PUnit value → value ≠ 0)
    (h_compare : OrthogonalPluckerComparison delta diagonalPairing)
    (h_bad_delta : BadDetectedByDelta delta Bad)
    (h_producer :
      InitialDominanceProducer diagonalPairing initial higher PUnit Small)
    (h_initial : InitialTermsPUnit initial PUnit)
    (h_higher : HigherTermsSmall higher Small)
    (h_good : GoodFromNoBad Bad Good) :
    ConsecutiveArc Good := by
  intro t
  exact h_good t
    (no_bad_from_diagonal_pairing_punits
      delta diagonalPairing Bad PUnit h_punit_nonzero h_compare h_bad_delta
      (diagonal_pairing_punits_from_initial_dominance
        diagonalPairing initial higher PUnit Small h_producer h_initial
        h_higher)
      t)

end P24.CenteredHermitianPluckerGate
