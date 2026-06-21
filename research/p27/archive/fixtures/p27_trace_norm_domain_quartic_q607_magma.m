// P27 trace/norm domain spin cover: online Magma validation.
//
// Eliminating t from
//   a = t - 1/t
//   r^2 = t*(t^2 + 2*t - 1)*(t^2 + 1)
// gives the quartic cover
//   r^4 - (a+2)(a^2+1)(a^2+4) r^2 + (a+2)^2(a^2+4) = 0.
//
// This is the concrete cover behind the domain_line spin obstruction.  The
// script checks the elimination identity and asks Magma for the projective
// genus over q = 607, which has the same chi(-1), chi(2) signs as p27.

SetColumns(0);
q := 607;
Fq := GF(q);

K<a> := FunctionField(Fq);
Pt<t> := PolynomialRing(K);
Fpoly := t*(t^2 + 2*t - 1)*(t^2 + 1);
relation := t^2 - a*t - 1;
rem := Fpoly mod relation;
Acoef := a*(a+2)*(a^2+3);
Bcoef := (a+2)*(a^2+2);
rem_ok := rem eq (a+2)*(a*(a^2+3)*t + (a^2+2));

Pr<r> := PolynomialRing(K);
quartic_from_elim := (r^2 - Bcoef)^2 - a*Acoef*(r^2 - Bcoef) - Acoef^2;
quartic_named := r^4 - (a+2)*(a^2+1)*(a^2+4)*r^2 + (a+2)^2*(a^2+4);
elim_ok := quartic_from_elim eq quartic_named;

A2<a0,r0> := AffineSpace(Fq, 2);
C := Curve(A2, r0^4 - (a0+2)*(a0^2+1)*(a0^2+4)*r0^2 + (a0+2)^2*(a0^2+4));
PC := ProjectiveClosure(C);
genus := Genus(PC);
pts := #Points(C);
sing := #SingularPoints(PC);

print "RESULT p27_domain_quartic_q607", elim_ok, rem_ok, genus, pts, sing;
