# P27 Trace/Norm Half-Norm Test Card

Date: 2026-06-22

## Claim

The trace/norm lane is now a narrow theorem/evaluator task, not a bucket or
feature-search lane.

The known structure is:

```text
C: b^2 = 16 - a^4
E: v^2 = u^3 - u
u = 4/a^2
T = chi(y - 2) * h * vq
```

The `vq` component carries the `b -> -b` cocycle, while `h` and `chi(y-2)` are
b-invariant.  The missing win would be a theta/additive/Hilbert-90 identity on
the supersingular j=1728 curve that couples these half-norm phases and either
predicts a post-Dplus selected gate or gives a direct sampler/source map.

## Artifacts

Use these as the current trace/norm source of truth:

```text
research/p27/evidence/p27_tline_component_descent_20260621.md
research/p27/evidence/p27_hv_trace_coupling_audit_20260621.md
research/p27/evidence/p27_trace_norm_elliptic_line_coset_20260621.md
research/p27/evidence/p27_trace_norm_dplus_prefix_identity_20260621.md
research/p27/evidence/p27_trace_norm_post_dplus_screen_20260621.md
```

Evaluator:

```text
research/p27/archive/gates/p27_line_rational_evaluator.py
```

## Accepted Inputs

A useful proposal must be one of these:

```text
1. A rational squareclass R(a,u) on C/E whose chi(R) predicts domain_line,
   T_line, or a post-Dplus selected gate.

2. A theta/additive/Hilbert-90 identity on E: v^2=u^3-u that reduces to a
   finite-field squareclass test or source map.

3. A direct sampler/source map into Dplus plus a later selected gate, with
   raw-source denominator stated.
```

Do not ask for or test broad feature families.  The already-killed nearby
families are:

```text
small torsion/coset projections m=2,3,4,6,12
branch functions a, a±2, a^2±4, u, u±1, u^2±1
first 2-isogeny branch-character products
large-factor quotient collisions for m=345451 and small multiples
simple Tr/anti-Tr/Norm of H, V, HV, pref_HV, BC_HV
low-weight post-Dplus products from H/VQ/X/T_line/root atoms
```

## Machine Check

For any rational candidate `R(a,u)`, run the evaluator with at least four
heldout seeds:

```bash
for seed in 121 122 123 124; do
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
  python3 research/p27/archive/gates/p27_line_rational_evaluator.py \
    --seeds "$seed" \
    --chunks 0,1 \
    --tids 0:64 \
    --draws-per-thread 256 \
    --max-records 8192 \
    --expr candidate='R(a,u)' \
    | tee "research/p27/archive/probe_outputs/p27_line_candidate_${seed}_20260622.txt"
done
```

The evaluator variables are:

```text
a, a2, a4, u, u2
phi0, phi0_2, phi1, phi1_2, phim1, phim1_2
```

with:

```text
u = 4/a^2
phi0  = u - 1/u
phi1  = u*(u+1)/(u-1) - 2
phim1 = u*(u-1)/(u+1) + 2
```

For a non-rational theta/additive proposal, first provide the finite-field
squareclass, divisor, or source map it predicts, then add an evaluator or probe
for exactly that object.

## Promotion

Promote only if one of these holds:

```text
exact chi(R) identity for T_line, domain_line, or a named post-Dplus gate
>=1.25x heldout target/source_draw lift with a raw-source denominator
direct sampler into Dplus plus a later gate, not merely a conditional filter
explicit low-genus/theta source map controlling more than one selected gate
```

## Kill

Kill a proposal if:

```text
it only rederives Dplus as the first-two-gate prefix
it needs a killed visible branch/torsion/norm feature family
heldout lift is noise-scale or not stable across seeds 121..124
it reports conditional lift without raw-source accounting
it cannot be reduced to a finite-field squareclass, divisor, or source map
```

## Expert Ask

The narrow expert question is:

```text
On C: b^2 = 16 - a^4, equivalently E: v^2 = u^3 - u with p = 3 mod 4,
is there a theta/additive/Hilbert-90 identity coupling the h and vq
half-norm phases so that chi(y-2)*h*vq predicts a later selected halving
gate, or gives a direct source for the Dplus stratum plus a later gate?
```

The answer is useful only if it yields a named finite-field test, divisor
class, source map, or sharp obstruction.

```text
p27_trace_norm_halfnorm_test_card_rows=1/1
```
