// P27 Dplus U6 row-bit factor-label probe over q607.
//
// This starts from the local Magma factor split:
//   domain-spin: 32 -> 16 + 16
//   Aeta eta=+1: 32 -> 8 + 8 + 8 + 8
//
// It checks whether the factors descend from S to Y=S^2, whether rho-paired
// Aeta factors multiply back to domain-spin factors, and how complex the first
// Aeta factor's quartic-in-Y coefficients are in the basis
//   1,w,z,wz,rho,rho*w,rho*z,rho*w*z.

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

function MatchFactor(poly, factors)
    for j := 1 to #factors do
        if poly eq factors[j] then
            return j;
        end if;
    end for;
    return 0;
end function;

function ToEvenY(poly)
    P := Parent(poly);
    Base := BaseRing(P);
    PY<Y> := PolynomialRing(Base);
    out := PY!0;
    for i := 0 to Degree(poly) do
        c := Coefficient(poly, i);
        if c ne 0 then
            if i mod 2 ne 0 then
                return false, PY!0;
            end if;
            out +:= c*Y^(i div 2);
        end if;
    end for;
    return true, out;
end function;

function KDeg(x)
    if x eq 0 then
        return -1, -1;
    end if;
    return Degree(Numerator(x)), Degree(Denominator(x));
end function;

procedure AddKDeg(~max_num, ~max_den, x)
    n, d := KDeg(x);
    if n gt max_num then
        max_num := n;
    end if;
    if d gt max_den then
        max_den := d;
    end if;
end procedure;

function FlatMetrics(x)
    // x in N = L + L*rho; L = E + E*z; E = K + K*w.
    seqN := Eltseq(x);
    max_num := -1;
    max_den := -1;
    nonzero := 0;
    for aN in seqN do
        seqL := Eltseq(aN);
        for aL in seqL do
            seqE := Eltseq(aL);
            for aE in seqE do
                if aE ne 0 then
                    nonzero +:= 1;
                    AddKDeg(~max_num, ~max_den, aE);
                end if;
            end for;
        end for;
    end for;
    return nonzero, max_num, max_den;
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
PN<S> := Parent(LiftN);
FacL_N := [ PN!f : f in FacL ];

phir := hom< N -> N | -rho >;

print "RESULT factor_label_setup", q, #FacL, [ Degree(f) : f in FacL ], #FacN, [ Degree(f) : f in FacN ];
print "RESULT factor_label_even_domain", [ (ToEvenY(f)) select true else false : f in FacL ];
print "RESULT factor_label_even_Aeta", [ (ToEvenY(f)) select true else false : f in FacN ];
print "RESULT factor_label_rho_perm", [ MatchFactor(ApplyCoeffHom(phir, f), FacN) : f in FacN ];

for pair in [ [1,2], [3,4] ] do
    prod := FacN[pair[1]] * FacN[pair[2]];
    prod := prod / LeadingCoefficient(prod);
    print "RESULT factor_label_pair_domain_match", pair, MatchFactor(prod, FacL_N);
end for;

for i := 1 to #FacN do
    ok, fy := ToEvenY(FacN[i]);
    print "RESULT factor_label_Aeta_Y_degree", i, ok, Degree(fy);
end for;

for fidx := 1 to #FacN do
    ok, fy := ToEvenY(FacN[fidx]);
    print "RESULT factor_label_coeff_profile_start", q, fidx, ok, Degree(fy);
    for i := 0 to Degree(fy) do
        c := Coefficient(fy, i);
        nz, mn, md := FlatMetrics(c);
        print "RESULT factor_label_coeff", fidx, i, "nonzero_basis", nz, "max_num_degree", mn, "max_den_degree", md;
    end for;
end for;

print "RESULT p27_trace_norm_dplus_u6_rowbit_factor_label_q607 done";
