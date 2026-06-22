# P27 Signature-Field Branch-Divisor Replay

Date: 2026-06-21

## Claim

After the guard-field signature audit, the low-degree K/S branch-divisor
screens were replayed using p27-compatible fields only:

```text
p27 mod 16 = 7
promotion fields here: q = 7 mod 16
```

The result is negative for the decisive `d3` source bit.  There is no exact
K-line or S-root split branch divisor of degree `<=4` on the tested
p27-signature fields.

The `d4` K-line has small degree-3 fits in q1607 and q2087, but not q1847.
Because `d4` is only relevant after a stable `d3` source is named, and because
the q1607/q2087 factors do not survive q1847, these remain local finite-row
interpolation artifacts rather than a sqrt-beating route.

## Probes

K-line command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kummer_branch_divisor_probe.py \
  --small-primes 1607,1847,2039 \
  --targets d3,d4 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kummer_branch_divisor_signature_fields_20260621.txt
```

S-root command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_sroot_branch_divisor_probe.py \
  --small-primes 1607,1847,2039 \
  --targets d3,d4 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_branch_divisor_signature_fields_20260621.txt
```

Clean nonconstant d4 add-on:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kummer_branch_divisor_probe.py \
  --small-primes 2087 \
  --targets d3,d4 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kummer_branch_divisor_q2087_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_sroot_branch_divisor_probe.py \
  --small-primes 2087 \
  --targets d3,d4 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_branch_divisor_q2087_20260621.txt
```

## Results

### K-Line

For `d3`:

```text
q1607: rows=49, plus/minus=28/21, exact degree <=4 = none
q1847: rows=63, plus/minus=45/18, exact degree <=4 = none
q2039: rows=51, plus/minus=19/32, exact degree <=4 = none
q2087: rows=57, plus/minus=25/32, exact degree <=4 = none
```

For `d4`:

```text
q1607: rows=28, plus/minus=19/9,  degree-3 local fits exist
q1847: rows=45, plus/minus=19/26, exact degree <=4 = none
q2039: rows=19, plus/minus=19/0,  constant field; not promotion evidence
q2087: rows=25, plus/minus=18/7,  degree-3 local fits exist
```

The q1607 and q2087 `d4` degree-3 fits are different field-local factors.
They are killed as a stable source by q1847.

### S-Root

For `d3`:

```text
q1607: rows=98,  plus/minus=56/42, exact degree <=4 = none
q1847: rows=126, plus/minus=90/36, exact degree <=4 = none
q2039: rows=102, plus/minus=38/64, exact degree <=4 = none
q2087: rows=114, plus/minus=50/64, exact degree <=4 = none
```

For `d4`:

```text
q1607: rows=56, plus/minus=38/18, exact degree <=4 = none
q1847: rows=90, plus/minus=38/52, exact degree <=4 = none
q2039: rows=38, plus/minus=38/0,  constant field; not promotion evidence
q2087: rows=50, plus/minus=36/14, exact degree <=4 = none
```

## Interpretation

Positive:

```text
The q mod 16 correction did not revive a missed low-degree K/S branch divisor.
The decisive d3 bit is negative on four p27-signature fields.
S-root remains cleaner than K for d4: no degree <=4 split divisors appeared.
```

Negative:

```text
No rational or elliptic split branch divisor of degree <=4 explains d3.
The K-line d4 degree-3 positives do not survive q1847.
q2039 is useful for d3 but unusable for d4 promotion because d4 is constant.
```

This strengthens the current K/S rule: do not widen visible coefficient or
split-divisor scans.  The only remaining K/S moonshot test worth treating as
first-class is actual normalization/branch-class/genus extraction over
`P^1_K` or `P^1_Sroot` in p27-signature fields.

## Continue / Kill

```text
continue = K/S function-field extraction over q = 7 mod 16 fields
continue = use q1607/q1847/q2087 as the first nonconstant d4 comparison set
continue = promote only a recovered branch class, genus <=1 source, recurrence, or sampler

kill = K or S split branch divisors of degree <=4 for d3
kill = q1607/q2087-only K-line d4 degree-3 fits
kill = q2039 d4 constants as source evidence
```

## Linked Artifacts

- Guard-field audit: [P27 Guard-Field Signature Audit](p27_guard_field_signature_audit_20260621.md)
- K/S packet: [P27 K/S Branch-Extraction Packet](p27_ks_branch_extraction_packet_20260621.md)
- K-line output: `research/p27/archive/probe_outputs/p27_kummer_branch_divisor_signature_fields_20260621.txt`
- S-root output: `research/p27/archive/probe_outputs/p27_sroot_branch_divisor_signature_fields_20260621.txt`
- q2087 K output: `research/p27/archive/probe_outputs/p27_kummer_branch_divisor_q2087_20260621.txt`
- q2087 S output: `research/p27/archive/probe_outputs/p27_sroot_branch_divisor_q2087_20260621.txt`

```text
p27_signature_field_branch_divisor_replay_rows=1/1
```
