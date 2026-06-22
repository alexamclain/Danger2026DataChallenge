// P27 label-2 alpha projective quotient smoke.
//
// This homogenizes the eliminated cyclic-quartic model and the explicit
// alpha_R rational map, then asks Magma for the quotient by the resulting
// projective order-4 automorphism.  q=7 is intentionally tiny: this is a
// CAS-interface smoke, not a guard-field theorem check.

SetColumns(0);
q := 7;
F := GF(q);
P3<X,W,R,Z> := ProjectiveSpace(F,3);

T2h := X*(X^2 + Z^2)*(X^2 + 2*X*Z - Z^2);
mth := (X + Z)*(2*W*X*Z + X^3 + X^2*Z - X*Z^2 - Z^3);
m0h := (X^2 + Z^2)*(X^2 + 2*X*Z - Z^2)*(W*X + W*Z + 2*X^2);
Sh := W*(X + Z) + 2*X^2;
Ph := W*(X^2 + Z^2);

eqE := W^2*Z - X^3 + X*Z^2;
eqQ := X^2*R^4*Z^9
    - 2*X*W*(X^2 + Z^2)*m0h*R^2*Z^3
    + 4*W^2*(X^2 + Z^2)^2*T2h*Sh^2;

PCraw := Curve(P3, [eqE, eqQ]);
RC := ReducedSubscheme(PCraw);
comps := IrreducibleComponents(RC);
print "PROJ_COMPS", #comps;
for i in [1..#comps] do
    print "PROJ_COMP", i, Dimension(comps[i]), Degree(comps[i]), #Points(comps[i]);
end for;

main_idx := 1;
for i in [1..#comps] do
    if Degree(comps[i]) gt Degree(comps[main_idx]) then
        main_idx := i;
    end if;
end for;
print "MAIN_IDX", main_idx;

C := Curve(comps[main_idx]);
print "MAIN_GENUS", Genus(C), #Points(C);

P2<Xe,We,Ze> := ProjectiveSpace(F,2);
E := Curve(P2, We^2*Ze - Xe^3 + Xe*Ze^2);
piE := map< C -> E | [X, W, Z] >;
print "E_PROJECTION_OK", Genus(E), #Points(E), Domain(piE) eq C,
    Codomain(piE) eq E;

try
    print "E_PROJECTION_DEGREE", Degree(piE);
catch e
    print "E_PROJECTION_DEGREE_ERROR";
    print e`Object;
end try;

try
    Rdiv := RamificationDivisor(piE);
    print "RAMIFICATION_OK", Degree(Rdiv);
catch e
    print "RAMIFICATION_ERROR";
    print e`Object;
end try;

N := R*mth*(2*Ph*m0h - X*R^2*Z^6);
D := 2*Sh*(X*R^2*Z^6 - Ph*m0h);

phi_coords := [
    X*D*Z^3,
    W*D*Z^3,
    N*Z,
    D*Z^4
];
psi_coords := [
    X*D*Z^3,
    W*D*Z^3,
    -N*Z,
    D*Z^4
];

try
    aut := iso< C -> C | phi_coords, psi_coords >;
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

print "RESULT p27_label2_alpha_projective_quotient_q7 done";
