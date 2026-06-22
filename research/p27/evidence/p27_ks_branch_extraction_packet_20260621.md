# P27 K/S Branch-Extraction Packet

Date: 2026-06-21

## Claim

The visible K-line and S-root searches are now closed enough that the next
credible sqrt-beating test is not another coefficient scan.  The remaining
K/S route is an actual function-field extraction:

```text
recover the d3 branch class over P1_K or P1_Sroot
compute branch degree / support degrees / genus
decompose under Sroot -> -Sroot
carry the order-4 H90 action if feasible
```

This packet packages the exact equations and the acceptance test for that CAS
pass.

## Artifact

Generator:

```text
research/p27/archive/gates/p27_ks_branch_extraction_packet.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_ks_branch_extraction_packet_20260621.txt
```

Online Magma sanity fixture:

```text
research/p27/archive/fixtures/p27_ks_branch_sanity_q1471_magma.m
```

Online Magma output:

```text
research/p27/archive/probe_outputs/p27_ks_branch_sanity_q1471_magma_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_ks_branch_extraction_packet.py \
  > research/p27/archive/probe_outputs/p27_ks_branch_extraction_packet_20260621.txt
```

## Decisive Equations

The packet uses:

```text
E: W^2 = X^3 - X
U = X - 1/X
V = W*(X^2+1)/X^2
K = x([2]P) = (X^2 - 2X - 1)^2*(X^2 + 2X - 1)^2
               / (4*X*(X - 1)*(X + 1)*(X^2 + 1)^2)
Sroot = (U^2 - 4)/(2V)
K = Sroot^2
```

Symbolic checks in the packet:

```text
Sroot_square_check_mod_E = 0
Sroot_branch_resultant =
  const*Sroot^8*(Sroot^2 - 2*Sroot + 2)^4*(Sroot^2 + 2*Sroot + 2)^4
K_branch_resultant =
  const*K^4*(K^2 + 4)^4
```

The packet also carries the label-2 H90/order-4 identities:

```text
Salpha^2 = X*L
m0^2 - mt^2*T2 = 4*T2*Salpha^2
alpha: T -> -T, R -> R*(m0 - mt*T)/(2*T*Salpha)
alpha^2 = R-deck involution
```

## Online Magma Sanity Check

The Magma fixture is a small algebraic sanity validation, not the full
normalization and not a promotion-field test.  The later guard-field signature
audit demotes q1471 for 2-adic-sensitive K/S positives.  This fixture was
submitted to the online Magma calculator and emitted:

```text
RESULT p27_ks_branch_sanity_q1471 ok 1468 0 0 0 0 0 -1
```

This checks, over `q=1471`, zero mismatches for:

```text
Sroot^2 = K
K*K_den = K_num
2*Sroot*W*(X^2+1) = Sroot_num
Salpha^2 = X*L
m0^2 - mt^2*T2 = 4*T2*Salpha^2
chi(-1) = -1
```

## Why This Is The Right Next Test

Already killed:

```text
K degree 1/2 polynomial characters
small-integer K degree 3/4 coefficient scans
split K branch divisors of degree <=4
split Sroot branch divisors of degree <=4
visible Sroot odd classes in the p27 sign regime
```

The S-root parity reduction says visible even Sroot classes reduce to K, and
visible odd Sroot classes flip on `Sroot/-Sroot` pairs while the target does
not.  So a win must come from the actual non-visible branch class, quotient,
or recurrence, not from more visible branch atoms.

## Promotion Bar

Promote only if the CAS extraction finds one of:

```text
stable branch class over p27-signature fields q = 7 mod 16
first promotion set: q=1607, q=1847, q=2087
genus <= 1
named recurrence or sourceable walk
cheap character/source sampler that avoids a fresh Legendre toll
```

## Kill Condition

Kill the K/S branch route if:

```text
the normalized branch degree is high/generic
only the visible K/S branch atoms appear
d4 is an unrelated fresh half-cover
only small-field local interpolation survives
```

## Continue / Kill

```text
continue = Magma/Sage normalization over P1_K and P1_Sroot in q = 7 mod 16 fields
continue = Sroot -> -Sroot decomposition of the recovered class
continue = alpha-equivariant quotient/Prym extraction if the model is tractable

kill = broader visible K/S coefficient scans
kill = odd Sroot semi-invariant classes
kill = GPU production work until this yields a direct sampler or cheap test
```

## Linked Artifacts

- Parent: [P27 Kummer Branch-Extraction Handoff](p27_kummer_branch_extraction_handoff_20260621.md)
- S parity: [P27 S-Root Parity Reduction](p27_sroot_parity_reduction_20260621.md)
- H90 lift: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Generator: `research/p27/archive/gates/p27_ks_branch_extraction_packet.py`
- Output: `research/p27/archive/probe_outputs/p27_ks_branch_extraction_packet_20260621.txt`
- Magma fixture: `research/p27/archive/fixtures/p27_ks_branch_sanity_q1471_magma.m`
- Magma output: `research/p27/archive/probe_outputs/p27_ks_branch_sanity_q1471_magma_20260621.txt`

```text
p27_ks_branch_extraction_packet_rows=1/1
```
