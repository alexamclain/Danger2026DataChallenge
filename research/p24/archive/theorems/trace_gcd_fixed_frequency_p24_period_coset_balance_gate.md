# Fixed-Frequency p24 Period-Coset Balance Gate

Date: 2026-06-06

## Point

The Gaussian-period internal trace target can be inverted.  For a relative
packet polynomial

```text
P(X) = sum_k c_k X^k
```

and internal subgroup

```text
U = <Q>,        Q = p^5460 mod n,        |U| = 5549,
```

the per-factor internal trace is

```text
Tr_U(P)(a) = sum_{u in U} P(zeta_n^(a u)).
```

Writing

```text
C_D = sum_{k in D} c_k
```

for the nonzero `U`-cosets `D <= F_n^*`, the trace depends only on `c_0` and
the `C_D`:

```text
Tr_U(P)(a) = |U| c_0 + sum_D C_D eta_{aD},
eta_D = sum_{u in U} zeta_n^(d u).
```

The quotient Gaussian-period matrix is invertible: after Fourier transform on
`F_n^*/U`, its eigenvalues are the nonzero Gauss sums for quotient characters
and the trivial eigenvalue is `-1`.  Therefore

```text
Tr_U(P)(a) = 0 for every nonzero U-coset a

<=>

C_D = |U| c_0 for every nonzero U-coset D.
```

## p24 Meaning

For p24:

```text
n = 3107441
Q = p^5460 mod n = 209035
|<Q>| = 5549 = 31 * 179
(n-1)/5549 = 560
```

For the Gauss-normalized right obstruction

```text
G_chi(X) = sum_k c_k(chi) X^k,
c_k(chi) = sum_r chi^(-1)(r mod 211) j_{r + m*k},
```

the strong per-factor internal-trace theorem is exactly:

```text
For every nonzero <p^5460>-coset D in F_n^*,

  sum_{k in D} c_k(chi) = 5549 * c_0(chi).
```

This is sharper than the previous phrase "weighted Gaussian-period
cancellation": it names the coefficient-side balance that the CM/Lang proof
must produce.

## Complete Recombination

The strong target above is per `E`-tensor idempotent.  The earlier descent
guardrail says the p24 proof may instead recombine all `70` `E`-idempotents
inside one `F_p` packet before asking for descent.  On the `n`-coordinate this
replaces

```text
U = <p^5460>,       |U| = 5549,       (n-1)/|U| = 560
```

by

```text
W = <p>,            |W| = 388430,     (n-1)/|W| = 8.
```

The same period-matrix inversion gives the weaker recombined target:

```text
For every nonzero <p>-coset D in F_n^*,

  sum_{k in D} c_k(chi) = 388430 * c_0(chi).
```

This is the coefficient-side form of respecting complete recombination.  It
is much more plausible than proving the 560 per-factor balances separately,
but it still needs real CM/Lang arithmetic; it is not a cyclotomic identity.

## Decomposition-Field Trace Form

Let

```text
K_n = Q(zeta_n),        M = K_n^<p>,        [M:Q] = 8.
```

For a characteristic-zero lift of the weighted relative polynomial
`G_chi(X)`, the recombined target is:

```text
Tr_{K_n/M}(G_chi(zeta_n)) == 0 mod the selected prime above p.
```

Indeed, the eight coefficients of this relative trace in the Gaussian-period
basis are exactly the eight `<p>`-coset sums above, together with the
constant-term contribution.  This is the cleanest arithmetic statement of the
current fixed-frequency route: prove a named degree-8 decomposition-field
trace is zero modulo `p`, without computing the order-`3107441` relative
class projection by enumeration.

## Guardrail

This is a statement about the ordered CM root sequence, not a formal
cyclotomic identity.  Random coefficient vectors fail the balance, while
forced balanced vectors have zero internal trace.  The theorem still has to
come from the actual weighted CM/Lang packet.

This is also the strong per-factor trace target.  A proof using only complete
recombination over tensor idempotents may avoid proving each factor balance
separately, but then it must explain the cross-factor cancellation explicitly.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_period_coset_balance_gate.py
```

Key markers:

```text
toy_period_matrix_rank=6/6
trace_zero_iff_U_coset_balanced_failures=0
random_unbalanced_trace_nonzero=48/48
forced_balanced_trace_zero=48/48
toy_recombined_period_matrix_rank=2/2
recombined_trace_zero_iff_W_coset_balanced_failures=0
recombined_forced_balanced_trace_zero=48/48
p24_internal_q_generator=p^5460_mod_n=209035
p24_internal_order_check=5549
p24_internal_coset_count=560
p24_recombined_subgroup_order=ord_n(p)=388430
p24_recombined_coset_count=8
p24_E_idempotents_per_Fp_factor=70
complete_recombination_reduces_balance_cosets_560_to_8=1
p24_recombined_scalar_equations=48
p24_recombined_nontrivial_octic_equations=42
p24_recombined_anchor_equations=6
p24_recombined_compressed_values_with_c0=54
p24_per_factor_trace_target_equiv_to_560_coset_balance=1
p24_recombined_trace_target_equiv_to_8_coset_balance=1
recombined_balance_splits_into_42_octic_plus_6_anchor_equations=1
remaining_theorem_is_weighted_CM_sequence_U_coset_balance=1
recombined_theorem_is_weighted_CM_sequence_p_coset_balance=1
```

2026-06-08 refresh: reran this gate with the markers above.  The Lean
recombined mixed-spectrum gate now also pins the p24 factor accounting:

```text
560 = 70 * 8
388430 = 70 * 5549
```

so the 560 per-`E`-idempotent balance equations and the 8 recombined
`<p>`-coset balances are tied to the same recombination arithmetic.

For the six nontrivial right quotient characters, the recombined compressed
verifier therefore checks `6*8=48` base-field equalities, after the tower proof
has supplied the eight `<p>`-coset sums and the `c_0` anchor for each
character.  This is a different compressed interface from the older `1092`
right-H-coset verifier; neither interface permits enumerating the class set.

Equivalently, per right character the eight balance equations split into:

```text
7 nontrivial octic quotient-character equations;
1 anchor equation: sum_{k != 0} c_k(chi) = (n-1) * c_0(chi).
```

Across the six right characters this is `42 + 6 = 48`.  The anchor equation
is important: proving only the seven nontrivial octic projections vanish would
show that the eight nonzero `<p>`-coset sums are equal, but would not identify
their common value with `388430*c_0(chi)`.
