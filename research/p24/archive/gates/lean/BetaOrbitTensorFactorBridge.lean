/-!
Finite gate for the beta-orbit / tensor-factor bridge.

The arithmetic accounting is:

  560 nonzero E-Frobenius beta orbits
    = 8 F_p H-packets * 70 E-tensor factors per packet.

This file does not prove the finite-field order calculation.  It records the
certificate logic that follows after that indexing is fixed: factorwise
nonvanishing in the scalar-extension factors implies every beta orbit is good,
and therefore the selected beta orbit is good.
-/

namespace P24.BetaOrbitTensorFactorBridge

abbrev HPacketCount : Nat := 8
abbrev TensorFactorCount : Nat := 70
abbrev NonzeroBetaOrbitCount : Nat := 560

example : NonzeroBetaOrbitCount = HPacketCount * TensorFactorCount := by
  decide

def FactorwiseCertificate {Packet Factor : Type}
    (FactorGood : Packet → Factor → Prop) : Prop :=
  ∀ packet factor, FactorGood packet factor

def PacketProductCertificate {Packet : Type}
    (PacketGood : Packet → Prop) : Prop :=
  ∀ packet, PacketGood packet

def BetaOrbitCovered {BetaOrbit Packet Factor : Type}
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood : BetaOrbit → Prop) : Prop :=
  ∀ beta, FactorGood (packetOf beta) (factorOf beta) → BetaGood beta

theorem all_beta_orbits_from_factorwise_certificate
    {BetaOrbit Packet Factor : Type}
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood : BetaOrbit → Prop)
    (h_covered :
      BetaOrbitCovered packetOf factorOf FactorGood BetaGood)
    (h_factors : FactorwiseCertificate FactorGood) :
    ∀ beta, BetaGood beta := by
  intro beta
  exact h_covered beta (h_factors (packetOf beta) (factorOf beta))

theorem selected_beta_from_factorwise_certificate
    {BetaOrbit Packet Factor : Type}
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood : BetaOrbit → Prop)
    (selected : BetaOrbit)
    (h_covered :
      BetaOrbitCovered packetOf factorOf FactorGood BetaGood)
    (h_factors : FactorwiseCertificate FactorGood) :
    BetaGood selected := by
  exact all_beta_orbits_from_factorwise_certificate
    packetOf factorOf FactorGood BetaGood h_covered h_factors selected

theorem factorwise_from_packet_products
    {Packet Factor : Type}
    (PacketGood : Packet → Prop)
    (FactorGood : Packet → Factor → Prop)
    (h_packet_to_factors :
      ∀ packet, PacketGood packet → ∀ factor, FactorGood packet factor)
    (h_packets : PacketProductCertificate PacketGood) :
    FactorwiseCertificate FactorGood := by
  intro packet factor
  exact h_packet_to_factors packet (h_packets packet) factor

theorem selected_beta_from_packet_products
    {BetaOrbit Packet Factor : Type}
    (packetOf : BetaOrbit → Packet)
    (factorOf : BetaOrbit → Factor)
    (PacketGood : Packet → Prop)
    (FactorGood : Packet → Factor → Prop)
    (BetaGood : BetaOrbit → Prop)
    (selected : BetaOrbit)
    (h_packet_to_factors :
      ∀ packet, PacketGood packet → ∀ factor, FactorGood packet factor)
    (h_covered :
      BetaOrbitCovered packetOf factorOf FactorGood BetaGood)
    (h_packets : PacketProductCertificate PacketGood) :
    BetaGood selected := by
  apply selected_beta_from_factorwise_certificate
    packetOf factorOf FactorGood BetaGood selected h_covered
  exact factorwise_from_packet_products
    PacketGood FactorGood h_packet_to_factors h_packets

end P24.BetaOrbitTensorFactorBridge
