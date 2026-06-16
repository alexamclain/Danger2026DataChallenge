/-!
Finite gate for a quotient-plus-recovery CM certificate.

This is the generic gate behind surfaces such as:

  degree-19 quotient root + selected degree-14670196166 recovery root

for the first p24 strict trace, or the larger phase-lifted quotient/recovery
surfaces for the third trace.

The arithmetic producer theorem is external: it must prove that the quotient
root and recovery relation are embedded and paired with the correct CM torsor.
-/

namespace P24.QuotientRecoveryCertificateGate

def QuotientRecoveryChain
    {Q J : Type}
    (QuotientRoot : Q → Prop)
    (Recovery : Q → J → Prop)
    (q : Q) (j : J) : Prop :=
  QuotientRoot q ∧ Recovery q j

def QuotientProducerSound
    {Q J : Type}
    (QuotientRoot : Q → Prop)
    (Recovery : Q → J → Prop)
    (StrictJ : J → Prop) : Prop :=
  ∀ q j, QuotientRecoveryChain QuotientRoot Recovery q j → StrictJ j

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

theorem strict_j_from_quotient_recovery
    {Q J : Type}
    (QuotientRoot : Q → Prop)
    (Recovery : Q → J → Prop)
    (StrictJ : J → Prop)
    (q : Q) (j : J)
    (h_sound : QuotientProducerSound QuotientRoot Recovery StrictJ)
    (h_chain : QuotientRecoveryChain QuotientRoot Recovery q j) :
    StrictJ j := by
  exact h_sound q j h_chain

theorem danger_from_quotient_recovery_certificate
    {Q J A X : Type}
    (QuotientRoot : Q → Prop)
    (Recovery : Q → J → Prop)
    (StrictJ : J → Prop)
    (MontgomeryAbove : J → A → Prop)
    (TargetA : A → Prop)
    (OddProjection : A → X → Prop)
    (DangerTriple : A → X → Prop)
    (q : Q) (j : J) (a : A) (x : X)
    (h_quotient :
      QuotientProducerSound QuotientRoot Recovery StrictJ)
    (h_mont : MontgomerySound StrictJ MontgomeryAbove TargetA)
    (h_proj : ProjectionSound TargetA OddProjection DangerTriple)
    (h_chain : QuotientRecoveryChain QuotientRoot Recovery q j)
    (h_above : MontgomeryAbove j a)
    (h_odd : OddProjection a x) :
    DangerTriple a x := by
  have h_strict : StrictJ j :=
    strict_j_from_quotient_recovery
      QuotientRoot Recovery StrictJ q j h_quotient h_chain
  have h_target : TargetA a := h_mont j a h_strict h_above
  exact h_proj a x h_target h_odd

end P24.QuotientRecoveryCertificateGate
