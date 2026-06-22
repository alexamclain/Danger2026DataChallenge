# P27 Trace/Norm Dplus U6 Row-Bit Aeta Factor Boundary

Date: 2026-06-22

## Claim

The next decisive Dplus row-bit test is now staged, but online Magma cannot
run it at the `q=607` size.

After the row-bit lift stayed irreducible over `F_607(t)` and over the H90
elliptic base `E_h90`, the next bridge test is:

```text
does the row-bit lift factor after adjoining the H90 domain-spin layer z,
or after adjoining the second-layer payload rho^2 = A_eta?
```

The fixtures are concrete.  Online Magma returns `504 Gateway Timeout` for
the `q=607` domain-spin and `eta=+1` `A_eta` factorization tests.  A tiny
`q=31` domain-spin smoke fixture is also staged, but the calculator was
temporarily disabled when submitted.

## Artifacts

Fixtures:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q607_magma.m
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_aeta_factor_eta1_q607_magma.m
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q31_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q607_magma_20260622.xml
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_eta1_q607_magma_20260622.xml
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q31_magma_20260622.xml
```

## Online Results

`q=607` domain-spin factorization:

```text
504 Gateway Timeout
```

`q=607`, `eta=+1`, `A_eta` factorization:

```text
504 Gateway Timeout
```

`q=31` domain-spin smoke:

```text
<calculator><offline>The Magma calculator is temporarily disabled.</offline></calculator>
```

## Required Offline Results

For the domain-spin fixture:

```text
factor degrees of R(t,S^2-2) over L = E_h90(z), z^2=t*(t^2+2t-1)*(t^2+1)
```

For the `A_eta` fixture:

```text
factor degrees of R(t,S^2-2) over N = L(rho), rho^2 = A_eta
```

Promotion:

```text
degree drop or structured factorization over L or N,
especially a split compatible with the descended d3 row bit.
```

Kill:

```text
irreducible degree 32 over L and over both eta A_eta covers.
```

## Interpretation

This is not a mathematical negative yet.  It is a boundary:

```text
online Magma can factor the row-bit lift over E_h90;
online Magma cannot factor it after adjoining the H90 spin/payload layers.
```

The next concrete CAS ask is therefore narrow enough for an offline Magma/Sage
agent: run these fixtures, first `q=31`, then `q=607`, and report factor
degrees over the domain-spin and `A_eta` covers.

Point-fiber follow-up:
[P27 Trace/Norm Dplus U6 Row-Bit H90 Point-Fiber Probe](p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_20260622.md)
shows that rational point fibers are already uniform over `E_h90`, domain-spin,
and `A_eta` in the tested small fields, while `t` alone can be mixed.  This
keeps the offline factor test relevant: the question is not whether H90 matters,
but whether the pointwise uniformity comes from a true quotient/Prym relation,
local solubility, or selected-source side conditions.

## Continue / Kill

```text
continue = offline factorization over domain-spin and A_eta covers
continue = if any factor drops, extract the quotient/Prym/source relation
continue = if irreducible, record a sharp independence obstruction

kill = using online Magma for this factorization tier
kill = assuming E_h90 irreducibility already proves A_eta-cover irreducibility
```

```text
p27_trace_norm_dplus_u6_rowbit_aeta_factor_boundary_rows=1/1
```
