/-!
Finite gate for the two-moment and lambda-packaged content certificates.

This file uses only Lean core.  It does not prove the p24 arithmetic theorem
that the actual moments are p-units.  It checks the finite logic used in
`moment_lambda_packaging_boundary.md`:

* if a harmful packet is all zero, then both moments M0 and M1 vanish;
* therefore a nonzero moment pair rules out the harmful packet;
* if a chosen lambda avoids the packetwise forbidden lambda values, then the
  one-scalar projections M0 + lambda*M1 are nonzero and also rule out harmful
  packets.

The finite safe-lambda choice itself remains an external certificate datum:
for p24 there are only eight packet orbits, so the implementation can test a
small list of lambda candidates once the moments are constructible.
-/

namespace P24.MomentLambdaGate

def AllZero {α : Type} [Zero α] {m : Nat} (v : Fin m → α) : Prop :=
  ∀ u, v u = 0

def PairZero {α : Type} [Zero α] (m0 m1 : α) : Prop :=
  m0 = 0 ∧ m1 = 0

def PairGood {α : Type} [Zero α] (m0 m1 : α) : Prop :=
  ¬ PairZero m0 m1

def PacketContentGood {α : Type} [Zero α] {m : Nat}
    (packet : Fin m → α) : Prop :=
  ¬ AllZero packet

def GlobalContentGood {α : Type} [Zero α] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α) : Prop :=
  ∀ orbit, PacketContentGood (packet orbit)

theorem pair_good_content
    {α β : Type} [Zero α] [Zero β] {m : Nat}
    (packet : Fin m → α)
    (m0 m1 : β)
    (h_all_zero_pair_zero : AllZero packet → PairZero m0 m1)
    (h_pair_good : PairGood m0 m1) :
    PacketContentGood packet := by
  intro hzero
  exact h_pair_good (h_all_zero_pair_zero hzero)

theorem global_content_from_moment_pairs
    {α β : Type} [Zero α] [Zero β] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (m0 m1 : Fin orbitCount → β)
    (h_all_zero_pair_zero :
      ∀ orbit, AllZero (packet orbit) → PairZero (m0 orbit) (m1 orbit))
    (h_pair_good :
      ∀ orbit, PairGood (m0 orbit) (m1 orbit)) :
    GlobalContentGood packet := by
  intro orbit
  exact pair_good_content (packet orbit) (m0 orbit) (m1 orbit)
    (h_all_zero_pair_zero orbit) (h_pair_good orbit)

theorem no_harmful_from_moment_pairs
    {α β : Type} [Zero α] [Zero β] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (m0 m1 : Fin orbitCount → β)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_all_zero_pair_zero :
      ∀ orbit, AllZero (packet orbit) → PairZero (m0 orbit) (m1 orbit))
    (h_pair_good :
      ∀ orbit, PairGood (m0 orbit) (m1 orbit)) :
    ∀ orbit, ¬ harmful orbit := by
  intro orbit hh
  have h_content : GlobalContentGood packet :=
    global_content_from_moment_pairs packet m0 m1
      h_all_zero_pair_zero h_pair_good
  exact h_content orbit (h_harmful_all_zero orbit hh)

def AvoidsForbidden {Lam : Type} {orbitCount : Nat}
    (forbidden : Fin orbitCount → Option Lam) (chosen : Lam) : Prop :=
  ∀ orbit, forbidden orbit ≠ some chosen

theorem safe_lambda_projection_nonzero
    {α Lam : Type} [Zero α] {orbitCount : Nat}
    (projection : Fin orbitCount → Lam → α)
    (forbidden : Fin orbitCount → Option Lam)
    (chosen : Lam)
    (h_safe : AvoidsForbidden forbidden chosen)
    (h_zero_implies_forbidden :
      ∀ orbit lam, projection orbit lam = 0 → forbidden orbit = some lam) :
    ∀ orbit, projection orbit chosen ≠ 0 := by
  intro orbit hzero
  exact h_safe orbit (h_zero_implies_forbidden orbit chosen hzero)

theorem one_lambda_global_content
    {α β Lam : Type} [Zero α] [Zero β] {orbitCount m : Nat}
    (packet : Fin orbitCount → Fin m → α)
    (projection : Fin orbitCount → Lam → β)
    (forbidden : Fin orbitCount → Option Lam)
    (chosen : Lam)
    (h_all_zero_projection_zero :
      ∀ orbit, AllZero (packet orbit) → projection orbit chosen = 0)
    (h_safe : AvoidsForbidden forbidden chosen)
    (h_zero_implies_forbidden :
      ∀ orbit lam, projection orbit lam = 0 → forbidden orbit = some lam) :
    GlobalContentGood packet := by
  have h_projection_nonzero :
      ∀ orbit, projection orbit chosen ≠ 0 :=
    safe_lambda_projection_nonzero projection forbidden chosen
      h_safe h_zero_implies_forbidden
  intro orbit hzero
  exact h_projection_nonzero orbit
    (h_all_zero_projection_zero orbit hzero)

theorem no_harmful_from_one_safe_lambda
    {α β Lam : Type} [Zero α] [Zero β] {orbitCount m : Nat}
    (harmful : Fin orbitCount → Prop)
    (packet : Fin orbitCount → Fin m → α)
    (projection : Fin orbitCount → Lam → β)
    (forbidden : Fin orbitCount → Option Lam)
    (chosen : Lam)
    (h_harmful_all_zero :
      ∀ orbit, harmful orbit → AllZero (packet orbit))
    (h_all_zero_projection_zero :
      ∀ orbit, AllZero (packet orbit) → projection orbit chosen = 0)
    (h_safe : AvoidsForbidden forbidden chosen)
    (h_zero_implies_forbidden :
      ∀ orbit lam, projection orbit lam = 0 → forbidden orbit = some lam) :
    ∀ orbit, ¬ harmful orbit := by
  have h_content : GlobalContentGood packet :=
    one_lambda_global_content packet projection forbidden chosen
      h_all_zero_projection_zero h_safe h_zero_implies_forbidden
  intro orbit hh
  exact h_content orbit (h_harmful_all_zero orbit hh)

end P24.MomentLambdaGate
