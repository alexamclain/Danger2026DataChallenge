# P27 S-Root Belyi Structure Probe

Date: 2026-06-21

## Claim

The rational square-root coordinate

```text
S = (U^2 - 4)/(2V),  K = S^2
```

has an exact branch structure, but its visible branch atoms are already
pre-paid on the selected p27 rows.  They do not explain `d3` or `d4`, and they
do not give a sampler.

The target bits are even under `S -> -S`, while `chi(S)` is odd in the p27
sign regime.  Any useful source must therefore come from a non-visible branch
class over the K/S function field, not from the obvious ramification atoms.

## Probe

Gate:

```text
research/p27/archive/gates/p27_sroot_belyi_structure_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_sroot_belyi_structure_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_sroot_belyi_structure_probe.py \
  --small-primes 1471,1607,1847 \
  --top 8 \
  | tee research/p27/archive/probe_outputs/p27_sroot_belyi_structure_probe_20260621.txt
```

## Symbolic Result

For the `S` map, the branch resultant is:

```text
-4503599627370496*S^8*(S^2 - 2S + 2)^4*(S^2 + 2S + 2)^4
```

So the finite branch atoms are:

```text
S
S^2 - 2S + 2
S^2 + 2S + 2
```

## Pair Structure

In the guard fields, all rows are paired under `S -> -S`, and the target is
constant on each pair:

```text
q=1471 d3: pairs=50, same_target_pairs=50, opposite_chi_s_pairs=50
q=1607 d3: pairs=49, same_target_pairs=49, opposite_chi_s_pairs=49
q=1847 d3: pairs=63, same_target_pairs=63, opposite_chi_s_pairs=63
```

For `d4`:

```text
q=1471 d4: pairs=28, same_target_pairs=28, opposite_chi_s_pairs=28
q=1607 d4: pairs=28, same_target_pairs=28, opposite_chi_s_pairs=28
q=1847 d4: pairs=45, same_target_pairs=45, opposite_chi_s_pairs=45
```

Thus `chi(S)` cannot be the selector: it flips across each pair while the
target does not.

## Branch-Atom Screen

The quadratic branch atoms are already square on every selected row:

```text
q=1471 d3: S2m2Sp2_plus=100/100, S2p2Sp2_plus=100/100, S2_plus=100/100
q=1607 d3: S2m2Sp2_plus=98/98,   S2p2Sp2_plus=98/98,   S2_plus=98/98
q=1847 d3: S2m2Sp2_plus=126/126, S2p2Sp2_plus=126/126, S2_plus=126/126
```

For `d4`:

```text
q=1471 d4: S2m2Sp2_plus=56/56, S2p2Sp2_plus=56/56, S2_plus=56/56
q=1607 d4: S2m2Sp2_plus=56/56, S2p2Sp2_plus=56/56, S2_plus=56/56
q=1847 d4: S2m2Sp2_plus=90/90, S2p2Sp2_plus=90/90, S2_plus=90/90
```

Products of the visible branch atoms therefore score like either the constant
selector or the anti-invariant `chi(S)` selector.  They do not identify `d3`
or `d4`.

## Interpretation

Positive:

```text
The S map has exact marked branch values.
The d3/d4 target class is even under S -> -S.
```

Negative:

```text
The visible S-branch atoms are pre-paid by the selected source rows.
chi(S) is anti-invariant and cannot select an even target.
No GPU sampler follows from visible S ramification.
```

## Next Test

Use the S branch values only as markers for a real function-field extraction.
The remaining useful computation is:

```text
1. Build the d3 source cover over P^1_S or P^1_K.
2. Compute its actual branch divisor/class and genus.
3. Check whether the class is even under S -> -S and whether it descends to K.
4. Promote only if the branch class is low genus or yields a named sourceable
   recurrence/walk inside the rational K-square stratum.
```

Kill condition:

```text
The recovered branch class is high/generic and d4 is an unrelated fresh cover.
```

## Continue / Kill

```text
continue = Magma/Sage K/S branch-class extraction with S branch values marked
continue = even/odd class decomposition under S -> -S during extraction
kill = visible S branch atoms as d3/d4 selectors
kill = chi(S) or products containing only visible branch atoms as a GPU sampler
```

## Linked Artifacts

- Parent: [P27 S-Root Branch-Divisor Screen](p27_sroot_branch_divisor_screen_20260621.md)
- Related: [P27 Lambda Rational-Quotient Obstruction](p27_lambda_rational_quotient_obstruction_20260621.md)
- Probe: `research/p27/archive/gates/p27_sroot_belyi_structure_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_sroot_belyi_structure_probe_20260621.txt`

```text
p27_sroot_belyi_structure_probe_rows=1/1
```
