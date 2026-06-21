# P27 E-Prime T-Cover Twist Obstruction

Date: 2026-06-21

## Claim

The descent from the residual elliptic curve

```text
E: W^2 = X^3 - X
```

to the 2-isogenous quotient

```text
E': V^2 = U^3 + 4U
U = X - 1/X
V = W*(X^2 + 1)/X^2
```

is real for the observed `d3`/`d4` bits, but the label-2 `T` source cover does
not descend as a plain rational `T`-linear object over `E'` in the p27 sign
regime.

This is a useful obstruction: it explains why plain `E'` line, two-line,
low-pole, affine-walk, and visible branch-factor screens can all be negative
without killing the quotient route.  The next viable test must keep the
twisted/Prym/Hilbert-90 class of the `T` cover, not just search functions of
`U,V`.

## Probe

Gate:

```text
research/p27/archive/gates/p27_eprime_tcover_twist_obstruction.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_eprime_tcover_twist_obstruction_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p27/archive/gates/p27_eprime_tcover_twist_obstruction.py \
  --small-primes 607,1471,1607,1847 \
  | tee research/p27/archive/probe_outputs/p27_eprime_tcover_twist_obstruction_20260621.txt
```

## Symbolic Identities

Use the involution from the rational `(0,0)` translation on `E`:

```text
sigma(X,W) = (-1/X, W/X^2)
```

The quotient coordinates satisfy:

```text
U = X - 1/X
V = W*(X^2 + 1)/X^2
V^2 = U^3 + 4U
```

The label-2 `T` cover is:

```text
T^2 = S
S = X*(X^2 + 1)*(X^2 + 2X - 1)
```

Under `sigma`:

```text
sigma(S) = (X^2 + 1)*(X^2 + 2X - 1)/X^5
sigma(S)/S = X^-6
S/sigma(S) = X^6
```

So a lift has:

```text
sigma(T) = +/- T/X^3
```

A rational `T`-linear invariant `T*f` over the quotient would require:

```text
sigma(f)/f = +/- X^3
```

But every expression of the form `sigma(f)/f` has norm `1`, while:

```text
Norm(+X^3) = -1
Norm(-X^3) = -1
```

Thus there is no such rational invariant over the base field.  The obstruction
would disappear only after adjoining a constant square root of `-1`.

## Finite-Field Checks

The guard fields used in the p27 quotient lane all match the p27 sign regime
`chi(-1)=-1`:

```text
q=607:  chi(-1) = -1, rational_T_linear_invariant_possible_over_Fq = 0
q=1471: chi(-1) = -1, rational_T_linear_invariant_possible_over_Fq = 0
q=1607: chi(-1) = -1, rational_T_linear_invariant_possible_over_Fq = 0
q=1847: chi(-1) = -1, rational_T_linear_invariant_possible_over_Fq = 0
```

The same enumeration verified:

```text
E' quotient relation mismatches = 0
sigma(S)/S ratio mismatches = 0
sigma(T) lift mismatches = 0
```

Only zero counters are omitted from the output; no mismatch counters appear.

## Online Magma Check

Input:

```text
research/p27/archive/fixtures/p27_eprime_tcover_twist_q1471_magma.m
```

Output:

```text
research/p27/archive/probe_outputs/p27_eprime_tcover_twist_q1471_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_tcover_twist_q1471_magma_20260621.xml
```

Result:

```text
RESULT p27_eprime_tcover_twist_q1471 ok -1 1660 0 0 0 0 0
```

This independently confirms the quotient equation, the `sigma(S)/S=X^-6`
ratio, the `sigma(T)=T/X^3` lift, and the absence of a base-field constant
that would trivialize the `Norm=-1` obstruction over `q=1471`.

## Interpretation

Positive:

```text
The 2-isogeny quotient remains valid for the observed d3/d4 bits.
The obstruction is explicit and symbolic, not a sampling artifact.
It identifies the missing structure as a twisted T-cover/Prym class.
```

Negative:

```text
Plain rational searches on E' are structurally incomplete.
The killed E' low-pole and branch-factor screens should not be repeated with
more arbitrary coefficients.
No GPU sampler follows from the E' quotient alone.
```

## Next Test

Work with the twisted `T`-cover quotient rather than plain `E'`:

```text
sigma(T)=T/X^3
Norm(X^3)=-1
```

Concrete next tests:

```text
1. Build the quotient/Prym of the label-2 T-cover by sigma, allowing the
   constant twist j^2=-1 over F_{q^2}; then descend the resulting Kummer
   class back to the p27 sign regime.

2. In Magma/Sage, compute the divisor class of the d3 and d4 double covers on
   this twisted quotient, not on E' alone.

3. Validate any named class on q=1471 or q=1607 before testing on p27 rows.
```

A GPU-worthy candidate would be a formula or sampler that remembers this
twisted class and predicts `d3` or a recurrence to `d4` without paying a new
half-density gate.

## Continue / Kill

```text
continue = twisted T-cover / Prym / Hilbert-90 quotient extraction
continue = Magma/Sage validation over q=1471/q=1607 for named twisted classes
continue = p27 validation only after a named twisted formula exists

kill = repeating plain E' low-pole or sparse branch-factor screens
kill = treating the E' quotient alone as a source sampler
kill = expecting a T-linear invariant over F_q when chi(-1)=-1
```

```text
p27_eprime_tcover_twist_obstruction_rows=1/1
```
