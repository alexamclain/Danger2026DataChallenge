# Centered Marginal Transversality Boundary

Date: 2026-06-06

This note records the exact probabilistic/Schubert shape of the centered
right-product theorem.  It is a calibration, not a certificate.

## Plateau As Schubert Divisor

Let

```text
P_b in F_p^156,     b mod 211,
```

be the centered marginal point columns.  A right-window factor vanishes
exactly when some nonzero dual word is constant on a cyclic block of length
`157`.

For a fixed block, the words constant on that block form a subspace of
`F_p^211` cut out by:

```text
157 - 1 = 156
```

linear equations.  Its full ambient dimension is therefore:

```text
211 - 156 = 55.
```

But the centered column `P_0` is zero, so the actual dual row space lies in:

```text
H = {w_0 = 0},      dim H = 210.
```

The effective bad subspace is the centered plateau subspace:

```text
B_t^0 = {w in H : w is constant on the t-plateau},
dim B_t^0 = 54.
```

The centered-profile row space has dimension `156`, so the effective
dimensions are complementary in `H`:

```text
156 + 54 = 210.
```

Thus each bad plateau condition is one Schubert-divisor transversality event:

```text
RowSpace(C) cap B_t^0 = {0}.
```

The p24 theorem asks for this transversality for all `211` cyclic plateaus.

## Random Baseline

Added:

```text
p24/centered_marginal_transversality_baseline.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/centered_marginal_transversality_baseline.py
```

Output:

```text
q=1000000000000000000000007
centered_ambient_dim=210
right=211
row_dim=156
plateau_length=157
plateau_constraints=156
centered_plateau_subspace_dim=54
dimension_sum=210
window_count=211
fixed_plateau_failure_probability=1.000000000000E-24
union_bound_any_plateau_failure=2.110000000000E-22
```

So a random `156`-plane in the centered `210`-dimensional hyperplane avoids
all cyclic centered plateau subspaces with overwhelming probability.

## What This Does And Does Not Prove

This explains why every actual-CM small row has succeeded so far and why
random controls also succeed.  It does **not** certify p24.  The selected CM
row space is a single arithmetic point in the Grassmannian, and a probability
bound over random planes says nothing about that selected point unless it is
lifted to an arithmetic theorem.

The theorem import would have to be one of:

```text
1. Schubert p-unit theorem:
   the p24 centered CM row space avoids the 211 named Schubert divisors.

2. Equidistribution with explicit exclusion:
   the CM trace-form point in the Grassmannian is shown not to lie on these
   divisors by a class-field/Hecke equidistribution plus exact local check.

3. Deterministic derandomization:
   identify the row space with a known rank condenser/MSRD/LRS object whose
   Schubert divisor avoidance is theorem-level, not heuristic.
```

Existing audits rule out the easy versions:

```text
p24/centered_marginal_cyclic_code_boundary.md
p24/centered_marginal_resultant_factor_boundary.md
p24/centered_marginal_projective_geometry_boundary.md
p24/msrd_lrs_import_boundary.md
p24/lang_block_subspace_design_boundary.md
```

## Current Use

The transversality language is still productive because it names the exact
divisors:

```text
Delta_C(t) = 0,     t mod 211.
```

The compact p24 certificate asks to prove:

```text
prod_{t mod 211} Delta_C(t) != 0 mod p,
```

or equivalently the seven Frobenius-orbit products are all p-units.  Any
probability/CS theorem must now target those divisors explicitly; generic
random-rank intuition is only a guide for which p-unit theorem should be true.
