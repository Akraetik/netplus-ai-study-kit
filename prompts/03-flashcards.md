# 03 · Flashcard Prompts

All prompts output CSV that [`tools/make_deck.py`](../tools/make_deck.py) reads, and that Anki's own **File → Import** also accepts.

```csv
front,back,extra,tags,deck,reverse
```

Save the output as a `.csv` file. Then:

```bash
python tools/make_deck.py cards.csv --name "Network+ N10-009::My Cards" --out my-cards.apkg
```

---

## Shared rules block

```text
CARD RULES
- Output ONLY a CSV in one code block. Header: front,back,extra,tags,deck,reverse
- Quote every field with double quotes. Escape internal double quotes by doubling them.
- One fact per card. The back is 1–7 words when possible.
- "extra" holds the reason, a memory hook, or the common trap. One or two sentences.
- Use simple HTML only: <b>, <i>, <code>, <br>.
- "tags": space-separated. Always include the objective as objN.N (e.g. obj1.4) and the domain as domainN.
- "deck": a short subdeck name (e.g. Ports, Wireless, Troubleshooting).
- "reverse": put y ONLY for pure pairs where both directions are useful (port <-> service, acronym <-> meaning). Otherwise leave empty.
- Prefer scenario prompts ("A user reports X. What is the most likely cause?") over definitions for any objective that starts "Given a scenario".
- Only include facts on the CompTIA N10-009 objectives. If unsure of a fact, omit the card.
- Never copy practice-exam questions. Write new cards that test the same concept.
```

---

## Prompt 3A — Full coverage for one objective

```text
You are a CompTIA Network+ instructor who writes excellent Anki cards.

Create {{N e.g. 25–40}} cards that fully cover N10-009 objective {{OBJECTIVE}}.
Mix: ~40% fact cards, ~30% scenario cards, ~30% "X vs Y" discriminator cards.
Cover every sub-bullet in the objective text below. Add a final card that asks for the full list if the objective is a list (e.g. "Name the 7 steps of the CompTIA troubleshooting methodology").

OBJECTIVE TEXT:
{{PASTE}}

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 3B — Rapid-recall deck

```text
Create a rapid-recall deck for CompTIA Network+ N10-009 on: {{TOPIC e.g. ports and protocols, IEEE 802.11 standards, copper and fiber cable specs, PoE standards, syslog severity levels}}.
Every card must be answerable in under 3 seconds. Back = the bare answer only. Put context in extra.
Set reverse=y for every pair.

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 3C — Miss-driven trouble-area cards

**The most important card prompt.** Run it after every practice test.

**Paste in:** your miss log rows (or the output of [Prompt 4A](04-practice-test-analysis.md)).

```text
You are a CompTIA Network+ instructor. Below is my practice-test miss log with a root-cause code for each miss:
K = knowledge gap, D = discrimination (confused two similar things), A = application (knew the fact, not how to apply it), R = misread, P = procedure/PBQ, G = lucky guess.

For each miss, write cards based on its code:
- K or G: 1 fact card + 1 scenario card + 1 "why the wrong answer is wrong" card.
- D: 2 discriminator cards (ask it from each side: "Which one measures X?" and "Which one measures Y?") + 1 scenario card that forces the choice.
- A: 2–3 scenario cards with different surface details but the same underlying concept.
- R: no cards. List it at the end under "// READING MISSES" with the qualifier I missed.
- P: no cards. List it at the end under "// DESK PRACTICE NEEDED" with a suggested exercise.

Tag every card with its objective, domain, and "missed-once". If my log says a concept was missed before, use "missed-twice".
Deck column: "Trouble Areas".
If several misses share one root concept, write one strong set of cards for the root concept instead of repeating.

MISS LOG:
{{PASTE}}

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 3D — Discriminator pairs

```text
List the {{N e.g. 30}} pairs or groups of terms most often confused on CompTIA Network+ N10-009.
For each, write two cards: one from each side of the pair. The front names the pair and asks which one matches a specific property. The back names the answer. Extra gives a memory hook.
Deck: "Discriminators". Tag "discriminator" plus objective and domain.

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 3E — Symptom → cause → tool (Domain 5)

```text
Write {{N}} troubleshooting scenario cards for CompTIA Network+ N10-009 Domain 5.
Front: a short symptom a user or technician would report, including one telling detail (e.g. an IP in 169.254.0.0/16, a specific error, a cable length).
Back: the most likely cause AND the first tool or command to confirm it.
Extra: the next step in the CompTIA methodology, plus one tempting-but-wrong cause.
Cover cable, wireless, IP/DNS/DHCP, routing/switching, and performance issues roughly evenly.
Deck: "Troubleshooting". Tag domain5 plus the objective.

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 3F — Audit my cards

Run this on any AI-generated CSV before you import it.

```text
Audit these flashcards for a CompTIA Network+ N10-009 student. Check each card for:
1. Factual errors (especially port numbers, standards, distances, speeds, wattages).
2. More than one fact per card.
3. Vague fronts with more than one correct answer.
4. Content not on the N10-009 objectives.
Return: (a) a table of problem cards with the issue and a fix, then (b) the corrected full CSV in one code block with the same header.
If you are not certain a fact is wrong, flag it as "verify" instead of changing it.

{{PASTE CSV}}
```
