// P27 E-prime d3 z-source pullback, saturated q7 smoke.
//
// This extends the E' first-half pullback by one actual d3-source variable:
// x6 = z^2, with the reverse-doubling equation xDBL_A(z^2)=x5.
//
// It deliberately does not adjoin Y^2=d3 yet.  On the nonsplit path the
// x-square criterion is the d-next criterion, so this is the cheapest staged
// cover for the d3 all-plus/source question.

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

// Scaled version of:
//   4*z^2*H_num*(U_num + B*U_den)
//     - 2*U_den*A_den*(z^4 - 1)^2 = 0
// with U_num = U_num_scaled / D.
eq_reverse_z := 4*z^2*H_num*(U_num_scaled + B*U_den*D)
    - 2*U_den*D*A_den*(z^4 - 1)^2;

I := ideal<P | eq_Ep, eq_X, eq_T, eq_compact, eq_first_half, eq_reverse_z>;
bad := X*(X - 1)*(X + 1)*D*(T - 2*X^2)*z;

try
    Sraw := Scheme(A7, Basis(I));
    print "EPRIME_D3_ZSOURCE_RAW_SCHEME", Dimension(Sraw), #Basis(I), #Points(Sraw);
catch e
    print "EPRIME_D3_ZSOURCE_RAW_ERROR";
    print e`Object;
end try;

try
    Isat := Saturation(I, bad);
    S := Scheme(A7, Basis(Isat));
    print "EPRIME_D3_ZSOURCE_SAT_SCHEME", Dimension(S), #Basis(Isat), #Points(S);

    try
        C := Curve(S);
        print "EPRIME_D3_ZSOURCE_SAT_CURVE", Genus(C), #Points(C);
    catch e
        print "EPRIME_D3_ZSOURCE_SAT_CURVE_ERROR";
        print e`Object;
    end try;
catch e
    print "EPRIME_D3_ZSOURCE_SATURATION_ERROR";
    print e`Object;
end try;

print "RESULT p27_eprime_d3_zsource_saturated_q7 done";
