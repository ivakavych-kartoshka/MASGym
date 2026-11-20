"""Report where the main paper's body ends (the AAMAS 8-page test).

The body limit applies to everything before the bibliography. This script finds
the first page whose text begins the References section and reports it, so
"body pages" = that page number - 1 (References may start mid-page, in which
case the body has already been counted on it).

Usage:  python -X utf8 pagecheck.py [main.pdf]
"""
from __future__ import annotations

import re
import sys

import PyPDF2


def body_pages(pdf: str) -> tuple[int, int]:
    reader = PyPDF2.PdfReader(pdf)
    total = len(reader.pages)
    refs_page = None
    for i, page in enumerate(reader.pages):
        text = (page.extract_text() or "").replace("\n", " ")
        # the bibliography heading is alone on its line(s); match it at a
        # word boundary near the start of a page's text run
        if re.search(r"(^|\s)References(\s|$)", text[:400]):
            refs_page = i + 1
            break
    return total, (refs_page or total)


def main() -> int:
    pdf = sys.argv[1] if len(sys.argv) > 1 else "main.pdf"
    total, refs_page = body_pages(pdf)
    print(f"{pdf}: {total} pages total")
    print(f"  References start on page : {refs_page}")
    print(f"  body content pages       : {refs_page - 1} (plus part of page {refs_page})")
    print(f"  reference pages          : {total - refs_page + 1}")
    print("  AAMAS main-track limit   : 8 body pages ->",
          "OK" if refs_page - 1 <= 8 else "OVER LIMIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
