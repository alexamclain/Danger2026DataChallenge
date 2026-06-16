# L1 Axis-Injectivity Theorem Candidate

This note records the sharpened replacement for the earlier selected-origin
`L1` p-unit hope.

## p24 Statement

For the third trace,

```text
h = m*n
m = 66254 = 2*157*211
n = 3107441
ord_n(p) = 388430
```

fix one Frobenius packet factor

```text
f_a | Phi_n over F_p,        deg(f_a)=388430.
```

Let

```text
F_r(X) = sum_k j_{n*r + m*k} X^k mod f_a,      0 <= r < m.
```

The tower-native axis coefficient space is

```text
W_axis = { a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211) }.
```

After quotienting redundant constants, a concrete basis is

```text
1,
1_{r == t mod 2}      for 1 <= t < 2,
1_{r == t mod 157}    for 1 <= t < 157,
1_{r == t mod 211}    for 1 <= t < 211.
```

Thus

```text
dim_Fp(W_axis) = 1 + 1 + 156 + 210 = 368.
```

The refined theorem target is:

```text
T_a : W_axis -> F_p[X]/(f_a)
T_a(w) = sum_r w(r) F_r(X)

is injective for each of the eight Frobenius packet orbits a.
```

Equivalently, the 368 packet-field elements

```text
Y_0      = sum_r F_r,
Y_2,1    = sum_{r == 1 mod 2} F_r,
Y_157,t  = sum_{r == t mod 157} F_r,   1 <= t < 157,
Y_211,t  = sum_{r == t mod 211} F_r,   1 <= t < 211
```

are linearly independent over `F_p` inside the degree-`388430` packet field.

## Why This Is Better Than the Previous L1 Scalar Target

The previous one-scalar target was:

```text
Res(Phi_3107441, L1) != 0 mod p,
L1 = M0 + P2 + P157 + P211.
```

That asks for selected-origin nonvanishing of one special axis-supported
weight

```text
w_L1(r) = 1 + (r mod 2) + (r mod 157) + (r mod 211).
```

Axis injectivity proves more:

```text
every nonzero axis-supported weight has nonzero selected packet value.
```

So it rules out selected-origin cancellation for `L1` without needing a
separate lucky-lambda argument.

This also explains why the old translate-rank theorem was insufficient.
Nonzero character components prove that the translate family is not
identically zero.  Axis injectivity instead proves that no base-field linear
combination of the 368 axis components vanishes at the selected origin.

## Certificate Shape

A certificate for a packet can be a 368-column rank certificate in
`F_p[X]/(f_a)`: choose 368 coefficient positions in the degree-388430 basis
whose 368-by-368 determinant is nonzero modulo `p`.

This is finite-field data of size roughly

```text
368 * 388430 = 142942240 base-field coefficients per packet
```

before compression.  The important asymptotic point is that the theorem lives
in the degree-`ord_n(p)` packet field and the 368-dimensional smooth-axis
space, not in the full class set of size

```text
h = 205880396014.
```

The construction remains tower-native: the basis elements are traces over the
two, 157, and 211 complement axes.

## Small CM Stress Tests

I added:

```text
p24/l1_axis_injectivity_scan.py
```

It builds the basis above for each small CM packet and computes the rank of

```text
W_axis -> F_q[X]/(f).
```

Pinned `M0` failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --only-D -899 --min-h 12 --max-h 20 \
  --q-start 281 --q-stop 282 --include-linear \
  --max-prime-quotients 3 --max-composite-quotients 3 \
  --min-n 3 --max-n 10 --scan-origins \
  --random-trials 32 --summary-only
```

Output:

```text
packet_rows=84
dimension_bound_rows=84
injective_possible_rows=0
m0_zero_rows=14
l1_zero_rows=0
rank_defect_histogram={1: 84}
```

Here `deg(f) < dim(W_axis)`, so injectivity is impossible for dimension
reasons.  `L1` still rescues the known `M0` zero.

Pinned prime-`n` coordinate-product counterexample:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --q-start 3307 --q-stop 3308 --include-linear \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --scan-origins \
  --random-trials 32 --summary-only
```

Output:

```text
packet_rows=45
dimension_bound_rows=30
injective_possible_rows=15
injective_rows=15
injective_failures=0
m0_zero_rows=0
l1_zero_rows=0
rank_defect_histogram={0: 15, 4: 30}
```

Broader eligible scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --max-cases 70 --min-h 12 --max-h 180 --max-abs-D 80000 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 3 --max-n 180 --q-stop 800000 \
  --max-splitting-primes 2 --include-linear \
  --require-deg-ge-axis-dim --random-trials 8 --summary-only
```

Output:

```text
packet_rows=148
injective_possible_rows=148
injective_rows=148
injective_failures=0
l1_zero_rows=0
rank_defect_histogram={0: 148}
injective_pivot_prefix_min=2
injective_pivot_prefix_max=4
```

All-origin eligible scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --max-cases 12 --min-h 12 --max-h 80 --max-abs-D 16000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 80 --q-stop 120000 \
  --max-splitting-primes 1 --include-linear --scan-origins \
  --require-deg-ge-axis-dim --random-trials 8 --summary-only
```

Output:

```text
packet_rows=272
injective_possible_rows=272
injective_rows=272
injective_failures=0
l1_zero_rows=0
rank_defect_histogram={0: 272}
```

Composite-`m`, all-origin eligible scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --max-cases 12 --min-h 12 --max-h 100 --max-abs-D 25000 \
  --max-prime-quotients 6 --max-composite-quotients 6 \
  --min-n 3 --max-n 100 --q-stop 220000 \
  --max-splitting-primes 1 --include-linear --scan-origins \
  --require-composite-m --require-deg-ge-axis-dim \
  --random-trials 8 --summary-only
```

Output:

```text
packet_rows=162
injective_possible_rows=162
injective_rows=162
injective_failures=0
block_internal_failure_rows=0
l1_zero_rows=0
rank_defect_histogram={0: 162}
injective_pivot_prefix_min=4
injective_pivot_prefix_max=4
```

All rank defects seen so far are explained by the obvious dimension bound
`deg(f) < dim(W_axis)`.  In the p24 target the inequality goes strongly in the
opposite direction:

```text
388430 >> 368.
```

The base-field Frobenius-module audit

```text
p24/l1_axis_frobenius_module_audit.py
```

shows that p24 does not require treating these as 368 unrelated geometric
characters.  Over `F_p`, the nontrivial axis support is:

```text
2-axis:    1 orbit of size 1,
157-axis:  1 orbit of size 156,
211-axis:  6 orbits of size 35.
```

So the 368-dimensional axis space consists of nine Frobenius-stable modules:
the trivial module plus eight nontrivial modules.  A proof can aim at
directness of these modules in the packet field.

The stronger parent theorem in

```text
p24/relative_k_normality_parent_theorem.md
```

asks for the full set of complement fibers `F_0,...,F_{m-1}` to be linearly
independent in each packet field.  This would imply axis injectivity by
restriction.  The scan now records full-`K` rank and found no failures when
`deg(f) >= m`.

## Lean Gate

The finite implication is checked in:

```text
p24/lean/AxisInjectivityGate.lean
```

Lean proves:

```text
axis evaluation injective
+ L1 coefficient function nonzero
=> selected L1 packet value nonzero
=> the packet content vector is not all zero
=> harmful all-zero packet vanishing is ruled out.
```

The remaining arithmetic theorem is exactly the p24 axis-injectivity statement
above.

## Proof Direction

The natural proof object is not a scalar norm.  It is a reduced-normality
statement for a small explicit subspace of the group algebra:

```text
W_axis ∩ Ann_{F_p[K]}(packet vector) = {0}.
```

This is a much cleaner target than proving one chosen sum is a p-unit.  It
also has a plausible CM interpretation: the target packet vector should be
normal enough that no low-dimensional smooth-axis trace relation can
annihilate it after reduction at the selected prime.

What would falsify it:

```text
an eligible small CM packet with deg(f) >= dim(W_axis)
but rank(T_f) < dim(W_axis).
```

No such failure has appeared yet.

The scan also reports pivot prefixes for full-rank rows.  In the broad
eligible window above, the largest prefix needed to witness injectivity was
`4`, matching the tiny axis dimensions present in those small analogues.  This
does not prove a p24 low-prefix determinant, but it is useful certificate-shape
evidence: in the tested cases the rank witness is visible immediately rather
than only after searching deep packet-field coordinates.

The updated scan also separates internal axis-block failures from cross-axis
direct-sum failures.  No internal block failures appeared in the tested rows.
That points to a plausible proof split:

```text
1. each c-axis block {sum_{r == t mod c} F_r}_t has full rank modulo its
   one trace relation;

2. the trace-zero parts for c=2,157,211 have zero mutual intersection over the
   common constant line.
```

Together these imply the full 368-dimensional axis injectivity theorem.

## Tensor-Factor Reduction

The sharper p24 accounting now reduces the arithmetic determinant to one
scalar-extension factor.  Let

```text
E = F_p(mu_m),      [E:F_p] = ord_m(p) = 5460.
```

For each degree-`388430` packet field `A_a`,

```text
A_a tensor_{F_p} E ~= product_{70} B_i,
[B_i:E] = 5549.
```

The p24 axis dimension still satisfies

```text
368 < 5549.
```

The Lean gates

```text
p24/lean/ScalarExtensionGate.lean
p24/lean/AxisInjectivityGate.lean
```

now explicitly check that injectivity on one extended tensor factor is a
sufficient certificate for base-field packet axis injectivity.  Therefore the
preferred axis theorem is:

```text
for one B_i over E, the 368 K-character resolvents R_s for s in S_axis
are E-linearly independent.
```

Equivalently, the first 368 rows of the `Q=p^5460` Moore matrix have
nonzero determinant:

```text
det(R_s^(Q^j)) != 0,      s in S_axis, 0 <= j < 368.
```

Latest bounded one-factor controls are clean: `130` tensor-factor rows had
equal factor ranks, `6/6` one-factor dimension-possible rows had a full
axis factor, and the block scan had no unforced component, pair, or full
directness failures.
