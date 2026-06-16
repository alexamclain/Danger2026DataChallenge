# p24 Jacobi-Carry Fourier Formula Gate

Date: 2026-06-07

## Point

The four dual Fourier condition families for the admissible Jacobi target are
not only empirical rank facts.  They follow symbolically from the Fourier
formula for the cyclic sawtooth terms in an admissible C-axis Jacobi carry.

Let:

```text
N = 7*c
g_m(t) = [m*t]_N
theta_{u,v}(t) = g_u(t) + g_v(t) - g_{u+v}(t)
```

For the admissible family:

```text
u is C-axis: u = 7*s, s != 0 mod c;
v has nontrivial C-component;
u+v has nontrivial C-component.
```

## Sawtooth Formula

Let `d = gcd(m,N)`, `M = N/d`, and `m' = m/d mod M`.  For nonzero frequency
`k`, the Fourier coefficient of `g_m` is:

```text
hat g_m(k) = 0
  if d does not divide k;

hat g_m(k) = -d^2*M / (1 - zeta_M^(-k/d * (m')^(-1)))
  if d divides k.
```

At zero frequency:

```text
hat g_m(0) = d^2 * M * (M-1) / 2.
```

The product-coordinate frequency dictionary has the CRT normalization:

```text
k == a*c mod 7
k == b*7 mod c
```

for product Fourier coefficient `F(a,b)` on `C_7 x C_c`.

## Sources Of The Four Families

### Family 1

For `a != 0`, `b = 0`, the `u=7*s` term has no support.  The `v` and `u+v`
terms have the same right component, so their sawtooth coefficients cancel:

```text
F(a,0)=0.
```

This is the forbidden `C_7^nontrivial x {C/E trivial}` vanishing.

### Family 2

For a single sawtooth term:

```text
hat g_m(k) + hat g_m(-k) = -d*N
```

whenever both sides are supported.  In the admissible carry, the right
nontrivial slice sees only the `v` and `u+v` terms, with the same divisor `d`,
so the constants cancel:

```text
F(a,b) + F(-a,-b) = 0.
```

Thus conjugate skew is a real carry identity.  It is not a consequence of
generic inversion symmetry for arbitrary packets.

### Family 3

For right-trivial nonzero `C` frequency, all three sawtooth pieces contribute.
The pair sum is:

```text
F(0,b) + F(0,-b) = -7*N.
```

The zero-frequency carry value is:

```text
F(0,0) = 7*N*(c-1)/2.
```

Therefore:

```text
F(0,b) + F(0,-b) = (-2/(c-1)) * F(0,0).
```

For p24, `c=179`, so:

```text
lambda_179 = -2/178 = -1/89.
```

This explains the previously empirical normalization scalar.

### Family 4

Every admissible carry vanishes on the `C`-zero fiber:

```text
theta_{u,v}(right, 0) = 0.
```

Fourier inversion along the `C` coordinate gives:

```text
sum_b F(a,b) = 0
```

for each nontrivial right character `a`.  Using Family 1 and the conjugate
pairing, this is equivalent to the three independent global balances:

```text
sum_{b>0}(F(-a,b) - F(a,b)) = 0,
  a = 1,2,3.
```

## Consequence

The dual Fourier system has a clean symbolic Jacobi-carry proof:

```text
admissible C-axis Jacobi carry
=> Families 1-4.
```

This does not yet prove the p24 selected weighted packet is a sum of
admissible carries.  It does sharpen the missing theorem:

```text
construct the selected weighted packet as a p-integral combination of
admissible C-axis Jacobi carries, or prove the four symbolic carry identities
directly for that packet.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate.py
```

Observed:

```text
formula_matches=3/3
lambda_formula_matches=3/3
dual_condition_rows_match=3/3
c_zero_fiber_rows_match=3/3
p24_pair_sum_lambda_rational=-2/(179-1)=-1/89
```

No p24 class set or CM root enumeration is used.
