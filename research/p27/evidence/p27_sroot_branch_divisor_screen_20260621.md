# P27 S-Root Branch-Divisor Screen

Date: 2026-06-21

## Claim

The rational square-root coordinate of the Kummer line is the right next
source coordinate after the lambda obstruction, but its nearest low-genus
branch-divisor source family is negative.

On

```text
E': V^2 = U^3 + 4U
```

the signed-doubling Kummer coordinate satisfies:

```text
K = x([2]P) = ((U^2 - 4)/(2V))^2.
```

So define the rational square-root coordinate:

```text
S = (U^2 - 4)/(2V),  K = S^2.
```

Unlike `lambda=-K^2/4`, this keeps the rational p27 K-square stratum rather
than quotienting by `K -> -K`.

## Probe

Gate:

```text
research/p27/archive/gates/p27_sroot_branch_divisor_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_sroot_branch_divisor_probe_d3_20260621.txt
research/p27/archive/probe_outputs/p27_sroot_branch_divisor_probe_d4_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_sroot_branch_divisor_probe.py \
  --small-primes 1471,1607,1847 \
  --targets d3 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_branch_divisor_probe_d3_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_sroot_branch_divisor_probe.py \
  --small-primes 1471,1607,1847 \
  --targets d4 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_branch_divisor_probe_d4_20260621.txt
```

The screen tested exact double-cover selectors:

```text
z^2 = f(S)
deg_S(f) <= 4
```

where the branch divisor splits over each guard field into rational linear
factors and irreducible quadratic factors.

## Results

### S Rows

The `S` coordinate is the oriented lift of the K-line rows:

```text
q=1471 d3: E' rows = 100, S rows = 100, paired S/-S = 100
q=1607 d3: E' rows = 98,  S rows = 98,  paired S/-S = 98
q=1847 d3: E' rows = 126, S rows = 126, paired S/-S = 126
```

For `d4`:

```text
q=1471 d4: E' rows = 56, S rows = 56, paired S/-S = 56
q=1607 d4: E' rows = 56, S rows = 56, paired S/-S = 56
q=1847 d4: E' rows = 90, S rows = 90, paired S/-S = 90
```

### d3

No exact `d3` S-divisors exist in the split degree `<=4` family:

```text
q=1471 d3 exact divisors = none
q=1607 d3 exact divisors = none
q=1847 d3 exact divisors = none
```

Search sizes:

```text
q=1471 d3:
  S rows = 100
  linear atoms = 1371
  irreducible quadratic atoms = 1081185
  distinct degree-2 side masks = 2020319

q=1607 d3:
  S rows = 98
  linear atoms = 1509
  irreducible quadratic atoms = 1290421
  distinct degree-2 side masks = 2428206

q=1847 d3:
  S rows = 126
  linear atoms = 1721
  irreducible quadratic atoms = 1704781
  distinct degree-2 side masks = 3184840
```

### d4

Unlike the K and lambda quotient screens, `d4` also has no local exact fits:

```text
q=1471 d4 exact divisors = none
q=1607 d4 exact divisors = none
q=1847 d4 exact divisors = none
```

## Interpretation

Positive:

```text
S is the correct rational square-root coordinate to test after the lambda
obstruction.
The S/-S pairing is explicit in the guard-field data.
```

Negative:

```text
No split degree <=4 S-branch divisor explains d3.
No genus <=1 rational S-line sampler follows.
The same split family also fails for d4, so there is no later-gate local-fit
lead to chase in S.
```

## Next Test

The cheap rational line-source family is now exhausted across:

```text
K split degree <=4
lambda split degree <=4
S split degree <=4
```

The remaining K-square-stratum route should be one of:

```text
1. actual Magma/Sage branch-class/genus extraction over K or S;
2. a non-split irreducible cubic/quartic support test that is not blind fitting;
3. a named recurrence/sourceable walk tied to the S/-S involution.
```

Promotion bar:

```text
a stable d3 class over q=1471,1607,1847 with genus <=1, or a named recurrence
that sources the d3 all-plus condition inside the rational K-square stratum.
```

Kill condition:

```text
the recovered K/S branch class has high/generic degree and d4 is an unrelated
fresh half-cover.
```

## Continue / Kill

```text
continue = Magma/Sage K/S branch-class and genus extraction
continue = exact non-split cubic/quartic support only if theorem-shaped
kill = split degree <=4 S-branch divisors for d3/d4
kill = GPU sampler from S-line low-degree branch factors
```

## Linked Artifacts

- Parent: [P27 Lambda Rational-Quotient Obstruction](p27_lambda_rational_quotient_obstruction_20260621.md)
- Related: [P27 Kummer Branch-Divisor Screen](p27_kummer_branch_divisor_screen_20260621.md)
- Related: [P27 Lambda Branch-Divisor Screen](p27_lambda_branch_divisor_screen_20260621.md)
- Probe: `research/p27/archive/gates/p27_sroot_branch_divisor_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_sroot_branch_divisor_probe_d3_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_sroot_branch_divisor_probe_d4_20260621.txt`

```text
p27_sroot_branch_divisor_screen_rows=1/1
```
