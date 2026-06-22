// P27 trace/norm Dplus H90 branch/Kummer pricing.
//
// For the normalized quartic over E_h90:
//
//   rho^4 - 2*U_eta*rho^2 + V = 0
//   V = F*Sprime^2
//
// the first quadratic resolvent is
//
//   q_eta^2 = U_eta^2 - V.
//
// This fixture factors the symbolic branch class on E_h90 and prices the
// intermediate quadratic cover over q=607.

SetColumns(0);
q := 607;
Fq := GF(q);

K<t> := FunctionField(Fq);
P<W> := PolynomialRing(K);

B := t^2 + 1;
C := t^2 + 2*t - 1;
R := t^2 - 2*t - 1;
Fspin := t*C*B;
Ktrace := -C*R;

E<w> := ext<K | W^2 - Ktrace>;
PE<Q> := PolynomialRing(E);
tE := E!t;
wE := E!w;
BE := tE^2 + 1;
CE := tE^2 + 2*tE - 1;
FspinE := tE*CE*BE;
Sprime := (tE - 1)^3*(tE + 1)^2*BE;

function OddDivisorStats(f)
    D := Divisor(f);
    odddeg := 0;
    oddcount := 0;
    for pl in Support(D) do
        v := Valuation(D, pl);
        if v mod 2 ne 0 then
            odddeg +:= Degree(pl);
            oddcount +:= 1;
        end if;
    end for;
    return oddcount, odddeg;
end function;

print "RESULT h90_branch_base", Genus(E), Degree(E,K), #Places(E,1);

ocF, odF := OddDivisorStats(FspinE);
print "RESULT h90_branch_F", ocF, odF;

for eta in [ 1, -1 ] do
    Ueta := 2*tE^2*(tE - 1)*BE^2*(eta*wE + CE);
    Delta := Ueta^2 - FspinE*Sprime^2;
    Leta := tE^8 - 20*tE^6 - 10*tE^4 - 4*tE^2 + 1
        - 8*eta*tE^3*(tE^2 + 1)*wE;
    Weta := (tE - 1)*BE*(4*tE^3 + eta*BE*wE);

    ocD, odD := OddDivisorStats(Delta);
    ocL, odL := OddDivisorStats(Leta);
    ocDW, odDW := OddDivisorStats(Delta/(FspinE*Weta^2));
    print "RESULT h90_branch_delta", eta, ocD, odD;
    print "RESULT h90_branch_Leta", eta, ocL, odL;
    print "RESULT h90_branch_delta_over_F_Wsquare", eta, ocDW, odDW;

    Qeta<qeta> := ext<E | Q^2 - Delta>;
    print "RESULT h90_branch_resolvent", eta, Genus(Qeta), Degree(Qeta,E), Degree(Qeta,K);

    // The resolvent is just the domain-spin cover because
    // Delta = Fspin * Weta^2.  The hard layer is rho^2 = Ueta + z*Weta.
    L<z> := ext<E | Q^2 - FspinE>;
    PL<RHO> := PolynomialRing(L);
    tL := L!t;
    wL := L!w;
    zL := L!z;
    BL := tL^2 + 1;
    CL := tL^2 + 2*tL - 1;
    UetaL := 2*tL^2*(tL - 1)*BL^2*(eta*wL + CL);
    WetaL := (tL - 1)*BL*(4*tL^3 + eta*BL*wL);
    Aeta := UetaL + zL*WetaL;
    ocA, odA := OddDivisorStats(Aeta);
    Neta<rho> := ext<L | RHO^2 - Aeta>;
    print "RESULT h90_branch_second_layer", eta, ocA, odA, Genus(L), Genus(Neta), Degree(Neta,L), Degree(Neta,E);
end for;
