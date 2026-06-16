# Relative Augmentation-Order Theorem Target

This note reframes the low-moment packet certificate as a first-order
augmentation-jet statement.  It is a sharper arithmetic target than a generic
two-moment random projection, and it explains why the complement trace is the
most constructive scalar but not quite safe enough as a universal theorem.

## Packet Polynomial

For the third p24 target,

```text
h = m*n
m = 66254
n = 3107441
```

and a Frobenius packet factor `f_a | Phi_n`, define

```text
V_a(Y) = sum_{u=0}^{m-1} (J_u mod f_a) Y^u
       in (F_p[X]/f_a)[Y].
```

The exact relative-content theorem is simply

```text
V_a(Y) != 0
```

for each of the eight nontrivial Frobenius packets.

The low-moment certificate asks for the first two Hasse derivatives at
`Y=1`:

```text
D_0 V_a(1) = sum_u J_u mod f_a = M_0 mod f_a
D_1 V_a(1) = sum_u u J_u mod f_a = M_1 mod f_a.
```

Since `m < p` for p24, ordinary and Hasse first derivatives agree up to the
same coefficient convention.  Thus

```text
gcd(Phi_n, M_0, M_1) = 1
```

is equivalent to saying no nonzero packet polynomial lies in

```text
(Y - 1)^2.
```

## Theorem Candidate

The clean p24-specific theorem is:

```text
Relative augmentation order-one theorem:
  For the selected p24 conductor-2 CM embedding and every nontrivial
  Frobenius packet f_a | Phi_3107441, if V_a(Y) is nonzero then
  V_a(Y) has augmentation order at most one at Y=1.
```

Equivalently:

```text
V_a in (Y-1)^2  =>  V_a = 0.
```

This is strictly stronger than exact relative content, but far weaker than
prime augmentation normality.  It is also a more structured statement than an
arbitrary pair of linear projections: it says the embedded CM packet survives
in the first-order neighborhood of the complement quotient identity.

## Constructive Meaning

For `gcd(m,n)=1`, write

```text
G = H x K,       |H| = n, |K| = m.
```

The zeroth derivative is the `K`-trivial class-character resolvent:

```text
M_0(zeta_n^a) = Tr_K(j) evaluated at the H-character a.
```

This is the most constructive one-scalar route: if

```text
Res(Phi_n, M_0) != 0 mod p,
```

then the harmful packet is ruled out using a degree-`n` quotient trace.

The first derivative is not just another quotient-field trace; it is the
first augmentation jet in the `K` direction.  Therefore the two-moment theorem
is safer than `M_0` alone, but an end-to-end construction must still build
either:

```text
1. the quotient trace and prove it is a selected-prime p-unit; or
2. the first-order K-augmentation jet in compressed tower form.
```

The first attempt to decompose this jet through the smooth factorization of
`m` exposed an important carry term.  This is recorded in:

```text
p24/crt_partial_moment_tower_boundary.md
p24/augmentation_crt_derivative_toy.py
p24/crt_partial_moment_projection_scan.py
```

For `m = prod_i c_i`, CRT partial moments

```text
P_i(X) = sum_t t * sum_{r == t mod c_i} F_r(X)
```

are tower-native, but

```text
M_1 != sum_i e_i P_i
```

as an identity over `F_p` when `m` is composite.  The equality needs a carry
correction:

```text
M_1 = sum_i e_i P_i - m*C.
```

Thus the literal Hasse derivative still carries a joint labeling term.  A
safer compressed projection target is the family

```text
gcd(Phi_n, M_0, {P_i}) = 1,
```

which avoids the carry and, for p24, uses intermediate degrees
`n*2`, `n*157`, and `n*211`.

## Experiments

I added:

```text
p24/relative_augmentation_order_scan.py
```

It computes the first nonzero Hasse derivative of `V_a(Y)` at `Y=1`.

Pinned known complement `M_0` failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_augmentation_order_scan.py \
  --only-D -899 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 281 --q-stop 282 \
  --include-linear --max-order 4 --section complement
```

reports:

```text
packet_rows=6
first_order_failures=1
pair_failures=0
augmentation_histogram={'0': 5, '1': 1}
```

So `M_0` alone is false, but the packet has augmentation order exactly one.

Bounded non-origin comparison:

```text
complement section:
  packet_rows=320
  first_order_failures=0
  pair_failures=0
  augmentation_histogram={'0': 320}
  expected_prefix_1_zeros_random=0.232139
  expected_prefix_2_zeros_random=0.000494

contiguous section:
  packet_rows=472
  first_order_failures=1
  pair_failures=0
  augmentation_histogram={'0': 471, '1': 1}
  expected_prefix_1_zeros_random=0.348498
  expected_prefix_2_zeros_random=0.000784
```

Origin-rotated small-field stress window:

```text
complement section:
  packet_rows=4051
  first_order_failures=0
  pair_failures=0
  augmentation_histogram={'0': 4051}
  expected_prefix_1_zeros_random=2.257256
  expected_prefix_2_zeros_random=0.005546

contiguous section:
  packet_rows=5861
  first_order_failures=5
  pair_failures=0
  augmentation_histogram={'0': 5856, '1': 5}
  expected_prefix_1_zeros_random=3.512963
  expected_prefix_2_zeros_random=0.009254
```

Prime `n >= 11`, complement section, no origin scan:

```text
packet_rows=533
first_order_failures=0
pair_failures=0
augmentation_histogram={'0': 533}
expected_prefix_1_zeros_random=0.080318
expected_prefix_2_zeros_random=0.000059
```

This does not prove a theorem.  It does suggest the complement trace has
extra structure beyond a random linear projection, while the two-moment
augmentation-jet certificate has not failed in any bounded CM window.

## Boundary

The theorem cannot be pure linear algebra: for `m >= 3`, nonzero vectors can
lie in `(Y-1)^2`.  It also cannot be a universal complement-trace theorem,
because small CM rows with `n=3` and `n=7` have `M_0=0`.

The plausible arithmetic input must use at least one of:

```text
1. the selected p24 split prime above p;
2. the high prime recovery length n=3107441;
3. the conductor-2/nonsplit p24 CM branch;
4. the principal singular modulus dominance plus a p-adic unit argument.
```

The most useful next proof target is therefore:

```text
prove the p24 complement trace is a p-unit;
if that fails or cannot be proved, prove the first-order augmentation jet
(M_0,M_1) is not simultaneously zero in any packet.
```

For a tower-native construction, replace the second line by the slightly
different but safer family:

```text
prove gcd(Phi_3107441, M_0, P_2, P_157, P_211) = 1 mod p.
```

The family can also be packaged into one scalar:

```text
L_1 = M_0 + P_2 + P_157 + P_211.
```

This scalar is not the literal Hasse derivative, but it is a valid projection
of the same packet vector.  It has principal coefficient `1`, all other
coefficients at most `368`, and therefore keeps the principal complex
dominance input.  The refined one-resultant target is:

```text
Res(Phi_3107441, L_1) != 0 mod p.
```

This is now the cleanest augmentation-flavored scalar target: tower-native
construction shape, one resultant, and no CRT carry term.  The open part is
again selected-prime p-unitness.

The support audit in

```text
p24/l1_character_support_audit.py
p24/l1_punit_boundary.md
```

shows the tradeoff: `L_1` has only `368` K-character frequencies, but its
K-translation orbit has full size `66254`.  It remains an H-eigenvector, so
H/Frobenius zero propagation survives, but it is not K-trivial and therefore
does not inherit the degree-`n` quotient-field norm package of `M_0`.
