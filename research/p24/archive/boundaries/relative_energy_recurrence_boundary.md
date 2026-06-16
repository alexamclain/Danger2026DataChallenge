# Relative Energy Recurrence Boundary

The energy certificate reduces one harmful packet to the scalar

```text
E_a = sum_d zeta_n^(a*d) C_d,
C_d = sum_i j_{i+m*d} j_i.
```

This suggests a possible constructive shortcut: maybe the autocorrelation
sequence `C_d` has a low-order recurrence along the recovery subgroup.  Then
the eight energy values might be computable without enumerating all
`n=3107441` recovery shifts.

I tested this at small CM scale in:

```text
p24/relative_autocorrelation_complexity_scan.py
```

A 100-case run with the same range as the natural relative-resolvent scan
reported:

```text
rows=237
full_or_near_full_bm_rows=237
low_bm_rows=0
dft_rows=237
full_dft_support_rows=237
total_energy_zeros=0
```

Every tested autocorrelation row had full or near-full Berlekamp-Massey
complexity and full DFT support.

## Interpretation

The scalar energy is a cleaner theorem target, but the natural
autocorrelation sequence still behaves like high-order class data in toy CM
cycles.  There is no visible low-recurrence or sparse-spectrum structure that
would let us compute the p24 energies from a bounded recurrence.

For p24, a recurrence shortcut would need a theorem explaining why

```text
Tr(j * sigma^(m*d)j)
```

for the order-`3107441` subgroup is governed by substantially fewer than
`3107441` parameters.  The small data gives no sign of such a theorem, and
the modular interpretation still ranges over high-order non-genus
autocorrelations.
