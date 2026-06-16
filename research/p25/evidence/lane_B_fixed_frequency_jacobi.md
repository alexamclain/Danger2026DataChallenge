# Lane B: Fixed-Frequency/Jacobi p25

Date: 2026-06-12

## Files inspected

- `Danger2026DataChallenge/p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.md`
- `Danger2026DataChallenge/p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_decomposition_theorem.md`
- `Danger2026DataChallenge/p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate.md`
- `Danger2026DataChallenge/p24/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.md`
- `Danger2026DataChallenge/p24/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.py`
- `Danger2026DataChallenge/p24/00_CURRENT_CONTEXT.md`
- `Danger2026DataChallenge/p24/all_trace_period_frontier.md`
- `Danger2026DataChallenge/p24/decomposed_certificate_handoff.md`
- `Danger2026DataChallenge/p24/trace_gcd_p24_compressed_search_readiness.md`
- `pomerance-p25-run/README.md`, `RESULT.md`, `src/vpp.py`, `runs/LATEST_P25_RUN.txt`

## p25 quotient/factor observations

For `p = 10^25 + 13`, `sqrt_floor(p)=3162277660168` and the DANGER exponent is
`k=42`.

The three supplied traces are exactly the three consecutive `N/2^42` branches:

```text
t= 5808037298190:  v2(N)=42, N/2^42=2273736754431
                   = 3^2 * 601 * 420361759

t= 1409990787086:  v2(N)=50, N/2^42=2273736754432
                   = 2^8 * 11 * 13 * 1543 * 40253
                   odd part = 8881784197

t=-2988055724018:  v2(N)=42, N/2^42=2273736754433
                   = 17 * 5503 * 24304783
```

The CM order discriminants have common shape `Delta=t^2-4p = 16*D_K`; all
three are conductor `4` maximal-field rows, not the p24 conductor-2 shape.
Bounded `quadclassunit` returned:

```text
t= 5808037298190:
  D_K=-391668921427112813920247
  h=453621311724 = 2^2 * 3 * 7 * 17^2 * 37 * 505027
  group=(226810655862, 2)

t= 1409990787086:
  D_K=-2375745373770787638476791
  h=1198636371592 = 2^3 * 11 * 13620867859
  group=(299659092898, 2, 2)

t=-2988055724018:
  D_K=-1941970186885204113620983
  h=499836054144 = 2^7 * 3 * 7 * 17 * 107 * 151 * 677
  group=(62479506768, 2, 2, 2)
```

A timeout-bounded p24-style composite split-ideal scan
(`prime_bound=200`, `max_factors=3`, `max_norm=100000`) found a real smaller
formal split on the negative trace:

```text
t=-2988055724018
terms=(2,127,-71)
index=203728 = 2^4 * 7 * 17 * 107
recovery/order n=2453448 = 2^3 * 3 * 151 * 677
max(index,n)/sqrt(p)=7.758e-7
seeded proxy/sqrt(p)=2.145e-2
```

This beats the p24 formal max-degree ratio and gives a much smaller quotient
skeleton than `C_7 x C_179`:

```text
n=2453448
rho=p^2 mod n
ord_n(rho)=12675 = 3 * 5^2 * 13^2
```

Two post-trace quotient choices check purely by coset arithmetic:

```text
B=325, right=3, c=13:
  <rho>/<B> ~= C_3 x C_13
  quotient size=39
  value-dual equations=21, admissible dimension=18
  product cosets cover quotient: yes

B=25, right=3, c=169:
  <rho>/<B> ~= C_3 x C_169
  quotient size=507
  value-dual equations=255, admissible dimension=252
  product cosets cover quotient: yes
```

There is also a cleaner prime-C-axis alternate on the same trace:

```text
terms=(41,-137)
index=43328 = 2^6 * 677
recovery/order n=11536098 = 2 * 3 * 7 * 17 * 107 * 151
rho=p^16 mod n
ord_n(rho)=3975 = 3 * 5^2 * 53
B=25 gives <rho>/<B> ~= C_3 x C_53
quotient size=159
value-dual equations=81, admissible dimension=78
product cosets cover quotient: yes
```

## Transferable gates

Transferable:

- The p24 value-side theorem shape ports formally: for a selected defect
  `f(r,c)` on `C_a x C_c`, target
  `C`-row sums independent of `r`, `f(r,0)=0`, and
  `f(r,c)+f(-r,-c)=kappa` for `c != 0`.
- The selected-defect producer split also ports: raw two-level inversion
  complement plus selected affine row balance.
- The finite quotient-provenance check ports cleanly: identify `rho`, a
  trace subgroup `B`, right generator `rho^c`, C-axis generator `rho^a`, and
  verify product cosets cover `<rho>/<B>`.

Not automatically transferable:

- The exact p24 constants `right=7`, `c=179`, `B=31`, and
  `lambda_179=-1/89`.
- The p24 proof pressure from conductor `2`; p25 rows above have conductor `4`.
- Any actual CM/Lang producer. The scan only finds formal quotient/recovery
  structure and Frobenius quotient skeletons; it does not construct the
  selected weighted packet or embedded recovery root.

Best p25 theorem labs:

```text
tiny smoke:     C_3 x C_13, quotient size 39, lambda=-1/6
clean prime C:  C_3 x C_53, quotient size 159, lambda=-1/26
larger square:  C_3 x C_169, quotient size 507, lambda=-1/84
```

Prefer `C_3 x C_53` for a theorem-shaped analogue because the C-axis is prime.
Keep `C_3 x C_13` as the cheapest falsifier.

## First falsifier / positive next command

First positive command: promote the quotient smoke below into a real p25 gate
only if needed. It does no class-set enumeration and should finish in seconds.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from sympy import factorint

p = 10**25 + 13
candidates = [
    ("tiny", 2453448, 2, 3, 13, 325),
    ("primeC", 11536098, 16, 3, 53, 25),
]

def subgroup(gen, order, mod):
    out, v = set(), 1
    for _ in range(order):
        out.add(v)
        v = v * gen % mod
    assert v == 1 and len(out) == order
    return out

def coset_key(v, sub, mod):
    return min(v*h % mod for h in sub)

for name, n, rho_exp, right, c, b in candidates:
    rho = pow(p, rho_exp, n)
    raw = right * b * c
    assert pow(rho, raw, n) == 1
    internal = pow(rho, right, n)
    B = subgroup(pow(internal, c, n), b, n)
    qcosets = {coset_key(pow(rho, e, n), B, n) for e in range(raw)}
    product = {
        coset_key(pow(rho, c*r, n) * pow(internal, ci, n) % n, B, n)
        for r in range(right)
        for ci in range(c)
    }
    equations = (right - 1) + right * (c - 1) // 2 + (right - 1) // 2
    print(name, "raw_order", raw, factorint(raw),
          "quotient", right*c, "equations", equations,
          "dimension", right*c - equations,
          "cover", qcosets == product)
PY
```

First real falsifier after any p25 selected packet builder exists:

```text
materialize f on C_3 x C_13 first;
reject immediately if any of:
  f(r,0) != 0,
  row sums depend on r,
  f(r,c)+f(-r,-c) is not constant for c != 0.
```

If `C_3 x C_13` passes only accidentally or is too small to authenticate the
producer, repeat the same value-side check on `C_3 x C_53`.

## Recommendation

Continue Lane B narrowly. The p25 negative trace has a surprisingly clean
formal quotient skeleton, and `C_3 x C_13` / `C_3 x C_53` are small enough to
make the p24 value-side theorem shape more testable than at p24.

Kill the broad port. Do not spend CPU on generic Jacobi decomposition or CM
enumeration, and do not claim a certificate path from the quotient skeleton
alone. Lane B earns one small quotient/value-side gate; if the actual selected
packet cannot be produced or fails the three value-side identities, kill this
route and leave the main p25 search fleet alone.
