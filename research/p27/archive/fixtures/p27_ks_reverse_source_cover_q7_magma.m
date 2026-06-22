// P27 K/S reverse-source cover extraction smoke.
//
// This is the smallest durable Magma fixture for the actual d3 all-plus
// reverse-source cover over the K-line.  q=7 is a tiny p27-signature field
// (7 mod 16), so this is only a CAS-interface and geometry smoke.  Promotion
// still requires q=1607/1847/2087 or a symbolic branch-class extraction.

SetColumns(0);
q := 7;
F := GF(q);
A9<X,W,T,B,R,z,Y,eta,K> := AffineSpace(F,9);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
X6 := X5*X;
X8 := X4^2;

T2 := X*(X2 + 1)*(X2 + 2*X - 1);
mt := (X + 1)*(2*W*X + X3 + X2 - X - 1);
m0 := (X2 + 1)*(X2 + 2*X - 1)*(W*X + W + 2*X2);
criterion_num := W*(X2 + 1)*(m0 + mt*T);

A_den := (X - 1)^4*(X + 1)^4;
A_num := -2*(X8 - 4*X6 - 26*X4 - 4*X2 + 1);

U_core := eta*4*T*W*X
    + T*X3 + T*X2 - T*X - T
    + 2*X5 + 2*X4 - 2*X3 - 2*X2;
U_num := 2*U_core;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;
H_num := z^4*A_den + A_num*z^2 + A_den;

K_num := (X^4 - 6*X^2 + 1)^2;
K_den := 4*X*(X - 1)*(X + 1)*(X^2 + 1)^2;

eq_eta := eta^2 - 1;
eq_E := W^2 - (X^3 - X);
eq_T := T^2 - T2;
eq_compact := X*R^2 - criterion_num;
eq_first_half := B^2*U_den^2 - (U_num^2 - 4*U_den^2);
eq_reverse_x := 4*z^2*H_num*(U_num + B*U_den)
    - 2*U_den*A_den*(z^4 - 1)^2;
eq_reverse_Y := Y^2*A_den - H_num;
eq_K := K*K_den - K_num;

eqs := [
    eq_eta,
    eq_E,
    eq_T,
    eq_compact,
    eq_first_half,
    eq_reverse_x,
    eq_reverse_Y,
    eq_K
];

try
    C := Curve(A9, eqs);
    print "CURVE_OK", Dimension(C), #DefiningEquations(C);

    try
        print "AFFINE_POINTS", #Points(C);
    catch e
        print "AFFINE_POINTS_ERROR";
        print e`Object;
    end try;

    try
        PC := ProjectiveClosure(C);
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
catch e
    print "CURVE_ERROR";
    print e`Object;
end try;

print "RESULT p27_ks_reverse_source_cover_q7 done";
