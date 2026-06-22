// P27 trace/norm Dplus H90 normalized quartic model.
//
// Over E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1), the scaled variable
// rho=s/((t+1)(t^2+2t-1)) satisfies
//
//   rho^4 - 2*U_eta*rho^2 + F*Sprime^2 = 0,
//
// where eta=eh*ev is the only remaining sign parameter.

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
PE<RHO> := PolynomialRing(E);
tE := E!t;
wE := E!w;
BE := tE^2 + 1;
CE := tE^2 + 2*tE - 1;
FspinE := tE*CE*BE;
Sprime := (tE - 1)^3*(tE + 1)^2*BE;

print "RESULT h90_quartic_base", Genus(E), Degree(E,K), #Places(E, 1);

for eta in [ 1, -1 ] do
    Ueta := 2*tE^2*(tE - 1)*BE^2*(eta*wE + CE);
    N<rho> := ext<E | RHO^4 - 2*Ueta*RHO^2 + FspinE*Sprime^2>;
    print "RESULT h90_quartic_model", eta, Genus(N), Degree(N,E), Degree(N,K);
end for;

