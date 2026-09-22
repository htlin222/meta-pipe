#!/usr/bin/env python3
"""Build database-specific queries from pico.yaml."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Iterable, List

import yaml


def split_terms(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        terms = []
        for item in value:
            terms.extend(split_terms(item))
        return terms
    if isinstance(value, str):
        raw = value.replace("|", ";")
        parts = [p.strip() for p in re.split(r";|,", raw) if p.strip()]
        return parts
    return []


def quote(term: str) -> str:
    term = term.strip()
    if " " in term and not term.startswith("\""):
        return f'"{term}"'
    return term


def group_terms(terms: List[str], fmt) -> str:
    if not terms:
        return ""
    formatted = [fmt(quote(t)) for t in terms]
    if len(formatted) == 1:
        return formatted[0]
    return "(" + " OR ".join(formatted) + ")"


def group_terms_raw(terms: List[str], fmt) -> str:
    """Like group_terms but without pre-quoting.

    The non-PubMed builders must see the raw term so they can detect and strip a
    trailing PubMed field tag. ``quote()`` would wrap the tag inside the quotes
    (``"Receptor, ErbB-2[mh]"``), hiding it from the tag parser. PubMed keeps
    using ``group_terms`` so its behaviour is unchanged.
    """
    if not terms:
        return ""
    formatted = [fmt(t) for t in terms]
    if len(formatted) == 1:
        return formatted[0]
    return "(" + " OR ".join(formatted) + ")"


TAG_RE = re.compile(r"\[([^\]]+)\]\s*$")


def split_field_tag(term: str) -> tuple[str, str]:
    """Split a PubMed-tagged term into (bare_term, normalized_tag).

    PubMed field tags are a PubMed-only construct. Emitting them inside another
    database's field operator produces invalid syntax -- e.g.
    ``TITLE-ABS-KEY("Breast Neoplasms"[MeSH])`` is rejected by Scopus. Every
    non-PubMed builder therefore strips the tag and maps it to that database's
    own field, instead of passing it through verbatim.

    Returns the bare term (quotes preserved) and one of:
    ``ti``, ``tiab``, ``mesh``, ``pt``, or ``""`` when the term carried no tag.
    """
    match = TAG_RE.search(term.strip())
    if not match:
        return term.strip(), ""

    bare = term[: match.start()].strip()
    raw = match.group(1).strip().lower()

    if raw in ("ti", "title"):
        tag = "ti"
    elif raw in ("tiab", "tw", "all fields"):
        tag = "tiab"
    elif raw in ("mesh", "mesh terms", "mh", "majr"):
        tag = "mesh"
    elif raw in ("pt", "publication type"):
        tag = "pt"
    else:
        tag = "tiab"
    return bare, tag


def requote(term: str) -> str:
    """Re-quote a bare term for databases that cannot parse bare commas.

    ``Receptor, ErbB-2`` is a legal unquoted PubMed MeSH term but breaks
    Scopus/Embase parsing, where the comma is a delimiter.
    """
    term = term.strip()
    if term.startswith('"') and term.endswith('"'):
        return term
    if " " in term or "," in term:
        return f'"{term}"'
    return term


def build_pubmed_group(terms: List[str]) -> str:
    # PubMed behaviour is unchanged: tagged terms pass through verbatim,
    # untagged terms default to [tiab].
    def fmt(term: str) -> str:
        return term if "[" in term else f"{term}[tiab]"
    return group_terms(terms, fmt)


def build_scopus_group(terms: List[str]) -> str:
    """Scopus: strip PubMed tags, map [ti] to TITLE(), everything else to
    TITLE-ABS-KEY(). Publication types have no Scopus field equivalent, so they
    degrade to a free-text TITLE-ABS-KEY match rather than being dropped."""
    def fmt(term: str) -> str:
        bare, tag = split_field_tag(term)
        bare = requote(bare)
        return f"TITLE({bare})" if tag == "ti" else f"TITLE-ABS-KEY({bare})"
    return group_terms(terms, fmt)


def build_embase_group(terms: List[str]) -> str:
    """Embase (Emtree syntax): strip PubMed tags, map [ti] to :ti and MeSH
    descriptors to an exploded Emtree term; everything else to :ti,ab,kw."""
    def fmt(term: str) -> str:
        bare, tag = split_field_tag(term)
        if tag == "mesh":
            return f"{requote(bare).lower()}/exp"
        if tag == "ti":
            return f"{requote(bare)}:ti"
        return f"{requote(bare)}:ti,ab,kw"
    return group_terms(terms, fmt)


def build_cochrane_group(terms: List[str]) -> str:
    """Cochrane CENTRAL: strip PubMed tags, map MeSH to [mh] and [ti] to :ti."""
    def fmt(term: str) -> str:
        bare, tag = split_field_tag(term)
        bare = requote(bare)
        if tag == "mesh":
            return f"[mh {bare}]"
        if tag == "ti":
            return f"{bare}:ti"
        return bare
    return group_terms(terms, fmt)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build database queries from pico.yaml")
    parser.add_argument("--pico", default="01_protocol/pico.yaml", help="Path to pico.yaml")
    parser.add_argument("--expanded", default=None, help="Expanded terms YAML")
    parser.add_argument("--out", default="02_search/round-01/queries.txt", help="Output file")
    args = parser.parse_args()

    if args.expanded:
        expanded_path = Path(args.expanded)
        if not expanded_path.exists():
            raise SystemExit(f"Missing expanded terms file: {expanded_path}")
        pico = yaml.safe_load(expanded_path.read_text()) or {}
        population = split_terms(pico.get("population"))
        intervention = split_terms(pico.get("intervention"))
        comparison = split_terms(pico.get("comparison"))
        outcomes = split_terms(pico.get("outcomes"))
    else:
        pico_path = Path(args.pico)
        if not pico_path.exists():
            raise SystemExit(f"Missing PICO file: {pico_path}")
        pico = yaml.safe_load(pico_path.read_text()) or {}
        population = split_terms(pico.get("population", {}).get("description"))
        intervention = split_terms(pico.get("intervention", {}).get("description"))
        comparison = split_terms(pico.get("comparison", {}).get("description"))

        outcomes = []
        outcomes_block = pico.get("outcomes", {})
        for outcome in outcomes_block.get("primary", []) or []:
            outcomes.extend(split_terms(outcome.get("name")))
        for outcome in outcomes_block.get("secondary", []) or []:
            outcomes.extend(split_terms(outcome.get("name")))

    # population, intervention, comparison, outcomes populated above

    def join_parts(parts: List[str]) -> str:
        parts = [p for p in parts if p]
        return " AND ".join(parts) if parts else ""

    pubmed = join_parts(
        [
            build_pubmed_group(population),
            build_pubmed_group(intervention),
            build_pubmed_group(comparison),
            build_pubmed_group(outcomes),
        ]
    )

    scopus = join_parts(
        [
            build_scopus_group(population),
            build_scopus_group(intervention),
            build_scopus_group(comparison),
            build_scopus_group(outcomes),
        ]
    )

    embase = join_parts(
        [
            build_embase_group(population),
            build_embase_group(intervention),
            build_embase_group(comparison),
            build_embase_group(outcomes),
        ]
    )

    cochrane = join_parts(
        [
            build_cochrane_group(population),
            build_cochrane_group(intervention),
            build_cochrane_group(comparison),
            build_cochrane_group(outcomes),
        ]
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Generated from 01_protocol/pico.yaml",
        "",
        "[pubmed]",
        pubmed or "",
        "",
        "[scopus]",
        scopus or "",
        "",
        "[embase]",
        embase or "",
        "",
        "[cochrane]",
        cochrane or "",
        "",
        "# Review and refine queries per database syntax before running searches.",
    ]
    out_path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
