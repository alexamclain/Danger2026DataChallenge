# Reduced-Anchor Low-Moment Pairing Window

The section-pairing guardrail says one trace/sum constraint is far too weak to
select a p24 child fiber.  This note records the sharper, potentially useful
window: a small number of power sums may behave like independent subset hashes.

For an unordered child set `S`, define:

```text
P_d(S) = sum_{x in S} x^d.
```

The deterministic Newton route needs all child-degree many power sums to
recover the child polynomial.  The probabilistic/anti-collision route would
try to prove far fewer moments uniquely identify the actual CM child among
the embedded quotient roots.

Toy checks:

```text
D=-5000, q=1259, h=30:
  one power sum already selects each true degree-3 child above the top parent.

random F_101 control, 20 choose 10:
  one power sum leaves 1820 subsets;
  two power sums leave 20 subsets;
  three power sums isolate the target subset.
```

p24 entropy estimates:

```text
first odd layer:
  choose 157 roots from 314
  log10 subsets = 93.176548
  random-unique moment count = 4

second odd layer:
  choose 211 roots from 66254
  log10 subsets = 616.781509
  random-unique moment count = 26
```

This is not a proof.  The required new theorem would be a selected-prime
CM anti-collision statement, plus a construction of these selected moments
without enumerating the class set.  It is, however, a sharper target than
full relative character reconstruction and may be a productive CS/probability
import point.
