// P27 K/S first-half alpha-ratio q1607 check.
//
// This validates the exact branch factorization and the same-eta alpha-ratio
// identity in a p27-signature guard field without attempting normalization.

SetColumns(0);
q := 1607;
F := GF(q);
P<X,W,T,eta> := PolynomialRing(F, 4);

X2 := X^2;
X3 := X2*X;
X4 := X2^2;
X5 := X4*X;
T2 := X*(X2 + 1)*(X2 + 2*X - 1);

U_core := eta*4*T*W*X
    + T*X3 + T*X2 - T*X - T
    + 2*X5 + 2*X4 - 2*X3 - 2*X2;
U_num := 2*U_core;
U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;
branch := 32*T*X
    *(eta*T*W + X*(X - 1)*(X + 1)^2)
    *(2*eta*W*X + X3 + X2 - X - 1);

print "FACTOR_DIFF_ZERO", U_num^2 - 4*U_den^2 - branch eq 0;

P3<X3v,W3v,T3v> := PolynomialRing(F, 3);
I := ideal<P3 | W3v^2 - (X3v^3 - X3v), T3v^2 - X3v*(X3v^2 + 1)*(X3v^2 + 2*X3v - 1)>;
pterm := X3v*(X3v - 1)*(X3v + 1)^2;
Aplus := T3v*W3v + pterm;
Aminus := -T3v*W3v + pterm;
ratio_identity := Aplus*Aminus + 4*X3v^2*W3v^2;
print "RATIO_IDEAL_MEMBER", ratio_identity in I;

same_plus := 0;
same_minus := 0;
same_zero := 0;
flip_plus := 0;
flip_minus := 0;
flip_zero := 0;
compact_points := 0;
compact_reject := 0;

for x in F do
    if x eq 0 or x eq 1 or x eq -1 then
        continue;
    end if;
    x2 := x^2;
    for w in Roots(Polynomial([-(x^3-x), 0, 1])) do
        wv := w[1];
        for t in Roots(Polynomial([-x*(x2+1)*(x2+2*x-1), 0, 1])) do
            tv := t[1];
            mt := (x + 1)*(2*wv*x + x^3 + x2 - x - 1);
            m0 := (x2 + 1)*(x2 + 2*x - 1)*(wv*x + wv + 2*x2);
            h := wv*(x2 + 1)*(m0 + mt*tv)/x;
            if h eq 0 then
                continue;
            end if;
            if not IsSquare(h) then
                compact_reject +:= 1;
                continue;
            end if;
            compact_points +:= 1;
            poly := x^3 + x2 - x - 1;
            pt := x*(x - 1)*(x + 1)^2;
            ap := tv*wv + pt;
            am := -tv*wv + pt;
            mp := 2*wv*x + poly;
            mf := 2*wv*x - poly;
            if ap eq 0 or am eq 0 then
                same_zero +:= 1;
            elif IsSquare(am/ap) then
                same_plus +:= 1;
            else
                same_minus +:= 1;
            end if;
            if mp eq 0 or mf eq 0 then
                flip_zero +:= 1;
            elif IsSquare(mf/mp) then
                flip_plus +:= 1;
            else
                flip_minus +:= 1;
            end if;
        end for;
    end for;
end for;

print "COUNTS", compact_points, compact_reject, same_plus, same_minus, same_zero,
    flip_plus, flip_minus, flip_zero;
print "RESULT p27_ks_first_half_alpha_ratio_q1607 done";
