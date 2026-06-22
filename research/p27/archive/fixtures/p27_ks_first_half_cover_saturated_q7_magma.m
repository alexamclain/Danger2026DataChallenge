// P27 K/S first-half cover, saturated q7 smoke.
//
// The raw eta=+1 first-half scheme has dimension 2 because clearing
// denominators leaves projection artifacts.  This fixture saturates by the
// known bad denominator product before attempting curve/component extraction.

SetColumns(0);
q := 7;
F := GF(q);
A5<X,W,T,R,B> := AffineSpace(F,5);
P := CoordinateRing(A5);

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

I := ideal<P | eq_E, eq_T, eq_compact, eq_first_half>;
bad := X*(X - 1)*(X + 1)*(T - 2*X^2);
Isat := Saturation(I, bad);
S := Scheme(A5, Basis(Isat));
print "SAT_SCHEME_OK", Dimension(S), #Basis(Isat), #Points(S);

try
    Csat := Curve(S);
    print "SAT_CURVE_OK", Genus(Csat), #Points(Csat);
catch e
    print "SAT_CURVE_ERROR";
    print e`Object;
end try;

try
    RA := ReducedSubscheme(S);
    acomps := IrreducibleComponents(RA);
    print "SAT_AFFINE_COMPONENTS", #acomps, IsReduced(RA), IsIrreducible(RA);
    for i in [1..#acomps] do
        comp := acomps[i];
        dim := Dimension(comp);
        if dim eq 1 and IsIrreducible(comp) then
            print "SAT_AFF_COMP", i, dim, -1, Genus(Curve(comp)), #Points(comp);
        else
            print "SAT_AFF_COMP", i, dim, -1, -1, #Points(comp);
        end if;
    end for;
catch e
    print "SAT_AFFINE_COMPONENTS_ERROR";
    print e`Object;
end try;

try
    PC := ProjectiveClosure(S);
    RC := ReducedSubscheme(PC);
    comps := IrreducibleComponents(RC);
    print "SAT_PROJECTIVE_COMPONENTS", #comps, IsReduced(RC), IsIrreducible(RC);
    for i in [1..#comps] do
        comp := comps[i];
        dim := Dimension(comp);
        deg := Degree(comp);
        if dim eq 1 and IsIrreducible(comp) then
            print "SAT_COMP", i, dim, deg, Genus(Curve(comp)), #Points(comp);
        else
            print "SAT_COMP", i, dim, deg, -1, #Points(comp);
        end if;
    end for;
catch e
    print "SAT_PROJECTIVE_ERROR";
    print e`Object;
end try;

print "RESULT p27_ks_first_half_cover_saturated_q7 done";
