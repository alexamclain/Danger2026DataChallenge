# P27 Component Involution Boundary

Date: 2026-06-21

## Claim

The quotient involution gives a clean Hilbert-90-shaped boundary for the
remaining `T_line` coupling.

Under the involution:

```text
sigma(t) = -1/t
sigma(w) = w/t^2
```

which preserves the quotient coordinates `(a,b)`, the component signs satisfy:

```text
pref(sigma) / pref = -chi(a)
(h*vq)(sigma) / (h*vq) = -chi(a)
D(sigma) / D = chi(a)
T(sigma) / T = 1
T_line(sigma) / T_line = 1
```

So `pref=chi(y-2)` and `h*vq` are two different solutions to the same
squareclass boundary.  The descended selector is their quotient/product:

```text
T = pref * h * vq
```

This is a better theorem target than another branch-divisor scan.

## Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_component_involution_gate.py
```

Run:

```bash
python3 research/p27/archive/gates/p27_component_involution_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  | tee research/p27/archive/probe_outputs/p27_component_involution_64tid_2chunk_256draw_20260621.txt
```

## Result

Sample:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
comparable_rows = 16096
```

For the quotient involution `neg_inv_t`:

```text
pref:  exact = -a_chi, -h_norm, -v_norm
h_vq:  exact = -a_chi, -h_norm, -v_norm
D:     exact =  a_chi,  h_norm,  v_norm
T:     ratio_+1 = 16096, ratio_-1 = 0
T_line: ratio_+1 = 16096, ratio_-1 = 0
```

The individual factors `h` and `vq` still have no simple exact ratio against
the named reference squareclasses.  The structure appears only after coupling
them as `h*vq`.

## Interpretation

Positive:

```text
The T selector is now a quotient of two same-boundary Hilbert-90 sign objects.
This is theorem-shaped and compact enough to show an expert.
```

Negative:

```text
This does not yet produce a sampler.  It proves/describes descent of T, not a
cheap enumeration of the T_line=+1 stratum.
```

## Continue / Kill

```text
continue = ask whether the same-boundary quotient pref/(h*vq), or pref*h*vq,
           is known as a theta multiplier, additive character, Weil-pairing, or
           Kummer/Hilbert-90 descent class on C: b^2=16-a^4
continue = build gates only for named formulas that claim to evaluate this
           descended quotient on the a-line

kill = testing h and vq as independent line selectors
kill = more branch/norm product searches that do not use the involution boundary
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_component_involution_gate.py`
- Output: `research/p27/archive/probe_outputs/p27_component_involution_64tid_2chunk_256draw_20260621.txt`
- Related: [P27 Component Norm / Half-Norm Audit](p27_component_norm_halfnorm_audit_20260621.md)
- Related: [P27 T-Line Component Descent](p27_tline_component_descent_20260621.md)

```text
p27_component_involution_boundary_rows=1/1
```
