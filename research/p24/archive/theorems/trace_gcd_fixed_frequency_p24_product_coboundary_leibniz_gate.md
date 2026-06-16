# Fixed-Frequency p24 Product-Coboundary Leibniz Gate

Date: 2026-06-06

## Point

The raw trace-resolvent term has product shape:

```text
x = T_left * R_right.
```

A noncircular way to construct the raw full-order coboundary is to use a
product rule.  If

```text
sigma(A) = alpha*A
B = sigma(V) - (epsilon/alpha)*V,
```

then

```text
A*B = alpha^(-1) * (sigma(A*V) - epsilon*(A*V)).
```

So, instead of constructing a potential for the whole product at once, it is
sufficient to prove:

```text
1. the left trace-resolvent factor has known sigma-covariance alpha;
2. the right multiplicative resolvent has a matching twisted coboundary with
   twist epsilon/alpha.
```

Then the product is the raw full-order coboundary needed by the transfer gate.
The nested `B/C`, `C/E`, and quotient Hilbert-90 stages are formal after that.

## p24 Interpretation

For the p24 fixed-frequency product

```text
T_{1,0,a} * R_{chi,-a},
```

the candidate source theorem becomes:

```text
sigma(T_{1,0,a}) = alpha_a * T_{1,0,a}

R_{chi,-a} = sigma(V_{chi,a}) - (epsilon_chi/alpha_a)*V_{chi,a}
```

or the same statement with orientation/inverses adjusted to the chosen
`lambda_chi` convention.

This is stronger than packet cancellation but weaker than termwise right-combo
vanishing.  It asks for a right-resolvent coboundary, not a right-resolvent
zero.

## Boundary

The twist must match.  In the finite model:

```text
wrong twist    -> usually nonzero full twisted trace;
random right   -> usually nonzero full twisted trace.
```

So this is not a generic product identity.  The CM/Lang theorem must explain
the right twist and potential.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_product_coboundary_leibniz_gate.py
```

Key output:

```text
product_coboundary_identity_failures=0
product_full_twisted_trace_nonzero=0/48
nested_quotient_trace_nonzero=0/48
wrong_twist_product_trace_zero=1/48
random_right_product_trace_zero=0/48
product_coboundary_leibniz_identity_holds=1
left_covariance_plus_matching_right_coboundary_suffices=1
p24_candidate_source_is_right_resolvent_coboundary_with_matching_twist=1
```
