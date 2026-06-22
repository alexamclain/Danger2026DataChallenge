# P27 Trace/Norm Automorphism Quotient Obstruction

Date: 2026-06-22

## Claim

The remaining trace/norm `T_line` object descends under exactly the quotient
involution used by the half-norm model, but not under the other visible
automorphisms of the `t`-line.

This sharpens the theorem ask: a useful identity must live on the
`sigma(t)=-1/t` quotient / `C: b^2=16-a^4` / `E: v^2=u^3-u` model.  There is
no smaller easy quotient from `t -> 1/t` or `t -> -t`.

## Artifacts

Gate:

```text
research/p27/archive/gates/p27_component_involution_gate.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_component_involution_heldout_121_124_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_component_involution_gate.py \
  --seeds 121,122,123,124 \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 256 \
  --top-matches 8 \
  | tee research/p27/archive/probe_outputs/p27_component_involution_heldout_121_124_20260622.txt
```

## Result

Heldout sample:

```text
raw_draws = 131072
nonsplit_y = 65475
k_points = 130950
comparable_rows = 65120 per transform
```

Under the quotient involution:

```text
sigma(t) = -1/t
T_line ratio +1/-1 = 65120/0
pref boundary exact = -chi(a)
h*vq boundary exact = -chi(a)
D boundary exact = chi(a)
```

Under the other visible automorphisms, `T_line` is mixed:

```text
t -> 1/t:
  T_line ratio +1/-1 = 32568/32552
  exact reference = none

t -> -t:
  T_line ratio +1/-1 = 32568/32552
  exact reference = none
```

The same mixed split appears for `T`, while `line_norm` has only the expected
`b_chi` boundary under those transforms.  Thus the obstruction is not sample
noise or a missing sign convention: the `T_line` class is tied to the
`-1/t` quotient.

## Interpretation

Positive:

```text
The same-boundary Hilbert-90 picture survives a four-seed heldout check.
The exact quotient is now sharply identified.
```

Negative:

```text
No descent to the smaller visible automorphism quotients appears.
The remaining identity is not a simple automorphism-orbit class on the t-line.
```

## Continue / Kill

```text
continue = expert/theorem ask on C: b^2=16-a^4 or E: v^2=u^3-u
continue = test only named finite-field squareclass/source maps on that quotient
continue = use p27_line_rational_evaluator.py for any proposed descended R(a,u)

kill = smaller quotient explanations using t -> 1/t or t -> -t
kill = automorphism-orbit bucket scans for T_line
kill = trying to make T_line a visible t-line orbit class
```

```text
p27_trace_norm_automorphism_quotient_obstruction_rows=1/1
```
