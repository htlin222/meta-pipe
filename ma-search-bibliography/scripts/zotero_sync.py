#!/usr/bin/env python3
"""Sync BibTeX entries to Zotero via the Write API (create/update/delete)."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import random
import re
import string
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

from env_utils import load_dotenv

BASE_URL = "https://api.zotero.org"
DEFAULT_LIMIT = 100
MAX_CREATE_BATCH = 50

BIB_TYPE_MAP = {
    "article": "journalArticle",
    "book": "book",
    "inbook": "bookSection",
    "incollection": "bookSection",
    "inproceedings": "conferencePaper",
    "proceedings": "conferencePaper",
    "techreport": "report",
    "report": "report",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "thesis": "thesis",
    "unpublished": "manuscript",
    "misc": "document",
}

MONTH_MAP = {
    "jan": "01",
    "january": "01",
    "feb": "02",
    "february": "02",
    "mar": "03",
    "march": "03",
    "apr": "04",
    "april": "04",
    "may": "05",
    "jun": "06",
    "june": "06",
    "jul": "07",
    "july": "07",
    "aug": "08",
    "august": "08",
    "sep": "09",
    "sept": "09",
    "september": "09",
    "oct": "10",
    "october": "10",
    "nov": "11",
    "november": "11",
    "dec": "12",
    "december": "12",
}


def build_prefix(library_type: str, library_id: str) -> str:
    library_type = (library_type or "").strip().lower()
    if library_type == "user":
        return f"{BASE_URL}/users/{library_id}"
    if library_type == "group":
        return f"{BASE_URL}/groups/{library_id}"
    raise SystemExit("library-type must be 'user' or 'group'")


def build_headers(api_key: Optional[str]) -> Dict[str, str]:
    headers = {
        "Zotero-API-Version": "3",
        "Accept": "application/json",
    }
    if api_key:
        headers["Zotero-API-Key"] = api_key
    return headers


def write_token() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(32))


def norm_doi(value: str) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    value = value.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return value


def norm_title(value: str) -> str:
    if not value:
        return ""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def extract_year(value: str) -> str:
    if not value:
        return ""
    match = re.search(r"(19|20)\d{2}", value)
    return match.group(0) if match else ""


def parse_month(value: str) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    if value.isdigit() and 1 <= int(value) <= 12:
        return f"{int(value):02d}"
    return MONTH_MAP.get(value, "")


def build_date(year: str, month: str) -> str:
    year = year.strip() if year else ""
    if not year:
        return ""
    month_value = parse_month(month)
    if month_value:
        return f"{year}-{month_value}"
    return year


def parse_creator_list(raw: str, creator_type: str) -> List[Dict[str, str]]:
    if not raw:
        return []
    creators = []
    for name in raw.split(" and "):
        name = name.strip()
        if not name:
            continue
        if "{" in name or "}" in name:
            cleaned = name.replace("{", "").replace("}", "").strip()
            if cleaned:
                creators.append({"creatorType": creator_type, "name": cleaned})
            continue
        if "," in name:
            last, first = name.split(",", 1)
            creators.append(
                {
                    "creatorType": creator_type,
                    "lastName": last.strip(),
                    "firstName": first.strip(),
                }
            )
            continue
        parts = name.split()
        if len(parts) == 1:
            creators.append({"creatorType": creator_type, "name": parts[0]})
        else:
            creators.append(
                {
                    "creatorType": creator_type,
                    "firstName": " ".join(parts[:-1]),
                    "lastName": parts[-1],
                }
            )
    return creators


def parse_keywords(raw: str) -> List[Dict[str, str]]:
    if not raw:
        return []
    tokens = re.split(r"[;,]", raw)
    tags = []
    for token in tokens:
        cleaned = token.strip()
        if cleaned:
            tags.append({"tag": cleaned})
    return tags


def score_entry(entry: Dict[str, Any]) -> Tuple[int, int]:
    fields = [v for v in entry.values() if isinstance(v, str) and v.strip()]
    has_doi = 1 if entry.get("doi") else 0
    return (len(fields), has_doi)


def entry_identity(entry: Dict[str, Any]) -> str:
    doi = norm_doi(str(entry.get("doi", "")))
    if doi:
        return f"doi:{doi}"
    pmid = str(entry.get("pmid", "")).strip()
    if pmid:
        return f"pmid:{pmid}"
    title = norm_title(str(entry.get("title", "")))
    year = str(entry.get("year", "")).strip()
    if title:
        return f"title:{title}|year:{year}"
    return ""


def item_identity(data: Dict[str, Any]) -> str:
    doi = norm_doi(str(data.get("DOI", "") or data.get("doi", "")))
    if doi:
        return f"doi:{doi}"
    extra = str(data.get("extra", "") or "")
    pmid_match = re.search(r"PMID\s*:\s*(\d+)", extra, flags=re.IGNORECASE)
    if pmid_match:
        return f"pmid:{pmid_match.group(1)}"
    pmid = str(data.get("pmid", "")).strip()
    if pmid:
        return f"pmid:{pmid}"
    title = norm_title(str(data.get("title", "")))
    year = extract_year(str(data.get("date", "")))
    if title:
        return f"title:{title}|year:{year}"
    return ""


def resolve_item_type(entry_type: str, item_types: Dict[str, str]) -> str:
    entry_type = (entry_type or "").lower()
    candidate = BIB_TYPE_MAP.get(entry_type, "journalArticle")
    if not item_types:
        return candidate
    return item_types.get(candidate.lower(), candidate)


def fetch_item_types(session: requests.Session, headers: Dict[str, str]) -> Dict[str, str]:
    url = f"{BASE_URL}/itemTypes"
    resp = session.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    mapping = {}
    for item in data:
        item_type = item.get("itemType")
        if item_type:
            mapping[item_type.lower()] = item_type
    return mapping


def fetch_item_template(
    session: requests.Session, headers: Dict[str, str], item_type: str
) -> Dict[str, Any]:
    url = f"{BASE_URL}/items/new"
    resp = session.get(url, headers=headers, params={"itemType": item_type}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def load_bib_entries(path: Path) -> List[Dict[str, Any]]:
    from bibtexparser import loads

    bib_text = path.read_text()
    bib_db = loads(bib_text)
    return bib_db.entries


def normalize_bib_entries(entries: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    deduped: Dict[str, Dict[str, Any]] = {}
    duplicates = 0
    for entry in entries:
        identity = entry_identity(entry)
        if not identity:
            identity = entry.get("ID", "") or str(id(entry))
        if identity in deduped:
            duplicates += 1
            if score_entry(entry) > score_entry(deduped[identity]):
                deduped[identity] = entry
        else:
            deduped[identity] = entry
    return list(deduped.values()), duplicates


def set_field(data: Dict[str, Any], key: str, value: Optional[str], changed: set[str]) -> None:
    if key in data and value:
        data[key] = value
        changed.add(key)


def build_item_data_from_entry(
    entry: Dict[str, Any],
    template: Dict[str, Any],
    collection_key: Optional[str],
    include_pmid_extra: bool = True,
) -> Tuple[Dict[str, Any], set[str]]:
    data = dict(template)
    changed: set[str] = set()

    title = str(entry.get("title", "")).strip()
    author = str(entry.get("author", "")).strip()
    editor = str(entry.get("editor", "")).strip()
    year = str(entry.get("year", "")).strip()
    month = str(entry.get("month", "")).strip()
    journal = str(entry.get("journal", "")).strip()
    booktitle = str(entry.get("booktitle", "")).strip()
    publisher = str(entry.get("publisher", "")).strip()
    address = str(entry.get("address", "")).strip()
    volume = str(entry.get("volume", "")).strip()
    number = str(entry.get("number", "")).strip()
    pages = str(entry.get("pages", "")).strip()
    doi = str(entry.get("doi", "")).strip()
    url = str(entry.get("url", "")).strip()
    abstract = str(entry.get("abstract", "")).strip()
    language = str(entry.get("language", "")).strip()
    isbn = str(entry.get("isbn", "")).strip()
    issn = str(entry.get("issn", "")).strip()
    keywords = str(entry.get("keywords", "")).strip()
    pmid = str(entry.get("pmid", "")).strip()

    date = build_date(year, month)

    set_field(data, "title", title, changed)
    set_field(data, "date", date, changed)
    set_field(data, "url", url, changed)
    set_field(data, "abstractNote", abstract, changed)
    set_field(data, "language", language, changed)

    if "DOI" in data:
        set_field(data, "DOI", doi, changed)
    else:
        set_field(data, "doi", doi, changed)

    set_field(data, "volume", volume, changed)
    set_field(data, "issue", number, changed)
    set_field(data, "pages", pages, changed)

    if "publicationTitle" in data:
        set_field(data, "publicationTitle", journal, changed)
    if "bookTitle" in data:
        set_field(data, "bookTitle", booktitle, changed)
    if "proceedingsTitle" in data:
        set_field(data, "proceedingsTitle", booktitle, changed)
    if "publisher" in data:
        set_field(data, "publisher", publisher, changed)
    if "place" in data:
        set_field(data, "place", address, changed)
    if "ISBN" in data:
        set_field(data, "ISBN", isbn, changed)
    if "ISSN" in data:
        set_field(data, "ISSN", issn, changed)

    creators = []
    creators.extend(parse_creator_list(author, "author"))
    creators.extend(parse_creator_list(editor, "editor"))
    if creators and "creators" in data:
        data["creators"] = creators
        changed.add("creators")

    tags = parse_keywords(keywords)
    if tags and "tags" in data:
        data["tags"] = tags
        changed.add("tags")

    if include_pmid_extra and pmid and "extra" in data:
        data["extra"] = f"PMID: {pmid}"
        changed.add("extra")

    if collection_key and "collections" in data:
        data["collections"] = [collection_key]
        changed.add("collections")

    return data, changed


def merge_tags(existing: List[Dict[str, str]], new_tags: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = {tag.get("tag") for tag in existing if tag.get("tag")}
    merged = list(existing)
    for tag in new_tags:
        value = tag.get("tag")
        if value and value not in seen:
            merged.append({"tag": value})
            seen.add(value)
    return merged


def merge_collections(existing: List[str], collection_key: str) -> List[str]:
    if collection_key in existing:
        return existing
    return existing + [collection_key]


def fetch_items(
    session: requests.Session,
    headers: Dict[str, str],
    prefix: str,
    collection_key: Optional[str],
    limit: int,
) -> List[Dict[str, Any]]:
    url = f"{prefix}/items" if not collection_key else f"{prefix}/collections/{collection_key}/items"
    items: List[Dict[str, Any]] = []
    start = 0
    total_results = None

    while True:
        params = {"format": "json", "limit": limit, "start": start}
        resp = session.get(url, headers=headers, params=params, timeout=60)
        resp.raise_for_status()
        page_items = resp.json()
        if not page_items:
            break
        items.extend(page_items)

        if total_results is None:
            try:
                total_results = int(resp.headers.get("Total-Results", ""))
            except ValueError:
                total_results = None

        start += limit
        if total_results is not None and start >= total_results:
            break
        if len(page_items) < limit:
            break

    return items


def coerce_item_record(item: Dict[str, Any]) -> Dict[str, Any]:
    data = item.get("data", item)
    return {
        "key": item.get("key") or data.get("key"),
        "version": item.get("version") or data.get("version"),
        "data": data,
    }


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Sync BibTeX entries to Zotero.")
    parser.add_argument("--in-bib", required=True, help="Input BibTeX path")
    parser.add_argument("--library-type", default=None, help="user or group (or ZOTERO_LIBRARY_TYPE)")
    parser.add_argument("--library-id", default=None, help="Library ID (or ZOTERO_LIBRARY_ID)")
    parser.add_argument(
        "--collection-key", default=None, help="Collection key (or ZOTERO_COLLECTION_KEY)"
    )
    parser.add_argument("--api-key", default=None, help="Zotero API key (or ZOTERO_API_KEY)")
    parser.add_argument("--delete-missing", action="store_true", help="Delete items not in BibTeX")
    parser.add_argument("--dry-run", action="store_true", help="Plan actions without writing")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Page size for reads")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("ZOTERO_API_KEY")
    library_type = args.library_type or os.getenv("ZOTERO_LIBRARY_TYPE")
    library_id = args.library_id or os.getenv("ZOTERO_LIBRARY_ID")
    collection_key = args.collection_key or os.getenv("ZOTERO_COLLECTION_KEY")

    if not api_key:
        raise SystemExit("Missing Zotero API key.")
    if not library_type or not library_id:
        raise SystemExit("Missing library type or library id.")

    prefix = build_prefix(library_type, library_id)
    headers = build_headers(api_key)
    session = requests.Session()

    bib_entries = load_bib_entries(Path(args.in_bib))
    bib_entries, duplicate_count = normalize_bib_entries(bib_entries)

    limit = max(1, min(args.limit, 100))
    raw_items = fetch_items(session, headers, prefix, collection_key, limit)
    items = [coerce_item_record(item) for item in raw_items]

    existing_by_identity: Dict[str, Dict[str, Any]] = {}
    collisions = 0

    for item in items:
        data = item["data"]
        if data.get("itemType") in {"attachment", "note"}:
            continue
        identity = item_identity(data)
        if not identity:
            continue
        if identity in existing_by_identity:
            collisions += 1
            existing_by_identity.pop(identity, None)
        else:
            existing_by_identity[identity] = item

    item_types: Dict[str, str] = {}
    try:
        item_types = fetch_item_types(session, headers)
    except requests.RequestException:
        item_types = {}

    templates: Dict[str, Dict[str, Any]] = {}

    created = 0
    updated = 0
    deleted = 0
    failed = 0

    to_create: List[Dict[str, Any]] = []
    update_requests: List[Tuple[str, int, Dict[str, Any]]] = []
    unmatched_existing = set(existing_by_identity.keys())

    for entry in bib_entries:
        identity = entry_identity(entry)
        entry_type = str(entry.get("ENTRYTYPE", ""))
        item_type = resolve_item_type(entry_type, item_types)

        if identity and identity in existing_by_identity:
            item = existing_by_identity[identity]
            data = item["data"]
            template = data
            new_data, changed = build_item_data_from_entry(
                entry, template, collection_key, include_pmid_extra=False
            )
            patch: Dict[str, Any] = {}

            for key in changed:
                patch[key] = new_data[key]

            if collection_key and "collections" in data:
                merged = merge_collections(data.get("collections", []), collection_key)
                if merged != data.get("collections", []):
                    patch["collections"] = merged

            if "tags" in new_data and new_data.get("tags"):
                merged_tags = merge_tags(data.get("tags", []), new_data.get("tags", []))
                if merged_tags != data.get("tags", []):
                    patch["tags"] = merged_tags

            if "extra" in data and entry.get("pmid"):
                existing_extra = str(data.get("extra", "") or "")
                if re.search(r"PMID\s*:\s*\d+", existing_extra, flags=re.IGNORECASE) is None:
                    pmid_value = str(entry.get("pmid", "")).strip()
                    if pmid_value:
                        patch["extra"] = (
                            (existing_extra + "\n" if existing_extra else "") + f"PMID: {pmid_value}"
                        )

            if patch:
                item_key = item.get("key")
                item_version = item.get("version")
                try:
                    item_version_int = int(item_version)
                except (TypeError, ValueError):
                    item_version_int = None
                if item_key and item_version_int is not None:
                    update_requests.append((item_key, item_version_int, patch))
            if identity in unmatched_existing:
                unmatched_existing.remove(identity)
            continue

        if identity and identity in unmatched_existing:
            unmatched_existing.remove(identity)

        if item_type not in templates:
            try:
                templates[item_type] = fetch_item_template(session, headers, item_type)
            except requests.RequestException:
                templates[item_type] = {"itemType": item_type}

        template = templates[item_type]
        template["itemType"] = item_type
        new_data, _ = build_item_data_from_entry(entry, template, collection_key)
        to_create.append(new_data)

    if args.dry_run:
        created = len(to_create)
        updated = len(update_requests)
        deleted = len(unmatched_existing) if args.delete_missing else 0
    else:
        for i in range(0, len(to_create), MAX_CREATE_BATCH):
            batch = to_create[i : i + MAX_CREATE_BATCH]
            if not batch:
                continue
            batch_headers = dict(headers)
            batch_headers["Content-Type"] = "application/json"
            batch_headers["Zotero-Write-Token"] = write_token()
            resp = session.post(f"{prefix}/items", headers=batch_headers, json=batch, timeout=60)
            if resp.status_code >= 400:
                failed += len(batch)
                continue
            result = resp.json()
            created += len(result.get("success", {}))
            failed += len(result.get("failed", {}))

        for key, version, patch in update_requests:
            patch_headers = dict(headers)
            patch_headers["Content-Type"] = "application/json"
            patch_headers["If-Unmodified-Since-Version"] = str(version)
            resp = session.patch(
                f"{prefix}/items/{key}", headers=patch_headers, json=patch, timeout=60
            )
            if resp.status_code == 204:
                updated += 1
            else:
                failed += 1

        if args.delete_missing:
            for identity in sorted(unmatched_existing):
                item = existing_by_identity.get(identity)
                if not item:
                    continue
                delete_headers = dict(headers)
                delete_headers["If-Unmodified-Since-Version"] = str(item["version"])
                resp = session.delete(f"{prefix}/items/{item['key']}", headers=delete_headers, timeout=60)
                if resp.status_code == 204:
                    deleted += 1
                else:
                    failed += 1

    log_lines = [
        f"date: {dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z",
        f"library_type: {library_type}",
        f"library_id: {library_id}",
        f"collection_key: {collection_key or ''}",
        f"input_entries: {len(bib_entries)}",
        f"duplicate_entries_removed: {duplicate_count}",
        f"existing_items: {len(items)}",
        f"collisions: {collisions}",
        f"to_create: {len(to_create)}",
        f"to_update: {len(update_requests)}",
        f"delete_missing: {args.delete_missing}",
        f"created: {created}",
        f"updated: {updated}",
        f"deleted: {deleted}",
        f"failed: {failed}",
        f"dry_run: {args.dry_run}",
    ]
    Path(args.out_log).write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
