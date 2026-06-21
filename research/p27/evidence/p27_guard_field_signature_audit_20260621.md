# P27 Guard-Field Signature Audit

Date: 2026-06-21

## Claim

For K/S orbit and recurrence claims, p27 promotion fields should match the
target's 2-adic sign regime:

```text
p27 = 10^27 + 103
p27 mod 16 = 7
v2(p27 + 1) = 3
```

The right finite-field promotion class for these K/S tests is therefore
`q = 7 mod 16`, not merely `q = 7 mod 8`.  Fields with `q = 15 mod 16`
have an extra 2-adic layer and can create false `K -> 4/K` closures.

## Probe

Gate:

```text
research/p27/archive/gates/p27_guard_field_signature_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_guard_field_signature_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_guard_field_signature_probe.py \
  --min-q 607 \
  --max-q 5000 \
  | tee research/p27/archive/probe_outputs/p27_guard_field_signature_probe_20260621.txt
```

The probe reuses the K/S row collector and Belyi transform stats, then audits
all primes `q = 7 mod 8` in `[607,5000]`, split by `q mod 16`.

## Result

Summary:

```text
fields = 144

q_mod16 = 7:
  fields = 73
  d3_4K_absent = 73
  d4_4K_absent = 73
  d4_constant = 33
  d4_nonconstant = 40
  total_d3_rows = 6374
  total_d4_rows = 3239

q_mod16 = 15:
  fields = 71
  d3_4K_absent = 37
  d3_4K_full_opposite = 17
  d3_4K_partial = 17
  d4_4K_absent = 57
  d4_4K_full_opposite = 8
  d4_4K_partial = 6
  d4_constant = 32
  d4_nonconstant = 39
  total_d3_rows = 5899
  total_d4_rows = 2957
```

Every tested `q = 7 mod 16` field had `K -> 4/K` absent on both selected
`d3` and selected `d4` K rows.  All full or partial `K -> 4/K` closures came
from `q = 15 mod 16` fields.

The `d4_constant` behavior is not solely explained by this split: it appears
at similar frequency in both groups.  The narrow conclusion is about
`K -> 4/K` orbit closures and any Lattes/recurrence positive that depends on
that orbit.

## Interpretation

The earlier q1471-looking K/S symmetry was not just "small-field noise"; it
was using a field with the wrong 2-adic signature for this p27 claim:

```text
q1471 mod 16 = 15
v2(q1471 + 1) = 6
```

That explains why q1471 supports the tempting `K -> 4/K` artifact while the
p27-signature fields q1607, q1847, q2039, and the full `q = 7 mod 16` audit
do not.

Going forward:

```text
promote = K/S orbit or recurrence positives surviving q = 7 mod 16 fields
demote = q1471-only or q = 15 mod 16-only K/S orbit positives
keep = q = 15 mod 16 fields as stress/falsifier fields, not promotion fields
```

## Continue / Kill

```text
continue = actual K/S branch-class and genus extraction over q = 7 mod 16 fields
continue = use q1471 as a stress checksum only after q = 7 mod 16 survival
continue = reroute future K/S promotion language to q1607/q1847/q2039-style fields

kill = promoting q1471-only K -> 4/K closure
kill = treating q = 15 mod 16 Lattes positives as p27-compatible structure
kill = broad q = 7 mod 8 guard-field claims for 2-adic-sensitive K/S orbits
```

## Linked Artifacts

- Belyi involution audit: [P27 K/S Belyi Involution Audit](p27_k_belyi_involution_audit_20260621.md)
- Lattes recurrence screen: [P27 K-Line Lattes Recurrence Screen](p27_k_lattes_recurrence_20260621.md)
- K/S packet: [P27 K/S Branch-Extraction Packet](p27_ks_branch_extraction_packet_20260621.md)
- Gate: `research/p27/archive/gates/p27_guard_field_signature_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_guard_field_signature_probe_20260621.txt`

```text
p27_guard_field_signature_probe_rows=1/1
```
