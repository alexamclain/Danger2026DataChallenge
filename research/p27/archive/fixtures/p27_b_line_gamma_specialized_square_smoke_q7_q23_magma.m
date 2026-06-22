// P27 B-line gamma specialized squareclass smoke.
//
// This is a small online-Magma-compatible falsifier for the visible claim that
// the gamma class is already square on the generic B/H transition.
//
// With A = B^2 - 2, H^2 = u + 2, and Y = v + 2, the transition is:
//
//   Y^4
//   - 4*H^2*Y^3
//   + (-4*B^2*H^2 + 8*B^2 + 32*H^2 - 32)*Y^2
//   + 16*H^2*(B^2 - 4)*Y
//   + 16*(B^2 - 4)^2.
//
// A universal square identity for Y over the visible B/H layer would survive
// nondegenerate one-parameter specializations.  These two small fields give
// irreducible quartic specializations with Y nonsquare.

SetColumns(0);

procedure Check(q, h_case)
    F := GF(q);
    K<B> := FunctionField(F);

    if h_case eq 0 then
        H := B;
        label := "HB";
    else
        H := B + 1;
        label := "HBPLUS1";
    end if;

    P<Y> := PolynomialRing(K);
    Pol := Y^4
        - 4*H^2*Y^3
        + (-4*B^2*H^2 + 8*B^2 + 32*H^2 - 32)*Y^2
        + 16*H^2*(B^2 - 4)*Y
        + 16*(B^2 - 4)^2;

    print "P27_GAMMA_SPEC", label, "Q", q, "IRR", IsIrreducible(Pol);
    L<V> := ext<K | Pol>;
    print "P27_GAMMA_SPEC", label, "Q", q, "Y_SQUARE", IsSquare(V);
    print "P27_GAMMA_SPEC", label, "Q", q, "NORM_FORM", Norm(V);
end procedure;

Check(7, 0);
Check(23, 1);

print "RESULT p27_gamma_specialized_square_smoke done";
