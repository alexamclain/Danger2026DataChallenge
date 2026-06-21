// P27 trace/norm quotient: small online Magma validation probe.
//
// This checks the exact finite-field shadow of the domain-line bit in the
// p27 trace/norm quotient.  The p27-compatible small field is q = 607
// (q mod 8 = 7), so chi(-1) = -1 and chi(2) = +1 as for p27.
//
// Expected output:
//
// RESULT p27_trace_norm_spin_q607 ok true 1 604 0 3

SetColumns(0);
q := 607;
Fq := GF(q);

P<t> := PolynomialRing(Fq);
Fpoly := t*(t^2 + 2*t - 1)*(t^2 + 1);
Ram := t^2 + 1;

function PolyVal(f, g)
    c := 0;
    while f mod g eq 0 do
        f := f div g;
        c +:= 1;
    end while;
    return c;
end function;

K<u> := FunctionField(Fq);
Ffun := u*(u^2 + 2*u - 1)*(u^2 + 1);
s := -1/u;
Fsigma := s*(s^2 + 2*s - 1)*(s^2 + 1);
ratio_ok := Ffun/Fsigma eq u^6;
ram_val := PolyVal(Fpoly, Ram);

function Leg(a)
    if a eq 0 then
        return 0;
    elif IsSquare(a) then
        return 1;
    else
        return -1;
    end if;
end function;

function Fval(tt)
    return tt*(tt^2 + 2*tt - 1)*(tt^2 + 1);
end function;

rows := 0;
mismatch := 0;
zeros := 0;
for tt in Fq do
    if tt eq 0 then
        zeros +:= 1;
        continue;
    end if;
    ss := -1/tt;
    fv := Fval(tt);
    fsv := Fval(ss);
    if fv eq 0 or fsv eq 0 then
        zeros +:= 1;
        continue;
    end if;
    rows +:= 1;
    if Leg(fv) ne Leg(fsv) then
        mismatch +:= 1;
    end if;
end for;

if ratio_ok and ram_val eq 1 and rows eq 604 and mismatch eq 0 and zeros eq 3 then
    print "RESULT p27_trace_norm_spin_q607 ok", ratio_ok, ram_val, rows, mismatch, zeros;
else
    print "RESULT p27_trace_norm_spin_q607 mismatch", ratio_ok, ram_val, rows, mismatch, zeros;
end if;
