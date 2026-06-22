# P27 S-Root Parity Reduction

Date: 2026-06-21

## Claim

The `S/-S` involution explains why the remaining visible low-degree `S`
families should not be rerun.

For

```text
S = (U^2 - 4)/(2V),  K = S^2
```

the selected `d3` and `d4` targets are constant on `S/-S` pairs.  But in the
p27 sign regime `q mod 8 = 7`, so `chi(-1)=-1`, and `chi(S)` flips on every
pair.  Therefore:

```text
even S-semi-invariant classes reduce to K=S^2 classes;
odd S-semi-invariant classes cannot match an even target.
```

This is the structural reason the S-root branch screens should be treated as
closed for visible low-degree candidates.

## Probe

Gate:

```text
research/p27/archive/gates/p27_sroot_parity_reduction_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_sroot_parity_reduction_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_sroot_parity_reduction_probe.py \
  --small-primes 1471,1607,1847 \
  | tee research/p27/archive/probe_outputs/p27_sroot_parity_reduction_probe_20260621.txt
```

## Guard-Field Results

For `d3`:

```text
q=1471: pairs=50, same_target_pairs=50, opposite_chi_s_pairs=50
q=1607: pairs=49, same_target_pairs=49, opposite_chi_s_pairs=49
q=1847: pairs=63, same_target_pairs=63, opposite_chi_s_pairs=63
```

For `d4`:

```text
q=1471: pairs=28, same_target_pairs=28, opposite_chi_s_pairs=28
q=1607: pairs=28, same_target_pairs=28, opposite_chi_s_pairs=28
q=1847: pairs=45, same_target_pairs=45, opposite_chi_s_pairs=45
```

The forced odd-class obstruction is exact: an odd semi-invariant squareclass
can match at most one side of each pair:

```text
q=1471 d3: max_odd_semivariant_good=50/100
q=1607 d3: max_odd_semivariant_good=49/98
q=1847 d3: max_odd_semivariant_good=63/126
```

and similarly for `d4`.

## Reduction

The low-degree global semi-invariant cases are:

```text
even in S: f(S)=g(S^2)=g(K)
odd in S:  f(S)=S*g(S^2)=S*g(K)
```

Even classes are already K-line classes.  The relevant low-degree cases were
covered by:

```text
P27 E-Prime Signed-Doubling Kummer Screen
P27 Kummer Branch-Divisor Screen
```

Odd classes are impossible for a pair-even target because `chi(-1)=-1`.

## Interpretation

Positive:

```text
The S/-S involution now gives a proof-shaped reason not to rerun visible
low-degree S families.
```

Negative:

```text
No visible S parity class gives a source.
No odd S-class GPU sampler can work for d3/d4 in this sign regime.
```

## Next Test

The only remaining S/K route worth a serious pass is function-field extraction:

```text
1. Recover the actual d3 branch class over K or S.
2. Decompose it under S -> -S.
3. Compute branch degree/support/genus.
4. Promote only if the even component is low genus or gives a named recurrence
   inside the rational K-square stratum.
```

Do not spend more effort on visible low-degree S coefficient scans unless a
new theorem names a non-semi-invariant accidental class.

## Continue / Kill

```text
continue = Magma/Sage branch-class extraction and S-parity decomposition
continue = named non-visible recurrence/sourceable walk
kill = global even low-degree S classes as new work; they are K classes
kill = global odd S classes in p27 sign regime
kill = broad S coefficient scans without a theorem-shaped reason
```

## Linked Artifacts

- Parent: [P27 S-Root Belyi Structure Probe](p27_sroot_belyi_structure_probe_20260621.md)
- Related: [P27 S-Root Branch-Divisor Screen](p27_sroot_branch_divisor_screen_20260621.md)
- Probe: `research/p27/archive/gates/p27_sroot_parity_reduction_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_sroot_parity_reduction_probe_20260621.txt`

```text
p27_sroot_parity_reduction_rows=1/1
```
