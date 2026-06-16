/-!
Finite gate for the phase-lifted decomposed CM tower certificate.

This file deliberately proves only the finite implication.  The arithmetic
producer theorem must still supply the embedded relative phase relations and
the selected recovery polynomial.
-/

namespace P24.PhaseLiftedTowerGate

def Chain
    {Z Y W J : Type}
    (TopRoot : Z → Prop)
    (Rel157 : Z → Y → Prop)
    (Rel211 : Y → W → Prop)
    (Recovery : W → J → Prop)
    (z : Z) (y : Y) (w : W) (j : J) : Prop :=
  TopRoot z ∧ Rel157 z y ∧ Rel211 y w ∧ Recovery w j

def PhaseProducerSound
    {Z Y W J : Type}
    (TopRoot : Z → Prop)
    (Rel157 : Z → Y → Prop)
    (Rel211 : Y → W → Prop)
    (Recovery : W → J → Prop)
    (StrictJ : J → Prop) : Prop :=
  ∀ z y w j,
    Chain TopRoot Rel157 Rel211 Recovery z y w j → StrictJ j

def MontgomerySound
    {J A : Type}
    (StrictJ : J → Prop)
    (MontgomeryAbove : J → A → Prop)
    (TargetA : A → Prop) : Prop :=
  ∀ j a, StrictJ j → MontgomeryAbove j a → TargetA a

def ProjectionSound
    {A X : Type}
    (TargetA : A → Prop)
    (OddProjection : A → X → Prop)
    (DangerTriple : A → X → Prop) : Prop :=
  ∀ a x, TargetA a → OddProjection a x → DangerTriple a x

theorem strict_j_from_phase_chain
    {Z Y W J : Type}
    (TopRoot : Z → Prop)
    (Rel157 : Z → Y → Prop)
    (Rel211 : Y → W → Prop)
    (Recovery : W → J → Prop)
    (StrictJ : J → Prop)
    (z : Z) (y : Y) (w : W) (j : J)
    (h_sound :
      PhaseProducerSound TopRoot Rel157 Rel211 Recovery StrictJ)
    (h_chain : Chain TopRoot Rel157 Rel211 Recovery z y w j) :
    StrictJ j := by
  exact h_sound z y w j h_chain

theorem danger_from_phase_lifted_certificate
    {Z Y W J A X : Type}
    (TopRoot : Z → Prop)
    (Rel157 : Z → Y → Prop)
    (Rel211 : Y → W → Prop)
    (Recovery : W → J → Prop)
    (StrictJ : J → Prop)
    (MontgomeryAbove : J → A → Prop)
    (TargetA : A → Prop)
    (OddProjection : A → X → Prop)
    (DangerTriple : A → X → Prop)
    (z : Z) (y : Y) (w : W) (j : J) (a : A) (x : X)
    (h_phase :
      PhaseProducerSound TopRoot Rel157 Rel211 Recovery StrictJ)
    (h_mont : MontgomerySound StrictJ MontgomeryAbove TargetA)
    (h_proj : ProjectionSound TargetA OddProjection DangerTriple)
    (h_chain : Chain TopRoot Rel157 Rel211 Recovery z y w j)
    (h_above : MontgomeryAbove j a)
    (h_odd : OddProjection a x) :
    DangerTriple a x := by
  have h_strict : StrictJ j :=
    strict_j_from_phase_chain
      TopRoot Rel157 Rel211 Recovery StrictJ z y w j h_phase h_chain
  have h_target : TargetA a := h_mont j a h_strict h_above
  exact h_proj a x h_target h_odd

end P24.PhaseLiftedTowerGate
