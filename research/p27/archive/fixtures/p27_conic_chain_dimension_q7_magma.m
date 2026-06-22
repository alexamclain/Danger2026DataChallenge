// P27 conic-chain dimension smoke, q7.

SetColumns(0);
q := 7;
F := GF(q);

A5<C,R,H,G,N> := AffineSpace(F, 5);
P := CoordinateRing(A5);
e1 := H^2 - (R^2 + C*R + 1);
e2 := G^2 - (R^2 - C*R + 1);
e3 := N^2 - (H + G)*N + 1;
I := ideal<P | e1, e2, e3>;
S := Scheme(A5, I);
print "CONIC_CHAIN_DEPTH1", Dimension(S), #Basis(I), #Points(S);

A8<C2,R20,H20,G20,R21,H21,G21,R22> := AffineSpace(F, 8);
P2 := CoordinateRing(A8);
f1 := H20^2 - (R20^2 + C2*R20 + 1);
f2 := G20^2 - (R20^2 - C2*R20 + 1);
f3 := R21^2 - (H20 + G20)*R21 + 1;
f4 := H21^2 - (R21^2 + C2*R21 + 1);
f5 := G21^2 - (R21^2 - C2*R21 + 1);
f6 := R22^2 - (H21 + G21)*R22 + 1;
I2 := ideal<P2 | f1, f2, f3, f4, f5, f6>;
S2 := Scheme(A8, I2);
print "CONIC_CHAIN_DEPTH2", Dimension(S2), #Basis(I2), #Points(S2);

A11<C3,R30,H30,G30,R31,H31,G31,R32,H32,G32,R33> := AffineSpace(F, 11);
P3 := CoordinateRing(A11);
k1 := H30^2 - (R30^2 + C3*R30 + 1);
k2 := G30^2 - (R30^2 - C3*R30 + 1);
k3 := R31^2 - (H30 + G30)*R31 + 1;
k4 := H31^2 - (R31^2 + C3*R31 + 1);
k5 := G31^2 - (R31^2 - C3*R31 + 1);
k6 := R32^2 - (H31 + G31)*R32 + 1;
k7 := H32^2 - (R32^2 + C3*R32 + 1);
k8 := G32^2 - (R32^2 - C3*R32 + 1);
k9 := R33^2 - (H32 + G32)*R33 + 1;
I3 := ideal<P3 | k1, k2, k3, k4, k5, k6, k7, k8, k9>;
S3 := Scheme(A11, I3);
print "CONIC_CHAIN_DEPTH3", Dimension(S3), #Basis(I3), #Points(S3);

print "RESULT p27_conic_chain_dimension_q7 done";
