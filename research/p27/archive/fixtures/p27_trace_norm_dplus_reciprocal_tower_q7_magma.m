// P27 Dplus reciprocal-coordinate tower q7 Magma fixture.
//
// This is the CAS object isolated after the Dplus A-coordinate bridge and
// x6/U-class probes:
//
//   t = y - 1
//   A = (t - 1/t)^4/4 - 2
//   X = t^3 + 2*t^2 - 1/t
//   F_A(X,U5) = 0
//   F_A(U5,U6) = 0
//   x6^2 - U6*x6 + 1 = 0
//
// with side square variables for U5^2-4, U5+A, U6^2-4, and U6+A.
// The next selected class after Dplus is the squareclass of x6.

SetColumns(0);
q := 7;
F := GF(q);
A11<t,it,A,X,U5,U6,R5,H5,R6,H6,x6> := AffineSpace(F,11);
P := CoordinateRing(A11);

t2 := t^2;
t3 := t2*t;
t4 := t2^2;
t6 := t4*t2;
t8 := t4^2;

eq_it := t*it - 1;
eq_A := 4*A*t4 - (t8 - 4*t6 - 2*t4 - 4*t2 + 1);
eq_X := X*t - (t4 + 2*t3 - 1);

FA_X_U5 := (U5^2 - 4)^2
    - 4*X*(U5^2 - 4)*(U5 + A)
    + 16*(U5 + A)^2;

FA_U5_U6 := (U6^2 - 4)^2
    - 4*U5*(U6^2 - 4)*(U6 + A)
    + 16*(U6 + A)^2;

eq_R5 := R5^2 - (U5^2 - 4);
eq_H5 := H5^2 - (U5 + A);
eq_R6 := R6^2 - (U6^2 - 4);
eq_H6 := H6^2 - (U6 + A);
eq_x6 := x6^2 - U6*x6 + 1;

J := ideal<P | eq_it, eq_A, eq_X, FA_X_U5, FA_U5_U6,
    eq_R5, eq_H5, eq_R6, eq_H6, eq_x6>;
S := Scheme(A11, Basis(J));

print "DPLUS_RECIPROCAL_TOWER_Q7_START", q, Dimension(S), #Basis(J);

try
    print "DPLUS_RECIPROCAL_TOWER_Q7_DEGREE", Degree(S);
catch e
    print "DPLUS_RECIPROCAL_TOWER_Q7_DEGREE_ERROR";
end try;

try
    C := Curve(S);
    print "DPLUS_RECIPROCAL_TOWER_Q7_CURVE", Genus(C), #Points(C);
catch e
    print "DPLUS_RECIPROCAL_TOWER_Q7_CURVE_ERROR";
end try;

print "RESULT p27_trace_norm_dplus_reciprocal_tower_q7 done";
