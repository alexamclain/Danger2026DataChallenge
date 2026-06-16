# Trace-GCD Actual-CM Orbit-Norm Mining

Date: 2026-06-06

This note records the small-data theorem microscope added after the
block-cycle/Fitting norm triangle.

## Script

```text
p24/trace_gcd_actual_cm_orbit_norm_miner.py
```

Default behavior is deliberately pinned and fast:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_actual_cm_orbit_norm_miner.py
```

It uses the faithful small trace-GCD row

```text
D=-13319, q=13463, h=140, m=28, n=5,
left=4, right=7, factor_degree=4, extension_degree=6.
```

For each positive-size omitted row and each Frobenius orbit on `Z/7Z`, it
computes:

```text
Pi_O = prod_{t in O} det(M_t) mod q,
```

where `M_t` is the actual tail-on-kernel matrix from the trace-GCD row.

The broad scan mode is opt-in:

```text
--profile scan
```

This is intentional.  A broad PARI/Hilbert splitting pass with
`max_cases=24`, `max_abs_D=30000`, and `q_stop=80000` ran for a minute without
producing a positive-size row and was stopped.  The useful computation here is
the exact small-row falsifier, not an open-ended search.

## Pinned Output

The default pinned run reports:

```text
matrix_rows=1
orbit_rows=6
```

The six orbit norms are:

```text
omitted=0, orbit=[0],     norm=2125
omitted=0, orbit=[1,2,4], norm=2515
omitted=0, orbit=[3,6,5], norm=603
omitted=1, orbit=[0],     norm=11423
omitted=1, orbit=[1,2,4], norm=9495
omitted=1, orbit=[3,6,5], norm=6085
```

and the summary is:

```text
nonzero_orbits=6
zero_or_bad_orbits=0
determinant_mismatch_orbits=0
local_zero_det_orbits=0
zero_norm_orbits=0
```

## Interpretation

This supports the current p24 theorem target:

```text
For each right Frobenius orbit O, the actual phase-aware Fitting norm Pi_O
is a p-unit at the selected ordinary prime.
```

It does not prove that target.  It says that on the faithful small row where
the scalar, block-cycle, and split-norm triangle is already known to agree,
the actual positive-size orbit norms are all units.

The result is useful because it tests the obstruction itself:

```text
not just fixed Fourier minors,
not just scalar split-norm algebra,
but the actual tail-on-kernel determinant values from a CM row.
```

The p24 proof still has to construct the embedded phase-aware determinant-line
section, or an equivalent Borcherds/Fitting norm identity, and prove its
selected local value has valuation zero.
