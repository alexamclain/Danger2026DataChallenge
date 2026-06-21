// P27 E-prime d3 z-source, sequential saturation q7 diagnostic.
//
// The all-at-once saturation of the z-source hits the online Magma memory
// limit.  This fixture saturates one denominator/artifact factor at a time and
// prints the dimension after each step, to identify whether the d3 cover can be
// staged below the memory limit.

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

J := ideal<P | eq_Ep, eq_X, eq_T, eq_compact, eq_first_half, eq_reverse_z>;
S := Scheme(A7, Basis(J));
print "SEQ_STEP raw", Dimension(S), #Basis(J), #Points(S);

try
    J := Saturation(J, X);
    S := Scheme(A7, Basis(J));
    print "SEQ_STEP X", Dimension(S), #Basis(J), #Points(S);
catch e
    print "SEQ_ERROR X";
    print e`Object;
end try;

try
    J := Saturation(J, X - 1);
    S := Scheme(A7, Basis(J));
    print "SEQ_STEP Xm1", Dimension(S), #Basis(J), #Points(S);
catch e
    print "SEQ_ERROR Xm1";
    print e`Object;
end try;

try
    J := Saturation(J, X + 1);
    S := Scheme(A7, Basis(J));
    print "SEQ_STEP Xp1", Dimension(S), #Basis(J), #Points(S);
catch e
    print "SEQ_ERROR Xp1";
    print e`Object;
end try;

try
    J := Saturation(J, D);
    S := Scheme(A7, Basis(J));
    print "SEQ_STEP D", Dimension(S), #Basis(J), #Points(S);
catch e
    print "SEQ_ERROR D";
    print e`Object;
end try;

try
    J := Saturation(J, T - 2*X^2);
    S := Scheme(A7, Basis(J));
    print "SEQ_STEP Tminus2X2", Dimension(S), #Basis(J), #Points(S);
catch e
    print "SEQ_ERROR Tminus2X2";
    print e`Object;
end try;

try
    J := Saturation(J, z);
    S := Scheme(A7, Basis(J));
    print "SEQ_STEP z", Dimension(S), #Basis(J), #Points(S);
catch e
    print "SEQ_ERROR z";
    print e`Object;
end try;

try
    C := Curve(S);
    print "SEQ_CURVE", Genus(C), #Points(C);
catch e
    print "SEQ_CURVE_ERROR";
    print e`Object;
end try;

print "RESULT p27_eprime_d3_zsource_sequential_saturation_q7 done";
