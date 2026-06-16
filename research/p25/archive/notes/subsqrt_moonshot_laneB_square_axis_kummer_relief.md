# Subsqrt Moonshot Lane B Square-Axis Kummer Relief

Date: 2026-06-12

## Result

The `C_3 x C_169` square-axis target has a cheaper single-anchor Kummer descent
than a naive degree-`169` reading suggests.

For the square-axis lab:

```text
C axis = 169 = 13^2
order = 507
base field q = 2029
value field l = 4057
anchor = q - 2 = 2027
class(anchor) = 13 mod 169
class order = 13
minimal Kummer extension degree = 13
```

The negative anchor has the same class, and `-1` is already a `169`-th power in
the value field, so sign choice still does not change the Kummer class.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_kummer_relief_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_kummer_relief_gate.py
```

Observed:

```text
square_axis_C3xC169:
  anchor_class_index = 13
  anchor_class_order = 13
  anchor_minimal_extension_degree = 13
  neg_anchor_class_index = 13
  neg_anchor_class_order = 13
  neg_anchor_minimal_extension_degree = 13
  sign_class_zero = 1
  sign_does_not_change_anchor_class = 1
  root_degrees_up_to_169 = [13, 26, 39, 52, 65, 78, 91, 104, 117, 130, 143, 156, 169]

square_axis_kummer_relief_rows = 1/1
conclusion=reported_p25_laneB_square_axis_kummer_relief_gate
```

## Consequence

This is a positive p25-specific artifact:

```text
the C_169 quotient is larger than C_13;
but its single-anchor Kummer descent is not degree 169;
it collapses to the same degree 13 burden as the tiny C_13 lab.
```

That does not make `C_3 x C_169` the primary path.  Its mask still has `507`
quotient rectangles and the same full-support, no-stabilizer behavior recorded
by the Lane B gates.  But it changes the discard logic: do not reject the
square-axis route solely because of an assumed degree-`169` anchor descent.

The live producer question becomes:

```text
Can the ray-local CM-Artin / modular-unit source produce the C_169 half-arc
more naturally than C_13, while paying only a degree-13 anchor descent?
```

The ray-local candidate harness now has a square-axis mode:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_ray_local_theta31_pullback_falsifier_gate.py \
  --case square_axis_C3xC169
```

The synthetic square-axis control passes with `507` quotient rectangles, `252`
carrying rectangles, `6300` raw carry-one positions, full `C_169` Fourier
support, and the expected degree-`13` Kummer descent.

The imprimitive-lift obstruction is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_imprimitive_lift_obstruction.md
```

It records that the `C_169` target traces down to the `C_13` half-arc plus a
constant background, but is not a pullback from `C_13`; it uses every
primitive/non-lifted `C_169` character.
