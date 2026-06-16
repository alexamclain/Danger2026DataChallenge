# Trace-GCD Prefix Gaussian Period Basis

Date: 2026-06-06

## Point

The right cyclotomic field in the p24 prefix theorem has a canonical
Gaussian normal basis.

For

```text
p = 10^24 + 7,
right = 211,
p mod 211 = 114,
ord_211(p) = 35,
211 = 6*35 + 1.
```

The integer `2` is primitive modulo `211`.  Let

```text
C0 = <2^35> subset (Z/211Z)^*
   = {1, 197, 196, 210, 14, 15}.
```

For a primitive `211`st root `zeta = zeta_211`, define

```text
eta_i = sum_{c in C0} zeta^(p^i c),     0 <= i < 35.
```

Since `gcd(6,35)=1` and `p` has order `35` modulo `211`, the standard
Gaussian-period theorem gives:

```text
eta_0, eta_1, ..., eta_34
```

as a normal basis of

```text
R = F_p(zeta_211)
```

over `F_p`.

## Prefix Coefficients

The normal-basis coefficient theorem from

```text
p24/trace_gcd_prefix_normal_basis_coefficients.md
```

can therefore be made canonical:

```text
C_{i,j} = Tr_{E/L}(eta_i * H_{157,211}(1,v_j)),
j in {2,3,5,6}, 0 <= i < 35.
```

The prefix Fitting theorem is exactly:

```text
rank_Fp(C_{i,j}) = 140.
```

Equivalently, the Moore/Chow determinant of these `140` elements of
`L=F_p(mu_157)` is a p-unit.

## Semilinear Convolution Form

Let `tau_R` generate `Gal(E/L)`, so `tau_R(zeta_211)=zeta_211^p`.  Then

```text
tau_R(eta_i) = eta_{i+1}.
```

For

```text
S_j = H_{157,211}(1,v_j),
```

the coefficient is

```text
C_{i,j}
  = sum_{h=0}^{34} tau_R^h(eta_i * S_j)
  = sum_{h=0}^{34} eta_{i+h} * H_{157,211}(1,p^h v_j),
```

with indices modulo `35`.  This is a phase-aware cyclic convolution along
the right Frobenius orbit.  It is not a pure right-Frobenius module statement:
the left/right Hermitian packet cocycle still moves the coupled phase, as in

```text
p24/axis_frobenius_cocycle_boundary.md
```

The value of the Gaussian-period basis is that the missing determinant is now
a named convolutional period determinant, not an arbitrary Plucker coordinate.

There is one important scalar-extension caveat.  The length-35 DFT uses
`K=F_p(mu_35)=F_{p^4}`, not just `F_p`.  Since `K subset L`, multiplying DFT
coefficients into `L` is tempting but not rank-safe.  The DFT diagonalization
must be performed in:

```text
L tensor_{F_p} K.
```

The safe tensor form and the collapse pitfall are recorded in:

```text
p24/trace_gcd_prefix_gaussian_dft_scalar_extension_boundary.md
p24/trace_gcd_prefix_gaussian_dft_boundary_toy.py
```

The Gaussian DFT factors `G_a` are units after scalar extension, but this
does not permit frequency-by-frequency division in the full rank problem.
That target-unit scaling caveat is recorded in:

```text
p24/trace_gcd_prefix_gaussian_unit_factor_boundary.md
```

The tensor product also decomposes as four copies of `L`; the global rank is
controlled by transversality of the four component kernels:

```text
p24/trace_gcd_prefix_tensor_component_rank_criterion.md
```

## Missing Arithmetic Theorem

Prove:

```text
rank_Fp{
  Tr_{E/L}(eta_i * H_{157,211}(1,v_j))
  : j in {2,3,5,6}, 0 <= i < 35
} = 140.
```

Equivalently:

```text
sum_{j in {2,3,5,6}} y_j * H_{157,211}(1,v_j)
  in (tau_R - 1)E
  =>
y_j = 0.
```

The Gaussian basis gives the explicit determinant section that a
local-intersection, Fitting, Borcherds, or phase-aware class-field proof must
show is a p-unit.

## Cheap Gate

The finite construction is guarded by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_gaussian_normal_basis_toy.py
```

The toy verifies a small Gaussian normal basis of type `2`, checks the
trace-dual reconstruction identity in a coprime tensor extension, and records
the exact p24 exponent data above.
