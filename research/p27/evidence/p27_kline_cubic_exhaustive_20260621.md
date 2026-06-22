# P27 K-Line Cubic Exhaustive Pilot

Date: 2026-06-21

## Claim

The nearest unresolved low-genus K-line subcase is negative on the small
p27-compatible guard field `q=607`.

On the balanced q607 `d3` K rows, no monic cubic

```text
f(K) = K^3 + a*K^2 + b*K + c
```

has quadratic character matching the `d3` target, even allowing global
polarity.  Since a nonzero leading coefficient only contributes a global
Legendre factor, this exhausts the degree-3 K-polynomial character shape on
this field.

This is a local falsifier and pilot, not a global p27 proof.  It says the
K-line route should continue through actual branch-class/genus extraction,
not broader blind cubic coefficient scans.

## Probe

Gate:

```text
research/p27/archive/gates/p27_kline_cubic_exhaustive_probe.c
```

Output:

```text
research/p27/archive/probe_outputs/p27_kline_cubic_exhaustive_probe_20260621.txt
```

Command:

```bash
cc -O3 -o tmp/p27_kline_cubic_exhaustive_probe \
  research/p27/archive/gates/p27_kline_cubic_exhaustive_probe.c

./tmp/p27_kline_cubic_exhaustive_probe \
  | tee research/p27/archive/probe_outputs/p27_kline_cubic_exhaustive_probe_20260621.txt
```

## Rows

The q607 pilot used 32 selected K rows with exactly balanced target signs:

```text
rows = 32
plus = 16
minus = 16
```

These rows are intentionally small-field screening data.  The promotion fields
for the K/S route remain `q=1471`, `q=1607`, and preferably `q=1847`.

## Result

The exhaustive run checked all monic cubics over `F_607`:

```text
tested_monic_cubics = 223648543
exact_cubics = 0
exact_irreducible_cubics = 0
best good=31/32 zeros=0 polarity=1 coeffs=K^3+16*K^2+234*K+378
```

There were no exact reducible or irreducible cubic character explanations.
The best cubic missed one row, which is useful only as a warning that small
samples can look close without defining a stable source.

## Interpretation

Positive:

```text
The K-line test is now exact for the nearest degree-3 character subcase on q607.
The balanced rows prevent a raw-majority explanation.
The exhaustive negative supports the existing decision to stop widening blind
coefficient scans.
```

Negative:

```text
No q607 cubic K-polynomial gives a d3 sampler.
No elliptic source of the simple shape z^2=cubic(K) is visible in this pilot.
This does not rule out a non-visible branch class or a higher-genus cover.
```

## Continue / Kill

```text
continue = normalize the actual d3 cover over P1_K and P1_Sroot
continue = compute branch degree, support field degrees, and genus
continue = compare q1471/q1607/q1847 only after a named branch class appears

kill = more blind small-coefficient K cubic scans
kill = treating near-miss 31/32 cubics as candidates without guard-field survival
```

## Linked Artifacts

- Parent packet: [P27 K/S Branch-Extraction Packet](p27_ks_branch_extraction_packet_20260621.md)
- Earlier K screen: [P27 Kummer Small-Integer Polynomial Screen](p27_kummer_small_integer_poly_screen_20260621.md)
- Branch screen: [P27 Kummer Branch-Divisor Screen](p27_kummer_branch_divisor_screen_20260621.md)
- Gate: `research/p27/archive/gates/p27_kline_cubic_exhaustive_probe.c`
- Output: `research/p27/archive/probe_outputs/p27_kline_cubic_exhaustive_probe_20260621.txt`

```text
p27_kline_cubic_exhaustive_probe_rows=1/1
```
