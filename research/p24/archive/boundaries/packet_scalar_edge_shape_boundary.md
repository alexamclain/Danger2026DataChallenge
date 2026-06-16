# Packet Scalar Edge-Shape Boundary

This note records a follow-up to the plain-`j` divisor diagnostics for the two
live scalar routes:

```text
Hermitian packet norm,
L1 packet norm.
```

The plain-`j` tests were negative.  A more phase-aware object could plausibly
live on an oriented correspondence edge, so the next cheap diagnostic is:

```text
(x_i,z_i) = (j_i, j_{i+step})
```

and ask whether the packet norm is a low-bidegree function of `(x_i,z_i)`.

## Diagnostic

I added:

```text
p24/packet_scalar_edge_shape_scan.py
```

For a small split CM cycle, quotient `h=m*n`, packet factor `f | Phi_n`, and
scalar `S`, it rotates the selected origin and computes

```text
N_i = Res(f, S_f(origin=i)) mod q.
```

It then searches for low-bidegree polynomial and rational relations

```text
N_i = F(j_i, j_{i+step}),
N_i = P(j_i, j_{i+step}) / Q(j_i, j_{i+step}).
```

A relation is counted as theorem-relevant only if it lies below the generic
interpolation threshold and random controls preserving any observed
`H`-periodicity do not also fit.  In particular, a rational fit with

```text
2 * (deg_x+1) * (deg_z+1) > h
```

is generic interpolation, not evidence for a modular correspondence identity.

## D=-5000 Sanity Run

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packet_scalar_edge_shape_scan.py \
  --only-D -5000 --min-h 20 --max-h 40 --q-stop 2000 \
  --include-linear --scalars hermitian ordinary L1 M0 \
  --max-prime-quotients 2 --max-composite-quotients 2 \
  --min-n 3 --max-n 8 --max-bidegree 3 \
  --random-trials 4 --random-combos 4 \
  --max-rows 16 --summary-only
```

Output:

```text
rows=16
rows_with_any_edge_fit_in_search_window=16
rows_with_theorem_relevant_edge_fit=8
l1_rows=4
l1_rows_with_theorem_relevant_edge_fit=0
hermitian_rows=4
hermitian_rows_with_theorem_relevant_edge_fit=0
```

The eight theorem-relevant fits are the expected symmetric constants
(`ordinary` and `M0`).  `L1` and Hermitian only fit at rational bidegree
`(3,3)` in the detailed version of this toy, where the monomial count is
already on the generic side; random controls fit too.

## Composite-m Live-Scalar Window

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packet_scalar_edge_shape_scan.py \
  --max-cases 5 --min-h 12 --max-h 70 --max-abs-D 16000 \
  --max-prime-quotients 0 --max-composite-quotients 2 \
  --min-n 3 --max-n 60 --q-stop 90000 \
  --max-splitting-primes 1 --include-linear --require-composite-m \
  --scalars hermitian L1 --max-bidegree 3 \
  --random-trials 4 --random-combos 4 \
  --max-rows 20 --summary-only
```

Output:

```text
rows=10
rows_with_any_edge_fit_in_search_window=0
rows_with_theorem_relevant_edge_fit=0
l1_rows=5
l1_rows_with_theorem_relevant_edge_fit=0
hermitian_rows=5
hermitian_rows_with_theorem_relevant_edge_fit=0
```

So the first oriented-edge coordinate does not reveal a low-bidegree structure
for the live scalars in this p24-like small window.

## Sidecar Criterion

Gibbs' sidecar reached the same threshold rule.  For `V=(a+1)(b+1)` monomials,
a rational edge formula on `h` samples is already generic around

```text
2V >= h.
```

The `D=-5000` `(3,3)` rational fits have `V=16` and `h=30`, hence
`2V > h`; random controls fitting is expected.

The mathematical obstruction is stabilizer mismatch.  A bounded oriented edge
still translates with the full CM torsor.  The large `H` stabilizer appears
only after whole-subgroup aggregation, so an edge formula would need to be a
new phase-aware modular identity rather than ordinary local `X0(ell)` data.

## Consequence

The current phase-aware identity search has now ruled out three cheap shapes:

```text
plain j-coordinate:
  generic for both L1 and Hermitian packet norms;

selected finite-field zero lemma:
  too few zeros for selected scalars;

single oriented edge (j_i, j_{i+1}):
  no below-interpolation bidegree relation for L1/Hermitian.
```

This does not disprove a Borcherds/Schofer or embedded class-field theorem.
It says the divisor, if it exists, must retain the high-order packet phase in
a less local way: a longer correspondence object, a true relative character
projection, or a higher-dimensional phase-aware construction rather than a
bounded edge function.
