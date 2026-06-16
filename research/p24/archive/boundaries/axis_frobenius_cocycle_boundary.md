# Axis Frobenius Cocycle Boundary

This note checks a tempting proof shortcut for the module direct-sum target.

## Tempting Shortcut

After the direct-sum gate, one might hope to prove axis injectivity by pure
Frobenius representation theory:

```text
source axis pieces are nonisomorphic Frobenius modules
  => their packet-field images are direct.
```

This would reduce the arithmetic theorem almost entirely to component
kernel-triviality.

## Audit

I added:

```text
p24/axis_frobenius_stability_audit.py
```

For a component `c | m`, it computes the packet image span

```text
span{Y_t = sum_{r == t mod c} F_r}
```

and the trace-zero span

```text
span{Y_t - Y_0 : 1 <= t < c}.
```

It then applies packet-field Frobenius `x -> x^q` and checks whether these
spans remain stable.

## Pinned Rows

First extra-dimensional composite row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_frobenius_stability_audit.py \
  --only-D -8711 --max-cases 1 --min-h 100 --max-h 160 \
  --max-abs-D 12000 --max-prime-quotients 8 \
  --max-composite-quotients 20 --min-n 3 --max-n 60 \
  --q-stop 500000 --max-splitting-primes 1 \
  --max-component 12 --max-factor-degree 20 \
  --include-linear --require-composite-m
```

Output:

```text
D=-8711, q=8747, h=132, m=12, n=11, deg=10

c=4:
  full_rank=4, full_plus_frob=8
  trace_zero_rank=3, trace_zero_plus_frob=6
  char_mismatch=3/3

c=3:
  full_rank=3, full_plus_frob=6
  trace_zero_rank=2, trace_zero_plus_frob=4
  char_mismatch=2/2
```

Second extra-dimensional composite row:

```text
D=-10919, q=11243, h=156, m=12, n=13, deg=12

c=4:
  full_rank=4, full_plus_frob=8
  trace_zero_rank=3, trace_zero_plus_frob=6
  char_mismatch=3/3

c=3:
  full_rank=3, full_plus_frob=6
  trace_zero_rank=2, trace_zero_plus_frob=4
  char_mismatch=2/2
```

Broader small window:

```text
rows=52
full_span_unstable_rows=13
trace_zero_unstable_rows=21
character_equivariance_rows=31
character_mismatch_rows=31
```

## Interpretation

The packet-field image of a component axis is not generally a Frobenius
submodule.  For a K-character value

```text
G_s(eta) = sum_{r,k} zeta_c^(s*r) j_{n*r+m*k} eta^k,
```

packet Frobenius gives

```text
sigma(G_s(eta)) = G_{p*s}(eta^p),
```

not

```text
G_{p*s}(eta).
```

The H-character coordinate moves at the same time.  This is the cocycle that
breaks the easy representation-theory proof.

## Consequence

The module direct-sum theorem remains a good target, but it is not forced by
nonisomorphic Frobenius constituents inside one packet field.  A proof has to
control the coupled `(K-character, H-character)` packet phase.

Two viable formulations remain:

```text
1. Tensor-separate the K-character roots from the H-packet root, prove
   rank after faithful scalar extension, then descend.

2. Prove a genuinely coupled p-unit determinant, such as the Hermitian axis
   determinant or the module direct-sum determinant, at the selected prime.
```

This explains why the Hermitian and sliding-window product routes continue to
look more intrinsic than a bare Frobenius-module argument.

The formal descent part of item 1 is Lean-checked in:

```text
p24/lean/ScalarExtensionGate.lean
```

The remaining arithmetic theorem would be:

```text
after adjoining independent K-character roots, the axis character resolvents
for the selected frequency set are linearly independent in
F_p[X]/(f_a) tensor F_p(mu_m).
```

Because scalar extension is faithful, this extended-rank theorem would imply
the original packet axis injectivity.  What failed above is only the stronger
hope that the same directness is automatic from packet-field Frobenius
submodules.

The p24 tensor accounting and small nonsplit tests are recorded in:

```text
p24/k_character_tensor_rank_theorem.md
```
