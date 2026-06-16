/-!
Finite handoff gate: generator-invariance of a selected kernel polynomial does
not supply the selected section/fiber.

This file records the logical distinction used by the Python guardrail.
-/

namespace P24.TraceGcdReducedAnchorKernelSectionPairingGuardrail

structure KernelGeneratorCollapse where
  fixedFiberGeneratorChoicesCollapse : Prop

structure SectionPairingInput where
  selectedFiberPairedToParentSection : Prop

structure ProducerNeeds where
  relativeClassCharacterTraces : Prop
  embeddedRelativeMorphism : Prop
  phaseAwareCMLangIdentity : Prop

def HasSectionPairing (input : SectionPairingInput) : Prop :=
  input.selectedFiberPairedToParentSection

def HasProducerRoute (needs : ProducerNeeds) : Prop :=
  needs.relativeClassCharacterTraces ∨
  needs.embeddedRelativeMorphism ∨
  needs.phaseAwareCMLangIdentity

theorem generator_collapse_needs_section_pairing
    (collapse : KernelGeneratorCollapse)
    (input : SectionPairingInput)
    (needs : ProducerNeeds)
    (h_collapse : collapse.fixedFiberGeneratorChoicesCollapse)
    (h_pairing : HasSectionPairing input)
    (h_route : HasProducerRoute needs) :
    collapse.fixedFiberGeneratorChoicesCollapse ∧
    input.selectedFiberPairedToParentSection ∧
    HasProducerRoute needs := by
  exact ⟨h_collapse, h_pairing, h_route⟩

def p24FirstLayerTotalRoots : Nat := 314
def p24FirstLayerChildSize : Nat := 157
def p24SecondLayerTotalRoots : Nat := 66254
def p24SecondLayerChildSize : Nat := 211
def p24KernelGeneratorOrbitsAfterFiberSelected : Nat := 1

theorem p24_first_layer_total_roots :
    p24FirstLayerTotalRoots = 2 * p24FirstLayerChildSize := by
  decide

theorem p24_second_layer_total_roots :
    p24SecondLayerTotalRoots = p24FirstLayerTotalRoots * p24SecondLayerChildSize := by
  decide

theorem p24_kernel_generator_orbits_after_fiber_selected :
    p24KernelGeneratorOrbitsAfterFiberSelected = 1 := by
  decide

end P24.TraceGcdReducedAnchorKernelSectionPairingGuardrail
