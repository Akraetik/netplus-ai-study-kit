# Anki Decks

About **2,000 cards** (1,950 exactly) for CompTIA Network+ N10-009. Double-click any `.apkg` to import it into [Anki](https://apps.ankiweb.net/).

| Deck | Cards | Use it for |
|---|---|---|
| [`netplus-n10-009-core.apkg`](netplus-n10-009-core.apkg) | 708 | **Start here.** Full objective coverage in 15 subdecks. Rich backs: a one-line summary, how it works, and exam traps. |
| [`netplus-n10-009-rapid-recall.apkg`](netplus-n10-009-rapid-recall.apkg) | 952 | Three-second facts in 23 subdecks: ports, protocol numbers, subnetting, cable specs, PoE, syslog levels, commands, acronyms. |
| [`netplus-n10-009-trouble-areas-sample.apkg`](netplus-n10-009-trouble-areas-sample.apkg) | 70 | A sample of what the [adaptive loop](../docs/06-adaptive-loop.md) produces: discriminator cards ("RPO vs RTO") and quick IEEE/port checks. |
| [`quick/`](quick/) | 220 | Five small decks for a 10-minute session: ports, OSI, cabling, tools, and common errors. |

## Core deck — subdecks

| Subdeck | Cards |
|---|---|
| 01 Ports and Protocols | 106 |
| 01b Devices & Topologies | 24 |
| 02 OSI Model & Encapsulation | 18 |
| 03 IPv4 Addressing & Subnetting | 33 |
| 04 IPv6 | 13 |
| 05 Cables, Connectors & Media | 30 |
| 06 Routing | 28 |
| 07 Switching, VLANs & STP | 30 |
| 08 Wireless | 33 |
| 09 Cloud, Virtualization & SDN | 25 |
| 10 Network Services (DHCP, DNS, NTP, VPN) | 37 |
| 11 Network Operations, DR & HA | 33 |
| 12 Network Security | 65 |
| 13 Troubleshooting & Tools | 89 |
| 14 Acronyms | 144 |

## Rapid Recall deck — subdecks

Ports (178) · IP Protocol Numbers (24) · TCP vs UDP (4) · Secure Swaps (10) · Subnetting (70) · Key Addresses (20) · OSI Model (52) · Cabling & Media (61) · PoE (8) · Wireless (25) · IEEE Standards (13) · Routing (22) · Switching & STP (16) · DNS, DHCP & Time (36) · Syslog (17) · Tools (56) · Commands (13) · Attacks (32) · Security (40) · Operations (40) · Core Concepts (54) · Troubleshooting Steps (17) · Acronyms (144)

## Which deck when?

| Stage | Deck |
|---|---|
| Learning a domain for the first time | Core, that domain's subdeck only |
| After you've seen every domain | Core, whole deck (interleaved) + Rapid Recall |
| After each practice test | Your own trouble-areas deck (build it with [Prompt 3C](../prompts/03-flashcards.md#prompt-3c--miss-driven-trouble-area-cards)) |
| Exam week | Rapid Recall + your trouble areas + the quick decks |

## Recommended settings

Turn on **FSRS** (Deck Options → Advanced). Desired retention 0.90. New cards per day 20–40. Details in [docs/05](../docs/05-flashcard-pipeline.md#step-6--set-anki-up-for-a-deadline).

## How these were made

Each deck was generated with AI from the official N10-009 objectives using the prompts in [`prompts/`](../prompts/), then reviewed. Readable exports of every card live in [`source/`](source/) so you can search them on GitHub or suggest fixes in a PR.

**Found an error?** [Open a content correction](../../../issues/new?template=content-correction.md).
