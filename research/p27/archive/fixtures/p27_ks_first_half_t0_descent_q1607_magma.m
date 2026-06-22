// P27 K/S first-half descent under translation by (0,0), q1607.
//
// This validates the algebraic T-cover transform and the finite squareclass
// compatibility of the first-half B branch with the E -> E' quotient.

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

print "BRANCH_FACTOR_DIFF_ZERO", U_num^2 - 4*U_den^2 - branch eq 0;

P1<Y> := PolynomialRing(F);
// direct symbolic check in one variable:
T2_image_scaled := X^6*((-1/X)*(((-1/X)^2)+1)*(((-1/X)^2)+2*(-1/X)-1));
print "T2_TRANSFORM_ZERO", T2_image_scaled - T2 eq 0;

same_plus := 0;
same_minus := 0;
compact_points := 0;
compact_reject := 0;
bad_tcover := 0;
bad_compact_image := 0;

for x in F do
    if x eq 0 or x eq 1 or x eq -1 then
        continue;
    end if;
    x2 := x^2;
    for wr in Roots(Y^2 - (x^3-x)) do
        w := wr[1];
        for tr in Roots(Y^2 - x*(x2+1)*(x2+2*x-1)) do
            t := tr[1];
            mt := (x + 1)*(2*w*x + x^3 + x2 - x - 1);
            m0 := (x2 + 1)*(x2 + 2*x - 1)*(w*x + w + 2*x2);
            h := w*(x2 + 1)*(m0 + mt*t)/x;
            if h eq 0 or not IsSquare(h) then
                compact_reject +:= 1;
                continue;
            end if;
            compact_points +:= 1;
            base := t*x*(t*w + x*(x-1)*(x+1)^2)*(2*w*x + x^3 + x2 - x - 1);
            xp := -1/x;
            wp := w/x2;
            for s in [F!1, F!-1] do
                tp := s*t/(x^3);
                xp2 := xp^2;
                if tp^2 ne xp*(xp2+1)*(xp2+2*xp-1) then
                    bad_tcover +:= 1;
                    continue;
                end if;
                mtp := (xp + 1)*(2*wp*xp + xp^3 + xp2 - xp - 1);
                m0p := (xp2 + 1)*(xp2 + 2*xp - 1)*(wp*xp + wp + 2*xp2);
                hp := wp*(xp2 + 1)*(m0p + mtp*tp)/xp;
                if hp eq 0 or not IsSquare(hp) then
                    bad_compact_image +:= 1;
                end if;
                image := tp*xp*(tp*wp + xp*(xp-1)*(xp+1)^2)
                    *(2*wp*xp + xp^3 + xp2 - xp - 1);
                if IsSquare(image/base) then
                    same_plus +:= 1;
                else
                    same_minus +:= 1;
                end if;
            end for;
        end for;
    end for;
end for;

print "COUNTS", compact_points, compact_reject, same_plus, same_minus,
    bad_tcover, bad_compact_image;
print "RESULT p27_ks_first_half_t0_descent_q1607 done";
