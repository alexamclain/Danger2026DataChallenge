// P27 E-prime first-half pullback, saturated q7 smoke.
//
// This is the next staged CAS packet after the E' descent result.  It rewrites
// the eta=+1 first-half layer in E' coordinates:
//
//   E' : V^2 = U^3 + 4U
//   U = X - 1/X
//   W = V*X^2/(X^2 + 1)
//
// and saturates the known denominator divisors before asking for curve/genus.

SetColumns(0);
q := 7;
F := GF(q);
A6<U,V,X,T,R,B> := AffineSpace(F, 6);
P := CoordinateRing(A6);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
D := X2 + 1;
Wnum := V*X2;

T2 := X*(X2 + 1)*(X2 + 2*X - 1);
eq_Ep := V^2 - (U^3 + 4*U);
eq_X := X^2 - U*X - 1;
eq_T := T^2 - T2;

mt_num := (X + 1)*(2*Wnum*X + D*(X3 + X2 - X - 1));
m0_poly := (X2 + 2*X - 1)*(Wnum*(X + 1) + 2*X2*D);

// Original compactD equation:
//   X*R^2 = W*(X^2+1)*(m0 + mt*T)
// with W = Wnum/D and mt = mt_num/D.
eq_compact := D*X*R^2 - Wnum*(D*m0_poly + mt_num*T);

U_core_num := 4*T*Wnum*X
    + D*(T*X3 + T*X2 - T*X - T
        + 2*X5 + 2*X4 - 2*X3 - 2*X2);
U_num_scaled := 2*U_core_num;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;

// D^2 times the first-half equation.
eq_first_half := B^2*U_den^2*D^2 - U_num_scaled^2 + 4*U_den^2*D^2;

I := ideal<P | eq_Ep, eq_X, eq_T, eq_compact, eq_first_half>;
bad := X*(X - 1)*(X + 1)*D*(T - 2*X^2);
Isat := Saturation(I, bad);
S := Scheme(A6, Basis(Isat));
print "EPRIME_PULLBACK_SAT_SCHEME", Dimension(S), #Basis(Isat), #Points(S);

try
    C := Curve(S);
    print "EPRIME_PULLBACK_SAT_CURVE", Genus(C), #Points(C);
catch e
    print "EPRIME_PULLBACK_SAT_CURVE_ERROR";
    print e`Object;
end try;

// Component decomposition exceeds the online calculator time limit.  The
// staged checkpoint is the saturated dimension/genus above.
print "RESULT p27_eprime_first_half_pullback_saturated_q7 done";
