# P27 B-Parameter Base-Curve Sampler Probe

Date: 2026-06-22

## Claim

The K/A base curve becomes cleaner after adjoining `B` with `A = B^2 - 2`.
In those coordinates there is a stable all-recall bucket that keeps every
observed legal row in the guard fields while shrinking the B-parameter rows by
about `8x`.

This is real structure and is worth a bounded GPU telemetry probe.  It is not
yet a production GPU source or a sqrt-beating mechanism, because the remaining
domain is still field-sized and the sharper high-lift buckets are not stable
enough to be a law.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_base_param_sampler_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kline_base_param_sampler_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_kline_base_param_sampler_probe_q1607_q1847_q2087_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_base_param_sampler_probe.py \
  --small-primes 607 \
  --max-weight 4 \
  --top 8 \
  --min-bucket 8 \
  | tee research/p27/archive/probe_outputs/p27_kline_base_param_sampler_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_base_param_sampler_probe.py \
  --small-primes 1607,1847,2087 \
  --max-weight 4 \
  --top 12 \
  --min-bucket 12 \
  | tee research/p27/archive/probe_outputs/p27_kline_base_param_sampler_probe_q1607_q1847_q2087_20260622.txt
```

## Parameterization

With `L = K^2`, the K/A base curve rationalizes as:

```text
A = B^2 - 2
branch0: L = -(B + 2)^4 / (8 B (B - 2)^2)
branch1: L =  (B - 2)^4 / (8 B (B + 2)^2)
```

The probe enumerates `(K,A,B,L,branch)` rows and compares them with the
actually realized label-2 / compactD legal rows.

## Stable Bucket

Across q607/q1607/q1847/q2087, every realized legal `d2` row and every
realized `d3plus` row lies in the same core bucket family:

```text
atoms: K, B+2, B-2, L
bits:  0, 0,   1,   0
```

Equivalent presentations replace `L` by `K^2+4` or replace the final bit with
`B^2-4`, `A+2`, or `A-2` using the corresponding bit convention.

Promotion-field counts for the `K * (B+2) * (B-2) * L` bucket:

```text
q1607 d2:     98 / 398, precision 0.246231156, recall 1.0, lift 8.050251
q1847 d2:    126 / 458, precision 0.275109170, recall 1.0, lift 8.043668
q2087 d2:    114 / 518, precision 0.220077220, recall 1.0, lift 8.038610

q1607 d3plus: 56 / 398, precision 0.140703518, recall 1.0, lift 8.050251
q1847 d3plus: 90 / 458, precision 0.196506550, recall 1.0, lift 8.043668
q2087 d3plus: 50 / 518, precision 0.096525097, recall 1.0, lift 8.038610
```

The all-recall lift is essentially the same in all fields, so this is not just
a q607 artifact.

## Higher-Lift Buckets

The best four-atom buckets often have higher lift, roughly `9x` to `12x`, but
they capture only about `50%` to `72%` of the observed positives and their
extra atom is not stable across q1607/q1847/q2087.

Examples:

```text
q1607 d2:     K, K+1, B+2, B-2     precision 0.306122449, recall 0.612244898
q1847 d2:     K, B+2, B-2, 3A+10   precision 0.324561404, recall 0.587301587
q2087 d2:     K, B+2, B-2, B^2+1   precision 0.261194030, recall 0.614035088

q1607 d3plus: K, B+2, B-2, A+14    precision 0.190000000, recall 0.678571429
q1847 d3plus: K, B+2, B-2, 3A+10   precision 0.236842105, recall 0.600000000
q2087 d3plus: K, K-1, B+2, B-2     precision 0.146341463, recall 0.720000000
```

These are telemetry candidates, not theorem candidates.

## Interpretation

Positive:

```text
The B-rationalized base curve exposes a reproducible all-recall 8x scope
shrink.
The stable bucket is a clean GPU telemetry target because it is a small number
of squareclass bits.
The result gives a concrete algebraic boundary for the legal cover over the
K/A base curve.
```

Negative for the moonshot:

```text
The 8x bucket is still constant-factor only.
The bucket domain is still field-sized, not below sqrt(p).
The sharper partial buckets are field-sensitive and cannot be treated as a law
without more structure.
This does not justify a large GPU production run by itself.
```

## GPU Recommendation

Run a bounded same-stream GPU telemetry test only if the implementation can
cheaply emit the B-bucket bits along the existing p27 recurrence path:

```text
chi(K)
chi(B+2)
chi(B-2)
chi(L) or chi(K^2+4)
```

Report:

```text
bucket counts
throughput cost
accepted/deep survivor distribution inside and outside the all-recall bucket
whether any partial high-lift bucket survives p27-scale telemetry
```

Do not launch a large p27 GPU hunt from this alone.  A production-scale GPU run
still needs a direct legal-pullback sampler, a multi-gate coupling law, or a
measured per-second survivor lift that beats the full exchange-rate cost.

## Continue / Kill

```text
continue = bounded GPU telemetry for the stable all-recall B bucket
continue = function-field/CAS extraction of the legal cover over the B curve
continue = search for a multi-gate coupling law inside the B bucket

kill = direct sampling of the full K/A or B base curve
kill = treating 8x all-recall shrink as sqrt-beating
kill = promoting field-sensitive higher-lift buckets without a theorem
```

```text
p27_kline_base_param_sampler_rows=1/1
```
