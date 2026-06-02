# p23 References and Attribution

This page centralizes the literature and provenance behind the p23 search.

## Used In The Winning Method

### Prescribed torsion / `X1(N)` sampling

Andrew V. Sutherland, "Constructing elliptic curves over finite fields with
prescribed torsion", Mathematics of Computation 81 (2012), 1131-1147.

```text
https://arxiv.org/abs/0811.0296
```

Sutherland's optimized modular-curve equation tables:

```text
https://math.mit.edu/~drew/X1_altcurves.html
https://math.mit.edu/~drew/X1_optcurves.html
```

Role in this result:

```text
The production search used the X1(16) prescribed-torsion family to sample
curves with a known rational point of order 16, then mapped those curves into
Montgomery form.
```

### 2-Sylow halving perspective

J. Miret, R. Moreno, A. Rio, M. Valls, "Determining the 2-Sylow subgroup of an
elliptic curve over a finite field", Mathematics of Computation 74 (2005),
411-427.

```text
https://doi.org/10.1090/S0025-5718-04-01640-0
```

Role in this result:

```text
The known order-16 point was tested for deeper rational 2-adic divisibility by
successive halving, aiming for the p23 verifier depth k = 39.
```

### Montgomery split/nonsplit structure

The split/nonsplit classifier is standard Montgomery-curve 2-torsion
arithmetic:

```text
E_A: v^2 = u^3 + A*u^2 + u
split    iff chi(A^2 - 4) =  1
nonsplit iff chi(A^2 - 4) = -1
```

Local p23 synthesis:

```text
For the X1(16) y-parameter:
chi(A^2 - 4) = chi((y^2 - 2)(y^2 - 4y + 2)).
```

Role in this result:

```text
This gave a cheap y-level nonsplit filter before constructing A. In the
nonsplit Montgomery case, the rational 2-Sylow subgroup is cyclic, so
first-branch halving is complete for survival.
```

Detailed local notes:

```text
research/p23/x16_split_nonsplit_pullback_proof.md
research/p23/x16_nonsplit_branch_collapse_proof_20260601.md
```

## Scaling Interpretation

### Gonality / generic growing `X1(N)` barrier

Dan Abramovich, "A linear lower bound on the gonality of modular curves".

```text
https://arxiv.org/abs/alg-geom/9609012
```

Maarten Derickx and Mark van Hoeij, "Gonality of the modular curve X1(N)",
Journal of Algebra 417 (2014), 52-71.

```text
https://arxiv.org/abs/1307.5719
```

Mark van Hoeij and Hanson Smith, "A Divisor Formula and a Bound on the
Q-gonality of the Modular Curve X1(N)".

```text
https://arxiv.org/abs/2004.13644
```

Role in this result:

```text
These references frame why fixed X1(16) is a constant-factor improvement, while
generic growing X1(N) sampling is not an automatic asymptotic sub-sqrt route:
the density gain is roughly N, but generic X1(N) fiber/gonality cost grows
roughly like N^2.
```

Detailed local note:

```text
research/p23/prescribed_torsion_scaling_barrier_20260602.md
```

## Challenge / Verification

Andrew Sutherland's DANGER3 repository:

```text
https://github.com/AndrewVSutherland/DANGER3
```

Role in this result:

```text
The final triple was checked against DANGER3 vpp.py, OpenSSL primality, and an
independent Montgomery doubling replay.
```

## Prior Local Experiments

Sibling short-certificate experiments repo:

```text
https://github.com/alexamclain/danger3-short-certificate-experiments
```

Role in this result:

```text
This repo did not provide the winning search method directly. It provided the
split/nonsplit Montgomery discriminant axis as a useful clue. The p23 search
then transferred that axis to the X1(16) y-line and used the opposite sign:
nonsplit rather than split.
```

Detailed local note:

```text
research/p23/danger3_short_certificate_transfer_recap_20260601.md
```
