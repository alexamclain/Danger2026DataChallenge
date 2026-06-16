# Hecke-Correlation Trace Boundary

This note records why moment, autocorrelation, Brandt/Hecke trace, and
correlation bookkeeping do not by themselves bypass the embedded
class-character trace primitive.

## Setup

Let the embedded CM roots be indexed by a cyclic class group

```text
G = <g>,      |G| = h = m*n,
H = <g^m>,    |H| = n.
```

Write

```text
j_i = j(g^i a_0),
y_r = sum_{k=0}^{n-1} j_{r + m*k},       0 <= r < m.
```

The target quotient polynomial is

```text
V(Y) = product_r (Y - y_r).
```

For the third p24 trace,

```text
m = 66254,
n = 3107441.
```

## Correlation Identities

Define cyclic correlations on the full CM torsor:

```text
C_2(d) = sum_i j_i j_{i+d},
C_k(d_2,...,d_k) = sum_i j_i j_{i+d_2} ... j_{i+d_k}.
```

Then the period power sums are subgroup projections of these correlations:

```text
sum_r y_r^2
  = sum_{d in H} C_2(d),

sum_r y_r^k
  = sum_{d_2,...,d_k in H} C_k(d_2,...,d_k).
```

Thus "compute the quotient polynomial by moments" is equivalent to computing
many `H`-projected correlations.  A global trace formula for all `d`, or a
genus-averaged trace formula, has erased exactly the odd quotient phase that
the p24 target needs.

## Fourier Form

Let

```text
T_s = sum_{r=0}^{m-1} zeta_m^(s*r) y_r
```

be the quotient-character traces.  If

```text
A(a) = sum_r y_r y_{r+a},
```

then

```text
DFT(A)(s) = T_s * T_{-s}.
```

Higher moments are the same convolution algebra:

```text
sum_r y_r^k
  = m^(1-k) * sum_{s_1+...+s_k=0 mod m} T_{s_1}...T_{s_k}.
```

So correlations and moments are diagonalized by the same high-order
class-character traces.  They are not a separate selector unless there is a
new formula that computes the `H`-projected correlations directly.

## Toy Calibration

The script

```text
p24/period_correlation_idempotent_toy.py
```

checks the `D=-5000`, `h=30`, quotient-size-10 calibration.  It verifies:

```text
square_sum_equals_projected_autocorrelation=1
autocorrelation_spectrum_matches_trace_products=1
period_autocorrelation_bm_complexity=10
nonzero_spectral_components=10
```

This is the expected "no collapse" behavior: the correlation sequence has full
quotient complexity, and every quotient spectral component is present.

The existing moment and norm toys show the same boundary:

```text
p24/period_moment_idempotent_toy.py
p24/relative_norm_phase_toy.py
```

## Implication For p24

For the third p24 target, a successful Hecke-correlation route would need to
compute the subgroup-projected correlations for

```text
H = <g^66254>,      |H| = 3107441,
```

or equivalently the non-genus quotient-character traces for the odd `157` and
`211` layers.  Standard global traces, ordinary Hecke traces, and genus traces
only give symmetric averages over too large a set of class differences.

Therefore:

```text
Brandt/Hecke/correlation bookkeeping is useful only after a new relative
projector theorem is supplied.  Without it, this is another formulation of
the same embedded non-genus relative-period problem.
```

This is not a lower bound against all possible correlation formulas.  It is a
normal-form warning: any claimed formula must specify where it gets the
high-order `H`-projection, not merely where it gets global Hecke traces.
