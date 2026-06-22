# P27 B/K/Sroot Fixture Bridge

Date: 2026-06-22

## Claim

The frozen B-line and K/Sroot Kummer fixtures are exact coordinate views of the
same conditional selected-gate classes through every recorded gate.

For q1607/q1847/q2087 and gates `d3..d6`:

```text
K^2 = (B - 2)^4 / (8*B*(B + 2)^2)
Sroot^2 = K
```

maps every active B row to exactly one signed K row, and every signed K row to
exactly two Sroot rows with matching signs.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_ksroot_fixture_bridge_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_ksroot_fixture_bridge_probe_20260622.txt
```

Input fixtures:

```text
research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json
research/p27/archive/fixtures/p27_ksroot_kummer_fixture_packet_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_ksroot_fixture_bridge_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_ksroot_fixture_bridge_probe_20260622.txt
```

## Results

Every nonempty gate/field row matched:

```text
q1607:
  d3: B rows 49, K sign matches 49, Sroot sheet matches 49
  d4: B rows 28, K sign matches 28, Sroot sheet matches 28
  d5: B rows 19, K sign matches 19, Sroot sheet matches 19
  d6: B rows 19, K sign matches 19, Sroot sheet matches 19

q1847:
  d3: B rows 63, K sign matches 63, Sroot sheet matches 63
  d4: B rows 45, K sign matches 45, Sroot sheet matches 45
  d5: B rows 19, K sign matches 19, Sroot sheet matches 19
  d6: empty tail

q2087:
  d3: B rows 57, K sign matches 57, Sroot sheet matches 57
  d4: B rows 25, K sign matches 25, Sroot sheet matches 25
  d5: B rows 18, K sign matches 18, Sroot sheet matches 18
  d6: B rows 18, K sign matches 18, Sroot sheet matches 18
```

All checked B rows had:

```text
K_roots_2
K_present_1
Sroot_present_2
Sroot_square_match for every Sroot row
```

There were no sign mismatches.

## Interpretation

Positive:

```text
The coordinate bridge is exact on the actual CAS fixtures.
Future B/K/Sroot branch-class output can be translated and cross-checked.
Sroot remains useful for signed-sheet parity and descent checks.
```

Negative:

```text
B-line, K-line, and Sroot should not be counted as independent moonshot lanes.
They are coordinated presentations of one descended Kummer-class problem.
The Sroot sheet does not add a source shrink; it doubles K rows with matching
signs.
```

This collapses the class-extraction queue to:

```text
primary = extract f3 on P1_B or P1_Sroot, whichever CAS handles better
check   = translate through K^2=(B-2)^4/(8B(B+2)^2) and Sroot^2=K
then    = compare f4/f3 after f3 is named
```

## Continue / Kill

```text
continue = one coordinated B/K/Sroot normalized-class extraction
continue = use B as the simpler genus-0 quotient and Sroot as parity/descent check
continue = compare f4/f3 only after f3 is explicit

kill = treating B-line and K/Sroot as independent evidence
kill = separate GPU bucket production for K/Sroot after B-line negatives
kill = Sroot-only source claims that do not survive K-square preservation
```

```text
p27_b_ksroot_fixture_bridge_rows=1/1
```
