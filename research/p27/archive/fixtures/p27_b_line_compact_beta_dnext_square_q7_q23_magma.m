// P27 B-line compactD_R / beta / d_next squareclass smoke.
//
// This checks the localized reduced-cover identity in small function fields:
//
//   compactD_R_rhs / (beta^2 * d_next) is a square
//
// where beta is the first-half branch and d_next = x5^2 + A*x5 + 1.
// It is a Magma function-field check, not a finite row count.

SetColumns(0);

procedure Check(q)
    F := GF(q);
    K<X> := FunctionField(F);

    P<Y> := PolynomialRing(K);
    L<W> := ext<K | Y^2 - (X^3 - X)>;

    P2<Q> := PolynomialRing(L);
    X2 := L!X^2;
    X3 := L!X^3;
    X4 := L!X^4;
    T2 := (L!X)*(X2 + 1)*(X2 + 2*(L!X) - 1);
    M<T> := ext<L | Q^2 - T2>;

    X := M!X;
    W := M!W;
    X2 := X^2; X3 := X^3; X4 := X^4; X5 := X^5; X6 := X^6; X8 := X^8;

    A_den := (X - 1)^4*(X + 1)^4;
    A_num := -2*(X8 - 4*X6 - 26*X4 - 4*X2 + 1);
    A := A_num/A_den;

    U_core := 4*T*W*X + T*X3 + T*X2 - T*X - T
        + 2*X5 + 2*X4 - 2*X3 - 2*X2;
    U_num := 2*U_core;
    U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;
    U := U_num/U_den;

    P3<R> := PolynomialRing(M);
    N<Z> := ext<M | R^2 - U*R + 1>;

    X := N!X;
    W := N!W;
    T := N!T;
    Z := N!Z;
    X2 := X^2; X3 := X^3; X4 := X^4; X5 := X^5; X6 := X^6; X8 := X^8;

    A_den := (X - 1)^4*(X + 1)^4;
    A_num := -2*(X8 - 4*X6 - 26*X4 - 4*X2 + 1);
    A := A_num/A_den;

    mt := 2*W*X2 + 2*W*X + X4 + 2*X3 - 2*X - 1;
    m0 := W*X5 + 3*W*X4 + 2*W*X3 + 2*W*X2 + W*X - W
        + 2*X6 + 4*X5 + 4*X3 - 2*X2;
    criterion_num := W*(X2 + 1)*(m0 + mt*T);
    compactD_R_rhs := criterion_num/X;

    U_core := 4*T*W*X + T*X3 + T*X2 - T*X - T
        + 2*X5 + 2*X4 - 2*X3 - 2*X2;
    U_num := 2*U_core;
    U_den := (T - 2*X2)*(X - 1)*(X + 1)^2;
    U := U_num/U_den;

    // Z is x5 and satisfies Z + 1/Z = U.  Therefore the first-half
    // beta branch is beta = Z - 1/Z and d_next = Z*(U + A).
    beta := (Z^2 - 1)/Z;
    d_next := Z*(U + A);
    ratio := compactD_R_rhs/(beta^2*d_next);

    is_sq, root := IsSquare(ratio);
    print "P27_COMPACT_BETA_DNEXT_Q", q, is_sq;
    if is_sq then
        print "P27_COMPACT_BETA_DNEXT_ROOT_CHECK_Q", q, root^2 eq ratio;
    end if;
end procedure;

Check(7);
Check(23);

print "RESULT p27_b_line_compact_beta_dnext_square_q7_q23 done";
