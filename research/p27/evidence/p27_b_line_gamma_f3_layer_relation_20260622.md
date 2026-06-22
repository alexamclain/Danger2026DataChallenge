# P27 B-Line Gamma Over F3/H90 Layer Relation Screen

Date: 2026-06-22

## Claim

After adjoining the explicit f3/H90 coordinate

```text
H^2 = u + 2,
```

the remaining class `gamma^2=v+2` still does not become visibly sourceable in
the screened low-degree coordinates.

The probe doubles each materialized pair by both sheets `H -> +/-H` and tests
the full layer and the `f4=+1` / `f4=-1` subcovers.  Stable pair-coordinate
screens in `(B,H)`, `(B,tau)`, `(B,H^2)`, and `(B,tau^2+tau^-2)` show no
field-stable low-degree relation producing the `f4` split.  The low-degree
triple relations in `(B,u,H)` are the known tautology `H^2=u+2`, not a new
gamma source law.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_gamma_f3_layer_relation_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_gamma_f3_layer_relation_probe_20260622.txt
```

Input fixture:

```text
research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_gamma_f3_layer_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --pair-degrees 2,4,6,8,10,12,14,16,18,20 \
  --triple-degrees 2,4,6,8,10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_gamma_f3_layer_relation_probe_20260622.txt
```

## Setup Checks

The f3/H90 layer identities held with zero failures:

```text
q1607: H2_minus_uplus2_fail = 0, tau_sym_formula_fail = 0
q1847: H2_minus_uplus2_fail = 0, tau_sym_formula_fail = 0
q2087: H2_minus_uplus2_fail = 0, tau_sym_formula_fail = 0
```

Row counts after doubling by `H -> +/-H`:

```text
q1607: h_layer_rows = 224, f4 plus/minus = 152/72
q1847: h_layer_rows = 360, f4 plus/minus = 152/208
q2087: h_layer_rows = 200, f4 plus/minus = 144/56
```

## Pair Screens

Stable all-layer pair systems:

```text
(B,H):        no stable extra relation through degree 20
(B,tau):      extra_nullity = 0 through degree 20 in all fields
(B,H^2):      extra_nullity = 0 through forced interpolation
(B,tau_sym):  extra_nullity = 0 through forced interpolation
```

The only all-layer exception is a tiny q1607-only `(B,H)` degree-20 extra
nullity.  It is killed by q1847 and q2087.

Sign subcovers:

```text
f4-plus (B,H):
  q1607/q1847 have small degree-16 extras,
  q2087 has no extra before forced interpolation.

f4-minus (B,H):
  q1607/q2087 have small tail extras,
  q1847 has no extra before forced interpolation.

f4-plus/minus (B,tau):
  the same extras are absent or killed by the third field.
```

So no plus/minus relation is stable across q1607/q1847/q2087.

## Triple Screens

The triple systems `(B,u,H)` and subcovers show low-degree relations because
the layer itself satisfies:

```text
H^2 = u + 2.
```

Likewise `(B,H,tau)` includes the Cayley relation between `H` and
`tau=(h-1)/(h+1)`.  These are layer-defining tautologies, not predictors of
`f4`.

## Interpretation

Positive:

```text
The f3/H90 layer is now explicitly included in the finite-field screen.
The screen is geometrically better than a one-sheet h fit because it includes
both H sheets.
```

Negative:

```text
No stable low-degree pair relation separates f4 after adjoining H^2=u+2.
The visible triple relations are the known f3/H90 layer equations.
No GPU bucket or direct sampler follows.
```

The live B-line moonshot is now very narrow:

```text
compute the actual divisor/Kummer class of gamma over the normalized f3/H90
layer, then test recurrence/telescoping at the next gate.
```

## Continue / Kill

```text
continue = offline CAS divisor/Kummer-class extraction for gamma on the f3/H90 layer
continue = compare the resulting class with the next f5/f4 construction
continue = ask for a theorem/source only after a named class or quotient appears

kill = visible pair-coordinate source laws on (B,H), (B,tau), (B,H^2), (B,tau_sym)
kill = treating H^2=u+2 or the Cayley H/tau relation as a gamma source
kill = GPU production from f3/H90-layer coordinate buckets
```

```text
p27_b_line_gamma_f3_layer_relation_rows=1/1
```
