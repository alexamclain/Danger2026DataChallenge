# Trace-GCD Trace-Pairing/Subspace-Polynomial Bridge

Date: 2026-06-06

## Point

The current trace-GCD p-unit theorem and the older Moore/subspace-polynomial
normality theorem are now the same finite nonzero event on the selected
leading coordinates.

For selected leading Lang/Fitting coordinates

```text
c_1,...,c_d in L,
d = [L:F_q],
```

and an `F_q`-basis `lambda_1,...,lambda_d` of `L`, the trace-GCD bad-lambda
matrix is

```text
B_ij = Tr_{L/F_q}(lambda_j * c_i).
```

Because the trace pairing on `L/F_q` is nondegenerate,

```text
det(B) != 0
```

is equivalent to

```text
span_Fq{c_1,...,c_d} = L.
```

The subspace-polynomial certificate tests the same statement by incrementally
building the monic `q`-linearized annihilator.  If `P_{i-1}` annihilates the
span of the first `i-1` coordinates, then the residual product

```text
prod_i Norm_{L/F_q}(P_{i-1}(c_i))
```

over all selected coordinates, including zero residuals from dependent
coordinates, is nonzero exactly when the same `c_i` form a basis.

Thus the fixed-orbit trace-GCD resultant

```text
Res_q-lin(P_K,T)
```

can be proved either as a trace-pairing/Fitting determinant p-unit or as a
Moore/subspace-polynomial residual-norm p-unit.  These are two coordinates on
one determinant line, not two separate conjectures.

## Audit

The actual-CM audit is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_trace_pairing_subspace_bridge_audit.py
```

It checks the equivalence on the pinned row, the independent holdout, and
three same-geometry controls.  Current output:

```text
rows=10
trace_rank_mismatches=0
nonzero_event_mismatches=0
missing_residual_norm_products=0
full_rank_rows=10/10
```

This is still small-row evidence, not the p24 theorem.  Its value is that it
identifies the exact finite object the missing theorem should prove.

A low-rank finite-field control is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_trace_pairing_subspace_bridge_toy.py
```

It deliberately repeats or zeroes a coordinate and checks that the
all-coordinate residual product vanishes in the same cases as the trace
determinant:

```text
rank_mismatches=0
event_mismatches=0
low_rank_zero_products=2
```

The finite implication is now also Lean-checked in:

```text
p24/lean/TraceGcdTracePairingSubspaceBridgeGate.lean
```

The Lean gate is intentionally abstract: given that the trace determinant and
residual product detect the same full-span proposition, it proves that a
p-unit residual product rules out the same trace-GCD bad event as a p-unit
trace determinant.

## Refined Missing Theorem

For p24, with

```text
L = F_p(mu_157),  [L:F_p]=156,
R_j = degree-35 right factors from F_p(mu_211),
S_j = H_{157,211}(1,v_j),
```

the representative fixed p-unit can be stated as:

```text
the selected 156 Lang/trace-dual coordinates
Tr_{LR_j/L}(delta_i*S_j)
have nonzero Moore determinant modulo the chosen ordinary prime above p.
```

Equivalently, the incremental subspace-polynomial residual product for the
four full prefix blocks plus the 16-coordinate tail is a p-unit.

The crossed nonzero-orbit p-unit is the same determinant-line statement after
transport around the degree-35 right Frobenius orbit and taking the crossed
norm.

## Why This Helps

The direct semilinear/Fitting route remains primary, but this bridge changes
the proof target from a black-box resultant to a standard finite-field
normality object:

```text
no nonzero p-linearized polynomial of p-degree < 156 kills the selected
leading coordinates.
```

That is the most precise place to import rank-metric, Moore determinant,
subspace-polynomial, or class-field normal-basis ideas.
