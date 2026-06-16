# Centered Marginal Phase-Aware Borcherds/Fitting Target

Date: 2026-06-06

This note specializes the phase-aware p-unit route to the smaller
centered-profile determinant surface.

## Object

For the p24 centered marginal, let

```text
Delta_C(t) =
  det(P_{t+1}-P_t, ..., P_{t+156}-P_t),     t mod 211,
```

where `P_b in F_p^156` are the centered right-profile point columns.  The
compact certificate target is:

```text
Pi_C,right = prod_{t mod 211} Delta_C(t) != 0 mod p.
```

Since `ord_211(p)=35`, this splits into seven base-field factors:

```text
Pi_O = prod_{t in O} Delta_C(t),
```

one singleton orbit `O={0}` and six nonzero Frobenius orbits of size `35`.

The finite handoff is checked in:

```text
p24/lean/CenteredArcProductGate.lean
p24/lean/CenteredBorcherdsPUnitGate.lean
```

The p-integral determinant-line model is separated in:

```text
p24/centered_marginal_chow_integral_model.md
```

A full-origin version of the same route is recorded in:

```text
p24/centered_marginal_full_origin_borcherds_gate.md
p24/lean/CenteredFullOriginBorcherdsGate.lean
```

It says that a closed full-origin centered Chow product formula would imply
the 211-term right product because:

```text
prod_all_origins Delta_origin
  = p-unit * Pi_C,right^(975736474).
```

The most explicit Fitting-object formulation is:

```text
p24/centered_marginal_crossed_product_fitting_target.md
```

It packages each orbit product as the zeroth Fitting determinant of the
transported Schubert quotient maps `W_C -> H/B_t`.

## Schubert/Fitting Form

Let `H={w_0=0}` and let `W_C` be the `156`-dimensional centered row space in
`H`.  For a cyclic plateau window `I_t={t,...,t+156}`, let `B_t` be the
centered plateau subspace of words in `H` that are constant on `I_t`.  Then:

```text
Delta_C(t) = 0
```

if and only if:

```text
W_C cap B_t != {0}.
```

Thus `Delta_C(t)` is a Schubert/Fitting determinant for a complementary
incidence problem:

```text
dim W_C = 156,
dim B_t = 54,
dim H = 210,
156 + 54 = 210.
```

The arithmetic theorem should construct, for each right Frobenius orbit
`O`, a p-integral phase-aware section

```text
Psi_O
```

on the conductor-2 CM phase torsor such that:

```text
Psi_O(x_p24) = p-unit * Pi_O.
```

Equivalently, `Psi_O` must be a Fitting/Chow/Borcherds realization of the
pulled-back orbit Schubert divisor:

```text
D_O = sum_{t in O} div(Delta_C(t)).
```

In the explicit Fitting formulation, this is the determinant line of:

```text
Phi_O : direct_sum_{t in O} W_C -> direct_sum_{t in O} H/B_t.
```

For nonzero p24 right orbits this is a `5460 x 5460` determinant-line object,
but its certificate payload is the single descended p-unit norm, not the
expanded matrix.

## Local p24 Input

The p-local arithmetic is already friendly and explicit:

```text
p = 10^24 + 7,
p is split and unramified in K=Q(sqrt(D_K)),
sqrt(D_K) = +/- t/2 mod p,
p is prime to 2, 157, 211, 66254, 3107441.
```

The exact numbers are recorded in:

```text
p24/trace_gcd_p24_local_invariants.py
p24/trace_gcd_p24_local_intersection_invariants.md
```

These data make the local step checkable.  A successful theorem must prove:

```text
v_p(Psi_O(x_p24)) = 0
```

for all seven orbits `O`, at the selected ordinary prime above `p`.

## Lemma Stack Needed

1. Integral centered Fitting determinant.

```text
Delta_C(t)
```

is the determinant of a p-integral Schubert/Chow pairing

```text
det(W_C) tensor det(B_t) -> det(H),
H={w_0=0}.
```

2. Phase descent.

The determinant section must descend only after retaining the embedded
`157/211` relative phase data.  Plain `j`, genus, or full-class norms are too
coarse.

3. Orbit norm comparison.

For each Frobenius orbit `O`:

```text
Pi_O = p-unit * Psi_O(x_p24).
```

4. Local intersection formula.

The divisor of `Psi_O` is the pulled-back orbit Schubert divisor plus
boundary/vertical terms with no support at the selected ordinary prime.

5. Local nonintersection.

```text
v_p(Psi_O(x_p24)) = 0.
```

Then every `Pi_O` is a p-unit, hence every `Delta_C(t)` is nonzero, hence the
centered columns form a cyclic consecutive `157`-arc, hence the centered
profile rank certificate follows.

## What This Improves

Compared with the trace-GCD Chow target, the centered target has the smaller
geometric surface:

```text
seven orbit products for a 156-by-211 Schubert transversality problem.
```

The payload is:

```text
seven orbit products plus inverses = 14 field elements,
```

or a single full product plus inverse if a global `Psi_all` is constructed.

## Current Obstruction

The hard bridge is still construction of `Psi_O`.  Existing audits demote the
easy explanations:

```text
base-coefficient cyclic resultant norm: false in small actual-CM rows;
elementary right-cyclotomic unit product: false in small actual-CM rows;
small Fourier support: false in small actual-CM rows;
cyclic-code/MDS structure in natural coordinates: false;
visible low-degree projective curve: random-like;
plain random transversality: not a certificate.
```

The elementary unit boundary is recorded in:

```text
p24/centered_marginal_phase_unit_span_boundary.md
p24/centered_marginal_phase_unit_span_scan.py
p24/centered_marginal_global_product_mining_boundary.md
p24/centered_marginal_global_product_miner.py
```

The full-origin phase-sensitivity boundary is:

```text
p24/centered_marginal_full_origin_phase_sensitivity_gate.md
p24/centered_marginal_full_origin_phase_sensitivity_gate.py
p24/centered_marginal_full_origin_edge_shape_boundary.md
p24/centered_marginal_full_origin_edge_shape_boundary.py
p24/centered_marginal_full_origin_path_shape_boundary.md
p24/centered_marginal_full_origin_path_shape_boundary.py
p24/centered_marginal_orbit_fitting_block_cycle_audit.md
p24/centered_marginal_orbit_fitting_block_cycle_audit.py
```

On the pinned `D=-13319, q=13463, m=28, n=5, pair=(4,7)` row, cyclic origin
shifts preserve the full-origin product, but shuffling child order inside
each unordered recovery fiber changes both the alpha product and reduced
right sequence in `8/8` controls.  Therefore unordered recovery fibers do not
determine the centered full-origin product.

The same row also rejects the first bounded oriented-edge model:
`Delta_origin(i)` has no polynomial or rational expression of bidegree at
most `4` in `(j_i,j_{i+1})`, with `0/8` random repeated-alpha controls
fitting either.  A local correspondence norm would need more than one bounded
edge or a different phase-aware divisor.
The short-path boundary extends this check: no polynomial or rational
subgeneric total-degree formula appears in the two-edge path
`(j_i,j_{i+1},j_{i+2})` or the three-edge path
`(j_i,j_{i+1},j_{i+2},j_{i+3})`.

The same pinned row now verifies the honest orbit-Fitting plumbing: for every
right Frobenius orbit, the direct-sum and signed block-cycle determinants of
the actual centered Schubert window matrices equal the orbit product, and
singular controls zero the block-cycle determinant.  The determinant-line
assembly is therefore ready; the missing theorem is p-unitness of the
phase-aware section.

So the remaining p-unit theorem must be genuinely phase-aware.  It must keep
the non-genus `157/211` class-field phase while proving a local p-unit for the
orbit Schubert determinant, or construct the Chow/Fitting divisor directly.
