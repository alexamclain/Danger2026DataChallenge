# Subsqrt Moonshot Lane B CM-Artin Sources

Date: 2026-06-12

## Result

The p25 Lane B source arithmetic is ray-local, not a plain split-prime class
quotient.

For the first `C_3 x C_13` lab:

```text
right C_3 source: prime 151, inert in D_K
C_13 source:      prime 677, split in D_K
```

After the `B=325` trace:

```text
ord_151(p^2) = 75 = 3 * 5^2      -> visible C_3
ord_677(p^2) = 169 = 13^2        -> visible C_13
```

So the missing producer has to couple an inert/ray-local right source with a
split C-axis source.  A split-prime-only CM/Lang search is the wrong next
falsifier for this p25 lane.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_cm_artin_source_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_cm_artin_source_gate.py
```

Observed:

```text
negative_trace = -2988055724018
D_K = -1941970186885204113620983

tiny_C3xC13:
  prime 151: inert,  ord(p^2)=75,  visible after B=325 is 3
  prime 677: split,  ord(p^2)=169, visible after B=325 is 13
  right source agreement = 12675/12675
  ok = 1

prime_axis_C3xC53:
  prime 7:   ramified, ord(p^16)=3,  visible after B=25 is 3
  prime 151: inert,    ord(p^16)=75, visible after B=25 is 3
  prime 107: split,    ord(p^16)=53, visible after B=25 is 53
  right source agreement = 3975/3975
  ok = 1

square_axis_C3xC169:
  prime 151: inert, ord(p^2)=75,  visible after B=25 is 3
  prime 677: split, ord(p^2)=169, visible after B=25 is 169
  ok = 1

cm_artin_local_source_rows = 3/3
conclusion=reported_p25_laneB_cm_artin_local_source_gate
```

## Consequence

The current p25 Lane B producer target is now:

```text
CM-Artin / modular-unit pullback on a ray-local product source
  right axis: inert or ramified rational residue source
  C axis:     split rational residue source
plus:
  reduced Jacobi packet
  single-anchor Kummer/sign descent
  two small real-cyclotomic residual resultants
```

For the first falsifier, focus on:

```text
151 inert right source x 677 split C source -> C_3 x C_13
```

Discard conditions:

```text
kill split-prime-only producer attempts;
kill cyclic-C norm attempts that do not keep the diamond residual;
kill product-formula attempts with no explicit degenerate-anchor correction;
kill local-unit attempts that separate the 151 and 677 factors additively.
```

This source gate does not construct the producer.  It makes the producer
search narrower and more honest: the next positive artifact must be a
ray-local CM-Artin pullback theorem or a toy model that actually realizes the
inert/split coupling.

The next module-shape checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_mixed_character_module.md
```

It records that the scalar-normalized packet splits as a pure-C line plus a
mixed right-character module.  The mixed module is generically rank `2`, with a
rank-`1` drop exactly on `u + 2v = 0 mod c`.  A serious producer should target
the nondegenerate rank-`2` module.
