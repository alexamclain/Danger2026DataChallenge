// P27 B-line reduced_Unext cover q7 staging without compactD_R.
//
// The full reduced cover with compactD_R exceeds the online Magma memory
// limit during saturation.  This fixture removes only the R^2 compactD layer
// and keeps the E, T, Bline, beta, and reduced_Unext equations.
//
// If this saturates, the offline attack order should be:
//   1. normalize this noR base curve over P1_Bline,
//   2. add compactD_R as a quadratic cover,
//   3. attach x6^2 - Unext*x6 + 1 and gamma^2 = Unext + 2.

SetColumns(0);
q := 7;
F := GF(q);
A6<X,W,T,beta,Bline,Unext> := AffineSpace(F,6);
P := CoordinateRing(A6);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
X6 := X5*X;
X8 := X4^2;
eta := F!1;

A_den := (X - 1)^4*(X + 1)^4;
A_num := -2*(X8 - 4*X6 - 26*X4 - 4*X2 + 1);

T2 := X*(X2 + 1)*(X2 + 2*X - 1);
U_core := eta*4*T*W*X
    + T*X3 + T*X2 - T*X - T
    + 2*X5 + 2*X4 - 2*X3 - 2*X2;
U_num := 2*U_core;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;
x5_num := U_num + beta*U_den;

eq_E := W^2 - (X^3 - X);
eq_T := T^2 - T2;
eq_Bline := Bline*(X^2 - 1)^2 - 8*X^2;
eq_first_half := beta^2*U_den^2 - (U_num^2 - 4*U_den^2);
eq_reduced_Unext := A_den*(Unext*U_den - x5_num)^2
    - (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2);

I := ideal<P | eq_E, eq_T, eq_Bline, eq_first_half, eq_reduced_Unext>;
bad := X*(X - 1)*(X + 1)*(T - 2*X^2)*(X^2 + 1)*U_den*A_den;

print "BREDUCED_NOR_START", q;
Isat := Saturation(I, bad);
S := Scheme(A6, Basis(Isat));
print "BREDUCED_NOR_SATURATION", Dimension(S), #Basis(Isat);

try
    C := Curve(S);
    print "BREDUCED_NOR_CURVE", Genus(C), #Points(C);
catch e
    print "BREDUCED_NOR_CURVE_ERROR";
end try;

print "RESULT p27_b_line_reduced_cover_noR_q7 done";
