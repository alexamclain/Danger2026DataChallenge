// P27 reverse-doubling source: small online Magma validation probe.
//
// This is intentionally tiny and finite-field only.  It mirrors the Python
// q=607 enumeration in p27_reverse_doubling_source_probe.py and should emit:
//
// RESULT p27_reverse_q607 ok 512 256 0 0 1024 2048

SetColumns(0);
q := 607;
F := GF(q);

function Leg(a)
    if a eq 0 then
        return 0;
    elif IsSquare(a) then
        return 1;
    else
        return -1;
    end if;
end function;

function Roots2(a)
    if a eq 0 then
        return [ F!0 ];
    elif not IsSquare(a) then
        return [ F | ];
    else
        r := Sqrt(a);
        return [ r, -r ];
    end if;
end function;

function X16ANum(y)
    num := F!1;
    coeffs := [ -8, 24, -32, 8, 32, -48, 32, -8 ];
    for c in coeffs do
        num := num*y + F!c;
    end for;
    return num;
end function;

function RootToAXP(root, y)
    den_a := 4*(y - 1)^4;
    den_x := root - y;
    if den_a eq 0 or den_x eq 0 then
        return false, F!0, F!0;
    end if;
    A := X16ANum(y)/den_a;
    xP := root/den_x;
    if A in {F!0, F!1, F!2, F!-1, F!-2} then
        return false, F!0, F!0;
    end if;
    return true, A, xP;
end function;

function HalveKnownD(x, sd)
    out := [ F | ];
    for rd in [ sd, -sd ] do
        u := 2*x + 2*rd;
        ww := u^2 - 4;
        for sw in Roots2(ww) do
            for cand in [ (u + sw)/2, (u - sw)/2 ] do
                if cand ne 0 and cand notin out then
                    Append(~out, cand);
                end if;
            end for;
        end for;
    end for;
    return out;
end function;

function HalveAll(A, x)
    d := x^2 + A*x + 1;
    if not IsSquare(d) then
        return Leg(d), [ F | ];
    end if;
    return 1, HalveKnownD(x, Sqrt(d));
end function;

function CompactClass(X, W, T)
    X2 := X^2;
    X3 := X2*X;
    X4 := X2^2;
    X5 := X4*X;
    X6 := X5*X;
    mt := 2*W*X2 + 2*W*X + X4 + 2*X3 - 2*X - 1;
    m0 := W*X5 + 3*W*X4 + 2*W*X3 + 2*W*X2 + W*X - W
        + 2*X6 + 4*X5 + 4*X3 - 2*X2;
    if X eq 0 then
        return 0;
    end if;
    criterion := W*(X2 + 1)/X*(m0 + mt*T);
    return -Leg(criterion);
end function;

function Label2Candidate(X, W, T, root_index)
    if X eq 0 or X eq 1 then
        return false, F!0, F!0;
    end if;
    y := 2*X/(X - 1);
    y2 := y^2;
    y3 := y2*y;
    nonsplit := (y2 - 2)*(y2 - 4*y + 2);
    if Leg(nonsplit) ne -1 then
        return false, F!0, F!0;
    end if;
    qa := y2 - 2*y;
    qb := 2*y2 - y3;
    if qa eq 0 then
        return false, F!0, F!0;
    end if;
    sd := 4*T/(X - 1)^3;
    sdr := sd;
    if root_index eq 1 then
        sdr := -sd;
    end if;
    root := (sdr - qb)/(2*qa);
    ok, A, xP := RootToAXP(root, y);
    if not ok then
        return false, F!0, F!0;
    end if;
    z := W*sd/(2*X);
    den := 2*(root - y)*(y - 1)^2;
    if den eq 0 then
        return false, F!0, F!0;
    end if;
    sd1 := y*z/den;
    d1 := xP^2 + A*xP + 1;
    if sd1^2 ne d1 then
        return false, F!0, F!0;
    end if;
    x5s := HalveKnownD(xP, sd1);
    if #x5s eq 0 then
        return false, F!0, F!0;
    end if;
    return true, A, x5s[1];
end function;

function XDouble(A, qx)
    den := 4*qx*(qx^2 + A*qx + 1);
    if den eq 0 then
        return false, F!0;
    end if;
    return true, (qx^2 - 1)^2/den;
end function;

oriented := 0;
d3_plus := 0;
x6_branches := 0;
x6_square := 0;
reverse_mismatch := 0;
point_mismatch := 0;
reverse_z_points := 0;
reverse_zy_points := 0;

for X in F do
    for W in Roots2(X^3 - X) do
        T2 := X*(X^2 + 1)*(X^2 + 2*X - 1);
        for T in Roots2(T2) do
            if CompactClass(X, W, T) ne -1 then
                continue;
            end if;
            for ri in [ 0, 1 ] do
                ok, A, x5 := Label2Candidate(X, W, T, ri);
                if not ok then
                    continue;
                end if;
                oriented +:= 1;
                d2, x6s := HalveAll(A, x5);
                if d2 ne 1 then
                    continue;
                end if;
                all_square := true;
                for x6 in x6s do
                    x6_branches +:= 1;
                    ok_dbl, prev := XDouble(A, x6);
                    if not ok_dbl or prev ne x5 then
                        reverse_mismatch +:= 1;
                    end if;
                    d3 := x6^2 + A*x6 + 1;
                    x6_chi := Leg(x6);
                    d3_chi := Leg(d3);
                    if x6_chi ne d3_chi then
                        point_mismatch +:= 1;
                    end if;
                    if x6_chi eq 1 then
                        x6_square +:= 1;
                        reverse_z_points +:= #Roots2(x6);
                        reverse_zy_points +:= #Roots2(x6) * #Roots2(d3);
                    else
                        all_square := false;
                    end if;
                end for;
                if #x6s gt 0 and all_square then
                    d3_plus +:= 1;
                end if;
            end for;
        end for;
    end for;
end for;

if oriented eq 512 and d3_plus eq 256 and reverse_mismatch eq 0
        and point_mismatch eq 0 and reverse_z_points eq 1024
        and reverse_zy_points eq 2048 then
    print "RESULT p27_reverse_q607 ok", oriented, d3_plus, reverse_mismatch,
        point_mismatch, reverse_z_points, reverse_zy_points;
else
    print "RESULT p27_reverse_q607 mismatch", oriented, d3_plus, reverse_mismatch,
        point_mismatch, reverse_z_points, reverse_zy_points;
end if;
