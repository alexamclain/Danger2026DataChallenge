/-!
Finite gate for cross-orbit Kummer glue.

This file formalizes the finite part of the corrected selected-chain Kummer
target.  In a multi-orbit prime relative layer, independent Kummer orbits do
not select a child polynomial.  If the producer also supplies cross-orbit glue
which forces every orbit phase to be one global cyclic shift, then the usual
cyclic-shift invariance recovers the selected child polynomial.

No CM arithmetic is proved here.  The external producer theorem must still
construct the embedded Kummer orbits and the glue invariants.

The accounting below distinguishes five extension-field glue objects from a
conservative base-field serialization.  For p24 the 211-layer Frobenius orbit
degree is 35, so the five glue objects cost 175 base-field coordinates if the
certificate is serialized over F_p.
-/

namespace P24.KummerCrossOrbitGlueGate

def p24SqrtFloor : Nat := 1000000000000
def p24KummerNormalFormSlots : Nat := 3107811
def p24Layer211PrimitiveOrbitCount : Nat := 6
def p24Layer211GlueObjectCount : Nat :=
  p24Layer211PrimitiveOrbitCount - 1
def p24Layer211GlueOrbitDegree : Nat := 35
def p24Layer211GlueBaseSlots : Nat :=
  p24Layer211GlueObjectCount * p24Layer211GlueOrbitDegree
def p24KummerWithGlueObjectSlots : Nat :=
  p24KummerNormalFormSlots + p24Layer211GlueObjectCount
def p24KummerWithGlueBaseSlots : Nat :=
  p24KummerNormalFormSlots + p24Layer211GlueBaseSlots

theorem p24_layer211_glue_object_count :
    p24Layer211GlueObjectCount = 5 := by
  decide

theorem p24_layer211_glue_base_slots_value :
    p24Layer211GlueBaseSlots = 175 := by
  decide

theorem p24_kummer_with_glue_object_slots_value :
    p24KummerWithGlueObjectSlots = 3107816 := by
  decide

theorem p24_kummer_with_glue_base_slots_value :
    p24KummerWithGlueBaseSlots = 3107986 := by
  decide

theorem p24_kummer_with_glue_object_slots_subsqrt :
    p24KummerWithGlueObjectSlots < p24SqrtFloor := by
  decide

theorem p24_kummer_with_glue_base_slots_subsqrt :
    p24KummerWithGlueBaseSlots < p24SqrtFloor := by
  decide

def GlobalCyclicPhase {Orbit : Type}
    (r : Nat)
    (rep phase : Orbit → Nat) : Prop :=
  ∃ c, ∀ orbit, phase orbit % r = (rep orbit * c) % r

def GluePreserved {Orbit : Type}
    (r : Nat)
    (rep phase : Orbit → Nat)
    (basePhase : Nat) : Prop :=
  ∀ orbit, phase orbit % r = (rep orbit * basePhase) % r

theorem glue_preserved_implies_global_phase
    {Orbit : Type}
    (r : Nat)
    (rep phase : Orbit → Nat)
    (basePhase : Nat)
    (h_glue : GluePreserved r rep phase basePhase) :
    GlobalCyclicPhase r rep phase := by
  exact ⟨basePhase, h_glue⟩

def ChildSelectedByGlobalPhase {Orbit Child : Type}
    (r : Nat)
    (rep : Orbit → Nat)
    (decodeChild : (Orbit → Nat) → Child)
    (trueChild : Child) : Prop :=
  ∀ phase, GlobalCyclicPhase r rep phase → decodeChild phase = trueChild

theorem child_selected_from_cross_orbit_glue
    {Orbit Child : Type}
    (r : Nat)
    (rep phase : Orbit → Nat)
    (decodeChild : (Orbit → Nat) → Child)
    (trueChild : Child)
    (basePhase : Nat)
    (h_global_selects :
      ChildSelectedByGlobalPhase r rep decodeChild trueChild)
    (h_glue : GluePreserved r rep phase basePhase) :
    decodeChild phase = trueChild := by
  exact h_global_selects phase
    (glue_preserved_implies_global_phase r rep phase basePhase h_glue)

abbrev KummerWithGlueProducerContract
    (producerSound : Prop) : Prop :=
  p24KummerWithGlueBaseSlots < p24SqrtFloor ∧ producerSound

theorem kummer_with_glue_contract_from_sound
    (producerSound : Prop)
    (h_sound : producerSound) :
    KummerWithGlueProducerContract producerSound := by
  exact ⟨p24_kummer_with_glue_base_slots_subsqrt, h_sound⟩

end P24.KummerCrossOrbitGlueGate
