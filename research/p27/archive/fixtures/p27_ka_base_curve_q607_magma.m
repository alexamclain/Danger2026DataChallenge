// P27 K/A base curve: online Magma validation.
//
// This is a small finite-field sanity check for the explicit base curve
//
//   64(A-2)^2(A+2)L^2 + 64(A+2)(A+14)(3A+10)L - (A-2)^4 = 0,
//   L = K^2.
//
// It validates the B-rationalized branches used by the sampler probes:
//
//   A = B^2 - 2,
//   L0 = -(B+2)^4/(8 B (B-2)^2),
//   L1 =  (B-2)^4/(8 B (B+2)^2).
//
// Expected output:
//
// RESULT p27_ka_base_q607 ok 607 604 3 0 1208 0 0 0

SetColumns(0);
q := 607;
F := GF(q);

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

function Key(K, A)
    return Integers()!K + q*(Integers()!A);
end function;

function BaseEquation(A, L)
    return 64*(A-2)^2*(A+2)*L^2
        + 64*(A+2)*(A+14)*(3*A+10)*L
        - (A-2)^4;
end function;

function BaseLValues(A)
    c2 := 64*(A-2)^2*(A+2);
    c1 := 64*(A+2)*(A+14)*(3*A+10);
    c0 := -(A-2)^4;
    out := [ F | ];
    if c2 eq 0 then
        if c1 ne 0 then
            Append(~out, -c0/c1);
        end if;
        return out;
    end if;
    disc := c1^2 - 4*c2*c0;
    for sd in Roots2(disc) do
        Append(~out, (-c1 + sd)/(2*c2));
        Append(~out, (-c1 - sd)/(2*c2));
    end for;
    return SetToSequence(SequenceToSet(out));
end function;

base_keys := {};
base_equation_mismatch := 0;
disc_factor_mismatch := 0;
for A in F do
    c2 := 64*(A-2)^2*(A+2);
    c1 := 64*(A+2)*(A+14)*(3*A+10);
    c0 := -(A-2)^4;
    disc := c1^2 - 4*c2*c0;
    expected_disc := 256*(A+2)*(A+6)^2*(A^2 + 60*A + 132)^2;
    if disc ne expected_disc then
        disc_factor_mismatch +:= 1;
    end if;
    for L in BaseLValues(A) do
        if BaseEquation(A, L) ne 0 then
            base_equation_mismatch +:= 1;
        end if;
        for K in Roots2(L) do
            Include(~base_keys, Key(K, A));
        end for;
    end for;
end for;

param_keys := {};
param_rows := 0;
param_equation_mismatch := 0;
param_denominator_skip := 0;
for B in F do
    if B eq 0 or B eq 2 or B eq -2 then
        param_denominator_skip +:= 1;
        continue;
    end if;
    A := B^2 - 2;
    L0 := -(B + 2)^4/(8*B*(B - 2)^2);
    L1 :=  (B - 2)^4/(8*B*(B + 2)^2);
    for L in [ L0, L1 ] do
        if BaseEquation(A, L) ne 0 then
            param_equation_mismatch +:= 1;
        end if;
        for K in Roots2(L) do
            param_rows +:= 1;
            Include(~param_keys, Key(K, A));
        end for;
    end for;
end for;

base_count := #base_keys;
param_count := #param_keys;
missing_count := #(base_keys diff param_keys);
extra_count := #(param_keys diff base_keys);

if base_count eq 607 and param_count eq 604 and missing_count eq 3
        and extra_count eq 0 and param_rows eq 1208
        and base_equation_mismatch eq 0 and param_equation_mismatch eq 0
        and disc_factor_mismatch eq 0 then
    print "RESULT p27_ka_base_q607 ok", base_count, param_count,
        missing_count, extra_count, param_rows, base_equation_mismatch,
        param_equation_mismatch, disc_factor_mismatch;
else
    print "RESULT p27_ka_base_q607 mismatch", base_count, param_count,
        missing_count, extra_count, param_rows, base_equation_mismatch,
        param_equation_mismatch, disc_factor_mismatch, param_denominator_skip;
end if;
