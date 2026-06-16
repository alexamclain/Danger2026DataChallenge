# Subsqrt Moonshot Lane B Kummer / Sign Descent

Date: 2026-06-12

## Result

The single-anchor correction from the punctured Hasse-Davenport gate needs a
genuine Kummer lift.  A sign choice alone cannot remove the obstruction.

For the prime-axis labs, the anchor scalar is:

```text
q - 2
```

in the Jacobi value field `F_l`.  Its class in:

```text
F_l^* / (F_l^*)^c
```

is primitive.  Also, `-1` is already a `c`-th power in `F_l`, so changing the
sign does not change the Kummer class:

```text
class(-(q-2)) = class(q-2).
```

Thus both `q-2` and `-(q-2)` require the full degree-`c` Kummer extension before
a `c`-th root exists.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_kummer_sign_descent_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_kummer_sign_descent_gate.py
```

Observed:

```text
tiny_C3xC13:
  base_field_q = 79
  value_field_l = 157
  anchor = 77
  class(anchor) = 6 mod 13
  class(-anchor) = 6 mod 13
  class(-1) = 0 mod 13
  anchor_has_13th_root_in_F_l = 0
  -anchor_has_13th_root_in_F_l = 0
  minimal_extension_degree(anchor) = 13
  minimal_extension_degree(-anchor) = 13
  root_degrees_up_to_c(anchor) = [13]

prime_axis_C3xC53:
  base_field_q = 3181
  value_field_l = 3499
  anchor = 3179
  class(anchor) = 38 mod 53
  class(-anchor) = 38 mod 53
  class(-1) = 0 mod 53
  anchor_has_53rd_root_in_F_l = 0
  -anchor_has_53rd_root_in_F_l = 0
  minimal_extension_degree(anchor) = 53
  minimal_extension_degree(-anchor) = 53
  root_degrees_up_to_c(anchor) = [53]

kummer_sign_descent_rows = 2/2
conclusion=reported_p25_laneB_kummer_sign_descent_gate
```

## Consequence

The post-producer anchor task is now precise:

```text
base-field sign changes do not help;
the single-anchor root is a full degree-c Kummer object;
for the first C_3 x C_13 lab, the missing root lives only after degree 13.
```

This rules out:

```text
base Jacobi-value-field c-th-root shortcuts;
sign-only descents;
producer claims that silently absorb the anchor scalar without a degree-c Kummer step.
```

Positive next artifact:

```text
an arithmetic producer that realizes the raw 151 x 677 half-arc packet and
also supplies a controlled degree-13 Kummer descent for the single anchor.
```

This is not yet the missing producer.  It makes the anchor obstruction exact:
the half-arc pullback and the Kummer root are separate obligations, and the
Kummer obligation has full degree `c`.

Square-axis note:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_kummer_relief.md
```

The `C_169` anchor is different: its class has order `13`, so the square-axis
anchor descent costs degree `13`, not degree `169`.
