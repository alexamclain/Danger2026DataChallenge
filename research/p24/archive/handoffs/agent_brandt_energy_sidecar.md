# Agent Brandt Energy Sidecar

Sidecar question: can the relative autocorrelation

```text
C_d = sum_i j_i * j_{i+m*d}
```

for the p24 third target be computed by a Brandt/Hecke trace, modular
polynomial resultant, or low-dimensional transfer operator without carrying
the full recovery subgroup?

## Setup

Use the cyclic CM class cycle

```text
G = <g>,        |G| = h = m*n
H = <g^m>,      |H| = n
j_i = j(g^i a_0).
```

For the third p24 target:

```text
m = 66254
n = 3107441
relative oriented move a = 2 * 463 * 223^(-1)
```

The relative energy certificate wants Fourier coefficients of the length-`n`
sequence `C_d`.

## Exact Brandt/Hecke Identity

Let `J = diag(j_0,...,j_{h-1})`, and let `P_t` be the permutation matrix for
the oriented class action `i -> i+t`.  Then the exact identity is

```text
C_d = Tr(J * P_{m*d} * J * P_{-m*d}).
```

If an unoriented split-prime packet is

```text
B_t = P_t + P_{-t},
```

and `2t != 0` in the class group, then

```text
Tr(J * B_t * J * B_t) = 2*C_t.
```

More generally, for a Hecke packet

```text
B = sum_t c_t P_t,        B* = sum_t c_t P_{-t},
```

one gets

```text
Tr(J * B * J * B*) = sum_t c_t^2 C_t.
```

So the matrix trace identity is real, but it computes a weighted Hecke packet
unless the operator already contains the desired oriented class element as a
singleton.  Supplying that singleton is exactly the relative class-action
projector.

## Modular Polynomial Resultant Boundary

A modular-polynomial resultant such as

```text
prod_{Phi_N(x,y)=0, H_D(x)=H_D(y)=0} (T - x*y)
```

has first symmetric coefficient equal to the corresponding Hecke packet sum
over CM pairs.  For a split prime whose two horizontal classes are `+t` and
`-t`, this gives `2*C_t`.

For the p24 oriented move `2*463*223^(-1)`, the scalar modular correspondence
at level `N = 2*463*223` does not remember the sign choice at `223`; it sees
the packet of local orientation choices.  Adding enough level/orientation data
to isolate `+2,+463,-223` is no longer a plain resultant shortcut; it is an
oriented class projector or a high-degree level-structure computation.

## Transfer Operator Boundary

The relative Fourier transform is

```text
E_a = sum_d zeta_n^(a*d) C_d
    = sum_u P_u(a) * P_u(-a).
```

Over a field containing `mu_n`, the minimal exact linear recurrence/transfer
dimension for the periodic sequence `C_d` is the number of nonzero Fourier
modes `E_a`.  Thus a low-dimensional transfer operator would require sparse
relative energy spectrum.

The small CM data shows the opposite.  I added the bounded probe

```text
p24/agent_brandt_energy_probe.py
```

and ran it on the existing `D=-5000` calibration:

```text
D=-5000, q=3851, class_number=30
quotient_m=6, recovery_n=5

C_1=3269
trace_D_P1_D_Pminus1=3269
trace_identity_ok=1
trace_D_B1_D_B1=2687
unoriented_hecke_equals_2C1=1

C_d_for_shifts_m_d=[607, 2114, 191, 191, 2114]
bm_complexity=5
dft_support=5
full_bm=1
full_dft_support=1
```

I also reran the existing broader toy scan:

```text
python3 p24/relative_autocorrelation_complexity_scan.py \
  --max-cases 20 --min-h 12 --max-h 96 --max-abs-D 12000 \
  --max-quotients 5 --q-stop 180000 --summary-only
```

It reported:

```text
rows=42
full_or_near_full_bm_rows=42
low_bm_rows=0
dft_rows=42
full_dft_support_rows=42
total_energy_zeros=0
```

## Conclusion

Exact identity viable:

```text
C_d = Tr(J * P_{m*d} * J * P_{-m*d}).
```

But this is not a p24 shortcut by itself.  Ordinary Brandt/Hecke matrices and
plain modular resultants compute norm/orientation packets, not the specific
relative class `2*463*223^(-1)`.  Once the oriented permutation or projector is
available, the trace formula is just bookkeeping on the full CM torsor or the
full recovery subgroup.

The transfer-operator route would need a theorem forcing the `C_d` spectrum to
have support far below `n`.  In all tested natural CM examples, the relative
autocorrelation has full Fourier support and full or near-full recurrence
complexity.  For the third p24 target, the present boundary is therefore:

```text
any Brandt/Hecke/resultant/transfer formula must still supply the
order-3107441 relative projector, or it has not avoided the n-shift support.
```
