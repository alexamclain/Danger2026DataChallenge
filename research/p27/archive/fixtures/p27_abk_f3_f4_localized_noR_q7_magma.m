// P27 A/B/K staged f3/f4 no-R localized q7 Magma fixture.
//
// This is the executable first chart for the symbolic Kummer CAS brief.
// It starts from the reduced B-line first transition, localizes denominator
// factors with inverse variables, imposes the f3-plus layer H^2=U+2, then
// attaches the generic f4/f3 transition F_A(U,V)=0 and gamma^2=V+2.
//
// compactD_R is intentionally omitted in this first chart.  Existing layer
// counts and small function-field checks show compactD_R is twinned with the
// beta/d_next layer after reduced_U, so the no-R base should be normalized
// before adding compactD_R back.

SetColumns(0);
q := 7;
F := GF(q);
A15<X,iX,iXm,iXp,iTm,iX2p,iU,W,T,beta,Bline,Unext,H,V,gamma> := AffineSpace(F,15);
P := CoordinateRing(A15);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
X6 := X5*X;
X8 := X4^2;
eta := F!1;

A_den := (X - 1)^4*(X + 1)^4;
A_num := -2*(X8 - 4*X6 - 26*X4 - 4*X2 + 1);
Aexpr := Bline^2 - 2;

T2 := X*(X2 + 1)*(X2 + 2*X - 1);
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
eq_Bline := Bline*(X^2 - 1)^2 - 8*X^2;
eq_first_half := beta^2*U_den^2 - (U_num^2 - 4*U_den^2);
eq_reduced_Unext := A_den*(Unext*U_den - x5_num)^2
    - (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2);
eq_H := H^2 - (Unext + 2);
eq_Fnext := (V^2 - 4)^2
    - 4*Unext*(V^2 - 4)*(V + Aexpr)
    + 16*(V + Aexpr)^2;
eq_gamma := gamma^2 - (V + 2);

J := ideal<P | eq_iX, eq_iXm, eq_iXp, eq_iTm, eq_iX2p, eq_iU,
    eq_E, eq_T, eq_Bline, eq_first_half, eq_reduced_Unext,
    eq_H, eq_Fnext, eq_gamma>;
S := Scheme(A15, Basis(J));

print "ABK_F3_F4_NOR_LOCALIZED_START", q, Dimension(S), #Basis(J);

try
    print "ABK_F3_F4_NOR_LOCALIZED_DEGREE", Degree(S);
catch e
    print "ABK_F3_F4_NOR_LOCALIZED_DEGREE_ERROR";
end try;

try
    C := Curve(S);
    print "ABK_F3_F4_NOR_LOCALIZED_CURVE", Genus(C), #Points(C);
catch e
    print "ABK_F3_F4_NOR_LOCALIZED_CURVE_ERROR";
end try;

print "RESULT p27_abk_f3_f4_localized_noR_q7 done";
