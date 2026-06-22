// P27 Dplus U6 row-bit factorization over the H90 domain-spin cover.
//
// Previous tests show the row-bit Kummer lift remains irreducible over
// E_h90.  This lighter fixture only adjoins the first H90/domain-spin layer:
//
//   z^2 = t*(t^2+2t-1)*(t^2+1).
//
// It separates the domain-spin factor question from the heavier A_eta
// second-layer factorization.

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
CE := tE^2 + 2*tE - 1;
BE := tE^2 + 1;
FspinE := tE*CE*BE;
L<z> := ext<E | Q^2 - FspinE>;

print "RESULT u6_rowbit_domainspin_setup", q, Genus(E), Degree(E,K), Genus(L), Degree(L,E);
LiftL := LiftPolynomial(L);
PrintFactorSummary("u6_rowbit_factor_domainspin", LiftL);
print "RESULT p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q607 done";
