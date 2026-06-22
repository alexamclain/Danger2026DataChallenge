// P27 K/S first-half cover smoke.
//
// This is a staged version of the reverse-source extraction.  It fixes
// eta=+1 and stops after adjoining B^2 = U^2 - 4 on top of the label-2
// compactD/alpha cover.  If this intermediate cover is already high genus,
// the full reverse-square source cannot be a cheap low-genus sampler without
// an additional quotient.

SetColumns(0);
q := 7;
F := GF(q);
A5<X,W,T,R,B> := AffineSpace(F,5);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
eta := F!1;

T2 := X*(X2 + 1)*(X2 + 2*X - 1);
mt := (X + 1)*(2*W*X + X3 + X2 - X - 1);
m0 := (X2 + 1)*(X2 + 2*X - 1)*(W*X + W + 2*X2);
criterion_num := W*(X2 + 1)*(m0 + mt*T);

U_core := eta*4*T*W*X
    + T*X3 + T*X2 - T*X - T
    + 2*X5 + 2*X4 - 2*X3 - 2*X2;
U_num := 2*U_core;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;

eq_E := W^2 - (X^3 - X);
eq_T := T^2 - T2;
eq_compact := X*R^2 - criterion_num;
eq_first_half := B^2*U_den^2 - (U_num^2 - 4*U_den^2);

S := Scheme(A5, [eq_E, eq_T, eq_compact, eq_first_half]);
print "SCHEME_OK", Dimension(S), #DefiningEquations(S);

try
    print "AFFINE_POINTS", #Points(S);
catch e
    print "AFFINE_POINTS_ERROR";
    print e`Object;
end try;

try
    RA := ReducedSubscheme(S);
    acomps := IrreducibleComponents(RA);
    print "AFFINE_COMPONENTS", #acomps, IsReduced(RA), IsIrreducible(RA);
    for i in [1..#acomps] do
        comp := acomps[i];
        dim := Dimension(comp);
        if dim eq 1 and IsIrreducible(comp) then
            print "AFF_COMP", i, dim, -1, Genus(Curve(comp));
        else
            print "AFF_COMP", i, dim, -1, -1;
        end if;
    end for;
catch e
    print "AFFINE_COMPONENTS_ERROR";
    print e`Object;
end try;

try
    PC := ProjectiveClosure(S);
    RC := ReducedSubscheme(PC);
    comps := IrreducibleComponents(RC);
    print "PROJECTIVE_COMPONENTS", #comps, IsReduced(RC), IsIrreducible(RC);
    for i in [1..#comps] do
        comp := comps[i];
        dim := Dimension(comp);
        deg := Degree(comp);
        pts := #Points(comp);
        if dim eq 1 and IsIrreducible(comp) then
            print "COMP", i, dim, deg, Genus(Curve(comp)), pts;
        else
            print "COMP", i, dim, deg, -1, pts;
        end if;
    end for;
catch e
    print "PROJECTIVE_ERROR";
    print e`Object;
end try;

print "RESULT p27_ks_first_half_cover_q7 done";
