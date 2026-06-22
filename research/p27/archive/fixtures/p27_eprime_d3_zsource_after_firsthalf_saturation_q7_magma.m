// P27 E-prime d3 z-source after first-half saturation, q7 smoke.
//
// Instead of saturating the full d3 z-source ideal at once, this stages the
// computation:
//   1. saturate the E' first-half pullback, which is known to succeed;
//   2. add the reverse-source z equation to that cleaned ideal;
//   3. ask for the resulting dimension/genus.

SetColumns(0);
q := 7;
F := GF(q);
A7<U,V,X,T,R,B,z> := AffineSpace(F, 7);
P := CoordinateRing(A7);

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
H_num := z^4*A_den + A_num*z^2 + A_den;
eq_reverse_z := 4*z^2*H_num*(U_num_scaled + B*U_den*D)
    - 2*U_den*D*A_den*(z^4 - 1)^2;

I0 := ideal<P | eq_Ep, eq_X, eq_T, eq_compact, eq_first_half>;
bad0 := X*(X - 1)*(X + 1)*D*(T - 2*X^2);
Iclean := Saturation(I0, bad0);
S0 := Scheme(A7, Basis(Iclean));
print "AFTER_FIRSTHALF_SAT", Dimension(S0), #Basis(Iclean), #Points(S0);

J := ideal<P | Basis(Iclean) cat [eq_reverse_z]>;
S := Scheme(A7, Basis(J));
print "D3_Z_AFTER_FIRSTHALF_SCHEME", Dimension(S), #Basis(J), #Points(S);

try
    C := Curve(S);
    print "D3_Z_AFTER_FIRSTHALF_CURVE", Genus(C), #Points(C);
catch e
    print "D3_Z_AFTER_FIRSTHALF_CURVE_ERROR";
    print e`Object;
end try;

try
    Jz := Saturation(J, z);
    Sz := Scheme(A7, Basis(Jz));
    print "D3_Z_AFTER_FIRSTHALF_ZSAT_SCHEME", Dimension(Sz), #Basis(Jz), #Points(Sz);
    try
        Cz := Curve(Sz);
        print "D3_Z_AFTER_FIRSTHALF_ZSAT_CURVE", Genus(Cz), #Points(Cz);
    catch e
        print "D3_Z_AFTER_FIRSTHALF_ZSAT_CURVE_ERROR";
        print e`Object;
    end try;
catch e
    print "D3_Z_AFTER_FIRSTHALF_ZSAT_ERROR";
    print e`Object;
end try;

print "RESULT p27_eprime_d3_zsource_after_firsthalf_saturation_q7 done";
