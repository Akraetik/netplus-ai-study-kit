#!/usr/bin/env python3
"""
make_deck.py — turn an AI-generated CSV of flashcards into an importable Anki .apkg.

CSV columns (header row required; only front and back are mandatory):

    front    The prompt. HTML allowed (<b>, <code>, <br>).
    back     The short answer. Keep it to what you must recall.
    extra    Optional. The "why", a memory hook, or the distractor that fools people.
    tags     Optional. Space-separated. Use obj2.3 domain5 missed-once etc.
    deck     Optional. Subdeck name. "Ports" becomes "<root>::Ports".
    reverse  Optional. Any non-empty value also creates a back->front card.

Usage:
    python make_deck.py cards.csv --name "Network+ N10-009::Trouble Areas" --out decks/trouble.apkg
    python make_deck.py a.csv b.csv --name "Network+ N10-009" --out decks/netplus.apkg

Re-importing an updated deck UPDATES existing cards instead of duplicating them,
because each note's GUID is derived from (root deck, front text). Your review
history survives. Change the front text and Anki treats it as a new card.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

try:
    import genanki
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency. Run: pip install -r tools/requirements.txt")

REQUIRED = {"front", "back"}

CSS = """
.card { font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 22px;
        line-height: 1.45; text-align: center; color: #1d1d1f; background: #fafafa; padding: 12px; }
.nightMode.card, .night_mode .card { color: #ececec; background: #1e1e1e; }
.answer { font-size: 26px; font-weight: 600; margin-top: 8px; }
.extra  { font-size: 17px; text-align: left; opacity: .85; margin: 18px auto 0; max-width: 34em;
          border-left: 3px solid #0a84ff; padding-left: 12px; }
code    { font-family: "Cascadia Code", Consolas, monospace; font-size: .9em; }
.tagline { font-size: 12px; opacity: .45; margin-top: 22px; }
"""

FRONT = "{{Front}}"
BACK = """{{FrontSide}}<hr id="answer">
<div class="answer">{{Back}}</div>
{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}
<div class="tagline">{{Tags}}</div>"""
REV_FRONT = "{{#Reverse}}{{Back}}{{/Reverse}}"
REV_BACK = """{{FrontSide}}<hr id="answer">
<div class="answer">{{Front}}</div>
{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}"""


def stable_id(text: str) -> int:
    """Deterministic 31-bit id so rebuilding a deck never creates a duplicate deck/model."""
    return int(hashlib.sha1(text.encode()).hexdigest()[:8], 16) & 0x7FFFFFFF


def build_model(name: str) -> genanki.Model:
    return genanki.Model(
        stable_id(f"model::{name}"),
        f"{name} (Basic+Extra)",
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Extra"}, {"name": "Reverse"}],
        templates=[
            {"name": "Forward", "qfmt": FRONT, "afmt": BACK},
            {"name": "Reverse", "qfmt": REV_FRONT, "afmt": REV_BACK},
        ],
        css=CSS,
    )


def load_rows(paths: list[Path]) -> list[dict]:
    rows = []
    for p in paths:
        with p.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cols = {c.strip().lower() for c in (reader.fieldnames or [])}
            if missing := REQUIRED - cols:
                sys.exit(f"{p}: missing column(s) {sorted(missing)}. Header must include front,back")
            for n, row in enumerate(reader, start=2):
                row = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
                if not row.get("front") or not row.get("back"):
                    print(f"  skip {p.name}:{n} (empty front or back)")
                    continue
                rows.append(row)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+", type=Path)
    ap.add_argument("--name", required=True, help='root deck name, e.g. "Network+ N10-009::Trouble Areas"')
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    rows = load_rows(args.csv)
    if not rows:
        sys.exit("No usable rows found.")

    model = build_model(args.name.split("::")[0])
    decks: dict[str, genanki.Deck] = {}
    seen: set[str] = set()
    for row in rows:
        full = f"{args.name}::{row['deck']}" if row.get("deck") else args.name
        deck = decks.setdefault(full, genanki.Deck(stable_id(f"deck::{full}"), full))
        guid = genanki.guid_for(args.name, row["front"])
        if guid in seen:
            print(f"  duplicate front skipped: {row['front'][:60]}")
            continue
        seen.add(guid)
        tags = [t.replace(" ", "_") for t in row.get("tags", "").split()]
        deck.add_note(genanki.Note(
            model=model,
            fields=[row["front"], row["back"], row.get("extra", ""), "y" if row.get("reverse") else ""],
            tags=tags,
            guid=guid,
        ))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(decks.values())).write_to_file(str(args.out))
    total = sum(len(d.notes) for d in decks.values())
    print(f"{args.out}  ·  {total} notes  ·  {len(decks)} deck(s)")


if __name__ == "__main__":
    main()
