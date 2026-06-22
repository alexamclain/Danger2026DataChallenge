// P27 B-line reduced cover q7 localized invariant smoke.
//
// This avoids saturation entirely and asks only cheap scheme-level questions
// about the fully localized complete-intersection chart.

SetColumns(0);
q := 7;
F := GF(q);
A13<X,iX,iXm,iXp,iTm,iX2p,iU,W,T,R,beta,Bline,Unext> := AffineSpace(F,13);
P := CoordinateRing(A13);

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
mt := 2*W*X2 + 2*W*X + X4 + 2*X3 - 2*X - 1;
m0 := W*X5 + 3*W*X4 + 2*W*X3 + 2*W*X2 + W*X - W
    + 2*X6 + 4*X5 + 4*X3 - 2*X2;
criterion_num := W*(X2 + 1)*(m0 + mt*T);
U_core := eta*4*T*W*X
    + T*X3 + T*X2 - T*X - T
    + 2*X5 + 2*X4 - 2*X3 - 2*X2;
U_num := 2*U_core;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;
x5_num := U_num + beta*U_den;

eq_iX := X*iX - 1;
eq_iXm := (X - 1)*iXm - 1;
eq_iXp := (X + 1)*iXp - 1;
eq_iTm := (T - 2*X^2)*iTm - 1;
eq_iX2p := (X^2 + 1)*iX2p - 1;
eq_iU := U_den*iU - 1;
eq_E := W^2 - (X^3 - X);
eq_T := T^2 - T2;
eq_compact := X*R^2 - criterion_num;
eq_Bline := Bline*(X^2 - 1)^2 - 8*X^2;
eq_first_half := beta^2*U_den^2 - (U_num^2 - 4*U_den^2);
eq_reduced_Unext := A_den*(Unext*U_den - x5_num)^2
    - (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2);

J := ideal<P | eq_iX, eq_iXm, eq_iXp, eq_iTm, eq_iX2p, eq_iU, eq_E, eq_T, eq_compact, eq_Bline, eq_first_half, eq_reduced_Unext>;
S := Scheme(A13, Basis(J));
print "BREDUCED_LOCALIZED_INV_START", q, Dimension(S), #Basis(J);

try
    print "BREDUCED_LOCALIZED_INV_DEG", Degree(S);
catch e
    print "BREDUCED_LOCALIZED_INV_DEG_ERROR";
end try;

try
    print "BREDUCED_LOCALIZED_INV_REDUCED", IsReduced(S);
catch e
    print "BREDUCED_LOCALIZED_INV_REDUCED_ERROR";
end try;

try
    print "BREDUCED_LOCALIZED_INV_IRREDUCIBLE", IsIrreducible(S);
catch e
    print "BREDUCED_LOCALIZED_INV_IRREDUCIBLE_ERROR";
end try;

print "RESULT p27_b_line_reduced_cover_localized_invariants_q7 done";
