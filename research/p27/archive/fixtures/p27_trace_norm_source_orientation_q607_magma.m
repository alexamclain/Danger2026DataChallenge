// P27 trace/norm D_plus source-orientation cover audit.
//
// The D_plus core formula uses eps_h=chi(t) and eps_v=chi((t+1)C).  To source
// those signs directly one must add orientation roots for t and (t+1)C.  This
// script avoids constructing the final degree-32 field.  It computes the base
// orientation-cover genus, then uses Riemann-Hurwitz and the odd branch
// divisor of core on M=Fq(t,z,w) to predict the final D_plus source-cover
// genus.

SetColumns(0);
q := 607;
Fq := GF(q);

K<t> := FunctionField(Fq);
P<X> := PolynomialRing(K);

// One orientation-source base component.  The genus is independent of the two
// sign twists over the algebraic closure.
L0<uh> := ext<K | X^2 - t>;
PL0<V0> := PolynomialRing(L0);
tL0 := L0!t;
C_L0 := tL0^2 + 2*tL0 - 1;
M0<uv> := ext<L0 | V0^2 - (tL0+1)*C_L0>;
PM0<Z0> := PolynomialRing(M0);
tM0 := M0!t;
B_M0 := tM0^2 + 1;
C_M0 := tM0^2 + 2*tM0 - 1;
R_M0 := tM0^2 - 2*tM0 - 1;
N0<z0> := ext<M0 | Z0^2 - tM0*C_M0*B_M0>;
PN0<W0> := PolynomialRing(N0);
tN0 := N0!t;
C_N0 := tN0^2 + 2*tN0 - 1;
R_N0 := tN0^2 - 2*tN0 - 1;
O0<w0> := ext<N0 | W0^2 + C_N0*R_N0>;
source_base_genus := Genus(O0);
source_base_degree := Degree(O0, K);

// Smaller fixed-sign field M=Fq(t,z,w), where the core branch divisor is easy
// to inspect.  Pulling through the two orientation roots has degree 4 except
// where t or (t+1)C has odd valuation, in which case the s-cover branch parity
// is killed.
F := t*(t^2 + 2*t - 1)*(t^2 + 1);
L<z> := ext<K | X^2 - F>;
PL<Y> := PolynomialRing(L);
tL := L!t;
Ktrace := -(tL^2 + 2*tL - 1)*(tL^2 - 2*tL - 1);
M<w> := ext<L | Y^2 - Ktrace>;
tM := M!t;
zM := M!z;
B := tM^2 + 1;
C := tM^2 + 2*tM - 1;
y := tM + 1;

print "RESULT source_orientation_base", source_base_genus, source_base_degree;

for eh in [ 1, -1 ] do
    for ev in [ 1, -1 ] do
        hcore := C*B + eh*2*tM*zM;
        vcore := 2*C*tM^2 + ev*zM*w;
        core := (1-tM^2)*B*C*y*vcore*hcore;
        D := Divisor(core);
        odddeg := 0;
        killdeg := 0;
        survivedeg := 0;
        oddcount := 0;
        killcount := 0;
        for pl in Support(D) do
            vc := Valuation(D, pl);
            if vc mod 2 ne 0 then
                oddcount +:= 1;
                d := Degree(pl);
                odddeg +:= d;
                vt := Valuation(tM, pl);
                vyc := Valuation(y*C, pl);
                if vt mod 2 ne 0 or vyc mod 2 ne 0 then
                    killdeg +:= d;
                    killcount +:= 1;
                else
                    survivedeg +:= d;
                end if;
            end if;
        end for;
        pred_genus := 2*source_base_genus - 1 + (4*survivedeg) div 2;
        print "RESULT source_branch_overlap", eh, ev, oddcount, odddeg,
            killcount, killdeg, survivedeg, pred_genus;
    end for;
end for;
