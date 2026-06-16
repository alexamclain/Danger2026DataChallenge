/-!
Paired-kernel criterion for the fixed-frequency H-coboundary route.

The paired profile target is weaker than a full right-resolvent coboundary.
For each right H-coset, let `leakage coset` be the H-trace of the
right-resolvent packet before pairing.  The paired H-coset trace vanishes
exactly when this leakage lies in the kernel of the selected left functional.

With the p24 rho-covariance convention, this can also be stated projector by
projector: the six nontrivial anchor/projector equations are exactly the six
assertions that the selected left functional kills the corresponding leakage
projector.  Thus the remaining theorem is arithmetic kernel membership for
the trace-GCD weighted product/section, not another finite H-coset step.
-/

namespace P24.TraceGcdPairedKernelCriterionGate

def AllPairedHCosetTracesZero {Coset : Type}
    (pairedTraceZero : Coset → Prop) : Prop :=
  ∀ coset, pairedTraceZero coset

def AllLeakageInLeftKernel {Coset : Type}
    (leakageInKernel : Coset → Prop) : Prop :=
  ∀ coset, leakageInKernel coset

theorem paired_hcoset_zero_iff_leakage_kernel
    {Coset : Type}
    (pairedTraceZero leakageInKernel : Coset → Prop)
    (h_to_kernel : ∀ coset, pairedTraceZero coset → leakageInKernel coset)
    (h_from_kernel : ∀ coset, leakageInKernel coset → pairedTraceZero coset) :
    AllPairedHCosetTracesZero pairedTraceZero ↔
      AllLeakageInLeftKernel leakageInKernel := by
  constructor
  · intro h_zero coset
    exact h_to_kernel coset (h_zero coset)
  · intro h_kernel coset
    exact h_from_kernel coset (h_kernel coset)

def AllPairedProjectorsZero {Character : Type}
    (pairedProjectorZero : Character → Prop) : Prop :=
  ∀ character, pairedProjectorZero character

def AllProjectedLeakageInLeftKernel {Character : Type}
    (projectedLeakageInKernel : Character → Prop) : Prop :=
  ∀ character, projectedLeakageInKernel character

theorem paired_projectors_zero_from_projected_kernel
    {Character : Type}
    (pairedProjectorZero projectedLeakageInKernel : Character → Prop)
    (h_from_kernel :
      ∀ character,
        projectedLeakageInKernel character → pairedProjectorZero character)
    (h_kernel : AllProjectedLeakageInLeftKernel projectedLeakageInKernel) :
    AllPairedProjectorsZero pairedProjectorZero := by
  intro character
  exact h_from_kernel character (h_kernel character)

theorem projected_kernel_from_paired_projectors_zero
    {Character : Type}
    (pairedProjectorZero projectedLeakageInKernel : Character → Prop)
    (h_to_kernel :
      ∀ character,
        pairedProjectorZero character → projectedLeakageInKernel character)
    (h_zero : AllPairedProjectorsZero pairedProjectorZero) :
    AllProjectedLeakageInLeftKernel projectedLeakageInKernel := by
  intro character
  exact h_to_kernel character (h_zero character)

def p24NontrivialOrder7Characters : Nat := 6
def p24RightHCosets : Nat := 7
def p24LeftRows : Nat := 156
def p24PairedKernelProjectorEquations : Nat :=
  p24NontrivialOrder7Characters
def p24HCosetScalarVerifierEquations : Nat :=
  p24RightHCosets * p24LeftRows

theorem p24_paired_kernel_projector_count :
    p24PairedKernelProjectorEquations = 6 := by
  decide

theorem p24_hcoset_scalar_verifier_count :
    p24HCosetScalarVerifierEquations = 1092 := by
  decide

theorem p24_paired_kernel_projectors_are_smaller_interface :
    p24PairedKernelProjectorEquations < p24HCosetScalarVerifierEquations := by
  decide

end P24.TraceGcdPairedKernelCriterionGate
