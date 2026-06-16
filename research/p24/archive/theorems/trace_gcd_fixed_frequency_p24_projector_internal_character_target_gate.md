# p24 Projector/Internal-Character Target Gate

This gate combines two equivalent descriptions of the remaining p24 theorem.

The raw tower shape is:

```text
right quotient: C_7
internal B/E:   C_179 x C_31
```

The right-axis target says the six nontrivial quotient projectors vanish.  The
internal trace target says that, after `Tr_{B/C}`, the trivial `C/E` character
component vanishes.

The combined finite statement is:

```text
Tr_{C/E}(Tr_{B/C}(Pi_m(packet))) = 0,
m = 1,...,6.
```

In the toy model `C_7 x C_5 x C_3`, quotient projectors commute with the
`B/C` trace.  Random projected packets still have nonzero final internal
trace, so the quotient projector alone is not enough.  Packets supported in a
nontrivial `C` character have zero final trace but nonzero `B/C` trace; packets
with trivial `C` support are detected by the final trace.

Latest markers:

```text
projector_idempotent_failures=0
projector_commutes_with_B_over_C_trace_failures=0
random_projected_packets_final_internal_trace_nonzero=143/144
forced_nontrivial_C_character_final_trace_zero=6/6
forced_nontrivial_C_character_B_trace_nonzero=6/6
forced_trivial_C_character_final_trace_nonzero=6/6
```

So the missing arithmetic theorem is now narrow:

```text
for the actual weighted CM/Lang obstruction,
each nontrivial right quotient projector has no trivial C/E component
after the B/C trace.
```
