# P27 Kummer Belyi Structure Probe

Date: 2026-06-21

## Claim

The signed-doubling K-line has a special Belyi/Lattes shape, but the visible
branch-value characters do not explain `d3` or `d4`.

This is positive structure for the next Magma/Sage extraction: normalize the
K-line problem by the branch values of the map.  It is negative for the cheap
sampler idea: products of the obvious branch atoms are already constant on the
selected rows.

## Probe

Gate:

```text
research/p27/archive/gates/p27_kummer_belyi_structure_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_kummer_belyi_structure_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kummer_belyi_structure_probe.py \
  --small-primes 1471,1607,1847 \
  --top 8 \
  | tee research/p27/archive/probe_outputs/p27_kummer_belyi_structure_probe_20260621.txt
```

## Symbolic Result

For residual coordinate `X`,

```text
K_num = (X^2 - 2X - 1)^2*(X^2 + 2X - 1)^2
K_den = 4*X*(X - 1)*(X + 1)*(X^2 + 1)^2
K = K_num / K_den
```

The branch resultant is:

```text
-4503599627370496*K^4*(K^2 + 4)^4
```

and the derivative numerator factors as:

```text
(X^2 - 2X - 1)*(X^2 + 2X - 1)
*(X^8 + 20X^6 - 26X^4 + 20X^2 + 1).
```

Thus the finite branch values are:

```text
K = 0
K^2 + 4 = 0
```

with `K = infinity` as the pole branch value.  The clean normalized coordinate is:

```text
lambda = -K^2/4
```

with branch values `0`, `1`, and `infinity`.

## Branch-Atom Screen

The nearest cheap explanation would be that `d3` or `d4` is a product of the
visible branch atoms:

```text
K
K^2 + 4
K^2
```

But on all guard-field K rows, these atoms are already square:

```text
q=1471 d3: K_plus=50/50, K2p4_plus=50/50, K2_plus=50/50
q=1471 d4: K_plus=28/28, K2p4_plus=28/28, K2_plus=28/28

q=1607 d3: K_plus=49/49, K2p4_plus=49/49, K2_plus=49/49
q=1607 d4: K_plus=28/28, K2p4_plus=28/28, K2_plus=28/28

q=1847 d3: K_plus=63/63, K2p4_plus=63/63, K2_plus=63/63
q=1847 d4: K_plus=45/45, K2p4_plus=45/45, K2_plus=45/45
```

Therefore every product of those atoms scores exactly like the constant
selector.  The best rates are just the majority classes:

```text
q=1471 d3: 28/50
q=1607 d3: 28/49
q=1847 d3: 45/63
```

and similarly for `d4`.

## Interpretation

Positive:

```text
The K-line map has an exact Belyi normalization.
The next extraction can work over lambda = -K^2/4 with branch values 0,1,infinity.
```

Negative:

```text
The visible branch-value characters are pre-paid by the selected source rows.
They do not explain d3/d4 and do not give a sampler.
```

## Next Test

Use the Belyi-normalized handoff for the actual source-cover extraction:

```text
1. Work over lambda = -K^2/4.
2. Normalize the d3 all-plus source cover over P^1_lambda or over P^1_K
   with the branch values marked.
3. Compute the branch divisor degree, support field degrees, and genus.
4. Promote only if the recovered class has genus <=1 or a named recurrence /
   sourceable walk.
```

This should replace blind coefficient-bound widening.  If the recovered branch
class is high/generic and `d4` is unrelated, the K-line source route should be
killed.

## Continue / Kill

```text
continue = Magma/Sage branch-class extraction in the Belyi-normalized K-line
continue = use lambda branch values as marked points in any genus computation
kill = products of K, K^2+4, K^2 as d3/d4 selectors
kill = branch-atom GPU sampler
```

## Linked Artifacts

- Parent: [P27 Kummer Branch-Extraction Handoff](p27_kummer_branch_extraction_handoff_20260621.md)
- Probe: `research/p27/archive/gates/p27_kummer_belyi_structure_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_kummer_belyi_structure_probe_20260621.txt`

```text
p27_kummer_belyi_structure_probe_rows=1/1
```
