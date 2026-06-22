// P27 trace/norm Dplus H90 quotient pricing.
//
// The relative identity Norm_z(-core)=z^2*S^2 gives an order-4 lift
//
//   alpha(t,z,w,s) = (t,-z,w,z*S/s).
//
// Since alpha fixes t,w, the quotient candidate is the genus-1 curve
//
//   E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1).
//
// This fixture prices the degree-4 relative Dplus cover over E_h90.

SetColumns(0);
q := 607;
Fq := GF(q);

K<t> := FunctionField(Fq);
P<W> := PolynomialRing(K);

C := t^2 + 2*t - 1;
R := t^2 - 2*t - 1;
B := t^2 + 1;
Fspin := t*C*B;
Ktrace := -C*R;

E<w> := ext<K | W^2 - Ktrace>;
PE<Z> := PolynomialRing(E);
tE := E!t;
wE := E!w;
CE := tE^2 + 2*tE - 1;
BE := tE^2 + 1;
yE := tE + 1;
FspinE := tE*CE*BE;

L<z> := ext<E | Z^2 - FspinE>;
PL<S> := PolynomialRing(L);
tL := L!t;
wL := L!w;
zL := L!z;
CL := tL^2 + 2*tL - 1;
BL := tL^2 + 1;
yL := tL + 1;

print "RESULT h90_quotient_base", Genus(E), Degree(E,K), #Places(E, 1);

for eh in [ 1, -1 ] do
    for ev in [ 1, -1 ] do
        hcore := CL*BL + eh*2*tL*zL;
        vcore := 2*CL*tL^2 + ev*zL*wL;
        core := (1 - tL^2)*BL*CL*yL*vcore*hcore;
        N<s> := ext<L | S^2 + core>;
        print "RESULT h90_relative_cover", eh, ev, Genus(N), Degree(N,E), Degree(N,K);
    end for;
end for;

