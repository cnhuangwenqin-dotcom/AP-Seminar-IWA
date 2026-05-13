#!/usr/bin/env python3
"""Lightweight helper for AP Seminar IWA citation audits.

This script extracts likely parenthetical in-text citations and bibliography
entries from a plain-text essay. It is intentionally conservative and does not
replace human judgment.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

BIB_HEADINGS = [
    "works cited",
    "references",
    "bibliography",
    "works consulted",
    "citation table",
]

CITATION_RE = re.compile(r"\(([^()]{2,90}?(?:\d{4}|\d+|et al\.|&|and|,)[^()]{0,40})\)")
QUOTE_RE = re.compile(r"[\"“”].{12,}?[\"“”]")


def normalize_label(text: str) -> str:
    text = text.strip().strip(".,;:")
    text = re.sub(r"\b(pp?\.?|p\.?|para\.?|ch\.?|sec\.?)\b", " ", text, flags=re.I)
    text = re.sub(r"\b\d{1,4}(-\d{1,4})?\b", " ", text)
    text = re.sub(r"\b(et al\.|and|&)\b", " ", text, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def split_bibliography(text: str) -> tuple[str, str]:
    lower = text.lower()
    candidates: list[tuple[int, str]] = []
    for heading in BIB_HEADINGS:
        match = re.search(rf"(?im)^\s*{re.escape(heading)}\s*$", text)
        if match:
            candidates.append((match.start(), heading))
    if not candidates:
        return text, ""
    start, _ = sorted(candidates)[0]
    return text[:start], text[start:]


def extract_citations(body: str) -> list[str]:
    citations: list[str] = []
    for match in CITATION_RE.finditer(body):
        raw = match.group(1).strip()
        if len(raw.split()) > 12:
            continue
        citations.append(raw)
    return citations


def bibliography_entries(bib: str) -> list[str]:
    if not bib.strip():
        return []
    lines = [line.strip() for line in bib.splitlines()]
    lines = [line for line in lines if line]
    if lines and lines[0].lower().strip().strip(":") in BIB_HEADINGS:
        lines = lines[1:]

    entries: list[str] = []
    current: list[str] = []
    for line in lines:
        # New entries often start flush-left with an author/title. If the previous
        # line already looks complete, start a new entry.
        if current and re.search(r"\.$", " ".join(current)) and re.match(r"^[A-Z0-9\"“]", line):
            entries.append(" ".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        entries.append(" ".join(current).strip())
    return entries


def entry_key(entry: str) -> str:
    # First meaningful author/title token cluster.
    entry = re.sub(r"^[-*\d.\s]+", "", entry.strip())
    before_period = entry.split(".", 1)[0]
    before_comma = entry.split(",", 1)[0]
    key = before_comma if len(before_comma) <= 45 else before_period
    return normalize_label(key)


def likely_matches(citation: str, entries: Iterable[str]) -> list[str]:
    cit = normalize_label(citation)
    if not cit:
        return []
    cit_tokens = [tok for tok in re.split(r"\W+", cit) if len(tok) > 2]
    matches: list[str] = []
    for entry in entries:
        e_norm = normalize_label(entry[:180])
        key = entry_key(entry)
        if key and (key in cit or cit in key):
            matches.append(entry)
            continue
        if cit_tokens and all(tok in e_norm for tok in cit_tokens[:2]):
            matches.append(entry)
    return matches[:3]


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract likely in-text citations and bibliography entries from an IWA draft.")
    parser.add_argument("essay", help="Path to a plain-text essay file")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of readable text")
    args = parser.parse_args()

    path = Path(args.essay)
    text = path.read_text(encoding="utf-8", errors="replace")
    body, bib = split_bibliography(text)
    citations = extract_citations(body)
    entries = bibliography_entries(bib)
    unique_citations = sorted(set(citations), key=str.lower)

    cited_missing = []
    citation_matches = {}
    for citation in unique_citations:
        matches = likely_matches(citation, entries)
        citation_matches[citation] = matches
        if not matches:
            cited_missing.append(citation)

    entry_usage = []
    for entry in entries:
        key = entry_key(entry)
        used = any(entry in citation_matches[cit] for cit in citation_matches)
        entry_usage.append({"key": key, "used_by_detected_citation": used, "entry": entry})

    quote_count = len(QUOTE_RE.findall(body))
    word_count = len(re.findall(r"\b\w+\b", body))

    result = {
        "approx_body_word_count_excluding_bibliography": word_count,
        "likely_quote_count": quote_count,
        "unique_in_text_citations": unique_citations,
        "bibliography_entry_count": len(entries),
        "cited_but_no_likely_bib_match": cited_missing,
        "bibliography_entries_usage_guess": entry_usage,
        "notes": [
            "This is a pattern-based helper; manually verify all matches.",
            "The script does not judge source credibility or citation-style correctness.",
        ],
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(f"Approx body word count excluding bibliography: {word_count}")
    print(f"Likely quote count: {quote_count}")
    print(f"Bibliography entries found: {len(entries)}")
    print("\nUnique in-text citations:")
    for citation in unique_citations:
        print(f"- {citation}")
    print("\nCited but no likely bibliography match:")
    if cited_missing:
        for citation in cited_missing:
            print(f"- {citation}")
    else:
        print("- none detected")
    print("\nBibliography entries usage guess:")
    for item in entry_usage:
        status = "used" if item["used_by_detected_citation"] else "not detected in in-text citations"
        print(f"- [{status}] {item['entry'][:180]}")
    print("\nReminder: manually verify all matches and source quality.")


if __name__ == "__main__":
    main()
