// P27 E-prime T-cover twist obstruction: online Magma validation.
//
// This mirrors p27_eprime_tcover_twist_obstruction.py over q=1471.
// Expected output:
//
// RESULT p27_eprime_tcover_twist_q1471 ok -1 1660 0 0 0 0 0

SetColumns(0);
q := 1471;
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

minus_one_chi := Leg(F!-1);
Eprime_mismatch := 0;
sigma_E_mismatch := 0;
sigma_S_ratio_mismatch := 0;
sigma_T_mismatch := 0;
T_points := 0;

for X in F do
    for W in Roots2(X^3 - X) do
        if X eq 0 then
            continue;
        end if;

        sX := -1/X;
        sW := W/X^2;
        if sW^2 ne sX^3 - sX then
            sigma_E_mismatch +:= 1;
        end if;

        U := X - 1/X;
        V := W*(X^2 + 1)/X^2;
        if V^2 ne U^3 + 4*U then
            Eprime_mismatch +:= 1;
        end if;

        S := X*(X^2 + 1)*(X^2 + 2*X - 1);
        sS := sX*(sX^2 + 1)*(sX^2 + 2*sX - 1);
        if S eq 0 or sS eq 0 then
            continue;
        end if;

        if sS/S ne 1/X^6 then
            sigma_S_ratio_mismatch +:= 1;
        end if;

        for T in Roots2(S) do
            T_points +:= 1;
            sT := T/X^3;
            if sT^2 ne sS then
                sigma_T_mismatch +:= 1;
            end if;
        end for;
    end for;
end for;

possible_plain_T_invariant := 0;
if minus_one_chi eq 1 then
    possible_plain_T_invariant := 1;
end if;

if minus_one_chi eq -1 and T_points eq 1660 and Eprime_mismatch eq 0 and
        sigma_E_mismatch eq 0 and sigma_S_ratio_mismatch eq 0 and
        sigma_T_mismatch eq 0 and possible_plain_T_invariant eq 0 then
    print "RESULT p27_eprime_tcover_twist_q1471 ok", minus_one_chi, T_points,
        Eprime_mismatch, sigma_E_mismatch, sigma_S_ratio_mismatch,
        sigma_T_mismatch, possible_plain_T_invariant;
else
    print "RESULT p27_eprime_tcover_twist_q1471 mismatch", minus_one_chi, T_points,
        Eprime_mismatch, sigma_E_mismatch, sigma_S_ratio_mismatch,
        sigma_T_mismatch, possible_plain_T_invariant;
end if;
