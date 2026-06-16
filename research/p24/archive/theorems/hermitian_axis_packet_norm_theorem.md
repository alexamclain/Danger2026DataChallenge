# Hermitian Axis Packet-Norm Theorem

This note packages the remaining Hermitian axis determinant checks into one
decomposition-field norm statement.

## Finite-Field Statement

For each H-character packet factor

```text
f_a | Phi_n
```

let

```text
D_a = det(Tr_{F_p[X]/(f_a)/F_p}(Y_i * Y_j^(p^(d/2)))).
```

Since the p24 packet degree is even and `p^(d/2) == -1 mod n`, this is also
the explicit autocorrelation determinant

```text
D_a = det(Tr_{F_p[X]/(f_a)/F_p}(Y_i(X) * Y_j(X^-1))).
```

The finite identity is checked in:

```text
p24/hermitian_axis_autocorrelation_formula.py
p24/hermitian_axis_autocorrelation_formula.md
```

The Hermitian axis certificate needs

```text
D_a != 0
```

for every packet `a`.

Equivalently, over the finite field:

```text
prod_a D_a != 0 mod p.
```

For p24 there are eight packets, so this is one degree-8 decomposition-field
norm condition rather than eight independent statements.

## Number-Field Interpretation

Let

```text
E^+ = Q(zeta_n + zeta_n^-1),
M^+ = (E^+)^<p>.
```

For p24,

```text
[E^+ : M^+] = 194215,
[M^+ : Q]   = 8.
```

The Hermitian axis determinant defines an algebraic element

```text
Delta_axis in M^+
```

whose residues at the eight primes of `M^+` above `p` are the eight finite
packet determinants `D_a`.  The p24 theorem can therefore be stated as:

```text
Delta_axis is a p-unit at every prime above p,
```

or equivalently:

```text
p does not divide Norm_{M^+/Q}(Delta_axis).
```

This is the matrix/lattice analogue of the scalar Hermitian packet norm in

```text
p24/decomposition_field_packet_norm_theorem.md
```

but it targets axis injectivity rather than one scalar energy.

## Data Check

I added:

```text
p24/hermitian_axis_packet_norm_scan.py
```

Compact multi-packet window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_axis_packet_norm_scan.py \
  --max-cases 2 --min-h 12 --max-h 40 --max-abs-D 6000 \
  --max-prime-quotients 4 --max-composite-quotients 4 \
  --min-n 3 --max-n 40 --q-stop 10000 \
  --max-splitting-primes 1 --max-axis-dim 20 --include-linear
```

reported:

```text
D=-5000 q=1259 m=2 n=15:
  packet_values=[1227, 469, 1137, 1135]
  packet_norm=741

D=-215 q=251 m=2 n=7:
  packet_values=[240, 106, 181]
  packet_norm=45
```

Broader small window:

```text
norm_rows=4
multi_packet_rows=2
zero_packet_norm_rows=0
non_origin_invariant_rows=0
max_packet_count=4
```

The packet values are not equal, so one packet cannot represent all packets.
The product is the correct scalar packaging.

## Current Target

The strongest compact theorem statement is:

```text
For the p24 third trace, the Hermitian axis determinant
Delta_axis in M^+ has p-unit norm to Q.
```

This would imply every packet determinant is nonzero, hence axis injectivity
in every packet, hence `L1` nonvanishing and the desired decomposed
certificate.

The theorem is still open.  It should be attacked as a degree-8 p-adic
unit/local-intersection statement for the selected CM axis lattice, not as an
origin-dependent statement and not as a product of independent CRT-axis
blocks.

A sidecar class-field pass reached the same target from the opposite
direction.  Known Gross-Zagier, Schofer/Lauter-Viray, theta/Borcherds,
Stickelberger/Jacobi-sum, and CM subfield tools naturally compute symmetric
norms, genus/ray data, or abstract quotient fields.  To finish this route they
would need a new phase-aware divisor or class-period formula whose CM value is
`Delta_axis` up to a p-unit, retaining both the order-`3107441` packet phase
and the `2*157*211` axis phase.
