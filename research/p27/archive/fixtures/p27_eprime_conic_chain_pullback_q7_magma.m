// P27 E-prime legal pullback to one conic-chain step, q7 smoke.
//
// This adds the new conic-chain coordinates to the already staged E-prime
// first-half / compactD source:
//   A = 2 - c^2
//   x5 = r0^2
//   h^2 = r0^2 + c*r0 + 1
//   g^2 = r0^2 - c*r0 + 1
//   r1^2 - (h+g)*r1 + 1 = 0

SetColumns(0);
q := 7;
F := GF(q);
A11<U,V,X,T,R,B,c,r0,h,g,r1> := AffineSpace(F, 11);
P := CoordinateRing(A11);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
X6 := X5*X;
X8 := X4^2;
D := X2 + 1;
Wnum := V*X2;

T2 := X*(X2 + 1)*(X2 + 2*X - 1);
eq_Ep := V^2 - (U^3 + 4*U);
eq_X := X^2 - U*X - 1;
eq_T := T^2 - T2;

mt_num := (X + 1)*(2*Wnum*X + D*(X3 + X2 - X - 1));
m0_poly := (X2 + 2*X - 1)*(Wnum*(X + 1) + 2*X2*D);
eq_compact := D*X*R^2 - Wnum*(D*m0_poly + mt_num*T);

U_core_num := 4*T*Wnum*X
    + D*(T*X3 + T*X2 - T*X - T
        + 2*X5 + 2*X4 - 2*X3 - 2*X2);
U_num_scaled := 2*U_core_num;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;
eq_first_half := B^2*U_den^2*D^2 - U_num_scaled^2 + 4*U_den^2*D^2;

A_den := (X - 1)^4*(X + 1)^4;
A_num := -2*(X8 - 4*X6 - 26*X4 - 4*X2 + 1);
Cterm := U_num_scaled + B*U_den*D;

eq_A_conic := A_num - (2 - c^2)*A_den;
eq_x5_square := Cterm - 2*U_den*D*r0^2;
eq_h := h^2 - (r0^2 + c*r0 + 1);
eq_g := g^2 - (r0^2 - c*r0 + 1);
eq_r1 := r1^2 - (h + g)*r1 + 1;

I0 := ideal<P | eq_Ep, eq_X, eq_T, eq_compact, eq_first_half>;
bad0 := X*(X - 1)*(X + 1)*D*(T - 2*X^2)*A_den*U_den;
Iclean := Saturation(I0, bad0);
S0 := Scheme(A11, Basis(Iclean));
print "AFTER_FIRSTHALF_SAT_FREE_CHAIN", Dimension(S0), #Basis(Iclean), #Points(S0);

J := ideal<P | Basis(Iclean) cat [eq_A_conic, eq_x5_square, eq_h, eq_g, eq_r1]>;
S := Scheme(A11, Basis(J));
print "EPRIME_CONIC_CHAIN_PULLBACK_SCHEME", Dimension(S), #Basis(J), #Points(S);

try
    Cc := Curve(S);
    print "EPRIME_CONIC_CHAIN_PULLBACK_CURVE", Genus(Cc), #Points(Cc);
catch e
    print "EPRIME_CONIC_CHAIN_PULLBACK_CURVE_ERROR";
    print e`Object;
end try;

print "RESULT p27_eprime_conic_chain_pullback_q7 done";
