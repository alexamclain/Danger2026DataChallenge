# P27 B-Line No-R B-Orbit Invariant Screen

Date: 2026-06-22

## Claim

The no-R `B_orbit` mechanism has a clean support signature but no visible
trace/norm/discriminant selector for `gamma`.

Across the tested degree-2 and degree-3 B-orbit fields, active B-orbits have:

```text
Norm(B) square
orbit discriminant nonsquare for degree 2
orbit discriminant square for degree 3
gamma_norm_mismatch = 0
Frobenius B-row signature mismatches = 0
```

That is useful CAS routing: B-orbit activity is not random noise.  But it is
not yet sourceable for the selected class.  The visible invariant screens do
not produce a stable gamma law, and the only exact cubic linear law appears in
`GF(7^3)` and fails in `GF(23^3)`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_borbit_invariant_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_borbit_invariant_probe_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_noR_borbit_invariant_probe_q167_q199_q263_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_borbit_invariant_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_borbit_invariant_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_borbit_invariant_probe.py \
  --fields 167^2,199^2,263^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_borbit_invariant_probe_q167_q199_q263_20260622.txt
```

## Result

Fields:

```text
23^2, 71^2, 103^2, 167^2, 199^2, 263^2, 7^3, 23^3
```

Global invariants:

```text
gamma_norm_mismatch = 0 in every field
b_signature_mismatch_orbits = 0 in every field
```

Degree-2 B-orbits:

```text
field    active B-orbits    dominant gamma profile
23^2     7                  all balanced half/half
71^2     100                all balanced half/half
103^2    196                all balanced half/half
167^2    552                mostly balanced; rare all-plus/all-minus
199^2    792                mostly balanced; rare all-plus/all-minus
263^2    1400               mostly balanced; rare all-plus/all-minus
```

The active degree-2 invariant signature is:

```text
chi(Norm(B)) = +1
chi(discriminant(B)) = -1
chi(Trace(B)) varies
```

In the larger degree-2 fields, the atom screen's best label for
`gamma_presence` is `e2 = Norm(B)`, but this is only the support law: `e2` is
square on all active orbits, so it cannot select the rare all-plus or all-minus
gamma rows.

Degree-3 B-orbits:

```text
GF(7^3):
  degree_3_orbits = 6
  gamma profiles = 3 absent, 3 half-present
  one exact linear character appears

GF(23^3):
  degree_3_orbits = 266
  gamma profiles = 61 absent, 133 half-present, 72 all-present
  best atom/linear screens miss by 61 orbits
```

The active degree-3 invariant signature is:

```text
chi(Norm(B)) = +1
chi(discriminant(B)) = +1
chi(Trace(B)) and chi(pair-sum(B)) vary
```

The `GF(7^3)` exact law is local interpolation.  In `GF(23^3)`, the best atom
for gamma presence is again `e3 = Norm(B)`, missing exactly the 61
gamma-absent orbits because `Norm(B)` is square on all active orbits.  The
best normalized linear character also misses by 61, so no visible
trace/norm/pair-sum law survives.

## Interpretation

Positive:

```text
B-orbit support is structured: active orbits have square Norm(B).
Gamma descends consistently to orbit-level finite-field data.
The CAS pass can use B-orbit invariants to separate this component from
fixed-B beta_U/hidden_mixed fibers.
```

Negative:

```text
Norm(B) is a support signature, not a selected gamma selector.
Degree-2 B-orbits are mostly or exactly half/half in gamma.
Degree-3 gamma presence/fullness is not carried by the tested atoms or
linear characters in trace/norm/pair-sum coordinates.
The exact GF(7^3) linear fit is killed by GF(23^3).
```

## CAS Consequence

The B-orbit subtest should now be phrased as:

```text
normalize the no-R component over active B-orbits with square Norm(B)
track the orbit discriminant sign by degree
test whether gamma lives on a quotient/Prym factor invisible to the base
trace/norm/discriminant coordinates
compare that factor with f3/f4
```

Do not ask a GPU agent to bucket by degree-2/degree-3 B-orbit invariants.  The
visible invariants identify support/components, not a sourceable selected
class.

## Continue / Kill

```text
continue = B-orbit component/quotient/Prym extraction with Norm(B) support noted
continue = compare B-orbit gamma class with beta_U Norm(Unext+2) after normalization
continue = keep GF(7^3) linear law only as a killed small-field artifact

kill = B-orbit trace/norm/discriminant character as gamma selector
kill = GPU production from B-orbit buckets
kill = treating square Norm(B) support as sqrt-beating
```

```text
p27_b_line_noR_borbit_invariant_screen_rows=1/1
```
