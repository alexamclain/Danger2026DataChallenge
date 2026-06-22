// P27 Dplus U6 row-bit factorization over the H90 A_eta covers, eta=+/-1.
//
// Local Magma version of the q607 second-layer row-bit split test.  The
// eta=+1 fixture was originally staged for online Magma and timed out.  This
// file checks both eta signs in one run.

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

procedure PrintFactorSummary(label, poly)
    Fac := Factorization(poly);
    print "RESULT", label, Degree(poly), #Fac;
    for item in Fac do
        print "RESULT", label cat "_factor", Degree(item[1]), item[2];
    end for;
end procedure;

PW<W> := PolynomialRing(K);
B := t^2 + 1;
C := t^2 + 2*t - 1;
Rbranch := t^2 - 2*t - 1;
Ktrace := -C*Rbranch;
E<w> := ext<K | W^2 - Ktrace>;

PE<Q> := PolynomialRing(E);
tE := E!t;
wE := E!w;
BE := tE^2 + 1;
CE := tE^2 + 2*tE - 1;
FspinE := tE*CE*BE;
L<z> := ext<E | Q^2 - FspinE>;

LiftL := LiftPolynomial(L);
print "RESULT u6_rowbit_botheta_setup", q, Genus(E), Degree(E,K), Genus(L), Degree(L,E);
PrintFactorSummary("u6_rowbit_factor_domainspin_botheta", LiftL);

for eta in [ 1, -1 ] do
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

    print "RESULT u6_rowbit_aeta_sign_setup", q, eta, Degree(N,L);
    LiftN := LiftPolynomial(N);
    PrintFactorSummary(Sprintf("u6_rowbit_factor_Aeta_eta%o", eta), LiftN);
end for;

print "RESULT p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q607 done";
