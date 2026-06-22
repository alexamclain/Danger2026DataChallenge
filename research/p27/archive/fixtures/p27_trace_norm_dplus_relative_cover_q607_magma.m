// P27 trace/norm Dplus relative cover: small online Magma pricing.
//
// This prices the reduced relative object identified by
// p27_trace_norm_dplus_relative_descent_probe.py.  It is not the full
// orientation-source cover.  For each fixed orientation sign pair eh,ev, build
//
//   z^2 = t*(t^2+2t-1)*(t^2+1)
//   w^2 = -(t^2+2t-1)*(t^2-2t-1)
//   s^2 = -core(eh,ev)
//
// over GF(607), matching p27-compatible signs chi(-1)=-1 and chi(2)=+1.

SetColumns(0);
q := 607;
Fq := GF(q);

K<t> := FunctionField(Fq);
P<Z> := PolynomialRing(K);

B := t^2 + 1;
C := t^2 + 2*t - 1;
R := t^2 - 2*t - 1;
F := t*C*B;

L<z> := ext<K | Z^2 - F>;
PL<W> := PolynomialRing(L);
tL := L!t;
zL := L!z;
BL := tL^2 + 1;
CL := tL^2 + 2*tL - 1;
RL := tL^2 - 2*tL - 1;
Ktrace := -CL*RL;

M<w> := ext<L | W^2 - Ktrace>;
PM<S> := PolynomialRing(M);
tM := M!t;
zM := M!z;
wM := M!w;
BM := tM^2 + 1;
CM := tM^2 + 2*tM - 1;
yM := tM + 1;

print "RESULT relative_base", Genus(L), Degree(L,K), Genus(M), Degree(M,K);

for eh in [ 1, -1 ] do
    for ev in [ 1, -1 ] do
        hcore := CM*BM + eh*2*tM*zM;
        vcore := 2*CM*tM^2 + ev*zM*wM;
        core := (1 - tM^2)*BM*CM*yM*vcore*hcore;
        N<s> := ext<M | S^2 + core>;
        print "RESULT relative_dplus_cover", eh, ev, Genus(N), Degree(N,K), Degree(N,M);
    end for;
end for;

