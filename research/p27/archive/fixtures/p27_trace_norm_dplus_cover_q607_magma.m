// P27 trace/norm D_plus cover: small online Magma validation.
//
// This validates the named combined squareclass behind the trace/norm D
// prefilter on q = 607, matching p27's chi(-1)=-1 and chi(2)=+1 signs.

SetColumns(0);
q := 607;
Fq := GF(q);

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
        return [ Fq!0 ];
    elif not IsSquare(a) then
        return [ Fq | ];
    else
        r := Sqrt(a);
        return [ r, -r ];
    end if;
end function;

rows := 0;
dplus := 0;
cover_square := 0;
cover_nonsquare := 0;
cover_zero := 0;
cover_points := 0;
mismatch := 0;
orientation_pp := 0;
orientation_pm := 0;
orientation_mp := 0;
orientation_mm := 0;

for t in Fq do
    y := t + 1;
    B := t^2 + 1;
    C := t^2 + 2*t - 1;
    R := t^2 - 2*t - 1;
    K := -C*R;
    F := t*C*B;
    if K eq 0 or F eq 0 then
        continue;
    end if;
    for w in Roots2(K) do
        for z in Roots2(F) do
            eps_h := Leg(t);
            eps_v := Leg(y*C);
            if eps_h eq 0 or eps_v eq 0 then
                continue;
            end if;
            hcore := C*B + eps_h*2*t*z;
            vcore := 2*C*t^2 + eps_v*z*w;
            core := (1 - t^2)*B*C*y*vcore*hcore;
            D := -Leg(core);
            rows +:= 1;
            if D eq 1 then
                dplus +:= 1;
            end if;
            if eps_h eq 1 and eps_v eq 1 then
                orientation_pp +:= 1;
            elif eps_h eq 1 and eps_v eq -1 then
                orientation_pm +:= 1;
            elif eps_h eq -1 and eps_v eq 1 then
                orientation_mp +:= 1;
            elif eps_h eq -1 and eps_v eq -1 then
                orientation_mm +:= 1;
            end if;
            cover_chi := Leg(-core);
            if cover_chi eq 1 then
                cover_square +:= 1;
            elif cover_chi eq -1 then
                cover_nonsquare +:= 1;
            else
                cover_zero +:= 1;
            end if;
            cover_points +:= #Roots2(-core);
            if (cover_chi eq 1) ne (D eq 1) then
                mismatch +:= 1;
            end if;
        end for;
    end for;
end for;

print "RESULT p27_dplus_cover_q607", rows, dplus, cover_square, cover_nonsquare,
    cover_zero, cover_points, mismatch, orientation_pp, orientation_pm,
    orientation_mp, orientation_mm;
