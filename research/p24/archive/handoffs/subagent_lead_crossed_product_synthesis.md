# Subagent Lead Crossed-Product Synthesis

Date: 2026-06-05

The existing subagent was reused after the thread hit the subagent limit.  It
returned the same theorem boundary as the local work:

```text
construct Xi_lead in S = Q(mu_m) Q(zeta_n)^<p>
with packet residues unit(a) * Delta_lead(a),
then prove Norm_{S/K_m}(Xi_lead) mod p != 0.
```

Equivalently, in the beta/Frobenius model:

```text
f_lead(theta^(-beta)) = Delta_lead(beta)
R_Omega = det_B(mul_f on B[Y]/phi_Omega)
        = product_{gamma in Omega} Delta_lead(gamma)
```

and the arithmetic theorem is that these `R_Omega` are p-units.

The subagent flagged the same traps:

```text
packetwise Gaussian pivots do not descend;
Delta_tail has kernel-basis denominators unless globally trivialized;
ordinary beta norms D_rep^|Omega| are false;
sparse support or E[Y] descent is not visible in the audits;
plain j and single-edge phase formulas are disfavored.
```

It suggested a phase-aware class-field/modular-unit proof as the most likely
positive route: realize the leading determinant-line norm as a CM value of a
global function and use local intersection/valuation formulas to prove that
the selected split ordinary prime contributes no zero.

This supports making:

```text
p24/trace_frame_lead_crossed_product_norm.md
```

the current front-door theorem statement.

