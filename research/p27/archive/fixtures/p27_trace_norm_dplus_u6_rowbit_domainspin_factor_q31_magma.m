// P27 Dplus U6 row-bit factorization over the H90 domain-spin cover, q=31.
//
// q=607 times out online once the domain-spin layer is adjoined.  This tiny
// field smoke asks whether the row-bit lift visibly splits after adjoining
// z^2=t*(t^2+2t-1)*(t^2+1).  Treat positive splits cautiously; irreducibility
// is useful evidence against an easy domain-spin source.

SetColumns(0);
q := 31;
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

print "RESULT u6_rowbit_domainspin_q31_setup", q, Genus(E), Degree(E,K), Genus(L), Degree(L,E);
LiftL := LiftPolynomial(L);
PrintFactorSummary("u6_rowbit_domainspin_q31", LiftL);
print "RESULT p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q31 done";
