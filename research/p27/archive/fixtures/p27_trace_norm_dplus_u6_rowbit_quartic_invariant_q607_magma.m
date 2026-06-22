// P27 Dplus U6 row-bit quartic-label invariant probe over q607.
//
// The Aeta factor-label probe shows each degree-8 factor descends to a
// quartic in Y=S^2=U6+2 over N = E_h90(z,rho).  This fixture computes the
// first invariants of that quartic label: irreducibility, discriminant
// squareclass, cubic resolvent factorization, and basic coefficient profiles.

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

function CubicResolvent(f)
    P := Parent(f);
    Base := BaseRing(P);
    PR<R> := PolynomialRing(Base);
    g := f / LeadingCoefficient(f);
    a := Coefficient(g, 3);
    b := Coefficient(g, 2);
    c := Coefficient(g, 1);
    d := Coefficient(g, 0);
    return R^3 - b*R^2 + (a*c - 4*d)*R + (4*b*d - a^2*d - c^2);
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
        for aL in Eltseq(aN) do
            for aE in Eltseq(aL) do
                if aE ne 0 then
                    nonzero +:= 1;
                    AddKDeg(~max_num, ~max_den, aE);
                end if;
            end for;
        end for;
    end for;
    return nonzero, max_num, max_den;
end function;

procedure PrintMetric(label, x)
    nz, mn, md := FlatMetrics(x);
    print "RESULT", label, "nonzero_basis", nz, "max_num_degree", mn, "max_den_degree", md;
end procedure;

PW<W> := PolynomialRing(K);
C := t^2 + 2*t - 1;
Rbranch := t^2 - 2*t - 1;
Ktrace := -C*Rbranch;
E<w> := ext<K | W^2 - Ktrace>;

PE<Q> := PolynomialRing(E);
tE := E!t;
FspinE := tE*(tE^2 + 2*tE - 1)*(tE^2 + 1);
L<z> := ext<E | Q^2 - FspinE>;

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
ok, fY := ToEvenY(FacN[1]);
fY := fY / LeadingCoefficient(fY);
tN := N!t;
Acoord := (tN^8 - 4*tN^6 - 2*tN^4 - 4*tN^2 + 1)/(4*tN^4);

print "RESULT invariant_setup", q, ok, Degree(fY);

FacY := Factorization(fY);
print "RESULT quartic_factorization", Degree(fY), #FacY;
for item in FacY do
    print "RESULT quartic_factor", Degree(item[1]), item[2];
end for;

Disc := Discriminant(fY);
disc_sq, _ := IsSquare(Disc);
print "RESULT quartic_discriminant_square", disc_sq;
PrintMetric("quartic_discriminant_metric", Disc);

phir := hom< N -> N | -rho >;
DiscNorm := Disc * phir(Disc);
disc_norm_sq, _ := IsSquare(DiscNorm);
print "RESULT quartic_discriminant_rho_norm_square", disc_norm_sq;
PrintMetric("quartic_discriminant_rho_norm_metric", DiscNorm);

Res := CubicResolvent(fY);
FacRes := Factorization(Res);
print "RESULT cubic_resolvent_factorization", Degree(Res), #FacRes;
for item in FacRes do
    print "RESULT cubic_resolvent_factor", Degree(item[1]), item[2];
    if Degree(item[1]) eq 1 then
        root := -Coefficient(item[1], 0) / Coefficient(item[1], 1);
        print "RESULT cubic_resolvent_linear_root_matches_16_minus_8A", root eq 16 - 8*Acoord;
        PrintMetric("cubic_resolvent_linear_root_metric", root);
    end if;
    if Degree(item[1]) eq 2 then
        a2 := Coefficient(item[1], 2);
        b2 := Coefficient(item[1], 1);
        c2 := Coefficient(item[1], 0);
        qdisc := b2^2 - 4*a2*c2;
        qdisc_sq, _ := IsSquare(qdisc);
        print "RESULT cubic_resolvent_quadratic_discriminant_square", qdisc_sq;
        PrintMetric("cubic_resolvent_quadratic_discriminant_metric", qdisc);
    end if;
end for;

DiscRes := Discriminant(Res);
res_disc_sq, _ := IsSquare(DiscRes);
print "RESULT cubic_resolvent_discriminant_square", res_disc_sq;
PrintMetric("cubic_resolvent_discriminant_metric", DiscRes);

print "RESULT p27_trace_norm_dplus_u6_rowbit_quartic_invariant_q607 done";
