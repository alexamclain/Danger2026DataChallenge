# P27 Arithmetic Baseline

Date: 2026-06-21

## Target

```text
p = 1000000000000000000000000103
p = 10^27 + 103
prime = true
sqrt_floor(p) = 31622776601683
sqrt_floor(p)^2 <= p < (sqrt_floor(p) + 1)^2 = true
k = ceil(log2(sqrt_floor(p))) = 45
bit_length(p) = 90
p mod 8 = 7
p mod 4 = 3
```

## Factor Data

```text
p - 1 = 2 * 122761 * 1325021 * 1455833 * 2111423087
p + 1 = 2^3 * 3 * 345451 * 120615272981310422221
```

## Immediate Consequences

Because `p mod 4 = 3`, the practical square-root branch family used for p26 is
still in the friendly regime for this codebase.

Because `p mod 8 = 7`, the quadratic character of `2` changes relative to p26:

```text
chi_p26(2) = -1
chi_p27(2) = +1
```

Any p26 formula involving `2`, `sqrt(2)`, reciprocal branches, or a
normalization chosen by squareclass must be reverified on p27 before it is used
as a filter or source selector.

## Command

```bash
python3 - <<'PY'
from math import isqrt, log2, ceil
import sympy as sp
p = 10**27 + 103
s = isqrt(p)
print('p =', p)
print('isprime =', sp.isprime(p))
print('sqrt_floor =', s)
print('sqrt_check =', s*s <= p < (s+1)*(s+1))
print('ceil_log2_sqrt =', ceil(log2(s)))
print('bit_length =', p.bit_length())
print('p mod 8 =', p % 8)
print('p mod 4 =', p % 4)
print('factor p-1 =', sp.factorint(p - 1))
print('factor p+1 =', sp.factorint(p + 1))
PY
```

## Output

```text
p = 1000000000000000000000000103
isprime = True
sqrt_floor = 31622776601683
sqrt_check = True
ceil_log2_sqrt = 45
bit_length = 90
p mod 8 = 7
p mod 4 = 3
factor p-1 = {2: 1, 122761: 1, 1325021: 1, 1455833: 1, 2111423087: 1}
factor p+1 = {2: 3, 3: 1, 345451: 1, 120615272981310422221: 1}
```

