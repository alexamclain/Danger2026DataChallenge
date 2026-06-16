# Subsqrt Moonshot Lane B Diamond Conjugacy

Date: 2026-06-12

## Result

The two right-character eigenvectors are not arbitrary independent C-axis
payloads.  For every admissible `C_3 x C_13` and `C_3 x C_53` packet, and for
the representative `C_3 x C_169` packets:

```text
E_2 = - < -1 > E_1
```

where `<-1>` is inversion on the C-axis:

```text
(<-1> E_1)[j] = E_1[-j].
```

The degenerate line:

```text
u + 2v = 0 mod c
```

is exactly the anti-invariant case:

```text
E_1 = - < -1 > E_1
```

and hence exactly the line where `E_1 = E_2` and the mixed module drops to rank
`1`.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_diamond_conjugacy_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_diamond_conjugacy_gate.py
```

Observed:

```text
tiny_C3xC13:
  pairs_checked = 264/264 exhaustive
  negative_inversion_conjugacy_hits = 264/264
  anti_invariant_hits = 24/264
  degenerate_line_pairs = 24
  degenerate_self_conjugate_hits = 24/24
  nondegenerate_independent_conjugate_hits = 240/240
  rank_counts = {1:24, 2:240}
  canonical theta_{3,1}: rank 2, support (6,6), non-anti-invariant

prime_axis_C3xC53:
  pairs_checked = 5304/5304 exhaustive
  negative_inversion_conjugacy_hits = 5304/5304
  anti_invariant_hits = 104/5304
  degenerate_line_pairs = 104
  degenerate_self_conjugate_hits = 104/104
  nondegenerate_independent_conjugate_hits = 5200/5200
  rank_counts = {1:104, 2:5200}
  canonical theta_{3,1}: rank 2, support (26,26), non-anti-invariant

square_axis_C3xC169:
  representative pairs checked = 4
  negative_inversion_conjugacy_hits = 4/4
  anti_invariant_hits = 0/4
  nondegenerate_independent_conjugate_hits = 4/4

diamond_conjugacy_rows = 3/3
conclusion=reported_p25_laneB_diamond_conjugacy_gate
```

## Consequence

The producer target is now more structured:

```text
produce one full nontrivial C-axis vector V for a nontrivial right character;
the second right-character vector must be -<-1>V;
V must not be anti-invariant under -<-1>.
```

Together with the C-axis Fourier payload gate, the first `151 x 677` lab now
requires:

```text
inert 151 right source x split 677 C source
  -> one C_13 vector V with zero mean
  -> V has all 12 nontrivial C_13 Fourier characters nonzero
  -> second vector is the prescribed negative inversion conjugate -<-1>V
  -> V is not anti-invariant, so E_1 and E_2 remain independent.
```

This kills:

```text
two-vector producers with no diamond relation;
anti-invariant one-vector producers;
one-eigenvector outputs;
low-frequency or orbit-sparse C-axis payloads;
any apparent win on u + 2v = 0 mod c.
```

Positive next artifact:

```text
a ray-local CM-Artin / modular-unit pullback whose C-axis footprint is one
full nontrivial vector V and whose conjugate right-character footprint is
exactly -<-1>V.
```

This still does not construct the missing producer.  It amortizes the p24 work
into a much narrower p25 falsifier: one full C-axis vector plus a prescribed
diamond conjugate, rather than two unrelated vectors.

The canonical half-arc checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_canonical_half_arc.md
```

It specializes the target to `theta_{3,1}`: the one-vector payload is supported
on the middle C-axis half-arc and comes from an explicit zero / one-hot /
two-hot / all-rows carry template.
