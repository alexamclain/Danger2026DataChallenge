// P27 Dplus U6 row-bit factorization over the H90 A_eta cover, eta=+1.
//
// Previous tests show the row-bit Kummer lift
//
//   R(t,S) = Res_U5(F_A(X(t),U5), F_A(U5,S^2-2))
//
// is irreducible over F_607(t) and remains irreducible over
// E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1).
//
// This fixture asks the decisive next bridge question for eta=+1:
// does R(t,S) factor after adjoining the H90 domain-spin variable z and the
// second-layer payload rho^2 = A_eta = U_eta + z*W_eta?

SetColumns(0);
q := 607;
eta := 1;
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

function PrintFactorSummary(label, poly)
    Fac := Factorization(poly);
    print "RESULT", label, Degree(poly), #Fac;
    for item in Fac do
        print "RESULT", label cat "_factor", Degree(item[1]), item[2];
    end for;
end function;

PW<W> := PolynomialRing(K);
B := t^2 + 1;
C := t^2 + 2*t - 1;
Rbranch := t^2 - 2*t - 1;
Fspin := t*C*B;
Ktrace := -C*Rbranch;
E<w> := ext<K | W^2 - Ktrace>;

PE<Q> := PolynomialRing(E);
tE := E!t;
wE := E!w;
BE := tE^2 + 1;
CE := tE^2 + 2*tE - 1;
FspinE := tE*CE*BE;

L<z> := ext<E | Q^2 - FspinE>;
tL := L!t;
wL := L!w;
zL := L!z;
BL := tL^2 + 1;
CL := tL^2 + 2*tL - 1;
Ueta := 2*tL^2*(tL - 1)*BL^2*(eta*wL + CL);
Weta := (tL - 1)*BL*(4*tL^3 + eta*BL*wL);
Aeta := Ueta + zL*Weta;

PL<RHO> := PolynomialRing(L);
N<rho> := ext<L | RHO^2 - Aeta>;

print "RESULT u6_rowbit_aeta_setup", q, eta, Genus(E), Degree(E,K), Genus(L), Degree(L,E), Degree(N,L);

LiftL := LiftPolynomial(L);
PrintFactorSummary("u6_rowbit_factor_domainspin_eta1", LiftL);

LiftN := LiftPolynomial(N);
PrintFactorSummary("u6_rowbit_factor_Aeta_eta1", LiftN);

print "RESULT p27_trace_norm_dplus_u6_rowbit_aeta_factor_eta1_q607 done";
