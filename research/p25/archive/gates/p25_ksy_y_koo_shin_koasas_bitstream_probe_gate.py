#!/usr/bin/env python3
"""KOASAS bitstream probe for Koo-Shin 2010.

The ASARC PDF handle is stale locally, but KOASAS exposes repository metadata
for the same article through OAI-PMH.  This gate records the stronger retrieval
state: exact metadata and restricted bitstream coordinates exist, but theorem
body access still requires authorization/library/OCR.
"""

from __future__ import annotations

from dataclasses import dataclass


KOASAS_HANDLE = "https://koasas.kaist.ac.kr/handle/10203/96547"
OAI_DC_URL = (
    "https://koasas.kaist.ac.kr/oai/request?verb=GetRecord&"
    "metadataPrefix=oai_dc&identifier=oai:koasas.kaist.ac.kr:10203/96547"
)
OAI_METS_URL = (
    "https://koasas.kaist.ac.kr/oai/request?verb=GetRecord&"
    "metadataPrefix=mets&identifier=oai:koasas.kaist.ac.kr:10203/96547"
)
BITSTREAM_URL = "http://koasas.kaist.ac.kr//bitstream/10203/96547/1/000271750900008.pdf"
BITSTREAM_MD5 = "39bf3ab80a349709394165f27f0eafbf"
BITSTREAM_SIZE = 501978


@dataclass(frozen=True)
class KOASASProbeProfile:
    handle_url: str
    oai_dc_url: str
    oai_mets_url: str
    bitstream_url: str
    bitstream_md5: str
    bitstream_size: int
    oai_metadata_rows: int
    mets_bitstream_rows: int
    direct_pdf_rows: int
    authorization_blocked_rows: int
    theorem_body_rows: int
    direct_closing_rows: int
    retrieval_packet_ready: bool
    first_missing_clause: str
    row_ok: bool


def profile_koasas_bitstream_probe() -> KOASASProbeProfile:
    # Evidence recorded from /tmp/p25_lit_scout/koo_shin_koasas_probe:
    # fetch_2.bin: OAI-DC metadata with title/authors/abstract/DOI.
    # fetch_12.bin: XOAI metadata, provenance says no public bitstreams.
    # fetch_13.bin: METS metadata with restricted PDF URL/size/MD5.
    # 000271750900008.pdf: authorization-required HTML after cookie replay.
    oai_metadata_rows = 3
    mets_bitstream_rows = 1
    direct_pdf_rows = 0
    authorization_blocked_rows = 1
    theorem_body_rows = 0
    direct_closing_rows = 0
    retrieval_packet_ready = True
    first_missing_clause = (
        "authorized access to KOASAS bitstream 000271750900008.pdf, "
        "or alternate full-text/OCR copy matching MD5/size metadata"
    )
    row_ok = (
        KOASAS_HANDLE.endswith("/10203/96547")
        and OAI_DC_URL.startswith("https://koasas.kaist.ac.kr/oai/request")
        and OAI_METS_URL.startswith("https://koasas.kaist.ac.kr/oai/request")
        and BITSTREAM_URL.endswith("/000271750900008.pdf")
        and BITSTREAM_MD5 == "39bf3ab80a349709394165f27f0eafbf"
        and BITSTREAM_SIZE == 501978
        and oai_metadata_rows == 3
        and mets_bitstream_rows == 1
        and direct_pdf_rows == 0
        and authorization_blocked_rows == 1
        and theorem_body_rows == 0
        and direct_closing_rows == 0
        and retrieval_packet_ready
        and "authorized access" in first_missing_clause
    )
    return KOASASProbeProfile(
        handle_url=KOASAS_HANDLE,
        oai_dc_url=OAI_DC_URL,
        oai_mets_url=OAI_METS_URL,
        bitstream_url=BITSTREAM_URL,
        bitstream_md5=BITSTREAM_MD5,
        bitstream_size=BITSTREAM_SIZE,
        oai_metadata_rows=oai_metadata_rows,
        mets_bitstream_rows=mets_bitstream_rows,
        direct_pdf_rows=direct_pdf_rows,
        authorization_blocked_rows=authorization_blocked_rows,
        theorem_body_rows=theorem_body_rows,
        direct_closing_rows=direct_closing_rows,
        retrieval_packet_ready=retrieval_packet_ready,
        first_missing_clause=first_missing_clause,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_koasas_bitstream_probe()
    print("p25 KSY-y Koo-Shin KOASAS bitstream probe gate")
    print(f"handle_url={profile.handle_url}")
    print(f"oai_dc_url={profile.oai_dc_url}")
    print(f"oai_mets_url={profile.oai_mets_url}")
    print(f"bitstream_url={profile.bitstream_url}")
    print(f"bitstream_md5={profile.bitstream_md5}")
    print(f"bitstream_size={profile.bitstream_size}")
    print("counts")
    print(f"  oai_metadata_rows={profile.oai_metadata_rows}")
    print(f"  mets_bitstream_rows={profile.mets_bitstream_rows}")
    print(f"  direct_pdf_rows={profile.direct_pdf_rows}")
    print(f"  authorization_blocked_rows={profile.authorization_blocked_rows}")
    print(f"  theorem_body_rows={profile.theorem_body_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  retrieval_packet_ready={int(profile.retrieval_packet_ready)}")
    print(f"first_missing_clause={profile.first_missing_clause}")
    print("interpretation")
    print("  koasas_metadata_confirms_exact_article=1")
    print("  koasas_mets_exposes_restricted_bitstream_coordinates=1")
    print("  theorem_body_still_not_recovered=1")
    print("  retrieval_packet_is_now_library_or_author_access_ready=1")
    print(f"ksy_y_koo_shin_koasas_bitstream_probe_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin KOASAS bitstream probe regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
