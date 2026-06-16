# Subsqrt Moonshot Lane B Mixed-Character Module

Date: 2026-06-12

## Result

The scalar-normalized p25 Lane B Jacobi-carry packet has a sharper module
shape:

```text
normalized packet = pure-C line + mixed right-character module
```

For the prime C-axis labs, the pure-C line is always rank `1` and has full
C-support.  The mixed module is generically rank `2` over the right axis.  It
drops to rank `1` exactly on the explicit degenerate line:

```text
u + 2v = 0 mod c
```

This gives a concrete producer filter.  A candidate ray-local CM-Artin pullback
must realize a nondegenerate rank-2 mixed module.  A construction that only
lands on the rank-1 line is too small; it is an accidental degeneracy, not the
full inert/split coupling needed by the moonshot.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_mixed_character_module_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_mixed_character_module_gate.py
```

Observed:

```text
tiny_C3xC13:
  pairs_checked = 264/264 exhaustive
  degenerate_line_pairs = 24 = 2*(13-1)
  pure_C_rank_counts = {1: 264}
  mixed_rank_counts = {1: 24, 2: 240}
  full_rank_counts = {2: 24, 3: 240}
  direct_sum_hits = 264/264
  degenerate_rank1_hits = 24/24
  nondegenerate_rank2_hits = 240/240

prime_axis_C3xC53:
  pairs_checked = 5304/5304 exhaustive
  degenerate_line_pairs = 104 = 2*(53-1)
  pure_C_rank_counts = {1: 5304}
  mixed_rank_counts = {1: 104, 2: 5200}
  full_rank_counts = {2: 104, 3: 5200}
  direct_sum_hits = 5304/5304
  degenerate_rank1_hits = 104/104
  nondegenerate_rank2_hits = 5200/5200

square_axis_C3xC169:
  representative pairs checked = 4
  pure_C_rank_counts = {1: 4}
  mixed_rank_counts = {2: 4}
  full_rank_counts = {3: 4}

mixed_character_module_rows = 3/3
conclusion=reported_p25_laneB_mixed_character_module_gate
```

## Consequence

The producer target is now:

```text
ray-local CM-Artin / modular-unit pullback
  on inert 151 x split 677
  whose scalar-normalized local divisor has:
    pure-C rank 1,
    mixed right-character rank 2,
    and avoids u + 2v = 0 mod 13.
```

Discard conditions:

```text
kill rank-1-only constructions;
kill separated local units;
kill pure-C residual-only constructions;
kill outputs whose apparent success depends on u + 2v = 0 mod c.
```

Positive next artifact:

```text
a toy ray-local CM-Artin pullback or modular-unit divisor whose local footprint
matches one nondegenerate rank-2 carry, ideally the canonical theta_{3,1}.
```

This still does not construct the p25 producer.  It makes the first producer
falsifier much more exact.

The right-character diagonalization checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_right_eigenbasis.md
```

It shows that the mixed module is two nontrivial right-character eigenvectors.
The degenerate line `u + 2v = 0 mod c` is exactly where those eigenvectors
coincide.  A serious producer should supply two independent C-axis coefficient
vectors for the inert-right characters.
