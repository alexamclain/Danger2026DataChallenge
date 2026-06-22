// P27 B-line reduced_Unext noR q7 X-inverted chart smoke.
//
// Stepwise saturation fails immediately on Saturation(J, X).  This fixture
// replaces that first saturation with an explicit chart variable iX satisfying
// X*iX = 1, then saturates only the remaining denominator factors.

SetColumns(0);
q := 7;
F := GF(q);
A7<X,iX,W,T,beta,Bline,Unext> := AffineSpace(F,7);
P := CoordinateRing(A7);

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

eq_chart := X*iX - 1;
eq_E := W^2 - (X^3 - X);
eq_T := T^2 - T2;
eq_Bline := Bline*(X^2 - 1)^2 - 8*X^2;
eq_first_half := beta^2*U_den^2 - (U_num^2 - 4*U_den^2);
eq_reduced_Unext := A_den*(Unext*U_den - x5_num)^2
    - (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2);

J := ideal<P | eq_chart, eq_E, eq_T, eq_Bline, eq_first_half, eq_reduced_Unext>;
S0 := Scheme(A7, Basis(J));
print "BREDUCED_NOR_INVX_START", q, Dimension(S0), #Basis(J);

bad := (X - 1)*(X + 1)*(T - 2*X^2)*(X^2 + 1)*U_den*A_den;
Isat := Saturation(J, bad);
S := Scheme(A7, Basis(Isat));
print "BREDUCED_NOR_INVX_SATURATION", Dimension(S), #Basis(Isat);

try
    C := Curve(S);
    print "BREDUCED_NOR_INVX_CURVE", Genus(C), #Points(C);
catch e
    print "BREDUCED_NOR_INVX_CURVE_ERROR";
end try;

print "RESULT p27_b_line_reduced_cover_noR_invX_q7 done";
