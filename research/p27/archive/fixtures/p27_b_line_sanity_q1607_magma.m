// P27 B-line Kummer extraction packet: small online Magma sanity check.
//
// This validates the B quotient, A+2=B^2 identity, and K/A branch equations
// over q=1607.  It does not perform the full d3 divisor extraction.
//
// Expected output:
// RESULT p27_b_line_sanity_q1607 1604 3 0 0 0 0

SetColumns(0);
q := 1607;
F := GF(q);

rows := 0;
a_identity_mismatch := 0;
b_relation_mismatch := 0;
k_branch_mismatch := 0;
branch_poly_mismatch := 0;
degenerate := 0;

for X in F do
    denB := (X^2 - 1)^2;
    denA := (X^2 - 1)^4;
    denK := 4*X*(X^2 - 1)*(X^2 + 1)^2;
    if denB eq 0 or denA eq 0 or denK eq 0 then
        degenerate +:= 1;
        continue;
    end if;

    B := 8*X^2/denB;
    A := -2*(X^8 - 4*X^6 - 26*X^4 - 4*X^2 + 1)/denA;
    K := (X^4 - 6*X^2 + 1)^2/denK;
    L := K^2;
    rows +:= 1;

    if B*denB ne 8*X^2 then
        b_relation_mismatch +:= 1;
    end if;
    if A + 2 ne B^2 then
        a_identity_mismatch +:= 1;
    end if;
    if B ne 0 and B ne -2 then
        if L ne (B - 2)^4/(8*B*(B + 2)^2) then
            k_branch_mismatch +:= 1;
        end if;
    end if;
    if B ne 0 and B ne 2 and B ne -2 then
        rel := (8*B*(B + 2)^2*L - (B - 2)^4)*
            (8*B*(B - 2)^2*L + (B + 2)^4);
        if rel ne 0 then
            branch_poly_mismatch +:= 1;
        end if;
    end if;
end for;

print "RESULT p27_b_line_sanity_q1607", rows, degenerate,
    b_relation_mismatch, a_identity_mismatch, k_branch_mismatch,
    branch_poly_mismatch;
