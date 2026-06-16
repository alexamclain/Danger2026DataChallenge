# Subsqrt Moonshot Lane B Source Half-Arc Lift

Date: 2026-06-12

## Result

The canonical half-arc target lifts cleanly from the quotient `C_3 x C_c` to
the actual raw local source cycles used by the p25 negative trace.

For the first lab:

```text
C_3 x C_13
right source: inert 151
C source:     split 677
B:            325
raw order:    12675 = 39 * 325
```

the local discrete-log coordinates read the same canonical four-zone carry
template as the quotient model.  Every quotient point has exactly `B = 325`
raw representatives, and the raw trace reconstructs the canonical
`theta_{3,1}` packet.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_source_half_arc_lift_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_source_half_arc_lift_gate.py
```

Observed:

```text
tiny_C3xC13:
  c = 13, B = 325, raw_order = 12675
  right_sources = ['mod151']
  c_source = mod677
  source_coordinate_hits = 12675/12675
  block_constancy_hits = 39/39
  quotient_bit_hits = 12675/12675
  raw_value_hits = 12675/12675
  trace_hits = 39/39
  raw_zone_counts:
    zero     = 3900
    one_hot  = 2925
    two_hot  = 2925
    all_rows = 2925
  raw_zone_carry_counts:
    zero     = 0
    one_hot  = 975
    two_hot  = 1950
    all_rows = 2925

prime_axis_C3xC53:
  c = 53, B = 25, raw_order = 3975
  source_coordinate_hits = 3975/3975
  block_constancy_hits = 159/159
  trace_hits = 159/159

square_axis_C3xC169:
  c = 169, B = 25, raw_order = 12675
  source_coordinate_hits = 12675/12675
  block_constancy_hits = 507/507
  trace_hits = 507/507

source_half_arc_lift_rows = 3/3
conclusion=reported_p25_laneB_source_half_arc_lift_gate
```

## Consequence

The arithmetic producer target can now be stated directly on the raw local
source cycle:

```text
Given e in Z/12675Z:
  read right coordinate from log_151((p^2)^e) mod 3;
  read C coordinate from log_677((p^2)^e) mod 13;
  assign the canonical theta_{3,1} carry bit from the four-zone half-arc table;
  raw values are constant on each B=325 block and trace back to the quotient packet.
```

For the `151 x 677` lab, a candidate CM-Artin / modular-unit pullback should
therefore realize not just an abstract quotient divisor, but this raw block
structure:

```text
39 quotient points
325 raw representatives per quotient point
four C-zone template visible from the local logs
5850 raw carry-one positions
```

Discard conditions:

```text
kill candidates whose local logs do not recover the C_3 x C_13 coordinates;
kill candidates that break B-block constancy;
kill candidates whose raw trace does not recover theta_{3,1};
kill candidates with the right Fourier payload but the wrong raw zone counts.
```

This still does not produce the missing arithmetic object.  It makes the next
producer test local-source explicit: the proposed object must realize the
canonical half-arc directly on the inert-151 x split-677 raw cycle.

The residue-coset version of the same target is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_residue_coset_mask.md
```

It records that the first `151 x 677` lab is a union of actual product coset
rectangles: three `mod151` classes of size `25` crossed with thirteen `mod677`
classes of size `13`, so each `C_3 x C_13` quotient point has `325` residue
pairs.

The separate single-anchor Kummer/sign checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_kummer_sign_descent.md
```

It shows that once the raw half-arc is produced, the anchor cannot be cleared
by a sign choice in the Jacobi value field; the first `C_3 x C_13` lab needs a
controlled degree-13 Kummer descent.
