# P27 K-Line Cubic Stdin Probe

Date: 2026-06-22

## Claim

The reusable monic-cubic K-line solver confirms that small-field cubic fits are
not reliable promotion evidence.

The nearest genus-1 K-line source shape is:

```text
z^2 = cubic(K)
K = x([2]P) on E': V^2 = U^3 + 4U
```

The old hardcoded q607 pilot was negative.  The new generic solver reproduces
that result, finds many exact q863 cubics, and then finds no q991 cubic.  This
field-to-field instability means q863 exact cubics are local interpolation
artifacts, not a stable p27 source.

The remaining serious K-line task is still branch-cover/genus extraction in
the promotion fields, not wider small-field cubic fitting.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_cubic_stdin_probe.c
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q607_20260622.txt
research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q863_20260622.txt
research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q991_20260622.txt
```

Commands:

```bash
cc -O3 -o tmp/p27_kline_cubic_stdin_probe \
  research/p27/archive/gates/p27_kline_cubic_stdin_probe.c

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 - <<'PY' | ./tmp/p27_kline_cubic_stdin_probe \
  | tee research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q607_20260622.txt
from p27_k_belyi_involution_probe import collect_rows
q=607
kd3, _kd4, _sd3, _sd4, _stats = collect_rows(q)
print(q, len(kd3))
for row in kd3:
    print(row.k, row.target)
PY

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 - <<'PY' | ./tmp/p27_kline_cubic_stdin_probe \
  | tee research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q863_20260622.txt
from p27_k_belyi_involution_probe import collect_rows
q=863
kd3, _kd4, _sd3, _sd4, _stats = collect_rows(q)
print(q, len(kd3))
for row in kd3:
    print(row.k, row.target)
PY

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 - <<'PY' | ./tmp/p27_kline_cubic_stdin_probe \
  | tee research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q991_20260622.txt
from p27_k_belyi_involution_probe import collect_rows
q=991
kd3, _kd4, _sd3, _sd4, _stats = collect_rows(q)
print(q, len(kd3))
for row in kd3:
    print(row.k, row.target)
PY
```

## Results

q607 replay:

```text
rows = 32
plus = 16
minus = 16
tested_monic_cubics = 223648543
exact_cubics = 0
exact_irreducible_cubics = 0
best = 31/32
```

q863:

```text
rows = 24
plus = 12
minus = 12
tested_monic_cubics = 642735647
exact_cubics = 58
exact_irreducible_cubics = 19
best = 24/24
```

q991:

```text
rows = 36
plus = 18
minus = 18
tested_monic_cubics = 973242271
exact_cubics = 0
exact_irreducible_cubics = 0
best = 34/36
```

## Interpretation

Positive:

```text
The reusable solver makes the cubic subcase easy to replay on any finite-field
K-row packet.
q607 reproduction matches the older hardcoded pilot exactly.
q991 gives a second balanced negative field.
```

Negative:

```text
q863 has many exact cubics, including irreducible cubics, but neighboring
balanced fields q607 and q991 have none.
Therefore a small-field exact cubic is not promotion evidence by itself.
No GPU sampler follows from these local cubic fits.
```

This also explains why q1471/q1607/q1847 remain the promotion fields: small
fields are useful falsifiers and sanity checks, but local exact fits can be
pure interpolation.

## Next Tests

Continue:

```text
Magma/Sage branch-cover normalization over P1_K in q1471/q1607/q1847
branch divisor degree, support field degrees, and genus
comparison of d4 only after a stable d3 branch class is named
```

Possible bounded CPU follow-up:

```text
Use the stdin solver only for a named K-row packet or a promotion-field subset.
Do not expand it into broad coefficient hunting.
```

Kill:

```text
q863 cubic formulas as source candidates
near-miss cubic scores as theorem candidates
production GPU based on K-line cubics without a stable promotion-field class
```

```text
p27_kline_cubic_stdin_probe_rows=1/1
```
