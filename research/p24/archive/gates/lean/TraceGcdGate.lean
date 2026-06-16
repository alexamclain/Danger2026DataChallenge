/-!
Finite gate for the linearized trace-gcd certificate.

The arithmetic input for the representative p24 row can be phrased as:

* the four full prefix trace blocks have common kernel `K` of dimension 16;
* the selected 16 tail trace coordinates have rank 16 on `K`.

Then the common zero space of the prefix and tail trace maps is zero.  In
linearized-polynomial language, the gcd degree of `P_K` with the tail maps is
zero.
-/

namespace P24.TraceGcdGate

def TraceGcdDegree (kernelDim tailRankOnKernel : Nat) : Nat :=
  kernelDim - tailRankOnKernel

def TrivialTraceGcd (kernelDim tailRankOnKernel : Nat) : Prop :=
  TraceGcdDegree kernelDim tailRankOnKernel = 0

theorem trivial_trace_gcd_from_tail_full
    (kernelDim tailRankOnKernel : Nat)
    (h_tail_full : kernelDim ≤ tailRankOnKernel) :
    TrivialTraceGcd kernelDim tailRankOnKernel := by
  simp [TrivialTraceGcd, TraceGcdDegree, Nat.sub_eq_zero_of_le h_tail_full]

theorem p24_representative_trace_gcd_zero
    (kernelDim tailRankOnKernel : Nat)
    (h_kernel : kernelDim = 16)
    (h_tail : tailRankOnKernel = 16) :
    TrivialTraceGcd kernelDim tailRankOnKernel := by
  apply trivial_trace_gcd_from_tail_full
  rw [h_kernel, h_tail]
  exact Nat.le_refl 16

def CommonZeroTrivial (commonZeroDim : Nat) : Prop :=
  commonZeroDim = 0

def SquareTailDetCertificate
    (kernelDim tailRankOnKernel : Nat) : Prop :=
  tailRankOnKernel = kernelDim

theorem trivial_trace_gcd_from_square_tail_det
    (kernelDim tailRankOnKernel : Nat)
    (h_det : SquareTailDetCertificate kernelDim tailRankOnKernel) :
    TrivialTraceGcd kernelDim tailRankOnKernel := by
  apply trivial_trace_gcd_from_tail_full
  rw [h_det]
  exact Nat.le_refl kernelDim

theorem common_zero_trivial_from_trace_gcd_degree
    (commonZeroDim kernelDim tailRankOnKernel : Nat)
    (h_common :
      commonZeroDim = TraceGcdDegree kernelDim tailRankOnKernel)
    (h_gcd : TrivialTraceGcd kernelDim tailRankOnKernel) :
    CommonZeroTrivial commonZeroDim := by
  simpa [CommonZeroTrivial, h_common] using h_gcd

end P24.TraceGcdGate
