# Relative K-Normality Parent Theorem

The `L1` axis-injectivity theorem may be a low-dimensional shadow of a
stronger relative normal-basis statement.

## Statement

For the p24 third trace,

```text
h = m*n
m = 66254
n = 3107441
deg(f_a) = ord_n(p) = 388430
```

and complement-section fibers

```text
F_r(X) = sum_k j_{n*r + m*k} X^k mod f_a,      0 <= r < m,
```

the parent theorem is:

```text
F_0, F_1, ..., F_{m-1}
are linearly independent over F_p in F_p[X]/(f_a)
```

for each of the eight Frobenius packet factors `f_a | Phi_n`.

This is dimensionally possible because

```text
m = 66254 < 388430 = deg(f_a).
```

It immediately implies axis injectivity, since the 368-dimensional axis
coefficient space is a subspace of all `K`-coordinate weights.

The finite implication is recorded in

```text
p24/lean/AxisInjectivityGate.lean
```

via `axis_injective_from_full_injective`.

## Why Keep the Axis Theorem?

Full `K`-normality is a better proof target if it can be proved using normal
basis or class-field arguments.  But it is a larger certificate surface:

```text
m * deg(f_a) = 66254 * 388430 = 25739985220
```

base-field coefficients per packet before compression.

Axis injectivity only asks for

```text
368 * 388430 = 142942240
```

coefficients per packet before compression, and the actual `L1` scalar is one
resultant.  So the current hierarchy is:

```text
relative K-normality
  => axis injectivity
  => L1 packet nonvanishing
  => exact content/harmful packet ruled out.
```

## Small CM Evidence

The axis scanner now records full `K` rank whenever `deg(f) >= m`.

All-origin eligible window:

```text
packet_rows=341
axis_injective_rows=341
full_k_injective_possible_rows=341
full_k_injective_rows=341
full_k_injective_failure_rows=0
```

Composite-`m`, all-origin eligible window:

```text
packet_rows=162
axis_injective_rows=162
full_k_injective_possible_rows=42
full_k_injective_rows=42
full_k_injective_failure_rows=0
```

Broad eligible window:

```text
packet_rows=148
axis_injective_rows=148
full_k_injective_possible_rows=147
full_k_injective_rows=147
full_k_injective_failure_rows=0
full_k_pivot_prefix_min=2
full_k_pivot_prefix_max=4
```

Larger targeted window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --max-cases 20 --min-h 80 --max-h 260 --max-abs-D 120000 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 5 --max-n 260 --q-stop 1000000 \
  --max-splitting-primes 1 --include-linear \
  --require-deg-ge-axis-dim --random-trials 0 --summary-only
```

reported:

```text
packet_rows=43
injective_rows=43
injective_failures=0
block_internal_failure_rows=0
pair_directness_failure_rows=0
cross_directness_failure_rows=0
full_k_injective_possible_rows=40
full_k_injective_rows=40
full_k_injective_failure_rows=0
injective_pivot_prefix_max=7
full_k_pivot_prefix_max=7
```

Mixed all-row window:

```text
packet_rows=129
injective_possible_rows=49
injective_rows=49
full_k_injective_possible_rows=49
full_k_injective_rows=49
full_k_injective_failure_rows=0
```

No full-`K` rank failure has appeared when the dimension bound allows
injectivity.

The full-`K` rank witnesses also appeared in the first few packet coefficients
in the small windows.  This is only certificate-shape evidence, but it suggests
that the normality determinant may have a low-order/leading-minor form in
structured cases rather than requiring a deep arbitrary submatrix.

The pinned prime-`n` product-coordinate counterexample `D=-956` also does not
contradict this parent theorem.  With origin scanning it reports:

```text
packet_rows=45
dimension_bound_rows=30
injective_possible_rows=15
injective_rows=15
full_k_injective_possible_rows=15
full_k_injective_rows=15
full_k_injective_failure_rows=0
```

So that row kills coordinate/product nonvanishing, but not full relative
`K`-rank in the dimension-eligible packets.

## Proof Shape

The normal-basis analogy is:

```text
the selected H-character projection of the CM class vector is a normal element
for the complement K-action after reduction at the p24 prime.
```

A basis-free certificate form is recorded in

```text
p24/k_normality_moore_certificate.md
```

For packet elements

```text
beta_r = F_r(zeta_a) in F_p[X]/(f_a),
```

full `K`-normality is equivalent to nonvanishing of the Moore determinant

```text
Delta_a = det(beta_r^(p^s))_{0 <= r,s < m}.
```

The same note records the coefficient-minor form and the failure
consequence:

```text
full K-rank failure
<=> exists nonzero w in F_p^m with f_a | sum_r w_r F_r(X).
```

This cannot be a pure formal consequence of nonzero content: a nonzero vector
in the packet field can have a large annihilator in `F_p[K]`.  The missing
arithmetic input is that the actual CM packet vector avoids such annihilators.

It also cannot be proved by the existing modular zero lemma alone.  The
boundary is recorded in

```text
p24/k_normality_fourier_zero_boundary.md
```

A rank failure gives

```text
f_a | A_w(X) = sum_k (sum_r w_r j_{n*r+m*k}) X^k,
```

which is vanishing on one packet of `H`-characters, not pointwise vanishing at
many CM points.  The elementary Fourier uncertainty bound is far too weak for
p24, giving only a support lower bound of `2`.

If full `K`-normality is too strong to prove, the fallback is the smaller
axis direct-sum theorem in

```text
p24/l1_axis_direct_sum_proof_strategy.md
```

which only needs the nine Frobenius-stable axis modules.

The split-character diagnostic is recorded in

```text
p24/k_character_rank_split_boundary.md
```

When `m | q-1`, the `K`-character DFT is available in the base field.  In the
broad split-character window it found:

```text
packet_rows=1422
dimension_possible_rows=628
full_rank_rows=628
dimension_possible_rank_defect_rows=0
zero_character_rows=0
rank_defect_with_full_character_support_rows=794
dimension_possible_rank_defect_with_full_character_support_rows=0
```

Thus all tested dimension-possible rows with split `K` characters had full
rank.  But dimension-bound rows had all character resolvents nonzero while
rank was necessarily deficient, so individual character nonvanishing is not a
formal substitute for the Moore/rank theorem.
