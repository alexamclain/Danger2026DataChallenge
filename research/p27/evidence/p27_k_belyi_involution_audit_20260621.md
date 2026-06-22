# P27 K/S Belyi Involution Audit

Date: 2026-06-21

## Claim

The visible Belyi involutions on the K/S quotient do not give a stable p27
source quotient or sampler for the decisive `d3` bit.

The K-line branch set is preserved by the base-field-visible involutions:

```text
K -> -K
K -> 4/K
K -> -4/K
```

and on the rational square-root coordinate `Sroot^2=K` by:

```text
Sroot -> -Sroot
Sroot -> 2/Sroot
Sroot -> -2/Sroot
```

The only universally closed symmetry on the selected rows is
`Sroot -> -Sroot`, which was already known and pair-even.  The potentially
new shortcut `K -> 4/K` is not stable across guard fields: it is closed in
some small fields, anti-invariant or invariant depending on the field, and
completely absent in the promotion fields `q=1607` and `q=1847`.

Thus the Belyi involution route is killed as a sqrt-beating quotient shortcut.
The K/S route, if alive, still requires actual branch-class/genus extraction.

## Probe

Gate:

```text
research/p27/archive/gates/p27_k_belyi_involution_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_k_belyi_involution_probe_20260621.txt
research/p27/archive/probe_outputs/p27_k_belyi_involution_probe_extended_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_k_belyi_involution_probe.py \
  --small-primes 1471,1607,1847 \
  | tee research/p27/archive/probe_outputs/p27_k_belyi_involution_probe_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_k_belyi_involution_probe.py \
  --small-primes 607,863,991,1087,1471,1607,1847,1951,1999,2039 \
  | tee research/p27/archive/probe_outputs/p27_k_belyi_involution_probe_extended_20260621.txt
```

## Main Guard Fields

For `d3` on the K-line:

```text
q=1471:
  K rows = 50
  4/K present = 49
  4/K same target = 49
  4/K missing = 1

q=1607:
  K rows = 49
  4/K present = 0
  4/K missing = 49

q=1847:
  K rows = 63
  4/K present = 0
  4/K missing = 63
```

For `d4`, `q=1471` has a clean anti-invariant `4/K` local pattern, while
`q=1607` and `q=1847` again have no `4/K` closure.  Since `d4` is only a
follow-up after `d3`, this reinforces that the q1471 pattern is local rather
than a source route.

## Extended Fields

The extended audit shows why this cannot be promoted:

```text
q=607:  d3 4/K present 32/32, opposite 32/32
q=863:  d3 4/K present 22/24, opposite 22/22
q=991:  d3 4/K present 36/36, opposite 36/36
q=1087: d3 4/K present 17/18, same 17/17
q=1471: d3 4/K present 49/50, same 49/49
q=1607: d3 4/K present 0/49
q=1847: d3 4/K present 0/63
q=1951: d3 4/K present 40/40, opposite 40/40
q=1999: d3 4/K present 0/67
q=2039: d3 4/K present 0/51
```

There is no stable invariant or anti-invariant law across the promotion
fields.  The local closures are field accidents in the selected finite model.

## Online Magma Check

Fixture:

```text
research/p27/archive/fixtures/p27_k_belyi_involution_q607_q1607_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_k_belyi_involution_q607_q1607_magma_20260621.txt
research/p27/archive/probe_outputs/p27_k_belyi_involution_q607_q1607_magma_20260621.html
```

The online Magma calculator independently validated the sharp contrast between
the tempting q607 artifact and the q1607 promotion-field failure:

```text
RESULT p27_k_belyi_involution ok 607 32 32 0 32 0 1607 49 0 0 0 49
```

This means:

```text
q=607:  rows=32,  4/K present=32, same=0, opposite=32, missing=0
q=1607: rows=49,  4/K present=0,  same=0, opposite=0,  missing=49
```

Follow-up:
[P27 K-Line Belyi-Reciprocal Quartic Screen](p27_kline_reciprocal_quartic_screen_20260622.md)
tests the nearest quartic family whose branch divisor is preserved by
`K -> 4/K`.  Both reciprocal signs,
`K^4+aK^3+bK^2+4aK+16` and `K^4+aK^3+bK^2-4aK-16`, have zero exact hits over
q1471/q1607/q1847 for `d3_on_K` and `d4_on_K_after_d3`.  So the involution is
not merely missing as an orbit quotient; it also does not supply the natural
Belyi-reciprocal quartic source.

## Interpretation

Positive:

```text
The K/S Belyi involution shortcut is now explicitly priced.
The q607/q1471-looking symmetries are not being silently ignored.
The online Magma workflow validates the finite-field orbit calculation.
```

Negative:

```text
No stable K -> 4/K quotient explains d3.
No Sroot -> +/-2/Sroot quotient gives a rational selected-row sampler.
The Belyi automorphism group does not produce a smaller sqrt-beating source.
```

## Continue / Kill

```text
continue = normalize the actual d3 branch class over P1_K and P1_Sroot
continue = use Belyi branch values only as marked points in that extraction
continue = promote only genus <=1, a recurrence, or a cheap direct sampler

kill = K -> 4/K or Sroot -> 2/Sroot as a p27 quotient shortcut
kill = promoting q607/q1471 local orbit closure without q1607/q1847 survival
kill = Belyi-involution GPU sampler
```

## Linked Artifacts

- Parent packet: [P27 K/S Branch-Extraction Packet](p27_ks_branch_extraction_packet_20260621.md)
- Belyi structure: [P27 Kummer Belyi Structure Probe](p27_kummer_belyi_structure_probe_20260621.md)
- Lambda obstruction: [P27 Lambda Rational-Quotient Obstruction](p27_lambda_rational_quotient_obstruction_20260621.md)
- Gate: `research/p27/archive/gates/p27_k_belyi_involution_probe.py`
- Magma fixture: `research/p27/archive/fixtures/p27_k_belyi_involution_q607_q1607_magma.m`

```text
p27_k_belyi_involution_probe_rows=1/1
```
