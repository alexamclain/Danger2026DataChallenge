# P27 B-Line CompactD/Beta/Dnext Squareclass

Date: 2026-06-22

## Claim

The `compactD_R` layer is now CAS-confirmed as a twinned layer after the
reduced `U_next` cover, not merely finite-row-count evidence.

In the function field with

```text
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
Z + 1/Z = U
beta = Z - 1/Z
d_next = Z*(U + A)
```

Magma verifies that

```text
compactD_R_rhs / (beta^2 * d_next)
```

is a square over both `GF(7)` and `GF(23)`.

This means that, after adjoining the first-half `beta` branch and the reduced
`d_next` square root, `compactD_R` adds no fresh Kummer class in these
function-field smokes.

## Artifacts

Magma fixture:

```text
research/p27/archive/fixtures/p27_b_line_compact_beta_dnext_square_q7_q23_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_compact_beta_dnext_square_q7_q23_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_compact_beta_dnext_square_q7_q23_magma_20260622.txt
```

Endpoint:

```text
https://magma.maths.usyd.edu.au/xml/calculator.xml
```

The calculator reported `Magma V2.29-8`.

## Command Shape

```bash
python3 - <<'PY'
from pathlib import Path
from urllib.parse import urlencode
from http import client as httplib
from xml.dom.minidom import parseString

fixture = Path("research/p27/archive/fixtures/p27_b_line_compact_beta_dnext_square_q7_q23_magma.m")
server = "magma.maths.usyd.edu.au"
params = urlencode({"input": fixture.read_text()})
headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "Accept: text/html, application/xml, application/xhtml+xml",
    "Referer": f"http://{server}/calc/",
}
conn = httplib.HTTPConnection(server, timeout=120)
conn.request("POST", "/xml/calculator.xml", params, headers)
raw = conn.getresponse().read()
Path("research/p27/archive/probe_outputs/p27_b_line_compact_beta_dnext_square_q7_q23_magma_20260622.xml").write_bytes(raw)
PY
```

## Result

```text
magma_version = 2.29-8
magma_time = 31.239
magma_memory = 32.09MB
P27_COMPACT_BETA_DNEXT_Q 7 true
P27_COMPACT_BETA_DNEXT_ROOT_CHECK_Q 7 true
P27_COMPACT_BETA_DNEXT_Q 23 true
P27_COMPACT_BETA_DNEXT_ROOT_CHECK_Q 23 true
RESULT p27_b_line_compact_beta_dnext_square_q7_q23 done
```

## Interpretation

Positive:

```text
The finite-field row-count identity has become a function-field square check.
compactD_R should be treated as beta*d_next times a square on the staged cover.
The no-R reduced cover is the correct first normalization target.
```

Negative:

```text
This is not yet a characteristic-zero proof or p27-prime-field Magma proof.
It does not compute genus, components, branch divisors, or a source map.
It gives no standalone GPU production mode.
```

## Continue / Kill

```text
continue = normalize the no-R reduced cover first
continue = extract f3 and then gamma/f4 as the next real Kummer class
continue = lift this square witness to characteristic 0 or p27 if CAS permits

kill = treating compactD_R as an independent first normalization layer
kill = GPU compactD_R bucket/filter work after reduced_U
kill = full-cover-first saturation strategy for the B-line CAS pass
```

```text
p27_b_line_compact_beta_dnext_squareclass_rows=1/1
```
