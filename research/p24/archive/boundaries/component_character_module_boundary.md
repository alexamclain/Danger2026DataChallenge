# Component Character-Module Boundary

This note records a packet-field version of the `K`-character diagnostic.

## Setup

For a complement component `c | m`, define packet-field axis sums

```text
Y_t = sum_{r == t mod c} F_r,      0 <= t < c.
```

If a packet field

```text
A = F_q[X]/(f)
```

contains `mu_c`, equivalently

```text
ord_c(q) | deg(f),
```

then the component axis diagonalizes inside `A`:

```text
G_s = sum_t zeta_c^(s*t) Y_t.
```

Frobenius groups the nontrivial `G_s` into character modules.  The p24
`211`-axis has exactly this shape because

```text
ord_211(p)=35 | ord_3107441(p)=388430.
```

The `157`-axis does not diagonalize inside the p24 packet field.

## Rank Warning

There is a subtle rank boundary here.  When the character roots lie in the
base field, the DFT matrix is a base-field change of coordinates and preserves
the base-field span of packet elements.  When the character roots lie in the
packet field itself, the DFT matrix is invertible over the packet field, but it
need not preserve the `F_p`-span of the coordinate entries.

I added the minimal warning toy:

```text
p24/packet_field_dft_rank_warning_toy.py
```

It works over `F_4/F_2`: an invertible `2 x 2` matrix over `F_4` sends
`(0,1)` to `(1,alpha)`, increasing the `F_2`-span of the coordinate entries
from `1` to `2`.

So packet-field diagonalization is a structural coordinate chart.  The formal
rank certificate still has to be stated either over the base field, or in the
tensor/Moore scalar-extension language.

## Scan

I added:

```text
p24/component_character_module_scan.py
```

Broader component window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/component_character_module_scan.py \
  --max-cases 12 --min-h 12 --max-h 100 --max-abs-D 20000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 100 --q-stop 250000 \
  --max-splitting-primes 4 --include-linear \
  --min-component 2 --max-component 40 --summary-only
```

Output:

```text
module_rows=132
dimension_possible_rows=63
dimension_bound_rows=69
full_module_rows=63
dimension_possible_internal_failure_rows=0
zero_orbit_rows=0
rank_defect_rows=0
rows_by_component={2: 80, 3: 34, 4: 8, 5: 9, 7: 1}
```

Smaller repeat:

```text
module_rows=66
dimension_possible_rows=38
dimension_bound_rows=28
full_module_rows=38
dimension_possible_internal_failure_rows=0
zero_orbit_rows=0
rank_defect_rows=0
rows_by_component={2: 36, 3: 23, 5: 7}
```

## Interpretation

No component character orbit vanished, and no dimension-possible Frobenius
module rank defect appeared.

This supports the p24 proof split from

```text
p24/l1_axis_direct_sum_proof_strategy.md
```

in which the `211`-axis character decomposition is used as structure:

```text
the 211-axis is organized by packet-field character modules;
the 157-axis requires an external character field with only quadratic
intersection with the packet field.
```

It is still evidence, not a proof: the missing p24 theorem is that the actual
selected CM packet reduction keeps these component modules normal and mutually
direct in the appropriate base-field or Moore/tensor rank sense.

For p24 itself, the packet-field module decomposition is in

```text
p24/packet_field_k_module_audit.py
```

Over one H-packet field, the axis pieces are:

```text
2-axis:   1 orbit of size 1
157-axis: 2 orbits of size 78
211-axis: 210 orbits of size 1
```

and the full nontrivial `K`-character set has orbit histogram

```text
{1: 421, 78: 844}.
```

These are Frobenius module counts for the scalar-extension picture.  They are
bookkeeping for Moore/rank statements, not by themselves a rank certificate.
A single embedding into the full splitting field would not preserve
packet-field linear rank, and a packet-field coordinate DFT need not preserve
the base-field coordinate-entry span.
