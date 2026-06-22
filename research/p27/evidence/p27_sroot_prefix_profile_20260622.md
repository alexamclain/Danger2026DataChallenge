# P27 K/Sroot Prefix Profile

Date: 2026-06-22

## Claim

`Sroot` is a clean normalization coordinate for the K/S branch extraction, but
it is not a stronger prefix sampler than `K`.

Across q1607/q1847/q2087 and exact extension-field checks, selected bits
`d3..d8` descend with no mixed K or Sroot groups.  However, every Sroot count is
exactly the doubled K count with identical prefix ratios:

```text
legal_Sroot = 2 * legal_K
Sroot_group_size = K_group_size / 2
scaled_prefix(Sroot) = scaled_prefix(K)
```

So `Sroot` remains the right coordinate for normalization, sheet separation,
and branch-class extraction.  It does not by itself supply a below-sqrt
source shrink or GPU bucket.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_sroot_prefix_profile_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q607_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q1607_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q1847_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q2087_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q31_degrees1_3_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q7_degrees3_5_gate8_20260622.txt
```

## Commands

Promotion fields:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_sroot_prefix_profile_probe.py \
  --q 1607 \
  --degrees 1 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q1607_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_sroot_prefix_profile_probe.py \
  --q 1847 \
  --degrees 1 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q1847_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_sroot_prefix_profile_probe.py \
  --q 2087 \
  --degrees 1 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q2087_gate8_20260622.txt
```

Extension checks:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_sroot_prefix_profile_probe.py \
  --q 31 \
  --degrees 1,2,3 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q31_degrees1_3_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_sroot_prefix_profile_probe.py \
  --q 7 \
  --degrees 3,4,5 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_prefix_profile_probe_q7_degrees3_5_gate8_20260622.txt
```

## Promotion Fields

q1607:

```text
legal_K = 49
legal_Sroot = 98
K_group_size_16 = 49
Sroot_group_size_8 = 98

K/Sroot scaled prefix:
  gate3: plus K/Sroot = 28/56, scaled = 1.142857143
  gate4: plus K/Sroot = 19/38, scaled = 1.551020408
  gate5: plus K/Sroot = 19/38, scaled = 3.102040816
  gate6: plus K/Sroot = 0/0
```

q1847:

```text
legal_K = 63
legal_Sroot = 126
K_group_size_16 = 63
Sroot_group_size_8 = 126

K/Sroot scaled prefix:
  gate3: plus K/Sroot = 45/90, scaled = 1.428571429
  gate4: plus K/Sroot = 19/38, scaled = 1.206349206
  gate5: plus K/Sroot = 0/0
```

q2087:

```text
legal_K = 57
legal_Sroot = 114
K_group_size_16 = 57
Sroot_group_size_8 = 114

K/Sroot scaled prefix:
  gate3: plus K/Sroot = 25/50, scaled = 0.877192982
  gate4: plus K/Sroot = 18/36, scaled = 1.263157895
  gate5: plus K/Sroot = 18/36, scaled = 2.526315789
  gate6: plus K/Sroot = 18/36, scaled = 5.052631579
  gate7: plus K/Sroot = 18/36, scaled = 10.105263158
  gate8: plus K/Sroot = 0/0
```

These are exact finite-field counts.  The q2087 plateau is real locally but
not transferable by itself: q1607 stops at gate6, q1847 stops at gate5, and
q2087 stops at gate8.

## Extension Checks

The exact extension fields show the same K/Sroot doubling:

```text
GF(31^3):
  legal_K = 930
  legal_Sroot = 1860
  K/Sroot scaled gates = 1.0000, 0.9677, 0.6452, 1.2903, 0

GF(7^5):
  legal_K = 590
  legal_Sroot = 1180
  K/Sroot scaled gates = 1.0678, 0.9492, 1.8983, 0
```

Again, the local tail behavior is field-dependent rather than a stable
source-normalized law.

## Interpretation

Positive:

```text
Selected prefix bits descend cleanly to K and Sroot in every tested field.
Sroot separates the two K sheets without introducing mixed prefix groups.
This strengthens Sroot as the preferred normalization coordinate for CAS.
```

Negative for sqrt beating:

```text
Sroot gives no prefix-density advantage over K.
The doubled Sroot group count exactly cancels the half-sized Sroot fibers.
Field-local all-plus plateaus do not transfer across q1607/q1847/q2087.
No GPU K/Sroot bucket or prefix production mode is justified.
```

## Continue / Kill

```text
continue = normalize the d3 cover over P1_Sroot with K as quotient check
continue = compute branch divisor/support degrees/genus
continue = compare d4 only after the d3 Kummer class is explicit

kill = Sroot prefix density as a below-sqrt source
kill = GPU K/Sroot bucket production without a named class or recurrence
kill = treating q2087's local plateau as transferable p27 structure
```

```text
p27_sroot_prefix_profile_rows=1/1
```
