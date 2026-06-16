# Actual-CM Right-Combo Anchor Boundary

Date: 2026-06-06

## Point

The p24 recombined period-coset balance is:

```text
sum_{k in D} c_k(chi) = 388430 * c_0(chi)
```

for each of the eight nonzero `<p>`-cosets `D <= F_n^*`.  Per right character,
this splits into:

```text
7 nontrivial octic quotient equations;
1 anchor equation: sum_{k != 0} c_k(chi) = (n - 1) * c_0(chi).
```

The anchor equation is the part that identifies the common octic sum with the
constant-term anchor.  It must not be silently replaced by the seven
nontrivial quotient equations.

## Small Actual-CM Boundary

The pinned actual-CM right-combo analogue has:

```text
D = -13319
q = 13463
h = 140
m = 28 = 4 * 7
n = 5
```

Here `<q>` has order `4` modulo `n=5`, so there is exactly one nonzero
recombined coset:

```text
<q> = {1, 3, 4, 2}.
```

Therefore the recombined balance has no nontrivial quotient equations at all.
It is exactly the anchor equation:

```text
sum_{k=1}^4 c_k(chi) = 4 * c_0(chi).
```

The actual right-combo `G_chi` analogue fails this equation.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary.py
```

Key markers:

```text
recombined_q_order=4
recombined_nonzero_coset=[1, 3, 4, 2]
recombined_nontrivial_quotient_equations=0
recombined_anchor_equations=1
anchor_balance_holds=0
anchor_defect_nonzero=1
weighted_polynomial_recombined_trace_zero=0
right_combo_recombined_trace_zero=0
```

Thus the p24 anchor equation is not a generic consequence of:

```text
actual CM right-combo shape
  + complete recombination
  + decomposition-field trace language.
```

The proof must use the specific p24 weighted `G_chi` packet, the 211-axis
H-coset equality/descent identity, or an explicit CM/Lang potential.
