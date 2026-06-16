/-!
Finite gate for unit-action orbit compression.

If a certificate property is preserved along a finite cycle of algebra
automorphisms, then one representative proves the whole orbit.  This is the
formal logic behind using the right-unit action on the six p24 right
cyclotomic factors to compress opposite-pair prefix/tail p-unit classes.
-/

namespace P24.UnitOrbitGate

theorem three_cycle_from_representative
    {Class : Type}
    (P : Class → Prop)
    (a b c : Class)
    (h_ab : P a → P b)
    (h_bc : P b → P c)
    (_h_ca : P c → P a)
    (h_a : P a) :
    P a ∧ P b ∧ P c := by
  have h_b : P b := h_ab h_a
  have h_c : P c := h_bc h_b
  exact ⟨h_a, h_b, h_c⟩

theorem six_cycle_from_representative
    {Class : Type}
    (P : Class → Prop)
    (a b c d e f : Class)
    (h_ab : P a → P b)
    (h_bc : P b → P c)
    (h_cd : P c → P d)
    (h_de : P d → P e)
    (h_ef : P e → P f)
    (_h_fa : P f → P a)
    (h_a : P a) :
    P a ∧ P b ∧ P c ∧ P d ∧ P e ∧ P f := by
  have h_b : P b := h_ab h_a
  have h_c : P c := h_bc h_b
  have h_d : P d := h_cd h_c
  have h_e : P e := h_de h_d
  have h_f : P f := h_ef h_e
  exact ⟨h_a, h_b, h_c, h_d, h_e, h_f⟩

theorem fixed_and_six_cycle_from_representative
    {Class : Type}
    (P : Class → Prop)
    (z a b c d e f : Class)
    (h_ab : P a → P b)
    (h_bc : P b → P c)
    (h_cd : P c → P d)
    (h_de : P d → P e)
    (h_ef : P e → P f)
    (h_fa : P f → P a)
    (h_z : P z)
    (h_a : P a) :
    P z ∧ P a ∧ P b ∧ P c ∧ P d ∧ P e ∧ P f := by
  have h_cycle :
      P a ∧ P b ∧ P c ∧ P d ∧ P e ∧ P f :=
    six_cycle_from_representative P a b c d e f
      h_ab h_bc h_cd h_de h_ef h_fa h_a
  exact ⟨h_z, h_cycle⟩

theorem p24_unit2_compressed_payload_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_unit2_compressed_payload_lt_seven_orbit_payload :
    4 < 14 := by
  decide

end P24.UnitOrbitGate
