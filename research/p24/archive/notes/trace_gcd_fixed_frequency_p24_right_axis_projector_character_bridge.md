# p24 Right-Axis Projector Character Bridge

This records the sign/index bridge between the newest anchor-projector target
and the older `1092` H-coset character payload.

For p24,

```text
rho = p^780
log_2(rho mod 211) = 90
90 mod 7 = 6
6^(-1) mod 7 = 6
```

Thus under covariance `rho^j(Y_0)=Y_{6j}`, the anchor projector

```text
Pi_m(Y_0) = (1/7) sum_j omega^(-m*j) rho^j(Y_0)
```

is one seventh of the H-quotient character projection with index
`k = 6m mod 7`.

So the six anchor equations are exactly the six nontrivial quotient-character
equations, relabeled as:

```text
m: 0 1 2 3 4 5 6
k: 0 6 5 4 3 2 1
```

This matters because it closes the convention gap:

```text
prove Pi_m(Y_0)=0 for m=1,...,6
iff
prove the six nontrivial H-quotient character sums vanish
iff
ordinary centering + those six characters give the 1092 scalar verifier
```

Latest gate markers:

```text
bridge_identity_failures=0
nontrivial_anchor_zero_iff_nontrivial_quotient_zero_failures=0
anchor_projector_to_quotient_character_index_map=[0, 6, 5, 4, 3, 2, 1]
```
