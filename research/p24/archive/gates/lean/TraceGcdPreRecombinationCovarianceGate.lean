/-!
Finite gate for the noncircular p24 fixed-frequency covariance route.

The arithmetic input is not ordinary Frobenius covariance, and not a
post-recombination eigenstatement.  It must be a covariance identity for the
Gauss-normalized trace-resolvent components before the complete 70-factor
recombination.  This file records the finite handoff:

* pre-recombination component covariance gives a nontrivial eigenstatement for
  the complete packet sum;
* complete recombination identifies that packet sum with the descended
  `L = F_p(mu_157)` projection;
* fixed-by-rho plus a nontrivial eigenspace intersection forces the packet sum
  to be zero;
* zero packet sums for the six nontrivial characters are the input expected by
  the H-coset/projector pipeline.

No CM periods, Gauss sums, idempotents, or finite-field traces are formalized
here.  They remain the missing arithmetic theorem.
-/

namespace P24.TraceGcdPreRecombinationCovarianceGate

def FixedBy {V : Type} (sigma : V → V) (value : V) : Prop :=
  sigma value = value

def EigenFor {V : Type} (sigma twist : V → V) (value : V) : Prop :=
  sigma value = twist value

def FixedEigenspaceIntersectionZero {V : Type} [Zero V]
    (twist : V → V) : Prop :=
  ∀ value, twist value = value → value = 0

def ComponentCovariance {Factor V : Type}
    (sigma twist : V → V)
    (shift : Factor → Factor)
    (component : Factor → V) : Prop :=
  ∀ factor, sigma (component factor) = twist (component (shift factor))

def CompleteRecombination {Factor V : Type}
    (combine : (Factor → V) → V)
    (component : Factor → V)
    (packetSum : V) : Prop :=
  combine component = packetSum

def ComponentCovarianceGivesPacketEigen {Factor V : Type}
    (sigma twist : V → V)
    (shift : Factor → Factor)
    (combine : (Factor → V) → V)
    (component : Factor → V)
    (packetSum : V) : Prop :=
  ComponentCovariance sigma twist shift component →
  CompleteRecombination combine component packetSum →
  EigenFor sigma twist packetSum

theorem zero_from_prerecombination_covariance
    {Factor V : Type} [Zero V]
    (sigma twist : V → V)
    (shift : Factor → Factor)
    (combine : (Factor → V) → V)
    (component : Factor → V)
    (packetSum : V)
    (h_component_to_packet :
      ComponentCovarianceGivesPacketEigen
        sigma twist shift combine component packetSum)
    (h_component :
      ComponentCovariance sigma twist shift component)
    (h_recombine :
      CompleteRecombination combine component packetSum)
    (h_descends : FixedBy sigma packetSum)
    (h_intersection :
      FixedEigenspaceIntersectionZero twist) :
    packetSum = 0 := by
  have h_eigen : EigenFor sigma twist packetSum :=
    h_component_to_packet h_component h_recombine
  apply h_intersection packetSum
  exact h_eigen.symm.trans h_descends

theorem all_character_sums_zero_from_prerecombination_covariance
    {Character Factor V : Type} [Zero V]
    (sigma : V → V)
    (twist : Character → V → V)
    (shift : Factor → Factor)
    (combine : (Factor → V) → V)
    (component : Character → Factor → V)
    (packetSum : Character → V)
    (h_component_to_packet :
      ∀ chi,
        ComponentCovarianceGivesPacketEigen
          sigma (twist chi) shift combine (component chi) (packetSum chi))
    (h_component :
      ∀ chi,
        ComponentCovariance sigma (twist chi) shift (component chi))
    (h_recombine :
      ∀ chi,
        CompleteRecombination combine (component chi) (packetSum chi))
    (h_descends :
      ∀ chi, FixedBy sigma (packetSum chi))
    (h_intersection :
      ∀ chi, FixedEigenspaceIntersectionZero (twist chi)) :
    ∀ chi, packetSum chi = 0 := by
  intro chi
  exact zero_from_prerecombination_covariance
    sigma (twist chi) shift combine (component chi) (packetSum chi)
    (h_component_to_packet chi)
    (h_component chi)
    (h_recombine chi)
    (h_descends chi)
    (h_intersection chi)

def p24LeftRows : Nat := 156
def p24RightHCosets : Nat := 7
def p24NontrivialCharacters : Nat := 6
def p24TensorFactorCount : Nat := 70
def p24QuotientCycleCount : Nat := 10
def p24QuotientCycleLength : Nat := 7

theorem p24_tensor_factor_cycle_count :
    p24QuotientCycleCount * p24QuotientCycleLength =
      p24TensorFactorCount := by
  decide

theorem p24_nontrivial_character_equations :
    p24NontrivialCharacters * p24LeftRows = 936 := by
  decide

theorem p24_hcoset_equations :
    p24RightHCosets * p24LeftRows = 1092 := by
  decide

theorem p24_centering_plus_characters :
    p24LeftRows + p24NontrivialCharacters * p24LeftRows = 1092 := by
  decide

theorem p24_prerecombination_payload_subsqrt :
    p24RightHCosets * p24LeftRows < 1000000000000 := by
  decide

end P24.TraceGcdPreRecombinationCovarianceGate
