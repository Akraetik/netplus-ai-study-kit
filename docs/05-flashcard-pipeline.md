# 5. Flashcard Pipeline — Cards That Hold Up on Exam Day

**Goal:** get well-formed cards into Anki fast, and keep improving them without losing your review history.

## Step 1 — Start with the prebuilt decks

Don't write 2,000 cards from scratch. Import the decks in [`decks/`](../decks/) and spend your energy on the cards only *you* need: the ones built from your misses.

## Step 2 — Know what a good card looks like

Bad cards are the main reason people quit Anki. These rules come from experience and from Piotr Wozniak's *Twenty Rules of Formulating Knowledge*.

| Rule | Bad | Good |
|---|---|---|
| **One fact per card** | "Explain SNMP" | "SNMP — which port receives traps?" → 162 |
| **Ask in the exam's direction** | "What is 443?" only | Both "HTTPS port?" and "Port 443?" (use `reverse`) |
| **Discriminate look-alikes** | "What is RPO?" | "RPO vs RTO — which measures acceptable *data* loss?" |
| **Use scenarios for Domain 5** | "What does APIPA mean?" | "A host shows 169.254.x.x. What failed?" |
| **Keep answers short** | A paragraph | 1–7 words. Put the "why" in `extra`. |
| **Put the trap in `extra`** | — | "Don't confuse SFTP (22, over SSH) with FTPS (989/990, over TLS)." |
| **Tag by objective** | No tags | `obj5.5 domain5 missed-once` |

Scenario and discriminator cards matter most. Network+ questions rarely ask "what is X." They ask "which X fits this situation."

## Step 3 — Generate cards with AI

Use the [flashcard prompts](../prompts/03-flashcards.md). They make the AI return a CSV that fits this format:

```csv
front,back,extra,tags,deck,reverse
"<b>SSH</b> — port and transport?","22 / TCP","Replaced Telnet (23).",obj1.4 ports,Ports,y
```

| Column | Required | Notes |
|---|---|---|
| `front` | ✅ | The prompt. Simple HTML allowed: `<b>`, `<i>`, `<code>`, `<br>` |
| `back` | ✅ | The answer. Short. |
| `extra` | | The reason, the memory hook, or the common trap |
| `tags` | | Space-separated. Objective numbers make weak-spot filtering easy |
| `deck` | | Subdeck name. Becomes `Root::Subdeck` |
| `reverse` | | Any value also makes a back→front card |

A blank template lives at [`templates/cards-template.csv`](../templates/cards-template.csv).

## Step 4 — Check the cards

Scan every AI-generated card before import. Look hard at numbers, standards, and anything that says "always" or "never." Delete cards that are vague or test two facts. Deleting is cheaper than learning something wrong.

## Step 5 — Build the deck

```bash
pip install -r tools/requirements.txt
python tools/make_deck.py my-cards.csv --name "Network+ N10-009::Trouble Areas" --out trouble.apkg
```

Double-click the `.apkg` to import.

**Why use the tool instead of Anki's CSV import?**

- **Stable IDs.** Each note's ID comes from the deck name plus the front text. Fix a typo in the answer, rebuild, re-import. Anki updates the card and keeps its schedule.
- **Clean template.** Answer, a highlighted "why" box, tags shown small, and dark-mode support.
- **Subdecks and reverse cards** from one CSV.
- **Validation.** It flags missing columns, empty rows, and duplicate fronts.

**No-code alternative:** in Anki, choose **File → Import**, pick the CSV, map the columns, and set the note type to "Basic (and reversed card)" if you want both directions.

## Step 6 — Set Anki up for a deadline

| Setting | Where | Value |
|---|---|---|
| FSRS scheduler | Deck Options → Advanced | **On** |
| Desired retention | Deck Options → FSRS | 0.90 (0.92–0.95 in the final week) |
| New cards/day | Deck Options → Daily Limits | 20–40 |
| Maximum reviews/day | Deck Options → Daily Limits | 9999 (never hide due reviews) |

**For a final push:** use **Tools → Create Filtered Deck** with a search like `tag:missed* OR prop:lapses>=2` to drill only your leeches and misses.

## Step 7 — Use tags to find your weak spots

Anki's Browse window turns tags into a diagnostic tool:

- `tag:obj5.*` — every troubleshooting card
- `tag:missed-twice` — misses that repeated
- `prop:lapses>=3` — cards you keep forgetting
- `rated:7:1` — cards you pressed **Again** on this week

Feed the results into the [adaptive loop](06-adaptive-loop.md).

---

**Next:** [6. The adaptive loop →](06-adaptive-loop.md)
