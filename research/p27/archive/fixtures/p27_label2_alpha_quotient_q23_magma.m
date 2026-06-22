// P27 label-2 alpha quotient smoke over a p27-signature small field.
//
// q=23 is 7 mod 16, matching the p27 2-adic sign regime while keeping the
// online Magma quotient attempt small.  This is a CAS-interface fixture: the
// alpha map has already been validated by enumeration over q=1607/1847/2087.
// Here we ask whether Magma can build an isomorphism/automorphism group and
// compute CurveQuotient directly from the explicit rational map.

SetColumns(0);
q := 23;
F := GF(q);
A3<X,W,R> := AffineSpace(F,3);

T2 := X*(X^2 + 1)*(X^2 + 2*X - 1);
mt := (X + 1)*(2*W*X + X^3 + X^2 - X - 1);
m0 := (X^2 + 1)*(X^2 + 2*X - 1)*(W*X + W + 2*X^2);
Salpha := W*(X + 1) + 2*X^2;
pref := W*(X^2 + 1)/X;

eqE := W^2 - (X^3 - X);
eqQ := R^4 - 2*pref*m0*R^2 + 4*pref^2*T2*Salpha^2;
C := Curve(A3, [eqE, Numerator(eqQ)]);

alphaR := R*mt*(2*pref*m0 - R^2)/(2*Salpha*(R^2 - pref*m0));

phi := map< C -> C | [X, W, alphaR] >;
psi := map< C -> C | [X, W, -alphaR] >;
print "MAP_OK", Domain(phi) eq C, Codomain(phi) eq C, Domain(psi) eq C,
    Codomain(psi) eq C;

try
    aut := iso< C -> C | [X, W, alphaR], [X, W, -alphaR] >;
    print "ISO_OK", true;

    try
        G := AutomorphismGroup(C, [aut]);
        print "AUT_GROUP_OK", #G;

        try
            CG, prj := CurveQuotient(G);
            print "QUOTIENT_OK", Genus(CG), #Points(CG);
        catch e
            print "QUOTIENT_ERROR";
            print e`Object;
        end try;
    catch e
        print "AUT_GROUP_ERROR";
        print e`Object;
    end try;
catch e
    print "ISO_ERROR";
    print e`Object;
end try;

print "RESULT p27_label2_alpha_quotient_q23 done";
