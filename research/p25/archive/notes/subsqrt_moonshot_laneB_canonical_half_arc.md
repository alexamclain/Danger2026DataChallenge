# Subsqrt Moonshot Lane B Canonical Half-Arc

Date: 2026-06-12

## Result

For the canonical packet `theta_{3,1}`, the one-vector payload from the
diamond-conjugacy checkpoint has an exact four-zone C-axis carry template.

For `c = 4m + 1`, the raw carry on `C_3 x C_c` is:

```text
C index 0..m:       no right row carries
C index m+1..2m:    exactly one right row carries, cycling through C_3
C index 2m+1..3m:  exactly two right rows carry, equivalently minus the missing row
C index 3m+1..4m:  all right rows carry
```

After scalar / pure-C subtraction and projection to a nontrivial right
character, the pure zones vanish and the mixed payload is exactly the middle
half-arc:

```text
support(V) = {m+1, ..., 3m}
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_canonical_half_arc_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_canonical_half_arc_gate.py
```

Observed:

```text
tiny_C3xC13:
  c = 13, m = 3
  template_bit_hits = 13/13
  packet_carry_hits = 39/39
  eigen_1_template_hits = 13/13
  eigen_2_template_hits = 13/13
  pure_zone_zero_hits = 7/7
  mixed_zone_nonzero_hits = 6/6
  support_1 = support_2 = (4, 9, 6)
  zone_lengths = zero:4 one_hot:3 two_hot:3 all_rows:3

prime_axis_C3xC53:
  c = 53, m = 13
  template_bit_hits = 53/53
  packet_carry_hits = 159/159
  eigen_1_template_hits = 53/53
  eigen_2_template_hits = 53/53
  pure_zone_zero_hits = 27/27
  mixed_zone_nonzero_hits = 26/26
  support_1 = support_2 = (14, 39, 26)
  zone_lengths = zero:14 one_hot:13 two_hot:13 all_rows:13

square_axis_C3xC169:
  c = 169, m = 42
  template_bit_hits = 169/169
  packet_carry_hits = 507/507
  eigen_1_template_hits = 169/169
  eigen_2_template_hits = 169/169
  pure_zone_zero_hits = 85/85
  mixed_zone_nonzero_hits = 84/84
  support_1 = support_2 = (43, 126, 84)
  zone_lengths = zero:43 one_hot:42 two_hot:42 all_rows:42

canonical_half_arc_rows = 3/3
conclusion=reported_p25_laneB_canonical_half_arc_gate
```

## Consequence

The first `151 x 677` producer target can now be stated as a concrete finite
divisor footprint:

```text
on C_3 x C_13:
  C slots 0..3    -> pure zero zone
  C slots 4..6    -> one-hot right-row carry zone
  C slots 7..9    -> two-hot right-row carry zone
  C slots 10..12  -> pure all-rows zone

after right-character projection:
  V is supported exactly on C slots 4..9
  -<-1>V is the second right-character vector
  V is not anti-invariant
  V has all 12 nontrivial C_13 Fourier characters nonzero.
```

This sharpens the positive artifact request:

```text
construct a ray-local CM-Artin / modular-unit pullback whose local carry bits
realize the four-zone theta_{3,1} template on the 151 x 677 source coupling.
```

Discard conditions:

```text
kill candidates that only match the Fourier support but not the half-arc;
kill candidates whose mixed support leaks outside m+1..3m;
kill candidates that miss either the one-hot or two-hot row-carry zone;
kill pure-zone-only or anti-invariant outputs.
```

This still is not the missing producer theorem.  It converts the canonical p25
Lane B target into a small, explicit row-carry divisor shape that an arithmetic
pullback can be tested against.

The raw local-source lift checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_source_half_arc_lift.md
```

It verifies that the same four-zone template is read directly from the actual
local source logs, especially the inert `151` right source and split `677`
C-axis source, with exactly `B = 325` raw representatives per quotient point.
