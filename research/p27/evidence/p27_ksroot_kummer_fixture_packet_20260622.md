# P27 K/Sroot Kummer Fixture Packet

Date: 2026-06-22

## Claim

The K/Sroot lane now has compact guard-field fixtures for the actual
conditional branch classes on both the rational K coordinate and the signed
Sroot sheet:

```text
f3(K), f4(K), ...
f3(Sroot), f4(Sroot), ...
Sroot^2 = K
```

This is the concrete CAS/expert input for normalized branch-class extraction.
It also makes the key constraint explicit: Sroot is useful for parity and
normalization, but any proposed source must preserve the rational K-square
stratum rather than winning only after K is forgotten.

## Artifacts

Generator:

```text
research/p27/archive/gates/p27_ksroot_kummer_fixture_packet.py
```

Readable packet:

```text
research/p27/archive/probe_outputs/p27_ksroot_kummer_fixture_packet_20260622.txt
```

JSON fixture:

```text
research/p27/archive/fixtures/p27_ksroot_kummer_fixture_packet_20260622.json
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_ksroot_kummer_fixture_packet.py \
  --small-primes 1607,1847,2087 \
  --max-gate 6 \
  | tee research/p27/archive/probe_outputs/p27_ksroot_kummer_fixture_packet_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_ksroot_kummer_fixture_packet.py \
  --small-primes 1607,1847,2087 \
  --max-gate 6 \
  --json \
  > research/p27/archive/fixtures/p27_ksroot_kummer_fixture_packet_20260622.json
```

## Fixture Contents

The guard fields show exact two-sheet behavior:

```text
q1607:
  legal_K = 49
  legal_Sroot = 98
  Sroot_per_K = 2 for all 49 K rows
  f3(K) plus/minus = 28/21
  f4(K) plus/minus = 19/9
  f3(Sroot) plus/minus = 56/42
  f4(Sroot) plus/minus = 38/18

q1847:
  legal_K = 63
  legal_Sroot = 126
  Sroot_per_K = 2 for all 63 K rows
  f3(K) plus/minus = 45/18
  f4(K) plus/minus = 19/26
  f3(Sroot) plus/minus = 90/36
  f4(Sroot) plus/minus = 38/52

q2087:
  legal_K = 57
  legal_Sroot = 114
  Sroot_per_K = 2 for all 57 K rows
  f3(K) plus/minus = 25/32
  f4(K) plus/minus = 18/7
  f3(Sroot) plus/minus = 50/64
  f4(Sroot) plus/minus = 36/14
```

Later `f5/f6` rows are included in the JSON fixture but are field-tail
dominated, just as in the B-line packet.  Use them as regression checks after
`f3` is named, not as promotion evidence.

## Interpretation

Positive:

```text
K/Sroot class extraction now has exact reusable row-level guard-field input.
Sroot separates sheets with no mixed groups.
The Sroot -> K map is explicit row-by-row in the fixture.
```

Bridge update:
[P27 B/K/Sroot Fixture Bridge](p27_b_ksroot_fixture_bridge_20260622.md)
shows that the K/Sroot rows are exactly the B-line rows pulled through
`K^2=(B-2)^4/(8B(B+2)^2)` and `Sroot^2=K`.  This keeps K/Sroot useful as a
normalization/parity coordinate, but collapses it with the B-line as one
coordinated branch-class extraction problem.

Negative:

```text
Sroot gives exactly two rows per K row and no source-density advantage.
The conditional signs are doubled from K to Sroot.
The guard-field f5/f6 tails are not transferable structure by themselves.
```

Thus the first-pass K/Sroot test is:

```text
recover f3 over P1_Sroot,
compute its Sroot -> -Sroot parity and descent to K,
then compare f4/f3 only after f3 is named.
```

## Continue / Kill

```text
continue = use JSON rows for normalized K/Sroot branch-class extraction
continue = compute f3 branch degree, support field degrees, genus, components
continue = test whether f3 descends to K or needs signed Sroot
continue = cross-check any class against the B-line fixture bridge
continue = compare f4/f3 only after f3 is explicit

kill = Sroot prefix density as a source
kill = accepting a Sroot source that only works after forgetting K
kill = treating K/Sroot as independent evidence from B-line
kill = more visible degree <=4 branch scans without a new divisor reason
kill = GPU K/Sroot bucket production before a named source/recurrent class
```

```text
p27_ksroot_kummer_fixture_packet_rows=1/1
```
