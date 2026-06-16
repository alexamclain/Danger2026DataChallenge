# p24 End-of-Day Search Status

Date: 2026-06-07

Question from the current thread: do we have enough to start testing inside the
compressed p24 search space, if we are willing to fill in proof after a
successful computational hit?

## Answer

Partly, but not in the strongest sense.

The finite verifier surface is ready:

```text
conditional p-unit payload:      4 field elements
fixed-frequency verifier:        1092 scalar equations
compressed independent surface:  48 scalar equations
deterministic residual choices:  2 anchor signs, Kummer exponent e=1
```

But the actual input to that verifier is still missing:

```text
selected p-integral CM/Lang subgroup kernel polynomial
```

or equivalently, in the low-moment reformulation:

```text
28 new truncated selected child-polynomial coefficients
  first layer:  e_2..e_4
  second layer: e_2..e_26
```

Without those values there is no honest `2`-case or `48`-case p24 search to
run.  Any direct search is still a generic DANGER3/Pomerance lottery.

## Commands Run

Compressed readiness:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_p24_compressed_search_readiness.py
```

Confirmed:

```text
p24_h_coset_equations=1092
p24_compressed_independent_equations=48
conditional_punit_payload_field_elements=4
p24_low_moment_pairing_constraints=30
conclusion=compressed_search_surface_ready_but_producer_missing
```

Full theorem-gate harness after adding adjacent-anchor cyclic divisibility:

```text
task_count=264
passed=264
failed=0
```

Truncated child-polynomial gate:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_truncated_polynomial_gate.py
```

Confirmed:

```text
p24_first_layer_new_coefficients=e2_to_e4_count=3
p24_second_layer_new_coefficients=e2_to_e26_count=25
p24_selected_path_new_coefficients=28
p24_low_moment_producer_can_target_28_new_child_polynomial_coefficients=1
```

Direct p24 Pomerance smoke:

```text
p24/pomerance_probe 1000000000000000000000007 0        10000000
p24/pomerance_probe 1000000000000000000000007 10000000 10000000
p24/pomerance_probe 1000000000000000000000007 20000000 10000000
```

Result:

```text
total_trials=30000000
rate_per_core=about 0.116M trials/sec
hits=0
```

Additional small smoke from seed offsets `30000000..33000000`:

```text
total_trials=4000000
rate_per_core=about 0.115M trials/sec
hits=0
```

This only covers about:

```text
3e7 / (20*sqrt(p)/3) ~= 4.5e-6
```

of the binary's own heuristic p24 budget, so it is not a serious route to an
end-of-day result without a new filter.

Small all-trace composite correspondence sweep:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/all_trace_composite_order_search.py \
  --prime-bound 200 --max-factors 3 --max-norm 100000000 --show 8
```

Best global row remained the known third-trace formal quotient family:

```text
trace=-1178414874616
norm=42158
x0_index=64152
index=422
order=487868237
terms=(2, -107, -197)
```

This is a useful formal decomposition but still prints the key caveat:

```text
seeded_proxy_assumes_a_seed_root_or_embedded_quotient=1
search_does_not_construct_CM_roots=1
```

## Current Operational Conclusion

The next computation worth running is not more generic Pomerance volume.  It is
a producer-facing search for the missing values:

```text
selected 179-subgroup CM/Lang kernel polynomial
```

or the equivalent:

```text
28 selected child-polynomial coefficients
```

Once one candidate for those values exists, the p24 verifier is small enough
to check immediately.
