# P27 K-Line Lattes Recurrence Screen

Date: 2026-06-21

## Claim

The `d4` bit is not a high-coverage recurrence of `d3` under small Lattes maps
on the reduced Kummer line.

After the signed-doubling descent, both `d3` and `d4` live on:

```text
K = x([2]P),  E': V^2 = U^3 + 4U.
```

This screen tests the natural Kummer-line recurrence family:

```text
K -> x([m]Q)
K -> x([m]Q + (0,0)) = 4 / x([m]Q)
```

for `m=1..16`, asking whether:

```text
d4(K) = +/- d3(phi_m(K)).
```

This is a real sqrt-beating test: a stable positive would mean later tower
gates reuse one K-line character under a named recurrence.  The result is
negative.  In the promotion fields, the only full-coverage map is identity
or the already-killed q1471 `4/K` artifact, and it scores like raw `d4` bias.
All nontrivial maps have too little coverage to define a sampler.

## Probe

Gate:

```text
research/p27/archive/gates/p27_k_lattes_recurrence_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_k_lattes_recurrence_probe_20260621.txt
research/p27/archive/probe_outputs/p27_k_lattes_recurrence_probe_extended_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_k_lattes_recurrence_probe.py \
  --small-primes 1471,1607,1847 \
  --multipliers 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 \
  --limit 16 \
  | tee research/p27/archive/probe_outputs/p27_k_lattes_recurrence_probe_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_k_lattes_recurrence_probe.py \
  --small-primes 607,863,991,1087,1471,1607,1847,1951,1999,2039 \
  --multipliers 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 \
  --limit 10 \
  | tee research/p27/archive/probe_outputs/p27_k_lattes_recurrence_probe_extended_20260621.txt
```

## Promotion Fields

For `q=1471`:

```text
d3 K rows = 50
d4 K rows = 28
full coverage maps = 2
best full coverage = 14/28 = 0.500000000
```

The two full-coverage maps are `m=1` with torsion `O`, and `m=1` followed by
`(0,0)`, i.e. the q1471-local `K -> 4/K` closure.  Both are flat.  The best
nontrivial coverage is `12/28`, also flat.

For `q=1607`:

```text
d3 K rows = 49
d4 K rows = 28
full coverage maps = 1
best full coverage = 19/28 = 0.678571429
```

The only full-coverage map is identity, and `19/28` is exactly the raw d4
majority.  The largest non-identity coverage is `13/28`, and the only exact
nontrivial overlap is `7/7`, only `25%` coverage.

For `q=1847`:

```text
d3 K rows = 63
d4 K rows = 45
full coverage maps = 1
best full coverage = 26/45 = 0.577777778
```

Again the only full-coverage map is identity, scoring as raw d4 majority.  The
largest non-identity coverage is `19/45`.

## Extended Fields

The small-field extension explains the possible false positives:

```text
q=607, 991, 1951, 2039: d4 is constant, so identity can look exact.
q=863: d4 is constant and identity is exact on 12/12 K rows.
q=1087: identity is full coverage but flat at 5/10.
```

These are field degeneracies already seen in earlier d4 screens, not stable
recurrences.  The promotion fields `q=1471,1607,1847` are the decisive ones.

## Interpretation

Positive:

```text
The K-line recurrence loophole is now explicitly tested.
The test works at the reduced Kummer level, not just on E'.
The negative result supports treating d4 as a fresh cover unless a real branch
class extraction says otherwise.
```

Negative:

```text
No small Lattes map K -> x([m]Q) gives a high-coverage d4-from-d3 law.
No composition with the rational 2-torsion map K -> 4/K promotes.
The identity scores are raw field bias, not recurrence structure.
```

## Continue / Kill

```text
continue = actual branch-class/genus extraction over P1_K and P1_Sroot
continue = compare d3 and d4 only after d3 branch class is named
continue = promote only a stable class, genus <=1 source, or cheap sampler

kill = K-line Lattes recurrences with m <= 16 as a sqrt-beating route
kill = d4-from-d3 via K -> 4/K or small multiplication maps
kill = promoting constant-d4 small fields as recurrence evidence
```

## Linked Artifacts

- Parent: [P27 E-Prime Signed-Doubling Kummer Screen](p27_eprime_signed_doubling_kummer_screen_20260621.md)
- Belyi involution audit: [P27 K/S Belyi Involution Audit](p27_k_belyi_involution_audit_20260621.md)
- K/S packet: [P27 K/S Branch-Extraction Packet](p27_ks_branch_extraction_packet_20260621.md)
- Gate: `research/p27/archive/gates/p27_k_lattes_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_k_lattes_recurrence_probe_20260621.txt`
- Extended output: `research/p27/archive/probe_outputs/p27_k_lattes_recurrence_probe_extended_20260621.txt`

```text
p27_k_lattes_recurrence_probe_rows=1/1
```
