// P27 K/S branch-extraction packet: small online Magma sanity check.
//
// This validates the K/S map and the H90 identities over q=1471.  It does not
// perform the full normalization/genus extraction.
//
// Expected output:
//
// RESULT p27_ks_branch_sanity_q1471 ok 1468 0 0 0 0 0 -1

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

points := 0;
sroot_square_mismatch := 0;
k_relation_mismatch := 0;
sroot_linear_mismatch := 0;
h90_salpha_mismatch := 0;
h90_norm_mismatch := 0;

for X in F do
    for W in Roots2(X^3 - X) do
        snum := (X^2 - 2*X - 1)*(X^2 + 2*X - 1);
        sden := 2*W*(X^2 + 1);
        kden := 4*X*(X - 1)*(X + 1)*(X^2 + 1)^2;
        if sden eq 0 or kden eq 0 then
            continue;
        end if;

        Sroot := snum/sden;
        K := snum^2/kden;
        points +:= 1;

        if Sroot^2 ne K then
            sroot_square_mismatch +:= 1;
        end if;
        if 2*Sroot*W*(X^2 + 1) ne snum then
            sroot_linear_mismatch +:= 1;
        end if;
        if K*kden ne snum^2 then
            k_relation_mismatch +:= 1;
        end if;

        T2 := X*(X^2 + 1)*(X^2 + 2*X - 1);
        mt := (X + 1)*(2*W*X + X^3 + X^2 - X - 1);
        m0 := (X^2 + 1)*(X^2 + 2*X - 1)*(W*X + W + 2*X^2);
        L := 4*W*X^2 + 4*W*X + X^4 + 6*X^3 - 2*X - 1;
        Salpha := W*(X + 1) + 2*X^2;

        if Salpha^2 ne X*L then
            h90_salpha_mismatch +:= 1;
        end if;
        if m0^2 - mt^2*T2 ne 4*T2*Salpha^2 then
            h90_norm_mismatch +:= 1;
        end if;
    end for;
end for;

minus_one_chi := Leg(F!-1);

if points eq 1468 and sroot_square_mismatch eq 0 and
        k_relation_mismatch eq 0 and sroot_linear_mismatch eq 0 and
        h90_salpha_mismatch eq 0 and h90_norm_mismatch eq 0 and
        minus_one_chi eq -1 then
    print "RESULT p27_ks_branch_sanity_q1471 ok", points,
        sroot_square_mismatch, k_relation_mismatch,
        sroot_linear_mismatch, h90_salpha_mismatch,
        h90_norm_mismatch, minus_one_chi;
else
    print "RESULT p27_ks_branch_sanity_q1471 mismatch", points,
        sroot_square_mismatch, k_relation_mismatch,
        sroot_linear_mismatch, h90_salpha_mismatch,
        h90_norm_mismatch, minus_one_chi;
end if;
