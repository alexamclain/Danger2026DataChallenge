// P27 label-2 cyclic-quartic component check.
//
// This validates the eliminated order-4/H90 cyclic-quartic model over q=1471.
// The raw projective scheme is not irreducible; reduce/decompose before
// asking for genus.
//
// Expected output:
//
// RESULT p27_label2_cyclic_components_q1471 2 true false
// COMP 1 1 30 17 1656
// COMP 2 1 1 0 1472

SetColumns(0);
q := 1471;
F := GF(q);
A3<X,W,R> := AffineSpace(F,3);

T2 := X*(X^2 + 1)*(X^2 + 2*X - 1);
mt := (X + 1)*(2*W*X + X^3 + X^2 - X - 1);
m0 := (X^2 + 1)*(X^2 + 2*X - 1)*(W*X + W + 2*X^2);
Salpha := W*(X + 1) + 2*X^2;

eqE := W^2 - (X^3 - X);
eqQ := X^2*R^4
    - 2*X*W*(X^2 + 1)*m0*R^2
    + 4*W^2*(X^2 + 1)^2*T2*Salpha^2;

C := Curve(A3, [eqE, eqQ]);
PC := ProjectiveClosure(C);
RC := ReducedSubscheme(PC);
comps := IrreducibleComponents(RC);

print "RESULT p27_label2_cyclic_components_q1471", #comps, IsReduced(RC),
    IsIrreducible(RC);
for i in [1..#comps] do
    comp := comps[i];
    dim := Dimension(comp);
    deg := Degree(comp);
    pts := #Points(comp);
    if dim eq 1 and IsIrreducible(comp) then
        g := Genus(Curve(comp));
        print "COMP", i, dim, deg, g, pts;
    else
        print "COMP", i, dim, deg, -1, pts;
    end if;
end for;
