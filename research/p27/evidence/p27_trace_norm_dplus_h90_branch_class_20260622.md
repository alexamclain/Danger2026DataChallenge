# P27 Trace/Norm Dplus H90 Branch Class

Date: 2026-06-22

## Claim

The normalized `Dplus` H90 quartic has no new first-resolvent class.  Its
quadratic resolvent is exactly the known domain-spin cover:

```text
z^2 = F = t*(t^2+2t-1)*(t^2+1)
```

The hard part is the second quadratic layer over the genus-5 cover
`E_h90(z)`:

```text
rho^2 = U_eta + z*W_eta
```

Online Magma prices that second layer with odd branch divisor degree `16`,
giving the already-observed genus `17`.  This is a useful obstruction: the
degree-4 cover is not secretly two cheap independent sourceable gates.  Any
win now needs a special relation of this second-layer Kummer class to `d3`, or
a non-obvious Prym/quotient.

Follow-up telemetry:
[P27 Trace/Norm Dplus H90 Payload Screen](p27_trace_norm_dplus_h90_payload_screen_20260622.md).
On production-style Dplus rows, `A_eta` and its opposite-eta variants are
already square, and low-weight products of `eta,U,W,rho` features do not
predict `d3` or `d4` on heldout.  This closes the cheap finite-field bucket
version of the branch-class idea.

Follow-up branch comparison:
[P27 Trace/Norm Dplus H90-X6 Coboundary Probe](p27_trace_norm_dplus_h90_x6_coboundary_20260622.md).
Simple H90 atoms and first-order `rho +/- atom` branch divisors have no exact
weight-`<=3` product for post-Dplus `chi(x6)`, and train skews do not hold out.
The remaining comparison is therefore exact Kummer/Prym structure, not a
finite-field sign bucket.

## Symbolic Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_h90_branch_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_branch_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_h90_branch_probe.py \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_branch_probe_20260622.txt
```

The verifier proves:

```text
U_eta^2 - F*Sprime^2 = F*W_eta^2
quartic = (rho^2 - (U_eta + z*W_eta))*(rho^2 - (U_eta - z*W_eta))
```

with both checks reporting:

```text
exact = 1
p27_trace_norm_dplus_h90_branch_probe_rows=1/1
```

## Formulas

Base:

```text
E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1)
B = t^2 + 1
C = t^2 + 2t - 1
F = t*C*B
Sprime = (t-1)^3*(t+1)^2*B
```

Quartic:

```text
rho^4 - 2*U_eta*rho^2 + F*Sprime^2 = 0
```

Resolvent and second layer:

```text
U_eta = 2*t^2*(t-1)*B^2*(eta*w + C)
W_eta = (t-1)*B*(4*t^3 + eta*B*w)
U_eta^2 - F*Sprime^2 = F*W_eta^2
rho^2 = U_eta + z*W_eta
```

## Magma Branch Pricing

Fixture:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_h90_branch_q607_magma.m
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_branch_q607_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_branch_q607_magma_20260622.xml
```

Command:

```bash
curl -sS \
  --data-urlencode input@research/p27/archive/fixtures/p27_trace_norm_dplus_h90_branch_q607_magma.m \
  https://magma.maths.usyd.edu.au/xml/calculator.xml \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_branch_q607_magma_20260622.xml
```

Results:

```text
RESULT h90_branch_base 1 2 608
RESULT h90_branch_F 4 8

RESULT h90_branch_delta 1 4 8
RESULT h90_branch_Leta 1 0 0
RESULT h90_branch_delta_over_F_Wsquare 1 0 0
RESULT h90_branch_resolvent 1 5 2 4
RESULT h90_branch_second_layer 1 12 16 5 17 2 4

RESULT h90_branch_delta -1 4 8
RESULT h90_branch_Leta -1 0 0
RESULT h90_branch_delta_over_F_Wsquare -1 0 0
RESULT h90_branch_resolvent -1 5 2 4
RESULT h90_branch_second_layer -1 12 16 5 17 2 4
```

Meaning:

```text
E_h90 has genus 1
F has odd branch divisor degree 8 on E_h90
Delta_eta = U_eta^2 - F*Sprime^2 has the same odd branch divisor as F
L_eta contributes no odd branch divisor after reduction on E_h90
the first resolvent cover has genus 5
the second layer over genus 5 has odd branch divisor degree 16
the full eta cover has genus 17 and degree 4 over E_h90
```

## Interpretation

Positive:

```text
The branch/Kummer class is explicit.
The first quadratic layer is exactly the known domain-spin cover.
The second-layer class has a concrete formula A_eta = U_eta + z*W_eta.
The cheap row-level payload screen is complete.
```

Negative:

```text
There is no hidden low-genus first-resolvent shortcut.
The second-layer branch divisor degree is 16, not a tiny sourceable support.
The A_eta squareclass is tautological after Dplus.
This does not justify GPU production by itself.
```

## Next Test

The next sqrt-beating test is no longer "decompose the quartic" broadly.  It is:

```text
compare A_eta = U_eta + z*W_eta on E_h90(z)
against the next selected gate d3 on the same or a mapped cover.
```

Promote only if:

```text
A_eta equals or predicts the d3 Kummer class,
A_eta recurs under the halving/trace-norm transition,
or a Prym/quotient split lowers the second-layer branch cost.
```

Kill if:

```text
d3 has an unrelated Kummer class over this cover,
or the second-layer branch divisor is generic under further quotient checks.
```

## Continue / Kill

```text
continue = compare A_eta to d3/d4 Kummer classes
continue = inspect Prym/quotient of the second-layer degree-2 cover
continue = use A_eta as the named payload for GPU telemetry only if cheap

kill = searching for a new first quadratic resolvent
kill = treating L_eta as branch support; it is square/even on E_h90
kill = low-weight eta/U/W/rho payload sign buckets
kill = simple rho +/- atom products as chi(x6) predictors
kill = treating eta quartic as sourceable without d3 coupling or quotient split
```

## Linked Artifacts

- Normalized quartic: [P27 Trace/Norm Dplus H90 Quartic Model](p27_trace_norm_dplus_h90_quartic_model_20260622.md)
- Payload screen: [P27 Trace/Norm Dplus H90 Payload Screen](p27_trace_norm_dplus_h90_payload_screen_20260622.md)
- H90/x6 coboundary: [P27 Trace/Norm Dplus H90-X6 Coboundary Probe](p27_trace_norm_dplus_h90_x6_coboundary_20260622.md)
- H90 quotient: [P27 Trace/Norm Dplus H90 Quotient](p27_trace_norm_dplus_h90_quotient_20260622.md)
- Relative descent: [P27 Trace/Norm Dplus Relative Descent](p27_trace_norm_dplus_relative_descent_20260622.md)
- GPU handoff: [P27 GPU Dplus-Native Source Handoff](p27_gpu_dplus_native_source_handoff_20260622.md)

```text
p27_trace_norm_dplus_h90_branch_class_rows=1/1
```
