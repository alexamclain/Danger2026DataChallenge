#!/usr/bin/env python3
"""KL inversion-pair decomposition for the p25 KSY packet.

The primitive-D crosswalk identifies the source packet as

    z^121 * (1 + z + z^2) * (1 - z^263).

This gate asks which subpackets of the six target cells already satisfy the
elementary Kubert-Lang exponent congruences.  The answer is exact: the legal
subpackets are precisely the nonempty unions of the three inversion pairs
z^a - z^-a.  The actual T-edge product is therefore not decomposed into three
legal T edges; the KL screen sees the anti-invariant pairing.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from p25_laneB_robert_ksy_theta2_kubert_lang_crt_coupling_gate import q_from_coord
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    C_ORDER,
    QUOTIENT_LEVEL,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    add_quotient,
    kl_profile,
    scale_quotient,
    source_packet,
)


Coord = tuple[int, int]
PacketTuple = tuple[tuple[Coord, int], ...]


@dataclass(frozen=True)
class InversionPair:
    positive_coord: Coord
    positive_primitive: int
    negative_coord: Coord
    negative_primitive: int
    primitive_sum: int
    packet: PacketTuple
    kl_congruence_ok: bool
    is_actual_t_edge: bool


@dataclass(frozen=True)
class LegalSubpacket:
    packet: PacketTuple
    primitive_support: tuple[tuple[int, int], ...]
    support: int
    pair_indices: tuple[int, ...]


@dataclass(frozen=True)
class TEdgeProfile:
    index: int
    positive_coord: Coord
    positive_primitive: int
    negative_coord: Coord
    negative_primitive: int
    primitive_difference: int
    primitive_sum: int
    kl_congruence_ok: bool


@dataclass(frozen=True)
class KLInversionPairProfile:
    d_q_step: int
    d_q_inverse: int
    target_primitive_support: tuple[tuple[int, int, Coord], ...]
    inversion_pairs: tuple[InversionPair, ...]
    legal_subpackets: tuple[LegalSubpacket, ...]
    t_edge_profiles: tuple[TEdgeProfile, ...]
    legal_subpacket_count: int
    nonempty_inversion_unions: int
    t_edges_legal_count: int
    inversion_pairs_are_exact_legal_atoms: bool
    t_edge_decomposition_is_not_kl_legal: bool
    full_packet_is_all_inversion_pairs: bool
    next_debt: str
    row_ok: bool


def packet_tuple(ring: Ring) -> PacketTuple:
    return tuple(sorted(ring.items()))


def primitive_exponent(coord: Coord, d_q_inverse: int) -> int:
    return (q_from_coord(coord) * d_q_inverse) % QUOTIENT_LEVEL


def primitive_support(packet: Ring, d_q_inverse: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            (primitive_exponent(coord, d_q_inverse), coefficient)
            for coord, coefficient in packet.items()
        )
    )


def kl_ok(packet: Ring) -> bool:
    return kl_profile(
        "subpacket",
        packet,
        QUOTIENT_LEVEL,
        C_ORDER,
        QUOTIENT_RIGHT_ORDER,
        preserves_right_data=True,
        preserves_t_edge=True,
        p25_finite_payload_ok=True,
        recommendation="subpacket screen",
    ).quadratic_relations_ok


def packet_union(packets: tuple[PacketTuple, ...]) -> PacketTuple:
    out: Ring = {}
    for packet in packets:
        for coord, coefficient in packet:
            out[coord] = out.get(coord, 0) + coefficient
            if out[coord] == 0:
                del out[coord]
    return packet_tuple(out)


def actual_t_edge_packet(index: int) -> PacketTuple:
    base = (1, 25)
    d_step = (1, 3)
    t_step = (2, 113)
    positive = add_quotient(base, scale_quotient(d_step, index))
    negative = add_quotient(positive, t_step)
    return packet_tuple({positive: 1, negative: -1})


def profile_inversion_pairs() -> KLInversionPairProfile:
    target = source_packet()
    d_q_step = q_from_coord((1, 3))
    d_q_inverse = pow(d_q_step, -1, QUOTIENT_LEVEL)
    target_primitive_support = tuple(
        sorted(
            (
                primitive_exponent(coord, d_q_inverse),
                coefficient,
                coord,
            )
            for coord, coefficient in target.items()
        )
    )
    positives = sorted(
        (primitive_exponent(coord, d_q_inverse), coord)
        for coord, coefficient in target.items()
        if coefficient > 0
    )
    negatives_by_primitive = {
        primitive_exponent(coord, d_q_inverse): coord
        for coord, coefficient in target.items()
        if coefficient < 0
    }
    t_edges = tuple(actual_t_edge_packet(index) for index in range(3))
    inversion_pairs: list[InversionPair] = []
    for positive_primitive, positive_coord in positives:
        negative_primitive = (-positive_primitive) % QUOTIENT_LEVEL
        negative_coord = negatives_by_primitive[negative_primitive]
        pair_packet = packet_tuple({positive_coord: 1, negative_coord: -1})
        inversion_pairs.append(
            InversionPair(
                positive_coord=positive_coord,
                positive_primitive=positive_primitive,
                negative_coord=negative_coord,
                negative_primitive=negative_primitive,
                primitive_sum=(positive_primitive + negative_primitive) % QUOTIENT_LEVEL,
                packet=pair_packet,
                kl_congruence_ok=kl_ok(dict(pair_packet)),
                is_actual_t_edge=pair_packet in t_edges,
            )
        )

    legal_subpackets: list[LegalSubpacket] = []
    target_items = tuple(target.items())
    pair_packets = tuple(pair.packet for pair in inversion_pairs)
    expected_legal = set()
    expected_pair_indices: dict[PacketTuple, tuple[int, ...]] = {}
    for size in range(1, len(pair_packets) + 1):
        for indices in combinations(range(len(pair_packets)), size):
            union = packet_union(tuple(pair_packets[index] for index in indices))
            expected_legal.add(union)
            expected_pair_indices[union] = indices

    observed_legal = set()
    for mask in range(1, 1 << len(target_items)):
        subpacket = {
            coord: coefficient
            for item_index, (coord, coefficient) in enumerate(target_items)
            if mask & (1 << item_index)
        }
        if not kl_ok(subpacket):
            continue
        packet = packet_tuple(subpacket)
        observed_legal.add(packet)
        legal_subpackets.append(
            LegalSubpacket(
                packet=packet,
                primitive_support=primitive_support(subpacket, d_q_inverse),
                support=len(packet),
                pair_indices=expected_pair_indices.get(packet, ()),
            )
        )

    t_edge_profiles = tuple(
        TEdgeProfile(
            index=index,
            positive_coord=edge[0][0] if edge[0][1] > 0 else edge[1][0],
            positive_primitive=primitive_exponent(
                edge[0][0] if edge[0][1] > 0 else edge[1][0],
                d_q_inverse,
            ),
            negative_coord=edge[0][0] if edge[0][1] < 0 else edge[1][0],
            negative_primitive=primitive_exponent(
                edge[0][0] if edge[0][1] < 0 else edge[1][0],
                d_q_inverse,
            ),
            primitive_difference=(
                primitive_exponent(
                    edge[0][0] if edge[0][1] < 0 else edge[1][0],
                    d_q_inverse,
                )
                - primitive_exponent(
                    edge[0][0] if edge[0][1] > 0 else edge[1][0],
                    d_q_inverse,
                )
            )
            % QUOTIENT_LEVEL,
            primitive_sum=(
                primitive_exponent(
                    edge[0][0] if edge[0][1] < 0 else edge[1][0],
                    d_q_inverse,
                )
                + primitive_exponent(
                    edge[0][0] if edge[0][1] > 0 else edge[1][0],
                    d_q_inverse,
                )
            )
            % QUOTIENT_LEVEL,
            kl_congruence_ok=kl_ok(dict(edge)),
        )
        for index, edge in enumerate(t_edges)
    )
    full_packet = packet_tuple(target)
    inversion_pairs_are_exact_legal_atoms = (
        observed_legal == expected_legal
        and all(pair.kl_congruence_ok for pair in inversion_pairs)
        and all(subpacket.pair_indices for subpacket in legal_subpackets)
    )
    t_edge_decomposition_is_not_kl_legal = (
        tuple(edge.kl_congruence_ok for edge in t_edge_profiles)
        == (False, True, False)
        and sum(edge.kl_congruence_ok for edge in t_edge_profiles) == 1
    )
    full_packet_is_all_inversion_pairs = packet_union(pair_packets) == full_packet
    row_ok = (
        d_q_step == 178
        and d_q_inverse == 94
        and target_primitive_support
        == (
            (121, 1, (1, 25)),
            (122, 1, (2, 28)),
            (123, 1, (0, 31)),
            (384, -1, (0, 138)),
            (385, -1, (1, 141)),
            (386, -1, (2, 144)),
        )
        and tuple(pair.primitive_sum for pair in inversion_pairs) == (0, 0, 0)
        and tuple(pair.is_actual_t_edge for pair in inversion_pairs) == (False, True, False)
        and len(observed_legal) == 7
        and len(expected_legal) == 7
        and inversion_pairs_are_exact_legal_atoms
        and t_edge_decomposition_is_not_kl_legal
        and full_packet_is_all_inversion_pairs
    )
    return KLInversionPairProfile(
        d_q_step=d_q_step,
        d_q_inverse=d_q_inverse,
        target_primitive_support=target_primitive_support,
        inversion_pairs=tuple(inversion_pairs),
        legal_subpackets=tuple(sorted(legal_subpackets, key=lambda row: row.primitive_support)),
        t_edge_profiles=t_edge_profiles,
        legal_subpacket_count=len(observed_legal),
        nonempty_inversion_unions=len(expected_legal),
        t_edges_legal_count=sum(edge.kl_congruence_ok for edge in t_edge_profiles),
        inversion_pairs_are_exact_legal_atoms=inversion_pairs_are_exact_legal_atoms,
        t_edge_decomposition_is_not_kl_legal=t_edge_decomposition_is_not_kl_legal,
        full_packet_is_all_inversion_pairs=full_packet_is_all_inversion_pairs,
        next_debt=(
            "try theorem sources that produce the three anti-invariant "
            "Siegel/Robert pairs z^a-z^-a and then identify their sum with "
            "the KSY T-edge product and period-156 theta2 payload"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang inversion-pair gate")
    profile = profile_inversion_pairs()
    print(f"inversion_pair_profile={profile}")
    print("target_primitive_support")
    print(f"  {profile.target_primitive_support}")
    print("inversion_pairs")
    for pair in profile.inversion_pairs:
        print(f"  {pair}")
    print("actual_T_edges")
    for edge in profile.t_edge_profiles:
        print(f"  {edge}")
    print("legal_subpackets")
    for row in profile.legal_subpackets:
        print(f"  support={row.support} pairs={row.pair_indices} primitive={row.primitive_support}")
    print("inversion_pair_laws")
    print("  KL_legal_target_subpackets_are_exactly_nonempty_unions_of_three_inversion_pairs=1")
    print("  full_packet_is_the_union_of_those_three_inversion_pairs=1")
    print("  only_the_middle_actual_T_edge_is_KL_legal_by_itself=1")
    print("  KL_screen_sees_anti_invariant_pairs_not_three_independent_T_edges=1")
    print("interpretation")
    print("  theorem_search_can_target_three_z_a_minus_z_minus_a_units_plus_KSY_identification=1")
    print("  a_T_edge_factorization_alone_is_not_the_KL_modular_unit_explanation=1")
    print(f"robert_ksy_theta2_kubert_lang_inversion_pair_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_inversion_pair_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
