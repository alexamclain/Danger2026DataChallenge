# P25 KSY-y Koo-Shin KOASAS Bitstream Probe

Updated: 2026-06-13 22:18 PDT

## Purpose

The ASARC PDF handle for Koo-Shin 2010 is stale from this machine.  KOASAS,
KAIST's repository, exposes a stronger handle for the same article through
OAI-PMH.  This note records the exact metadata and restricted bitstream
coordinates so a future library/subagent/human pass can target the right file.

## Verified Metadata

```text
KOASAS handle = https://koasas.kaist.ac.kr/handle/10203/96547
OAI-DC = https://koasas.kaist.ac.kr/oai/request?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:koasas.kaist.ac.kr:10203/96547
METS = https://koasas.kaist.ac.kr/oai/request?verb=GetRecord&metadataPrefix=mets&identifier=oai:koasas.kaist.ac.kr:10203/96547
title = On some arithmetic properties of Siegel functions
authors = Ja-Kyung Koo; Dong-Hwa Shin
journal = Mathematische Zeitschrift 264(1), 137-177
DOI = 10.1007/s00209-008-0456-9
```

Local evidence:

```text
/tmp/p25_lit_scout/koo_shin_koasas_probe/fetch_2.bin   OAI-DC metadata
/tmp/p25_lit_scout/koo_shin_koasas_probe/fetch_12.bin  XOAI metadata
/tmp/p25_lit_scout/koo_shin_koasas_probe/fetch_13.bin  METS metadata
```

## Restricted Bitstream

METS exposes the original bitstream:

```text
url = http://koasas.kaist.ac.kr//bitstream/10203/96547/1/000271750900008.pdf
originalName = 000271750900008.pdf
size = 501978
md5 = 39bf3ab80a349709394165f27f0eafbf
mime = application/pdf
```

Direct access state:

```text
normal handle page = JavaScript challenge
OAI endpoints = accessible
exact bitstream + challenge cookie = redirects to /password-login
result = Authorization Required HTML, not PDF
alternate /bitstream/handle/... shape = invalid bitstream
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_koasas_bitstream_probe_gate.py
```

```text
oai_metadata_rows          = 3
mets_bitstream_rows        = 1
direct_pdf_rows            = 0
authorization_blocked_rows = 1
theorem_body_rows          = 0
direct_closing_rows        = 0
retrieval_packet_ready     = 1
```

Marker:

```text
ksy_y_koo_shin_koasas_bitstream_probe_rows=1/1
```

## Verdict

The Koo-Shin retrieval target is now exact rather than fuzzy: the desired file
is KOASAS bitstream `000271750900008.pdf` with MD5
`39bf3ab80a349709394165f27f0eafbf` and size `501978`.  The theorem body is
still not recovered.  The next retrieval action is authorized KOASAS/KAIST
library access, author copy, Springer access, or an alternate mirror matching
the METS file metadata.
