// P27 Dplus U6 row-bit factor-action probe over q607.
//
// This checks how the domain-spin deck action z -> -z, Aeta deck action
// rho -> -rho, and row-bit sheet action S -> -S permute the factors of
// R(t,S^2-2) after the domain-spin and eta=+1 Aeta splits.

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

function ApplyCoeffHom(phi, poly)
    P := Parent(poly);
    S := P.1;
    out := P!0;
    for i := 0 to Degree(poly) do
        out +:= phi(Coefficient(poly, i))*S^i;
    end for;
    return out;
end function;

function ApplySNeg(poly)
    P := Parent(poly);
    S := P.1;
    out := P!0;
    for i := 0 to Degree(poly) do
        out +:= Coefficient(poly, i)*(-S)^i;
    end for;
    return out;
end function;

function MatchFactor(poly, factors)
    for j := 1 to #factors do
        if poly eq factors[j] then
            return j;
        end if;
    end for;
    return 0;
end function;

PW<W> := PolynomialRing(K);
C := t^2 + 2*t - 1;
Rbranch := t^2 - 2*t - 1;
Ktrace := -C*Rbranch;
E<w> := ext<K | W^2 - Ktrace>;

PE<Q> := PolynomialRing(E);
tE := E!t;
FspinE := tE*(tE^2 + 2*tE - 1)*(tE^2 + 1);
L<z> := ext<E | Q^2 - FspinE>;

LiftL := LiftPolynomial(L);
FacL := [ item[1] : item in Factorization(LiftL) ];
print "RESULT factor_action_domain_count", q, #FacL, [ Degree(f) : f in FacL ];

phiz := hom< L -> L | -z >;
print "RESULT factor_action_domain_z_perm", [ MatchFactor(ApplyCoeffHom(phiz, f), FacL) : f in FacL ];
print "RESULT factor_action_domain_Sneg_perm", [ MatchFactor(ApplySNeg(f), FacL) : f in FacL ];

eta := 1;
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

LiftN := LiftPolynomial(N);
FacN := [ item[1] : item in Factorization(LiftN) ];
print "RESULT factor_action_Aeta_count", q, eta, #FacN, [ Degree(f) : f in FacN ];

phir := hom< N -> N | -rho >;
print "RESULT factor_action_Aeta_rho_perm", [ MatchFactor(ApplyCoeffHom(phir, f), FacN) : f in FacN ];
print "RESULT factor_action_Aeta_Sneg_perm", [ MatchFactor(ApplySNeg(f), FacN) : f in FacN ];

print "RESULT p27_trace_norm_dplus_u6_rowbit_factor_action_q607 done";
