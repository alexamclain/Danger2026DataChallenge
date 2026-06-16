# Higher-Dimensional Factor Route Audit

Question: can a genus-2 curve, an abelian surface, a Weil restriction, or a
product/gluing construction hide the strict p24 elliptic factor cheaply and
then split it out afterward?

Current conclusion: no known bypass.  Every route that yields an explicit
elliptic factor with one of the strict p24 traces has already selected the
same target elliptic isogeny class.  The selector may be hidden inside a
Jacobian, an idempotent, a Weil restriction, or a splitting map, but Tate's
theorem makes the obstruction the same.

## Cases

Genus-2 / Jacobian:

```text
If Jac(C) has Weil polynomial f_target * f_other, Tate gives an F_p-isogeny
factor in the strict target class.  Constructing such a C without already
naming the target factor is the hard part.  Known genus-2 CM methods compute
Igusa/class data for the full surface, and split-Jacobian methods recover
elliptic subcovers only once the surface already encodes them.
```

Product with the cheap near-square curve:

```text
The D=-7 curve gives trace +/-2*10^12 and both curve/twist have only v2=3.
It is not a strict DANGER3 trace.  A product E_{-7} x E_target or a gluing
construction still requires E_target and its torsion/gluing data.
```

Weil restriction / descent:

```text
If Res_{F_{p^m}/F_p}(B) contains E/F_p, then B is isogenous over F_{p^m}
to E base-changed to F_{p^m}.  The extension-trace identity

    T_m^2 - 4*p^m = (t^2 - 4*p) * U_{m-1}(t,p)^2

shows that the target fundamental CM field is unchanged in extensions.
Thus extension/descent multiplies the large discriminant by a square instead
of turning it into small CM.
```

Small-CM abelian surface:

```text
A simple primitive quartic CM surface has no elliptic F_p factor.  If the
Weil polynomial splits with the strict elliptic factor, then the CM algebra
already contains the large target quadratic field and extracting the factor
amounts to constructing a curve in that target class.
```

## Anchors

- Tate's finite-field isogeny theorem:
  https://pazuki.perso.math.cnrs.fr/index_fichiers/Tate66.pdf
- Sutherland's CRT CM algorithm:
  https://arxiv.org/abs/0903.2785
- Genus-2 CM CRT:
  https://arxiv.org/abs/math/0405305
- Jacobians in abelian-surface isogeny classes:
  https://aif.centre-mersenne.org/articles/10.5802/aif.2430/

## Local Cross-Checks

```text
p24/near_square_cm_audit.py
p24/extension_trace_cm_audit.py
p24/subagent_root_only_cm_note.md
p24/smooth_class_tower_route_note.md
```

The smooth third class group remains a legitimate structural lead only if we
can build an explicit quotient tower plus a recovery map to `j`.  The
higher-dimensional wrapper does not supply that missing root selector.
