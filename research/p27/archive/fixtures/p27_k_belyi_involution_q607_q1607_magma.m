// P27 K-line Belyi involution audit: online Magma validation.
//
// This validates the tempting K -> 4/K shortcut on two small fields.
// Expected:
//   q=607  d3 rows 32, 4/K present 32, same 0, opposite 32, missing 0
//   q=1607 d3 rows 49, 4/K present 0,  same 0, opposite 0,  missing 49
//
// RESULT p27_k_belyi_involution ok 607 32 32 0 32 0 1607 49 0 0 0 49

SetColumns(0);

function Run(q)
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

    function KOfX(X)
        den := 4*X*(X - 1)*(X + 1)*(X^2 + 1)^2;
        if den eq 0 then
            return false, F!0;
        end if;
        num := (X^2 - 2*X - 1)^2*(X^2 + 2*X - 1)^2;
        return true, num/den;
    end function;

    Kvals := [ F | ];
    Targets := [ Integers() | ];
    mixed_k := 0;

    procedure AddK(~Kvals, ~Targets, ~mixed_k, k, target)
        idx := Index(Kvals, k);
        if idx eq 0 then
            Append(~Kvals, k);
            Append(~Targets, target);
        elif Targets[idx] ne target then
            mixed_k +:= 1;
        end if;
    end procedure;

    for X in F do
        okK, K := KOfX(X);
        if not okK then
            continue;
        end if;
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
                    d2, x6s := HalveAll(A, x5);
                    if d2 ne 1 or #x6s eq 0 then
                        continue;
                    end if;
                    target := Leg(x6s[1]);
                    branch_mixed := false;
                    for x6 in x6s do
                        if Leg(x6) ne target then
                            branch_mixed := true;
                        end if;
                    end for;
                    if not branch_mixed then
                        AddK(~Kvals, ~Targets, ~mixed_k, K, target);
                    end if;
                end for;
            end for;
        end for;
    end for;

    present := 0;
    same := 0;
    opposite := 0;
    missing := 0;
    for i in [1..#Kvals] do
        k := Kvals[i];
        image := 4/k;
        idx := Index(Kvals, image);
        if idx eq 0 then
            missing +:= 1;
        else
            present +:= 1;
            if Targets[idx] eq Targets[i] then
                same +:= 1;
            else
                opposite +:= 1;
            end if;
        end if;
    end for;

    return #Kvals, present, same, opposite, missing, mixed_k;
end function;

r607, p607, s607, o607, m607, mix607 := Run(607);
r1607, p1607, s1607, o1607, m1607, mix1607 := Run(1607);

if r607 eq 32 and p607 eq 32 and s607 eq 0 and o607 eq 32 and m607 eq 0
        and r1607 eq 49 and p1607 eq 0 and s1607 eq 0 and o1607 eq 0 and m1607 eq 49
        and mix607 eq 0 and mix1607 eq 0 then
    print "RESULT p27_k_belyi_involution ok", 607, r607, p607, s607, o607, m607,
        1607, r1607, p1607, s1607, o1607, m1607;
else
    print "RESULT p27_k_belyi_involution mismatch", 607, r607, p607, s607, o607, m607, mix607,
        1607, r1607, p1607, s1607, o1607, m1607, mix1607;
end if;
