// P27 A/B/K staged gamma4/gamma5 no-R localized q7 Magma fixture.
//
// This extends p27_abk_f3_f4_localized_noR_q7_magma.m by adding the next
// generic transition and both Kummer selector layers:
//
//   gamma4^2 = V + 2 on F_A(Unext,V)=0
//   gamma5^2 = Wnext + 2 on F_A(V,Wnext)=0
//
// The purpose is not point counting.  It is an offline CAS normalization and
// class-comparison fixture: decide whether gamma4 and gamma5 are pullbacks,
// translates, coboundaries, live on one quotient/Prym factor, or are fresh
// unrelated half-covers.

SetColumns(0);
q := 7;
F := GF(q);
A18<X,iX,iXm,iXp,iTm,iX2p,iU,W,T,beta,Bline,Unext,H,V,gamma4,Wnext,gamma5> := AffineSpace(F,18);
P := CoordinateRing(A18);

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

FAuv := (V^2 - 4)^2
    - 4*Unext*(V^2 - 4)*(V + Aexpr)
    + 16*(V + Aexpr)^2;
FAvw := (Wnext^2 - 4)^2
    - 4*V*(Wnext^2 - 4)*(Wnext + Aexpr)
    + 16*(Wnext + Aexpr)^2;

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
eq_gamma4 := gamma4^2 - (V + 2);
eq_gamma5 := gamma5^2 - (Wnext + 2);

J := ideal<P | eq_iX, eq_iXm, eq_iXp, eq_iTm, eq_iX2p, eq_iU,
    eq_E, eq_T, eq_Bline, eq_first_half, eq_reduced_Unext,
    eq_H, FAuv, eq_gamma4, FAvw, eq_gamma5>;
S := Scheme(A18, Basis(J));

print "ABK_GAMMA45_NOR_LOCALIZED_START", q, Dimension(S), #Basis(J);

try
    print "ABK_GAMMA45_NOR_LOCALIZED_DEGREE", Degree(S);
catch e
    print "ABK_GAMMA45_NOR_LOCALIZED_DEGREE_ERROR";
end try;

try
    C := Curve(S);
    print "ABK_GAMMA45_NOR_LOCALIZED_CURVE", Genus(C), #Points(C);
catch e
    print "ABK_GAMMA45_NOR_LOCALIZED_CURVE_ERROR";
end try;

print "RESULT p27_abk_gamma4_gamma5_localized_noR_q7 done";
