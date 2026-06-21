# P27 Kummer Branch-Divisor Screen

Date: 2026-06-21

## Claim

The Kummer-line descent remains the best reduced target, but the first
low-genus branch-divisor source family is negative.

The screen tested exact squarefree products of:

```text
rational linear factors in K
irreducible quadratic factors in K over F_q
```

with total degree `<= 4` on the Kummer line

```text
K = x([2]P),  E': V^2 = U^3 + 4U.
```

For the decisive next-gate target `d3`, there is no exact divisor of this form
over `q=1471`, `q=1607`, or `q=1847`.  This kills the nearest elliptic-source
subcase:

```text
z^2 = f(K), deg(f) <= 4, f split into degree 1/2 branch points over F_q.
```

The `d4` screen shows why guard fields matter: q1471 and q1607 have many
degree-3 exact fits, but q1847 has none.  Those d4 fits are treated as
small-row local interpolation, not a recurrence.

## Probe

Gate:

```text
research/p27/archive/gates/p27_kummer_branch_divisor_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kummer_branch_divisor_probe_d3_20260621.txt
research/p27/archive/probe_outputs/p27_kummer_branch_divisor_probe_d4_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kummer_branch_divisor_probe.py \
  --small-primes 1471,1607,1847 \
  --targets d3 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kummer_branch_divisor_probe_d3_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kummer_branch_divisor_probe.py \
  --small-primes 1471,1607,1847 \
  --targets d4 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kummer_branch_divisor_probe_d4_20260621.txt
```

The solver constructs character signatures for all zero-free rational linear
factors and all irreducible quadratic factors, then uses a meet-in-the-middle
search over products with total degree `<=4`.

## Results

### d3

The decisive source bit has no exact low-degree split divisor:

```text
q=1471 d3 exact divisors = none
q=1607 d3 exact divisors = none
q=1847 d3 exact divisors = none
```

Search sizes:

```text
q=1471 d3:
  linear atoms = 1421
  irreducible quadratic atoms = 1081185
  distinct degree-2 side masks = 2090095

q=1607 d3:
  linear atoms = 1558
  irreducible quadratic atoms = 1290421
  distinct degree-2 side masks = 2503324

q=1847 d3:
  linear atoms = 1784
  irreducible quadratic atoms = 1704781
  distinct degree-2 side masks = 3295217
```

### d4

Local fits appear in the smaller d4 samples:

```text
q=1471 d4: degree-3 exact divisors found
q=1607 d4: degree-3 exact divisors found
```

But the decisive guard field kills persistence:

```text
q=1847 d4 exact divisors = none
```

Interpretation:

```text
The q1471/q1607 d4 positives are local interpolation artifacts.
They do not define a stable d4 recurrence or source.
```

## Interpretation

Positive:

```text
The K-line divisor machinery is now executable.
The negative d3 result is stronger than the small-integer coefficient screen:
it includes non-rational quadratic branch points over each guard field.
```

Negative:

```text
No degree <=4 split branch divisor explains d3.
No elliptic source z^2=f(K), deg(f)<=4, follows from the K-line descent.
The d4 local positives do not persist to q1847.
```

## Next Test

The next K-line move should be one of:

```text
1. Search unrestricted irreducible cubic/quartic branch factors with a smarter
   finite-field algorithm.
2. Use Magma/Sage to recover the actual branch divisor/class and compute its
   degree/genus.
3. Compare d3 and d4 branch classes only after a stable d3 class is named.
```

Promotion bar:

```text
An exact d3 branch class that survives q=1471 and q=1607 and has genus <=1,
or a named recurrence relating the d4 branch class to the d3 class.
```

Kill condition:

```text
The recovered K-line branch divisor has high/generic degree and d4 is an
unrelated fresh half-cover.
```

## Continue / Kill

```text
continue = K-line branch-divisor extraction beyond split degree <=4
continue = Magma/Sage genus and divisor-class computation on P^1_K
continue = finite-field solver for irreducible cubic/quartic factors if it is
           exact and guard-field based

kill = degree <=4 split divisors using rational/irreducible-quadratic factors
kill = q1471/q1607-only d4 fits as recurrence evidence
kill = GPU sampler from the current K-line branch-divisor screens
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_kummer_branch_divisor_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_kummer_branch_divisor_probe_d3_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_kummer_branch_divisor_probe_d4_20260621.txt`
- Parent: [P27 E-Prime Signed-Doubling Kummer Screen](p27_eprime_signed_doubling_kummer_screen_20260621.md)
- Related: [P27 Kummer Small-Integer Polynomial Screen](p27_kummer_small_integer_poly_screen_20260621.md)

```text
p27_kummer_branch_divisor_screen_rows=1/1
```
