# P27 B-Line F5 Visible Character Screen

Date: 2026-06-22

## Claim

The mixed-`f5` guard-field signs are not explained by the cheapest visible
base-`B` characters.

After the mixed-guard transition result, the natural source-shaped loophole
was:

```text
maybe f5(B) = chi(simple B-divisor)
```

on the selected `f4=+1` B rows.  This probe tests named B atoms and split
linear branch support of degree `<=2`.  It finds no exact rule in the mixed
guard fields.

## Probe

Gate:

```text
research/p27/archive/gates/p27_b_line_f5_visible_character_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_f5_visible_character_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_f5_visible_character_probe.py \
  --small-primes 4999,5783,6007,6247 \
  --kummer-fixture research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json \
  | tee research/p27/archive/probe_outputs/p27_b_line_f5_visible_character_probe_20260622.txt
```

Families:

```text
named atoms:
  B, B+/-2, B+/-4, B^2+/-4, B^2+/-2B+4,
  B/(B+2), (B-2)/(B+2)

split linear support:
  chi((B-a)) and chi((B-a)(B-b))
```

## Result

Mixed-`f5` domains:

```text
field   rows   f5+   f5-
4999    39     27    12
5783    42     1     41
6007    38     18    20
6247    34     18    16
```

No exact named atom:

```text
field   atoms tested   exact   best distance
4999    11             none    12
5783    11             none    1
6007    11             none    17
6247    11             none    16
```

No exact split linear support of degree `<=2`:

```text
field   linear factors   degree2 exact   best single-linear distance
4999    4960             0               7
5783    5741             0               1
6007    5969             0               8
6247    6213             0               6
```

The near misses in `q5783` are not meaningful by themselves because that field
has only one plus row.  The balanced fields `q6007` and `q6247` are the better
guards, and they also have no exact visible rule.

## Interpretation

Positive:

```text
The repeated f4/f5 gamma transition remains a real structure to extract.
The mixed-f5 signs do not collapse to the cheapest visible B-character source.
```

Negative:

```text
No direct B-atom or split-degree-2 source follows.
This does not supply a GPU production bucket.
The next useful test is still divisor/Kummer/CAS comparison of gamma4/gamma5.
```

## Continue / Kill

```text
continue = compare repeated gamma classes as Kummer/divisor classes
continue = use mixed-f5 fields as CAS regression fixtures
continue = ask only theorem-shaped quotient/coboundary questions from here

kill = named B atoms as f5 source selectors
kill = split linear branch support of degree <=2 as an f5 source selector
kill = GPU production from visible f5(B) buckets
```

```text
p27_b_line_f5_visible_character_rows=1/1
```
