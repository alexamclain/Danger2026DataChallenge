// P27 B-line d3 cover q7 Magma smoke.
//
// Purpose:
//   Build the saturated B-line legal d2 cover and then add the reverse-source
//   d3 all-plus equations.  This is a small-field tractability smoke for the
//   actual Kummer/divisor extraction target over P1_B.
//
// Expected useful output:
//   BLEGAL_* lines for the legal source over Bline.
//   BD3_* lines for the d3 all-plus cover over Bline.

SetColumns(0);
q := 7;
F := GF(q);

procedure PrintSchemeStats(label, S)
    print label cat "_SCHEME", Dimension(S), #Basis(Ideal(S)), #Points(S);
    try
        C := Curve(S);
        print label cat "_CURVE", Genus(C), #Points(C);
    catch e
        print label cat "_CURVE_ERROR";
        print e`Object;
    end try;

    try
        R := ReducedSubscheme(S);
        comps := IrreducibleComponents(R);
        print label cat "_AFFINE_COMPONENTS", #comps, IsReduced(R), IsIrreducible(R);
        for i in [1..#comps] do
            comp := comps[i];
            dim := Dimension(comp);
            if dim eq 1 and IsIrreducible(comp) then
                print label cat "_AFF_COMP", i, dim, -1, Genus(Curve(comp)), #Points(comp);
            else
                print label cat "_AFF_COMP", i, dim, -1, -1, #Points(comp);
            end if;
        end for;
    catch e
        print label cat "_AFFINE_COMPONENTS_ERROR";
        print e`Object;
    end try;

    try
        PC := ProjectiveClosure(S);
        R := ReducedSubscheme(PC);
        comps := IrreducibleComponents(R);
        print label cat "_PROJECTIVE_COMPONENTS", #comps, IsReduced(R), IsIrreducible(R);
        for i in [1..#comps] do
            comp := comps[i];
            dim := Dimension(comp);
            deg := Degree(comp);
            if dim eq 1 and IsIrreducible(comp) then
                print label cat "_PROJ_COMP", i, dim, deg, Genus(Curve(comp)), #Points(comp);
            else
                print label cat "_PROJ_COMP", i, dim, deg, -1, #Points(comp);
            end if;
        end for;
    catch e
        print label cat "_PROJECTIVE_ERROR";
        print e`Object;
    end try;
end procedure;

// Legal d2 source over Bline, eta=+1 branch.
A6<X,W,T,R,beta,Bline> := AffineSpace(F,6);
P6 := CoordinateRing(A6);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
X6 := X5*X;
eta := F!1;

T2 := X*(X2 + 1)*(X2 + 2*X - 1);
mt := 2*W*X2 + 2*W*X + X4 + 2*X3 - 2*X - 1;
m0 := W*X5 + 3*W*X4 + 2*W*X3 + 2*W*X2 + W*X - W
    + 2*X6 + 4*X5 + 4*X3 - 2*X2;
criterion_num := W*(X2 + 1)*(m0 + mt*T);

U_core := eta*4*T*W*X
    + T*X3 + T*X2 - T*X - T
    + 2*X5 + 2*X4 - 2*X3 - 2*X2;
U_num := 2*U_core;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;

eq_E := W^2 - (X^3 - X);
eq_T := T^2 - T2;
eq_compact := X*R^2 - criterion_num;
eq_Bline := Bline*(X^2 - 1)^2 - 8*X^2;
eq_first_half := beta^2*U_den^2 - (U_num^2 - 4*U_den^2);

Ilegal := ideal<P6 | eq_E, eq_T, eq_compact, eq_Bline, eq_first_half>;
bad6 := X*(X - 1)*(X + 1)*(T - 2*X^2)*(X^2 + 1);
IlegalSat := Saturation(Ilegal, bad6);
Slegal := Scheme(A6, Basis(IlegalSat));
PrintSchemeStats("BLEGAL", Slegal);

// d3 all-plus cover: add reverse_x and reverse_Y.
A8<X8,W8,T8,R8,beta8,z,Y,Bline8> := AffineSpace(F,8);
P8 := CoordinateRing(A8);

X2 := X8^2;
X3 := X2*X8;
X4 := X2^2;
X5 := X4*X8;
X6 := X5*X8;
X8p := X4^2;

A_den := (X8 - 1)^4*(X8 + 1)^4;
A_num := -2*(X8p - 4*X6 - 26*X4 - 4*X2 + 1);

T2 := X8*(X2 + 1)*(X2 + 2*X8 - 1);
mt := 2*W8*X2 + 2*W8*X8 + X4 + 2*X3 - 2*X8 - 1;
m0 := W8*X5 + 3*W8*X4 + 2*W8*X3 + 2*W8*X2 + W8*X8 - W8
    + 2*X6 + 4*X5 + 4*X3 - 2*X2;
criterion_num := W8*(X2 + 1)*(m0 + mt*T8);

U_core := eta*4*T8*W8*X8
    + T8*X3 + T8*X2 - T8*X8 - T8
    + 2*X5 + 2*X4 - 2*X3 - 2*X2;
U_num := 2*U_core;
U_den := (T8 - 2*X2)*(X8 - 1)*(X8 + 1)^2;
H_num := z^4*A_den + A_num*z^2 + A_den;

eq_E := W8^2 - (X8^3 - X8);
eq_T := T8^2 - T2;
eq_compact := X8*R8^2 - criterion_num;
eq_Bline := Bline8*(X8^2 - 1)^2 - 8*X8^2;
eq_first_half := beta8^2*U_den^2 - (U_num^2 - 4*U_den^2);
eq_reverse_x := 4*z^2*H_num*(U_num + beta8*U_den)
    - 2*U_den*A_den*(z^4 - 1)^2;
eq_reverse_Y := Y^2*A_den - H_num;

Id3 := ideal<P8 | eq_E, eq_T, eq_compact, eq_Bline, eq_first_half,
    eq_reverse_x, eq_reverse_Y>;
bad8 := X8*(X8 - 1)*(X8 + 1)*(T8 - 2*X8^2)*(X8^2 + 1)*U_den*A_den;
Id3Sat := Saturation(Id3, bad8);
Sd3 := Scheme(A8, Basis(Id3Sat));
PrintSchemeStats("BD3", Sd3);

print "RESULT p27_b_line_d3_cover_q7 done";
