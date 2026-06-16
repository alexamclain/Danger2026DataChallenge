# Trace-Frame Schubert Packet-Norm Packaging

Date: 2026-06-05

This note specializes the decomposition-field packet-norm theorem to the
current trace-frame Schubert certificate.  It is a packaging theorem, not the
missing p-unit proof.  Its value is that it names the exact arithmetic object
that should replace the eight packetwise checks.

The determinant-line equivariance needed to construct those arithmetic
objects is isolated in:

```text
p24/trace_frame_schubert_equivariant_descent.md
p24/lean/SchubertEquivariantDescentGate.lean
```

## Fields

Keep the p24 constants:

```text
p = 10^24 + 7
m = 66254
n = 3107441
ord_m(p) = 5460
ord_n(p) = 388430
H-packet count = (n-1)/ord_n(p) = 8
```

Let:

```text
K_m = Q(mu_m)
E   = residue field of K_m at p = F_p(mu_m), [E:F_p]=5460
K_n = Q(zeta_n)
C   = <p> in (Z/nZ)^*
M   = K_n^C, [M:Q]=8.
```

Since the Frobenius class of `p` in `K_n/Q` lies in `C`, the prime `p`
splits completely in the decomposition field `M`.  Over the coefficient field
`K_m`, put:

```text
S = K_m M.
```

At the selected prime of `K_m` above `p`, the algebra `S` has eight residue
factors, each isomorphic to `E`.  These eight factors are exactly the eight
`F_p` H-packets, but with `mu_m` already adjoined.

## Schubert Factors

For one H-packet and one tensor factor after adjoining `E`, the factorized
trace-frame certificate has four named determinants:

```text
Delta_A:
  Top_1 is injective on A = W_constant + W_2 + W_157.

Delta_B:
  Top_2 is injective on B_axis = W_211.

Delta_AB:
  Top_2(B_axis) has rank 200 modulo Top_2(A),
  equivalently dim(Top_2(A) cap Top_2(B_axis)) = 10.

Delta_tail:
  the residual 10-coordinate tail is injective on
  K_2 = ker(Top_2|W_axis).
```

Write their residues in the eight H-packets as:

```text
Delta_F(a) in E,       F in {A, B, AB, tail},  a in Gal(M/Q)
```

where `a` ranges over the eight decomposition-field primes above `p`.

## Equivariance Hypothesis

The packet-norm compression is rigorous once the Schubert determinant is
constructed equivariantly over `S`.

Concretely, for each `F in {A,B,AB,tail}` we need either an algebraic element
or a determinant-line section with a fixed p-unit trivialization:

```text
Xi_F in S
```

such that, for the eight primes `P_a | p` of `S` over the fixed prime of
`K_m`, its residues are the packet determinants up to explicit p-units:

```text
Xi_F mod P_a = unit_F(a) * Delta_F(a) in E,
unit_F(a) in E^*.
```

This is the exact equivariance condition.  It says the basis choices,
normal-basis order, pivot convention, and tensor-factor representative are
defined from the cyclotomic/class-field packet algebra, not separately inside
each finite packet.

If this condition holds, then:

```text
Norm_{S/K_m}(Xi_F) mod p
  = unit_F * product_a Delta_F(a) in E,
unit_F in E^*.
```

Therefore:

```text
Norm_{S/K_m}(Xi_F) mod p != 0 in E
  => Delta_F(a) != 0 for every one of the eight H-packets.
```

Equivalently, after scalarizing to `F_p`:

```text
p does not divide Norm_{K_m/Q}(Norm_{S/K_m}(Xi_F))
  => Delta_F(a) != 0 for every H-packet.
```

## Reduction In Proof Surface

Before packet-norm packaging, the trace-frame Schubert theorem asks for:

```text
8 H-packets * 4 Schubert factors = 32 packetwise p-unit statements.
```

With the equivariant construction above, this becomes four degree-8 relative
p-unit statements over `K_m`:

```text
Xi_A, Xi_B, Xi_AB, Xi_tail are p-units.
```

With the tensor-factor rank-symmetry theorem, these four objects cover the
chosen tensor factor and hence the certificate surface already recorded in:

```text
p24/trace_frame_factorized_schubert_certificate_spec.md
p24/trace_frame_factorized_schubert_punit.md
```

Without tensor-factor symmetry, the same packet-norm compression still helps,
but it applies separately to each of the 70 scalar-extension tensor factors:

```text
4 * 70 = 280 degree-8 relative p-unit statements
```

instead of:

```text
4 * 8 * 70 = 2240 local factorwise p-unit statements.
```

## Finite Implication

The finite-field logic is:

```text
for every F:
  global product nonzero
    => no packet residue Delta_F(a) is zero;

for every packet a:
  Delta_A(a), Delta_B(a), Delta_AB(a), Delta_tail(a) all nonzero
    => Top_3,lead is injective on W_axis in that packet;

for every packet a:
  Top_3,lead injective
    => no harmful DANGER3 packet collapse.
```

The first and last steps are formal bookkeeping.  The finite implication for
the four Schubert factors is Lean-checked in:

```text
p24/lean/TraceFrameSchubertPacketNormGate.lean
```

The existing packet-global norm gate is:

```text
p24/lean/CertificateLogic.lean
```

## What Remains To Prove

This packaging does not prove that the four `Xi_F` are p-units.  The remaining
arithmetic theorem is now sharper:

```text
For the selected p24 CM trace-frame construction, the equivariant
decomposition-field Schubert elements

  Xi_A, Xi_B, Xi_AB, Xi_tail in K_m M

are integral at p and have nonzero residues under Norm_{S/K_m}.
```

The proof should use the CM/class-field origin of the trace-frame matrices:
either an explicit embedded class-field tower identity, a divisor
contradiction on the relevant modular curve/class-field packet, or a
phase-aware Borcherds/Siegel-unit construction.  A proof that only treats the
four determinants as generic random minors is not enough; the small audits
already show that component nonvanishing alone misses the cross-block
`Delta_tail` obstruction.

## Avoided False Strengthenings

The statement above avoids three stronger claims that prior toys/audits do
not support:

```text
ordinary beta norm collapse;
sparse beta interpolants for the determinant;
component nonvanishing implies residual-tail nonvanishing.
```

It also avoids requiring one rational degree-8 scalar before adjoining
`mu_m`.  The natural object is a relative degree-8 norm over `K_m`; only after
taking `Norm_{E/F_p}` do we get a single base-field scalar.
