# Fixed-Frequency p24 Twisted Hilbert-90 Payload Gate

Date: 2026-06-06

## Point

The current p24 covariance-plus-descent target can be made more explicit.  On
each `p^780` factor cycle, the Gauss-normalized contribution is a twisted
trace.  For a Frobenius `sigma` of order `7` and a nontrivial seventh-root
eigenvalue `epsilon`, define

```text
Tr_epsilon(x) = sum_{i=0}^6 epsilon^(-i) sigma^i(x)
D_epsilon(y)  = sigma(y) - epsilon*y.
```

Then finite Hilbert 90 gives

```text
im(D_epsilon) = ker(Tr_epsilon).
```

Therefore, after the internal degree-5549 trace/norm has produced an
E-valued seed, the missing arithmetic theorem can be sharpened:

```text
For each nontrivial right quotient character chi and each of the ten
p^780 quotient factor cycles, the Gauss-normalized E-valued seed contribution
is a D_epsilon-coboundary in the embedded degree-7 quotient-cycle algebra.
```

Equivalently, construct a CM/Lang potential `Y` such that

```text
seed_chi,cycle = sigma(Y_chi,cycle) - epsilon_chi * Y_chi,cycle
```

with the orientation adjusted to the chosen `lambda_chi` convention.  The
cycle twisted trace then vanishes before any class-set enumeration.

## Why This Helps

The previous theorem target was:

```text
complete twisted trace descends to L
+ nontrivial eigenvalue
=> zero.
```

That is logically correct but still opaque.  The Hilbert-90 form tells us what
an explicit embedded tower proof should construct: a potential for the
Gauss-normalized seed term.  It also separates the valid proof from the known
mirages:

```text
random seed                 -> usually nonzero twisted trace;
semilinear covariance alone -> nonzero eigenspace;
descended nonzero trace     -> impossible for nontrivial eigenvalue;
coboundary seed             -> zero twisted trace.
```

This is still finite linear algebra, not the CM/Lang construction itself.  The
remaining mathematical work is two-stage:

```text
1. identify the internal degree-5549 trace/norm that produces the E-valued
   seed from the raw relative factor contribution;
2. identify the actual CM source of the quotient-cycle potential.
```

Skipping step 1 is invalid: on the raw relative factor cycle `p^780` has order
`38843 = 7*5549`, not order `7`.

## p24 Numerology

```text
ord_m(p) = 5460
ord_n(p) = 388430
gcd(ord_m(p), ord_n(p)) = 70
rho = p^780
rho_order_on_E = 7
rho fixes F_p(mu_157)
rho shifts the 70 E-factors by +10
factor cycles = 10 cycles of length 7
rho shifts the right H-quotient nontrivially
```

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_twisted_hilbert90_payload_gate.py
```

Key output:

```text
rho_factor_cycle_count=10
rho_factor_cycle_length=7
twisted_trace_ranks=[1, 1, 1, 1, 1, 1]
twisted_coboundary_ranks=[6, 6, 6, 6, 6, 6]
twisted_trace_kernel_dimensions=[6, 6, 6, 6, 6, 6]
twisted_coboundary_kernel_dimensions=[1, 1, 1, 1, 1, 1]
image_subset_kernel_failures=0
image_equals_kernel_failures=0
random_twisted_traces_fixed_nonzero=0/48
coboundary_seeds_have_zero_twisted_trace=48/48
twisted_hilbert90_image_equals_trace_kernel=1
p24_payload_can_be_stated_as_factor_cycle_coboundary=1
cm_lang_work_is_constructing_the_coboundary_potential=1
```
