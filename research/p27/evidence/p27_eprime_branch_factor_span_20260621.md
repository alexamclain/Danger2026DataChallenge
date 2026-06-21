# P27 E-Prime Branch-Factor Span

Date: 2026-06-21

## Claim

The p26 visible branch/H90 packet does not transfer to a p27 source law for
the descended d3 or d4 bits on

```text
E': V^2 = U^3 + 4U.
```

This was the closest exact test suggested by the p26 genus-4 breadcrumb:
after quotienting by `(0,0)`, the p26 first-w cover looked like a branch-degree
6 double cover over `E'`.  For p27, sparse products of the corresponding
visible branch factors and nearby tangent/vertical factors do not give an
exact source, and their apparent p27 lifts do not replicate on fresh 20k
validation seeds.

## Probe

Sparse exact span command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_branch_factor_span_probe.py \
  --target 2000 \
  --heldout-target 2000 \
  --max-draws 500000 \
  --small-primes 1471,1607,1847 \
  --max-size 4 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_eprime_branch_factor_span_probe_20260621.txt
```

The feature packet contains:

```text
U, V, U +/- 1, U +/- 2, U +/- 4
U^2 +/- 1, U^2 +/- 4, U^2 +/- 2U + 4
V + aU + b for a,b in {-4,-2,-1,0,1,2,4}
(U+2)(U^2+4), tangent-pair packets, and p26 branch-packet products
```

The screen tests every sparse product of size `1..4`, i.e. `489405` products
per family after duplicate signatures are removed.  Exact promotion requires
zero-free agreement on all rows, up to global polarity.

Targeted fresh validation command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -u - <<'PY' \
  | tee research/p27/archive/probe_outputs/p27_eprime_branch_factor_candidate_20k_20260621.txt
...
PY
```

The validation re-evaluated the best p27 branch products on two fresh 20k-row
p27 seeds, without reusing the 2k train/heldout split.

## P27 Result

On the 2k train split:

```text
d3 rows = 2000
d3 exact sparse products = 0
d3 train best = 1130/2000 = 0.565000000
d3 heldout best from train-best list = 1038/2000 = 0.519000000

d4 rows = 992
d4 exact sparse products = 0
d4 train best = 574/992 = 0.578629032
d4 heldout best from train-best list = 592/1052 = 0.562737643
```

The d4 heldout lift was worth a larger check.  On two fresh 20k-row p27 seeds,
the apparent branch product collapsed:

```text
candidate = (V-4U+1)(V-U)(V+U)(V+4U-1)

seed 20260623:
  d4 = 5100/10122 = 0.503852993

seed 20260624:
  d4 = 5076/10056 = 0.504773270
```

The p26 branch packet itself is exactly flat in both fresh validations:

```text
p26_branch_packet_minus:
  seed 20260623 d3 = 10000/20000, d4 = 5061/10122
  seed 20260624 d3 = 10000/20000, d4 = 5028/10056
```

## Guard Fields

No exact sparse product appears over the non-degenerate guard fields:

```text
q1471: d3 exact = 0, d4 exact = 0
q1607: d3 exact = 0, d4 exact = 0
q1847: d3 exact = 0, d4 exact = 0
```

Small-field in-sample best rates can look high because the row counts are
small:

```text
q1471 d4 best = 46/54 usable rows, with 2 zeros
q1607 d4 best = 46/56
q1847 d4 best = 66/90
```

These do not promote: none is exact, and the p27 20k validations flatten the
best p27 candidates.

## Interpretation

Positive:

```text
The p26 genus-4/branch-degree-6 clue produced a concrete p27 transfer test.
The test is exact over the named sparse branch-factor packet, not a random fit.
The best p27-looking product was stress-tested on fresh larger samples.
```

Negative:

```text
No sparse product of size <= 4 from the visible E' branch/H90 packet explains d3 or d4.
The p26 branch packet is flat on p27.
The apparent 2k d4 lift does not replicate at 20k scale.
No guard field has an exact sparse product.
```

Thus the remaining `E'` route is not the visible branch-factor packet.  A
sqrt-beating advance now needs actual cover/divisor-class extraction on `E'`,
not another sparse product of the p26-visible factors.

## Continue / Kill

```text
continue = exact E' function-field / divisor-class extraction
continue = online Magma validation for a named cover/function, once derived
continue = exact finite-field solver for divisor classes beyond visible sparse factors

kill = p26 visible branch/H90 packet as a p27 d3/d4 source
kill = GPU sampler from the tested branch-factor products
kill = promoting small-field high in-sample branch scores without exactness
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_eprime_branch_factor_span_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_eprime_branch_factor_span_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_eprime_branch_factor_candidate_20k_20260621.txt`
- Parent: [P27 E-Quotient Kernel-8 / 2-Isogeny Screen](p27_equotient_kernel8_2isogeny_screen_20260621.md)
- Related: [P27 E-Prime Low-Pole Random Screen](p27_eprime_lowpole_random_screen_20260621.md)
- Related: [P27 E-Prime Affine-Walk Recurrence](p27_eprime_affine_walk_recurrence_20260621.md)

```text
p27_eprime_branch_factor_span_rows=1/1
```
