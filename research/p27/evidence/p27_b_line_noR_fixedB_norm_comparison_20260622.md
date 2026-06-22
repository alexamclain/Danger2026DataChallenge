# P27 B-Line No-R Fixed-B Norm Comparison

Date: 2026-06-22

## Claim

The fixed-`B` quadratic no-R classes both obey the formal finite-field norm
descent

```text
chi_GF(q^2)(Unext + 2) = chi_GF(q)(Norm_GF(q^2)/GF(q)(Unext + 2)),
```

and both are sign-uniform on each active base `B` row in the tested fields.
But the useful structure is still concentrated in `beta_U_fixedB`.

For `beta_U_fixedB`, the sign controls the fiber size:

```text
gamma = +1  <=>  16 beta_U points over B
gamma = -1  <=>  32 beta_U points over B
```

For `hidden_mixed_fixedB`, the visible fiber-size split is instead governed
by `chi(B)`:

```text
chi(B) = +1  =>  32 hidden_mixed points over B
chi(B) = -1  =>  64 hidden_mixed points over B
```

The hidden-mixed `gamma` sign is uniform per `B`, but it is not the visible
half-size/full-size split.  So `hidden_mixed_fixedB` remains a secondary
divisor/Kummer extraction target, not the first route to a source sampler.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_fixedB_norm_descent_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_norm_descent_probe_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_norm_descent_probe_q199_q263_q311_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_fixedB_norm_descent_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_norm_descent_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_fixedB_norm_descent_probe.py \
  --fields 199^2,263^2,311^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_norm_descent_probe_q199_q263_q311_20260622.txt
```

## Result

Fields:

```text
23^2, 71^2, 103^2, 167^2, 199^2, 263^2, 311^2
```

For both classes in every tested field:

```text
gamma_norm_mismatch = 0
B_gamma_conflicts = 0
B_norm_chi_conflicts = 0
```

Beta_U profile:

```text
field    active B   beta_U points   visible support
23^2     2          64              chi(B)=+1
71^2     8          128             chi(B)=+1
103^2    12         384             chi(B)=+1
167^2    20         544             chi(B)=+1
199^2    24         512             chi(B)=+1
263^2    32         832             chi(B)=+1
311^2    38         960             chi(B)=+1
```

The detailed `B_summary_top` rows confirm the previous beta_U signature:
gamma-positive rows have `16` points and gamma-negative rows have `32` points.

Hidden-mixed profile:

```text
field    active B   hidden points   chi(B)=+1 points   chi(B)=-1 points
23^2     4          192             64                 128
71^2     16         768             256                512
103^2    24         1152            384                768
167^2    40         1920            640                1280
199^2    48         2304            768                1536
263^2    64         3072            1024               2048
311^2    76         3648            1216               2432
```

In the detailed rows, `chi(B)=+1` hidden-mixed rows have `32` points and
`chi(B)=-1` hidden-mixed rows have `64` points.  The hidden-mixed `gamma`
polarity varies across active `B` rows and across guard fields; the earlier
fixed-`B` character screen already found no stable low-degree visible
base-`B` law for that polarity.

## Interpretation

Positive:

```text
hidden_mixed_fixedB is not random pointwise noise; its gamma class also
descends through Norm(Unext+2) and is uniform on each active B row.
```

Negative:

```text
The norm descent itself is formal for a quadratic finite-field extension.
hidden_mixed_fixedB does not reproduce the beta_U gamma/fiber-size split.
The obvious hidden-mixed fiber-size split is chi(B), not gamma.
No GPU sampler follows from hidden_mixed norm descent.
```

## CAS Consequence

Keep the fixed-`B` CAS order:

```text
1. beta_U_fixedB:
   support = chi(B)=+1
   class   = N_B = Norm(Unext+2)
   target  = divisor/Kummer explanation of the gamma-controlled 16/32 split

2. hidden_mixed_fixedB:
   support = both chi(B)=+1 and chi(B)=-1 rows
   class   = N_B = Norm(Unext+2)
   target  = only a second-pass Kummer comparison after beta_U, unless a
             quotient explains gamma independently of the chi(B) 32/64 split
```

Promote hidden_mixed only if a divisor or quotient carries `gamma` and couples
to f3/f4 or produces a direct sampler.  Kill it as a practical GPU route if
the only visible result remains the `chi(B)` fiber-size split.

## Continue / Kill

```text
continue = beta_U divisor/Kummer extraction for Norm(Unext+2)
continue = compare hidden_mixed norm class after beta_U, not before
continue = ask CAS whether beta_U and hidden_mixed norm classes share a Prym factor

kill = treating hidden_mixed norm descent as a production filter
kill = using chi(B) 32/64 hidden-mixed split as the selected gamma sampler
kill = broad hidden_mixed base-B atom hunting without a named divisor class
```

```text
p27_b_line_noR_fixedB_norm_comparison_rows=1/1
```
