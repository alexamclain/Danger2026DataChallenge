# Relative Origin-Shift Invariance

This note corrects the interpretation of origin-rotated relative-resultant
scans.

## Statement

Let

```text
h = m*n
J_u(X) = sum_{k=0}^{n-1} j_{u+m*k} X^k,      0 <= u < m.
```

After shifting the chosen class-cycle origin by `s`, the new fiber is

```text
J'_u(X) = sum_k j_{s+u+m*k} X^k.
```

Write

```text
s + u = r + m*c,       0 <= r < m.
```

Then, in `F[X]/(X^n - 1)`,

```text
J'_u(X) = X^(-c) J_r(X).
```

Therefore, for every factor `f | Phi_n`,

```text
J'_u mod f = 0    iff    J_r mod f = 0.
```

So an origin rotation does **not** produce an independent selected-prime test
for coordinate/resultant nonvanishing.  It only permutes the `m` coordinates
and multiplies them by units.

## Consequence

The selected-origin scans are still useful as consistency checks, and they
explain why the pinned composite `D=-1336, n=6` coordinate failure appears on
every origin.  But the random expectations that multiplied by the number of
origin shifts were too optimistic for coordinate-zero packets.

For relative-resultant evidence, the meaningful independent axes are:

```text
1. different CM discriminants;
2. different splitting primes q;
3. different quotient sizes n and packet factors f;
4. different coordinates u within one origin.
```

Origin shifts should be treated as a deterministic symmetry of the same packet.

## Impact On p24 Target

The prime-relative-normality target is unchanged:

```text
Res(Phi_3107441, J_u) != 0 mod p  for all u.
```

But empirical counts should be quoted by packet/coordinate rows before origin
duplication.  The strongest current bounded evidence is therefore the
multi-splitting packet scan with no coordinate failures, not the inflated
selected-origin count.
