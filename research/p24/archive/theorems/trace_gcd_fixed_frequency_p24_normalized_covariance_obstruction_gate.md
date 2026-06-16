# Fixed-Frequency p24 Normalized Covariance Obstruction Gate

Date: 2026-06-06

## Point

The pre-recombination covariance route has a normalization obstruction.

For the raw right factor

```text
R_chi = sum_v chi(v) T_{0,v,-a},
```

`rho = p^780` gives the expected nontrivial order-7 covariance.  But the right
Gauss sum has the same covariance:

```text
rho(R_chi)      = lambda_chi * shifted R_chi
rho(tau(chi))  = lambda_chi * tau(chi).
```

So after Gauss normalization,

```text
tau(chi)^(-1) R_chi
```

has trivial covariance under the same relative/factor shift.  The left factor
also has trivial `rho` covariance because `p^780 = 1 mod 157`.

Therefore the normalized product components satisfy the formal covariance

```text
rho(Z_delta,a) = Z_delta+10,rho*a,
```

with eigenvalue `1`.  If we also demand a nontrivial normalized covariance on
the same shifted components, then every component must be zero.

## Consequence

The surviving H-coset proof should not be phrased as:

```text
prove nontrivial covariance of the Gauss-normalized components.
```

That is componentwise too strong unless a new theorem really proves all those
components vanish.  Existing actual-CM product/internal-trace boundaries make
that implausible as a generic packet statement.

The cleaner surviving target is the internal-trace/right-coboundary theorem:

```text
prove the nested internal trace of the specific weighted G_chi packet is zero,
then use Hilbert 90 to construct the matching right coboundary.
```

This keeps the actual CM/Lang weighted packet in the theorem instead of trying
to extract a nontrivial eigenvalue after the Gauss factor has already canceled
it.

## Check

Added:

```text
p24/trace_gcd_fixed_frequency_p24_normalized_covariance_obstruction_gate.py
```

It verifies the p24 twist bookkeeping:

```text
raw_right_lambda_exponents=[6,5,4,3,2,1]
gauss_sum_lambda_exponents=[6,5,4,3,2,1]
normalized_right_exponents=[0,0,0,0,0,0]
normalized_product_exponents=[0,0,0,0,0,0]
```

and a finite-field control where imposing a nontrivial normalized covariance
in addition to the formal trivial covariance forces the component array to be
zero.
