// P27 B-line legal d2 cover q7 saturation-only Magma smoke.
//
// This isolates the bottleneck: if this times out, the saturation itself is too
// heavy for the online calculator.  If it returns, later Curve/Component calls
// are the bottleneck.

SetColumns(0);
q := 7;
F := GF(q);
A6<X,W,T,R,beta,Bline> := AffineSpace(F,6);
P := CoordinateRing(A6);

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

I := ideal<P | eq_E, eq_T, eq_compact, eq_Bline, eq_first_half>;
bad := X*(X - 1)*(X + 1)*(T - 2*X^2)*(X^2 + 1);
Isat := Saturation(I, bad);
S := Scheme(A6, Basis(Isat));

print "BLEGAL_SATURATION_ONLY", Dimension(S), #Basis(Isat);
print "RESULT p27_b_line_legal_saturation_q7 done";
