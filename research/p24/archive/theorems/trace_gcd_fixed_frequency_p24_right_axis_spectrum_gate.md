# Right-Axis Spectrum Gate

After the right Gauss-sum reduction, the remaining p24 theorem is a statement
about the right `211` axis of an internally traced profile.

Let `B_s` be the profile obtained by applying the `B/C` then `C/E` internal
trace to the weighted CM polynomial target and grouping by nonzero right
frequency `s in F_211^*`.  Then the six nontrivial order-7 equations are:

```text
sum_{s in F_211^*} chi^{-1}(s) B_s = 0
```

for every nontrivial order-7 multiplicative character `chi` of `F_211^*`.

Equivalently, the seven sums over

```text
H = <2^7> subset F_211^*
```

and its cosets are all equal.  This is the same H-coset condition as the
certificate verifier, now stated after the named right-obstruction
polynomial `G_chi`.

## p24 Frobenius Bookkeeping

```text
p log_2 mod 211      = 198, quotient shift 2 mod 7
p^780 log_2 mod 211  = 90,  quotient shift 6 mod 7
p^5460 mod 211       = 1
```

Thus the internal generator `p^5460` fixes the right `211` axis completely.
The internal `B/C` and `C/E` traces do not average the seven right H-cosets.
If the order-7 spectrum vanishes, it is a genuine CM/Lang identity for the
internally traced `G_chi` profile.

Harness markers:

```text
p780_shifts_right_order7_quotient_nontrivially=1
p5460_internal_trace_fixes_right_211_axis=1
internal_trace_does_not_average_right_H_cosets=1
target_is_no_order7_multiplicative_spectrum_on_traced_right_axis=1
equivalently_H_coset_sums_equal_on_F211_star=1
conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_spectrum_gate
```
