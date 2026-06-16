# K-Normality Fourier-Zero Boundary

This note records why the relative `K`-normality parent theorem does not
immediately follow from the finite-field modular zero lemma.

## Rank Failure Is a Fourier Zero

For packet factor `f_a | Phi_n`, full `K`-rank failure means there is a
nonzero weight vector

```text
w = (w_0,...,w_{m-1}) in F_p^m
```

such that

```text
sum_r w_r F_r(X) == 0 mod f_a.
```

Writing

```text
g_w(k) = sum_r w_r j_{n*r + m*k},
A_w(X) = sum_k g_w(k) X^k,
```

the failure is:

```text
f_a | A_w.
```

Thus `A_w` vanishes on one Frobenius packet of `H`-characters.  This is a
frequency-domain vanishing statement.

## Why The Modular Zero Lemma Does Not Apply

The finite-field modular zero lemma needs pointwise vanishing at many CM
points:

```text
g_w(k) = 0 for many k.
```

But `f_a | A_w` only says that the Fourier transform of the sequence `g_w(k)`
vanishes on one packet of characters:

```text
sum_k g_w(k) zeta^{a p^s k} = 0
```

for `0 <= s < ord_n(p)`.

That is not a divisor of zeros on a modular curve.  It is a linear-algebra
condition in the group algebra of the relative `H` direction.

## Uncertainty Bound Is Too Weak

For p24,

```text
n = 3107441
packet_size = ord_n(p) = 388430
packet_count = 8
```

If a nonzero sequence has Fourier transform vanishing on one packet, its
Fourier support may still have size

```text
n - packet_size = 2719011.
```

The elementary cyclic uncertainty bound gives only

```text
support(g_w) >= ceil(n / (n - packet_size)) = 2.
```

So Fourier uncertainty does not convert one packet zero into enough time-domain
zeros for a divisor-count argument.

The arithmetic is reproducible with:

```text
p24/k_normality_fourier_zero_audit.py
```

which reports:

```text
fourier_support_after_one_packet_zero_at_most=2719011
cyclic_uncertainty_time_support_lower_bound=2
```

## Consequence

The proof of full relative `K`-normality must use one of:

```text
1. a true normal-basis/Moore determinant p-unit theorem;
2. a special CM trace formula for the packet Fourier values;
3. a stronger multi-packet vanishing implication;
4. a direct axis-module directness theorem.
```

It cannot be obtained by applying the existing modular zero lemma to the
single-packet Fourier zero.
