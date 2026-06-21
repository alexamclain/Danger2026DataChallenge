# P27 T-Line Component Descent

Date: 2026-06-21

## Claim

The remaining `T_line` selector splits into a clean b-flip/cocycle factor and
several b-invariant half-norm factors, but no single component explains
`T_line`.

The defining signs are:

```text
D = -x_pref * vq * h
T = D * chi(y)
T_line = T                  if chi(a)=+1
       = T * chi(b)         if chi(a)=-1
```

The medium p27 component audit shows:

```text
vq carries the b -> -b cocycle exactly:
  vq(a,-b) / vq(a,b) = chi(a)

h, x_pref, chi(y), and pref=-x_pref*chi(y) are b-invariant.
```

Thus the line normalization is not arbitrary: it cancels the `vq` cocycle.
The remaining theorem target is a coupling identity for the line-descended
components, not a search for which raw factor descends.

## Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_tline_component_descent_gate.py
```

Run:

```bash
python3 research/p27/archive/gates/p27_tline_component_descent_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --top 20 \
  | tee research/p27/archive/probe_outputs/p27_tline_component_descent_64tid_2chunk_256draw_20260621.txt
```

## Result

Sample:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
component_rows = 16096
component_unusable = 16768
quotient_relation_fail = 0
```

B-flip ratios over `8048` pairs:

```text
x_pref: invariant = 8048
y:      invariant = 8048
pref:   invariant = 8048
h:      invariant = 8048

vq:        matches_chi_a = 8048
h_vq:      matches_chi_a = 8048
pref_vq:   matches_chi_a = 8048
D:         matches_chi_a = 8048
T:         matches_chi_a = 8048
line_norm: matches_chi_a = 8048

T_line: invariant = 8048
```

Line-descended single components, scored against `T_line`, are flat or
near-flat:

```text
x_pref raw best_lift = 1.010891650
y raw best_lift = 1.024741992
pref raw best_lift = 1.010959131
h raw best_lift = 1.003157475
vq p26line best_lift = 1.007151377
h_vq p26line best_lift = 1.004499329
pref_h raw best_lift = 1.012120057
pref_vq p26line best_lift = 1.002660494
D p26line best_lift = 1.028712898
```

Only the tautological recombination is exact:

```text
T p26line exact_plus = 1
T_line raw exact_plus = 1
```

## Algebra Notes

The `pref` component simplifies:

```text
x_pref = chi(-y(y-2)) = chi(1 - t^2)
y = t + 1
pref = -x_pref*chi(y)
     = chi(t - 1)
     = chi(y - 2)
```

So `T` can be viewed as:

```text
T = chi(y - 2) * h * vq
```

with `vq` the unique observed carrier of the `chi(a)` b-flip cocycle.

## Interpretation

Positive:

```text
The T_line obstruction is localized:
  vq carries the b-flip cocycle.
  h and pref are b-invariant.
  line_norm cancels exactly the vq cocycle.
```

Negative:

```text
No single component or simple normalized component explains T_line.
The useful theorem target is not "find which factor"; it is "explain the
coupling chi(y-2)*h*(vq normalized by chi(a),chi(b))."
```

## Continue / Kill

```text
continue = derive half-norm/descent identity for h
continue = derive half-norm/descent identity for vq with its chi(a) b-cocycle
continue = ask for theta/additive identity coupling h and vq on E: v^2=u^3-u

kill = treating h, vq, pref, or D alone as the missing selector
kill = another one-factor line character screen
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_tline_component_descent_gate.py`
- Output: `research/p27/archive/probe_outputs/p27_tline_component_descent_64tid_2chunk_256draw_20260621.txt`
- Related: [P27 Line Half-Norm And Joint Stratum](p27_line_half_norm_joint_stratum_20260621.md)
- Related: [P27 Trace/Norm Transfer Gate](p27_trace_norm_transfer_gate_20260621.md)

```text
p27_tline_component_descent_rows=1/1
```

