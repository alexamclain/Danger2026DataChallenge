// P27 E-prime d3 reverse-source reciprocal quotient, q7 smoke.
//
// The staged z-source equation is reciprocal in s=z^2.  Dividing by z^4 and
// setting r=s+1/s gives a lower-degree quotient equation:
//
//   2*C*(A_den*r + A_num) - U_den*D*A_den*(r^2 - 4) = 0
//
// where C = U_num_scaled + B*U_den*D.  This tests whether the actual d3 source
// has a low-genus quotient before normalizing the full z-cover.

SetColumns(0);
q := 7;
F := GF(q);
A7<U,V,X,T,R,B,r> := AffineSpace(F, 7);
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
Cterm := U_num_scaled + B*U_den*D;
eq_reverse_r := 2*Cterm*(A_den*r + A_num) - U_den*D*A_den*(r^2 - 4);

I0 := ideal<P | eq_Ep, eq_X, eq_T, eq_compact, eq_first_half>;
bad0 := X*(X - 1)*(X + 1)*D*(T - 2*X^2);
Iclean := Saturation(I0, bad0);
S0 := Scheme(A7, Basis(Iclean));
print "AFTER_FIRSTHALF_SAT", Dimension(S0), #Basis(Iclean), #Points(S0);

Jr := ideal<P | Basis(Iclean) cat [eq_reverse_r]>;
Sr := Scheme(A7, Basis(Jr));
print "D3_RQUOT_AFTER_FIRSTHALF_SCHEME", Dimension(Sr), #Basis(Jr), #Points(Sr);

try
    Cr := Curve(Sr);
    print "D3_RQUOT_AFTER_FIRSTHALF_CURVE", Genus(Cr), #Points(Cr);
catch e
    print "D3_RQUOT_AFTER_FIRSTHALF_CURVE_ERROR";
    print e`Object;
end try;

try
    Jr_sat := Saturation(Jr, bad0);
    Sr_sat := Scheme(A7, Basis(Jr_sat));
    print "D3_RQUOT_AFTER_FIRSTHALF_RESAT_SCHEME", Dimension(Sr_sat), #Basis(Jr_sat), #Points(Sr_sat);
    try
        Cr_sat := Curve(Sr_sat);
        print "D3_RQUOT_AFTER_FIRSTHALF_RESAT_CURVE", Genus(Cr_sat), #Points(Cr_sat);
    catch e
        print "D3_RQUOT_AFTER_FIRSTHALF_RESAT_CURVE_ERROR";
        print e`Object;
    end try;
catch e
    print "D3_RQUOT_AFTER_FIRSTHALF_RESAT_ERROR";
    print e`Object;
end try;

print "RESULT p27_eprime_d3_rquotient_after_firsthalf_saturation_q7 done";
