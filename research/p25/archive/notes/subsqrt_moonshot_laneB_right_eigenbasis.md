# Subsqrt Moonshot Lane B Right Eigenbasis

Date: 2026-06-12

## Result

The p25 Lane B mixed module diagonalizes under the right `C_3` action into two
nontrivial right-character eigencomponents.

For every admissible packet:

```text
mixed module = E_1 + E_2
```

where `E_1` and `E_2` are C-axis coefficient vectors for the two nontrivial
right characters.  Both eigenvectors are nonzero.  The nondegenerate packets
are exactly those where `E_1` and `E_2` are independent.  The explicit
degenerate line:

```text
u + 2v = 0 mod c
```

is exactly the line where:

```text
E_1 = E_2
```

So the producer burden is now concrete:

```text
supply two independent C-axis coefficient vectors for the two nontrivial
inert-right characters.
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_right_eigenbasis_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_right_eigenbasis_gate.py
```

Observed:

```text
tiny_C3xC13:
  pairs_checked = 264/264 exhaustive
  reconstruction_hits = 264/264
  both_nonzero_hits = 264/264
  eigen_rank_counts = {1: 24, 2: 240}
  ratio_counts = {'1': 24, 'independent': 240}
  degenerate_equal_hits = 24/24
  nondegenerate_independent_hits = 240/240
  canonical theta_{3,1}: rank 2, support pair (6,6), independent

prime_axis_C3xC53:
  pairs_checked = 5304/5304 exhaustive
  reconstruction_hits = 5304/5304
  both_nonzero_hits = 5304/5304
  eigen_rank_counts = {1: 104, 2: 5200}
  ratio_counts = {'1': 104, 'independent': 5200}
  degenerate_equal_hits = 104/104
  nondegenerate_independent_hits = 5200/5200
  canonical theta_{3,1}: rank 2, support pair (26,26), independent

right_eigenbasis_rows = 3/3
conclusion=reported_p25_laneB_right_eigenbasis_gate
```

## Consequence

The first producer falsifier is no longer just "rank 2":

```text
after scalar normalization and pure-C subtraction,
project to the two nontrivial right characters;
reject unless the two C-axis vectors are nonzero and independent.
```

For the first p25 lab:

```text
inert 151 right source:
  two nontrivial C_3 characters

split 677 C-axis:
  C_13 coefficient vectors

target:
  independent E_1, E_2 vectors matching a nondegenerate carry,
  ideally canonical theta_{3,1}.
```

Discard conditions:

```text
kill E_1 = E_2 outputs;
kill one-eigenvector constructions;
kill constructions that only produce the pure-C line;
kill any apparent win on u + 2v = 0 mod c.
```

This is still finite target-shaping, not the missing CM-Artin producer.  It is
the most explicit local footprint so far for what the producer must realize.

The next C-axis payload checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_c_axis_fourier_payload.md
```

It shows that each right-character eigenvector has zero C-mean but full
nontrivial C-axis Fourier support.  A serious producer therefore needs two
independent eigenvectors, and each one must fill every nontrivial C-character.
