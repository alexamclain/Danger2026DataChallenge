# Subsqrt Moonshot Lane B C-Axis Fourier Payload

Date: 2026-06-12

## Result

After the right-character split:

```text
mixed module = E_1 + E_2
```

each `E_i` is a C-axis vector.  The p25 packets do not merely require two
independent C-axis vectors.  Each vector has:

```text
zero C-mean
full support on every nontrivial C-axis Fourier character
```

So the producer burden is now:

```text
supply two independent right-character eigenvectors,
and each eigenvector must carry the full nontrivial C-character payload.
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_c_axis_fourier_payload_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_c_axis_fourier_payload_gate.py
```

Observed:

```text
tiny_C3xC13:
  pairs_checked = 264/264 exhaustive
  zero_mean_hits = 264/264
  full_nontrivial_c_fourier_hits = 264/264
  same_fourier_support_hits = 264/264
  real_pair_coverage_hits = 264/264
  frobenius_component_coverage_hits = 264/264
  real_component_count = 2
  real_orbit_lengths = [3, 3]
  coordinate_support_counts = {(6,6):48, (8,8):120, (10,10):48, (12,12):48}
  c_fourier_support_counts = {(12,12):264}
  canonical theta_{3,1}: coordinate support (6,6), C-Fourier support (12,12)

prime_axis_C3xC53:
  pairs_checked = 5304/5304 exhaustive
  zero_mean_hits = 5304/5304
  full_nontrivial_c_fourier_hits = 5304/5304
  same_fourier_support_hits = 5304/5304
  real_pair_coverage_hits = 5304/5304
  frobenius_component_coverage_hits = 5304/5304
  real_component_count = 2
  real_orbit_lengths = [13, 13]
  c_fourier_support_counts = {(52,52):5304}
  canonical theta_{3,1}: coordinate support (26,26), C-Fourier support (52,52)

square_axis_C3xC169:
  representative pairs checked = 4
  zero_mean_hits = 4/4
  full_nontrivial_c_fourier_hits = 4/4
  real_component_count = 4
  real_orbit_lengths = [39, 39, 3, 3]
  c_fourier_support_counts = {(168,168):4}

c_axis_fourier_payload_rows = 3/3
conclusion=reported_p25_laneB_c_axis_fourier_payload_gate
```

## Consequence

The first producer falsifier has tightened again:

```text
project a candidate producer to the two nontrivial right characters;
for each resulting C-axis vector, take the C-axis Fourier transform;
reject unless both vectors have zero mean and every nontrivial C-character is nonzero.
```

This kills the following as complete p25 Lane B producers:

```text
one-eigenvector constructions;
low-frequency C-axis constructions;
single real-cyclotomic component constructions;
orbit-sparse C-axis constructions;
coordinate-sparse guesses whose Fourier payload is not full;
degenerate E_1 = E_2 outputs.
```

The next diamond-conjugacy checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_diamond_conjugacy.md
```

It shows that the two right-character payloads are not unrelated: `E_2` is the
negative C-axis inversion conjugate of `E_1`, and the bad `E_1 = E_2` line is
exactly the anti-invariant case.

For the first `151 x 677` lab, the target is therefore not just a rank-`2`
coupling.  It is:

```text
inert 151 right source x split 677 C source
  -> one C_13 vector V with all 12 nontrivial Fourier characters
  -> second vector is the prescribed negative inversion conjugate -<-1>V
  -> both real Frobenius components are required.
```

This is still not the missing CM-Artin / modular-unit producer.  It makes the
next attempted producer much easier to falsify: a candidate that does not fill
the nontrivial C-Fourier payload cannot be the p25 Lane B moonshot object.
