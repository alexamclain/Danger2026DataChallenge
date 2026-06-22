// P27 Dplus U6 row-bit factorization over the H90 elliptic base.
//
// The Q(t)-screen shows that the Kummer lift
//
//   R(t,S) = Res_U5(F_A(X(t),U5), F_A(U5,S^2-2))
//
// does not factor over Q(t).  This fixture asks the next structural question:
// does the row-bit cover factor after adjoining the H90 quotient coordinate
//
//   E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1)?
//
// A split over E_h90 would be a serious bridge between the Dplus/H90 lane and
// the post-Dplus d3 row bit.  Irreducibility over E_h90 is a sharp obstruction
// to the nearest quotient explanation.

SetColumns(0);
q := 607;
Fq := GF(q);

K<t> := FunctionField(Fq);

function FA(A, U, V)
    return (V^2 - 4)^2
        - 4*U*(V^2 - 4)*(V + A)
        + 16*(V + A)^2;
end function;

function LiftPolynomial(Base)
    P2<U,Z> := PolynomialRing(Base, 2);
    tt := Base!t;
    A := (tt^8 - 4*tt^6 - 2*tt^4 - 4*tt^2 + 1)/(4*tt^4);
    X := (tt^4 + 2*tt^3 - 1)/tt;
    R := Resultant(FA(A, X, U), FA(A, U, Z), U);
    P1<S> := PolynomialRing(Base);
    return P1!Evaluate(R, [ 0, S^2 - 2 ]);
end function;

PK<S> := PolynomialRing(K);
LiftK := LiftPolynomial(K);
FacK := Factorization(LiftK);
print "RESULT u6_rowbit_factor_base", q, Degree(LiftK), #FacK;
for item in FacK do
    print "RESULT u6_rowbit_factor_K", Degree(item[1]), item[2];
end for;

PW<W> := PolynomialRing(K);
C := t^2 + 2*t - 1;
Rbranch := t^2 - 2*t - 1;
Ktrace := -C*Rbranch;
E<w> := ext<K | W^2 - Ktrace>;

PE<S2> := PolynomialRing(E);
LiftE := LiftPolynomial(E);
FacE := Factorization(LiftE);
print "RESULT u6_rowbit_factor_h90", q, Genus(E), Degree(E,K), Degree(LiftE), #FacE;
for item in FacE do
    print "RESULT u6_rowbit_factor_E", Degree(item[1]), item[2];
end for;

print "RESULT p27_trace_norm_dplus_u6_rowbit_h90_factor_q607 done";
