# Packet Rank Sidecar

Question: can the selected-prime Hermitian or `L1` packet nonvanishing theorem
be reframed as a determinant/rank/reduced-normality identity over the packet
field, plausibly provable by finite-field linear algebra plus CM constraints?

## Verdict

There are clean rank/determinant reformulations, but they are not equivalent
to the selected scalar nonvanishing needed for p24.

The useful reformulations are:

1. Coordinate/resultant normality:

   ```text
   Res(Phi_n, J_u) != 0
   ```

   is exactly nonvanishing of the `u`-th coordinate in every primitive
   relative packet.  For prime `n`, this is the augmentation/cyclotomic part
   of the length-`n` circulant determinant.  It is a genuine reduced-normality
   determinant and is already the cleanest rank theorem candidate.

2. Translate-rank packaging:

   after fixing a packet factor `f | Phi_n`, put

   ```text
   A = F_q[X]/(f),     y_u = J_u mod f.
   ```

   The full `K`-translate autocorrelation or `L1`-translate sequence has a
   circulant/group-determinant rank controlled by the nonzero `K`-Fourier
   components of `y` on the relevant support.

   For `L1`, the support has size

   ```text
   1 + 1 + 156 + 210 = 368.
   ```

   Thus the natural rank theorem is:

   ```text
   For every H-packet f and every K-character chi in the L1 axis support,
   the mixed CM resolvent R_{chi,a} is nonzero mod the selected prime.
   ```

   Equivalently, the `K`-translate span of the `L1` packet has rank `368`
   over the packet field.

This `L1` rank theorem would prove that the entire `K`-translate family is not
identically zero.  It still would not prove that the selected origin value
`L1_0` is nonzero: a nonzero 368-frequency cyclic-code word can vanish at a
specified coordinate by ordinary finite-field cancellation.

## Hermitian Obstruction

For a packet factor stable under inversion, the Hermitian scalar has the form

```text
H_f(y) = sum_u X^c(u) y_u y_{u*}
```

over the packet field `A`, with involution `X -> X^-1`.  In p24 this is a
Hermitian form over

```text
F_{Q^2}/F_Q,     Q = p^194215,
```

on a vector space of dimension

```text
m = 66254.
```

Finite-field Hermitian spaces of dimension at least `2` have many isotropic
vectors.  Therefore:

```text
y != 0, or even high/full reduced-normality rank of y,
does not formally imply H_f(y) != 0.
```

The existing toy

```text
p24/energy_isotropy_obstruction_toy.py
```

exhibits this directly over `F_1259[X]/(X^2 + 36X + 1)`: a nonzero content
vector has zero Hermitian/energy scalar.

So the Hermitian theorem cannot be reduced to packet-field linear algebra
unless the CM constraints cut the actual packet vector into an anisotropic
subvariety.  No current note gives such a constraint.  Characteristic-zero
principal dominance proves positivity before reduction, but the selected
prime p-unit issue remains.

## L1 Obstruction

`L1` is a linear functional on the packet vector after choosing a `K` origin.
Rank packaging can use all `K` translates, but selected nonvanishing is still
the assertion that one coordinate of that translate sequence is nonzero.

Finite-field linear algebra alone cannot prove this from translate rank:

```text
full rank on the 368 supported K-characters
  => translate sequence is not identically zero;

selected-origin p-unitness
  => a specified coordinate of that sequence is nonzero.
```

The second statement is a hyperplane-avoidance theorem for the specific CM
packet, not a determinant identity.  The interpolation boundary already shows
that the `L1` packet norm looks generic after the known `H`-periodicity, not
like a low-degree function of the selected `j` root.

## Sharp Candidate

The most honest theorem candidate is therefore two-stage.

First, prove a reduced-normality/rank statement:

```text
For each p24 H-packet f and each K-character chi in the L1 axis support,

R_{chi,f}
  = sum_{u,k} chi(u) zeta_n^k j_{u+m k}

is nonzero modulo the selected split prime.
```

Equivalently, the `K`-translate span of the `L1` packet has rank `368`.

Second, prove the extra selected-coordinate avoidance:

```text
sum_{chi in axis support} widehat(w)(chi) R_{chi,f} != 0
```

at the selected `K` origin.

The first part is a determinant/rank theorem.  The second part is not; it is
the remaining selected-origin p-unit theorem.

For Hermitian energy, the analogous rank theorem is full nonvanishing of the
Fourier components of the autocorrelation packet.  It is stronger than exact
content but still does not imply the identity coefficient `H_f(y) != 0`.

## Cheap Distinguishing Scan

Add a lightweight diagnostic to `hermitian_selected_prime_zero_scan.py` or a
new toy script:

```text
for each small CM packet (D,q,h,m,n,f):
  y = (J_0 mod f, ..., J_{m-1} mod f) in A^m
  scalar_zero = (Hermitian(y) == 0)
  coord_zero_count = #{u : y_u == 0}
  coeff_rank = rank_Fq(coefficients of y_u in A)
  translate_rank = rank of the K-autocorrelation or L1-translate circulant

  compare with random isotropic controls in the same (q, deg f, m)
```

Decision rule:

```text
random isotropy:
  scalar_zero occurs with full/near-full coeff_rank and translate_rank;

structured rank failure:
  scalar_zero is accompanied by coordinate zeros, low coeff_rank,
  dropped translate rank, or repeated character-support defects.
```

This scan is cheap because it reuses existing packet rows and only adds
Gaussian elimination over `F_q` plus small random controls.  It would not prove
p24, but it would separate a true reduced-normality mechanism from ordinary
finite-field isotropy.

## Tiny Checks Run

Existing quick checks were consistent with the obstruction:

```text
energy_isotropy_obstruction_toy.py:
  content_certificate_nonzero=1
  hermitian_energy=0

relative_circulant_rank_scan.py small window:
  fiber_rows=129
  rank_defects=0
  primitive_zero_fibers=0

hermitian_selected_prime_zero_scan.py small window:
  packet_rows=10
  selected_embedding_zeros=0

l1_selected_origin_zero_scan.py small window:
  l1_rows=14
  l1_selected_origin_zeros=0
```

These are sanity checks only.  They support the current hierarchy:
rank/resultant normality is a good structural diagnostic, while selected
Hermitian or `L1` nonvanishing still needs a selected-prime CM p-unit input.
