# p24 Right-Axis Anchor Projector Gate

After the seven-coset covariance reduction, the remaining finite condition is
that one anchor H-coset sum `Y_0` is fixed by `rho=p^780`.

Because `rho` has order `7`, this is equivalent to six explicit projector
vanishings:

```text
Pi_k(Y_0) = 0,  k = 1,...,6
Pi_k = (1/7) sum_{j=0}^6 omega^(-k*j) rho^j
```

The executable gate checks:

```text
anchor fixed <=> all six nontrivial rho-projectors vanish
the projectors are orthogonal idempotents
random anchors are not fixed
rho-averaged anchors are fixed
pure H-period anchor has all six nonfixed projectors nonzero
```

The verified fast version avoids degree-35 Frobenius powering in the default
harness.  It tests the abstract projector algebra in an order-7 Frobenius
quotient model over `F_43`, and tests the pure H-period leakage in the split
field `F_8863`, where `8863-1` is divisible by both `7` and `211`.

Latest direct run:

```text
projector_idempotent_failures=0
anchor_fixed_iff_nontrivial_projectors_zero_failures=0
random_anchor_fixed_count=0/24
forced_anchor_fixed_count=24/24
forced_anchor_nontrivial_projectors_zero=24/24
pure_H_anchor_fixed=0
pure_H_anchor_equal_cosets=0
pure_H_anchor_nontrivial_projectors_nonzero=6/6
```

So the arithmetic theorem can be stated as a concrete projector identity:
after internal tracing, the `G_chi` anchor must have zero component in all six
nontrivial `rho`-eigenspaces.  This is the exact meaning of anchor descent in
the current proof path.
