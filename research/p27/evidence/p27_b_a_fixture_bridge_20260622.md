# P27 B/A Fixture Bridge

Date: 2026-06-22

## Claim

The frozen A-level and B-line Kummer fixtures are exact signed coordinate
views of the same selected-gate classes for the recorded gates.

For q1607/q1847/q2087 and gates `d3,d4`:

```text
A = B^2 - 2
```

maps every active B row to exactly one A row with the same sign, and every A
row is covered exactly once.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_a_fixture_bridge_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_a_fixture_bridge_probe_20260622.txt
```

Input fixtures:

```text
research/p27/archive/fixtures/p27_a_level_kummer_extraction_packet_20260622.json
research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_a_fixture_bridge_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_a_fixture_bridge_probe_20260622.txt
```

## Results

Every recorded field/gate row matched:

```text
q1607:
  d3: A rows 49, B rows 49, sign matches 49
  d4: A rows 28, B rows 28, sign matches 28

q1847:
  d3: A rows 63, B rows 63, sign matches 63
  d4: A rows 45, B rows 45, sign matches 45

q2087:
  d3: A rows 57, B rows 57, sign matches 57
  d4: A rows 25, B rows 25, sign matches 25
```

Totals:

```text
A_rows = 267
B_rows = 267
B_to_A_sign_match = 267
A_preimages_1 = 267
exact_signed_bijection = 6/6 field-gate checks
```

There were no missing A rows, sign mismatches, uncovered A rows, or B-to-A
collisions.

## Interpretation

Positive:

```text
The A-level packet is a useful quotient view of the same conditional classes.
Any future class extraction can be checked in both A and B coordinates.
The identity A=B^2-2 is exact on the actual frozen CAS fixtures, not only on
counts.
```

Negative:

```text
A-level, B-line, K-line, and Sroot should not be counted as independent
moonshot lanes.
There is no separate GPU A-bucket reason after the B-line and K/Sroot bucket
negatives.
The A-line CAS ask should not duplicate the B-line class extraction.
```

The class-extraction queue is now:

```text
primary = extract f3 on P1_B, P1_A, or P1_Sroot, whichever CAS handles best
check   = translate through A=B^2-2, K^2=(B-2)^4/(8B(B+2)^2), and Sroot^2=K
then    = compare f4/f3 after f3 is named
```

## Continue / Kill

```text
continue = one coordinated A/B/K/Sroot normalized-class extraction
continue = use A as a quotient check and B as the explicit genus-0 source coordinate
continue = compare f4/f3 only after f3 is explicit

kill = treating A-level and B-line fixtures as independent evidence
kill = GPU A-bucket production before a named source/recurrent class
kill = separate A-line CAS work that ignores the B/A bridge
```

```text
p27_b_a_fixture_bridge_rows=1/1
```
