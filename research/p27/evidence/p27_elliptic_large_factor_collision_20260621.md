# P27 Elliptic Large-Factor Collision Audit

Date: 2026-06-21

## Claim

The descended `domain_line` and `T_line` bits are not determined by the tested
large-factor quotient classes on the elliptic model

```text
E: v^2 = u^3 - u
```

The small torsion audit had already killed `m=2,3,4,6,12`.  This pass tests
the p27-specific factor `345451` and small multiples of it.  Repeated
projection classes are mixed at roughly random rates, so the earlier
class-majority scores are not meaningful selectors.

## Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_elliptic_large_factor_collision_gate.py
```

Main run:

```bash
python3 research/p27/archive/gates/p27_elliptic_large_factor_collision_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --top 4 \
  | tee research/p27/archive/probe_outputs/p27_elliptic_large_factor_collision_64tid_2chunk_256draw_20260621.txt
```

Held-out run:

```bash
python3 research/p27/archive/gates/p27_elliptic_large_factor_collision_gate.py \
  --seeds 122 \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --moduli 345451,4145412 \
  --top 2 \
  | tee research/p27/archive/probe_outputs/p27_elliptic_large_factor_collision_seed122_20260621.txt
```

## Result

Main sample:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
domain_records = 16432
target_records = 8048
```

For `T_line` at `m=345451`:

```text
unsigned:
  non_singleton_classes = 178
  mixed_classes = 99
  collision_pairs = 184
  disagree_pairs = 101
  disagree_rate = 0.548913043

signed:
  non_singleton_classes = 88
  mixed_classes = 48
  collision_pairs = 92
  disagree_pairs = 50
  disagree_rate = 0.543478261
```

For `T_line` at `m=4145412 = 12*345451`:

```text
unsigned:
  non_singleton_classes = 27
  mixed_classes = 17
  collision_pairs = 27
  disagree_pairs = 17
  disagree_rate = 0.629629630

signed:
  non_singleton_classes = 14
  mixed_classes = 7
  collision_pairs = 14
  disagree_pairs = 7
  disagree_rate = 0.500000000
```

Held-out seed `122`:

```text
T_line, m=345451, unsigned disagree_rate = 0.502439024
T_line, m=345451, signed   disagree_rate = 0.500000000
T_line, m=4145412, unsigned disagree_rate = 0.424242424
T_line, m=4145412, signed   disagree_rate = 0.444444444
```

Projected-point characters were also flat/noise-scale:

```text
main best T_line projected char lift <= 1.019605204
held-out best T_line projected char lift <= 1.005705224
exact projected characters = 0
```

## Interpretation

Positive:

```text
This is a much sharper falsifier than the earlier majority-class score.
It tests a p27-specific large factor and confirms that repeated quotient
classes do not carry a consistent bit.
```

Negative:

```text
The line bits are not simple functions of the tested large-factor quotient
classes on E(F_p), either signed or modulo +/-.
Projected-point characters such as chi(x_m), chi(y_m), and chi(x_m^2+1) are
not exact and do not show stable lift.
```

## Continue / Kill

```text
continue = theta/additive/Kummer/Hilbert-90 identity tied to the component
           boundary, not a quotient-class lookup
continue = GPU same-stream line telemetry for practical survivor lift

kill = small torsion/coset explanations m=2,3,4,6,12
kill = large-factor quotient explanations for m=345451 and small multiples
kill = projected-point characters as production filters
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_elliptic_large_factor_collision_gate.py`
- Main output: `research/p27/archive/probe_outputs/p27_elliptic_large_factor_collision_64tid_2chunk_256draw_20260621.txt`
- Held-out output: `research/p27/archive/probe_outputs/p27_elliptic_large_factor_collision_seed122_20260621.txt`
- Related: [P27 Trace/Norm Elliptic Line / Coset Audit](p27_trace_norm_elliptic_line_coset_20260621.md)
- Related: [P27 Component Involution Boundary](p27_component_involution_boundary_20260621.md)

```text
p27_elliptic_large_factor_collision_rows=1/1
```
