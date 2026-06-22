# P27 K-Line Quartic GPU Test Card

Date: 2026-06-22

## Claim

The signed-doubling `E'` quotient gave a second bounded math test: exact monic
quartic support on the Kummer line

```text
K = x([2]P) = (U^2 - 4)^2 / (4U(U^2 + 4))
chi(K^4 + aK^3 + bK^2 + cK + d).
```

This was a genus-1 source test, not a production search.  The decisive q1847
`d3_on_K` screen is now complete and negative:
[P27 Full Quartic q1847 D3 Screen](p27_full_quartic_q1847_d3_screen_20260622.md).

```text
q1847 d3_on_K:
  triples_scanned = 6300872423
  exact_quartics = 0
```

Degree `<=2` support was already killed, the q1471 monic cubic promotion
screen found no exact d3 cubic, and q1847 now kills the visible monic quartic
d3 promotion path.  The K-line remains useful as a branch-class/genus
extraction coordinate, not via this simple quartic source shape.

Bridge update: [P27 B-Line / K-Line Bridge](p27_b_kline_bridge_20260622.md)
shows that the signed-doubling K-line and B-line target rows are the same
descended d3/d4 classes under
`K^2=(B-2)^4/(8B(B+2)^2)`.  Treat this as a coordinate alternative to the
B-line quartic screen, not independent confirmation.

## Why This Was GPU-Worthy

The search size is too large for local Python but natural for the same
bitset/intersection compiled-or-GPU pattern as the B-line quartic test:

```text
q1471: q^3 = 3,183,010,111 coefficient triples
q1607: q^3 = 4,150,168,943 coefficient triples
q1847: q^3 = 6,300,985,823 coefficient triples
```

Each triple fixes `(a,b,c)` and intersects allowed constant terms `d` over the
frozen K rows.

## Targets

Primary:

```text
d3_on_K
  q1471: rows=50 plus=28 minus=22
  q1607: rows=49 plus=28 minus=21
  q1847: rows=63 plus=45 minus=18
```

Secondary:

```text
d4_on_K_after_d3
  q1471: rows=28 plus=14 minus=14
  q1607: rows=28 plus=19 minus=9
  q1847: rows=45 plus=19 minus=26
```

Do not promote q1471/q1607 d4 quartics by themselves: the row counts are too
small, and exact quartics are expected by interpolation.

## Expected Random Counts

Random-sign model:

```text
expected exact monic quartics ~= 2*q^4 / 2^rows
```

For `d3_on_K`:

```text
q1471: expected ~= 8.32e-3
q1607: expected ~= 2.37e-2
q1847: expected ~= 2.52e-6
```

For `d4_on_K_after_d3`:

```text
q1471: expected ~= 3.49e4
q1607: expected ~= 4.97e4
q1847: expected ~= 6.62e-1
```

Thus the decisive test was d3 stability across the promotion fields, especially
q1847.  A q1847 d3 quartic would have been highly non-random; the full q1847
screen found none.

## Artifacts

Frozen target packet:

```text
research/p27/archive/fixtures/p27_kline_quartic_targets_20260622.json
```

Packet generator:

```text
research/p27/archive/gates/p27_kline_quartic_target_packet.py
```

Hit verifier:

```text
research/p27/archive/gates/p27_kline_quartic_verify.py
```

CPU reference chunk runner:

```text
research/p27/archive/gates/p27_kline_quartic_chunk_probe.py
```

Smoke output:

```text
research/p27/archive/probe_outputs/p27_kline_quartic_chunk_probe_q1471_d3_start0_count2000_20260622.txt
```

## Commands

Generate packet:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_kline_quartic_target_packet.py \
  --small-primes 1471,1607,1847 \
  --families d3_on_K,d4_on_K_after_d3 \
  > research/p27/archive/fixtures/p27_kline_quartic_targets_20260622.json
```

List target rows:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_quartic_verify.py \
  --list-targets
```

Reference chunk:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_quartic_chunk_probe.py \
  --field 1471 \
  --family d3_on_K \
  --start 0 \
  --count 2000 \
  | tee research/p27/archive/probe_outputs/p27_kline_quartic_chunk_probe_q1471_d3_start0_count2000_20260622.txt
```

Hit verifier:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_quartic_verify.py \
  --field <q> \
  --family <family> \
  --coeffs <a,b,c,d> \
  --polarity <1-or--1>
```

Flattened chunk convention:

```text
index = (a*q + b)*q + c
a = index // q^2
b = (index % q^2) // q
c = index % q
```

## Smoke Result

The local reference smoke scanned the first `2000` q1471 `d3_on_K` triples:

```text
field = 1471
family = d3_on_K
start = 0
triples_scanned = 2000
exact_quartics = 0
```

That was only an implementation sanity check.  The later full q1847 C-oracle
screen is the substantive negative evidence against the K-line d3 quartic
family.

Follow-up:
[P27 K-Line Even-Quartic Screen](p27_kline_even_quartic_screen_20260622.md)
exhausts the descended subfamily
`chi(K^4+a*K^2+b)` locally over q1471/q1607/q1847.  It finds zero exact hits
for both `d3_on_K` and `d4_on_K_after_d3`.  Therefore the cheap `K^2`-only
subfamily was correctly skipped; any useful K-line quartic hit would have had
to use odd powers of `K` and the signed K sheet.

[P27 K-Line Belyi-Reciprocal Quartic Screen](p27_kline_reciprocal_quartic_screen_20260622.md)
also exhausts the small subfamilies preserved by the visible Belyi
involution `K -> 4/K`:
`K^4+aK^3+bK^2+4aK+16` and `K^4+aK^3-4aK-16`.
It likewise finds zero exact hits over q1471/q1607/q1847.  The full q1847
screen was therefore the right decisive test, not a Belyi-reciprocal-only
proxy.

## Run Order

Original run order and current status:

```text
1. q1471 d3_on_K
   Purpose: implementation smoke and comparison with the killed q1471 cubic.
   Status: optional closure bookkeeping.

2. q1607 d3_on_K
   Purpose: second promotion-field guard.
   Status: optional closure bookkeeping.

3. q1847 d3_on_K
   Purpose: decisive low-random-expectation guard.
   Status: complete, exact_quartics = 0.

4. q1847 d4_on_K_after_d3
   Purpose: optional recurrence clue only if d3 has a candidate, or if runtime
   is already paid.
   Status: optional closure; not a d3 promotion path.
```

## Promotion / Kill

Promote:

```text
d3_on_K exact quartic in q1847 plus at least one of q1471/q1607
or a named quartic class that survives all three q1471/q1607/q1847 fields
```

Promotion artifact:

```text
construct z^2=f(K)
compute genus/sourceability and relation to the signed-doubling quotient
compare/pull back against the B-line coordinate via
  K^2=(B-2)^4/(8B(B+2)^2)
compare against d4_on_K_after_d3 if d3 is tractable
```

Kill:

```text
no exact d3_on_K quartic in decisive q1847
```

This closes the visible degree-4 K-polynomial d3 source shape.  The remaining
K-line route is non-polynomial branch-class extraction or offline normalization
of the reverse-source cover over `P1_K`.

```text
p27_kline_quartic_gpu_test_card_rows=1/1
```
