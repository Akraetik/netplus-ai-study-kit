# 02 · Audio Script Prompts

All prompts output the script format that [`tools/make_audio.py`](../tools/make_audio.py) reads:

```text
# TITLE: Track 04 - Port Drill
[A] Question or narration.
[PAUSE 4]
[B] Answer and one-line reason.
```

Save each script as `NN_short_name.txt` (e.g. `04_port_drill.txt`). The number becomes the track number.

---

## Shared rules block

Every prompt below includes this block. Reuse it in your own prompts.

```text
AUDIO WRITING RULES (the listener is driving and cannot see anything)
- Write for the ear. No tables, bullets, symbols, URLs, or markdown in the spoken text.
- Speak port numbers the way network techs say them: 443 = "four forty-three", 3389 = "thirty-three eighty-nine", 1433 = "fourteen thirty-three", 22 = "twenty-two".
- Spell acronyms with spaces so TTS reads letters: "S N M P", "D H C P". Use common spoken forms where they exist: TACACS+ = "tack-acks plus", VLAN = "V-lan", SIEM = "sim".
- Standards: 802.1Q = "eight oh two dot one Q". 802.11ax = "eight oh two eleven A X".
- Short sentences. One idea per sentence. Maximum about 20 words.
- In drills, ask the question, then [PAUSE 4] on its own line, then give the answer, then one sentence of why.
- Repeat the key fact twice: once in the answer, once in the reason.
- Use [A] for the host/asker and [B] for the answerer. Leave a blank line between blocks.
- Start with "# TITLE: " and a one-line title. Target {{MINUTES}} minutes at about 160 words per minute.
- Only include facts that are on the CompTIA N10-009 objectives. If you are unsure of a fact, leave it out.
```

---

## Prompt 2A — Teaching track for one objective

**Use it for:** first exposure to a topic on the commute.

```text
You are a CompTIA Network+ instructor recording an audio lesson for a student who is driving.

Write a {{MINUTES}}-minute audio script that teaches N10-009 objective {{OBJECTIVE e.g. "2.2 Given a scenario, configure switching technologies and features"}}.

Structure:
1. 20-second hook: why this matters on the exam and on the job.
2. Teach each sub-bullet of the objective in plain language with one real-world example each.
3. Every 2–3 minutes, a quick check: ask a question, [PAUSE 4], answer.
4. A "don't confuse these" section covering the two or three look-alike terms in this objective.
5. A 60-second recap as rapid-fire question, pause, answer.

Here is the official objective text:
{{PASTE OBJECTIVE TEXT}}

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 2B — Rapid-recall drill

**Use it for:** memorizing lists: ports, standards, cable specs, PoE wattages, OSI layers.

```text
Write a {{MINUTES}}-minute rapid-recall audio drill on: {{TOPIC e.g. "every port on the N10-009 objective 1.4 list"}}.

Format: [A] asks, [PAUSE 3], [B] answers in five words or fewer plus a short reason.
Go in BOTH directions: "What port does S S H use?" and "Port twenty-two is which service?"
Shuffle the order. Do not go in numeric order.
After every 10 items, [A] says "Round complete. Replay anything you missed."
End with the 5 most-missed items repeated once more.

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 2C — Miss-driven drill

**Use it for:** after every practice test. This is the highest-value audio you can make.

**Paste in:** the miss log rows for this test (or the output of [Prompt 4A](04-practice-test-analysis.md)).

```text
You are a CompTIA Network+ instructor. Below is my miss log from a practice exam.
Write a {{MINUTES}}-minute audio drill that fixes these specific gaps.

For each miss:
1. [A] states the concept as a scenario question (do NOT copy the practice-exam question; write a fresh scenario that tests the same concept).
2. [PAUSE 5]
3. [B] gives the answer, then explains why, then names the wrong answer I chose and why it was tempting but wrong.
Group related misses together. If several misses share a root cause, say so out loud and teach the root cause once.
End with a rapid-fire round: every concept once more as a short question, [PAUSE 3], short answer.

MISS LOG:
{{PASTE MISS LOG ROWS}}

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 2D — "Confusion killers"

**Use it for:** type-D misses. Look-alike pairs.

```text
Write a {{MINUTES}}-minute audio script called "Confusion Killers" for CompTIA Network+ N10-009.
Cover these pairs: {{e.g. RPO vs RTO; IDS vs IPS; SFTP vs FTPS; NAT vs PAT; Layer 2 vs Layer 3 switch; 802.11ac vs 802.11ax; TACACS+ vs RADIUS; hot site vs warm site vs cold site}}.
If I don't list pairs, choose the 12 most commonly confused pairs on N10-009.

For each pair:
- [A] names the pair and asks for the one difference that matters on the exam. [PAUSE 4]
- [B] gives that difference in one sentence, then a memory hook, then a one-sentence scenario showing when each applies.
Finish with a lightning round: [A] gives a scenario, [PAUSE 3], [B] names which one of the pair it is.

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 2E — Two-host podcast episode

**Use it for:** long drives. Easier to listen to for an hour than a drill.

```text
Write a {{MINUTES}}-minute two-host podcast episode on {{DOMAIN OR TOPIC}} for CompTIA Network+ N10-009.
[A] is a curious junior tech. [B] is a senior network engineer with field stories.
[A] asks questions a real student would ask, including wrong guesses that [B] gently corrects.
Every 3 minutes, [B] turns to the listener: "Pause and answer this one yourself." then a question, [PAUSE 5], then the answer.
Stories must be realistic but generic. No real company names.
Close with [B] giving "the three things you must know for the exam" on this topic.

{{PASTE SHARED RULES BLOCK}}
```

## Prompt 2F — Convert my notes to an audio script

```text
Convert the notes below into an audio drill script. Keep every fact. Drop anything that only works visually and list what you dropped at the very end under "// DROPPED:" so I can study it at a desk.

{{PASTE NOTES}}

{{PASTE SHARED RULES BLOCK}}
```
