# 04 · Practice-Test Analysis Prompts

These prompts power the [adaptive loop](../docs/06-adaptive-loop.md). Run them the same day as the test.

---

## Prompt 4A — Diagnose my practice test

**Paste in:** your domain scores and your miss log rows from [`templates/miss-log.csv`](../templates/miss-log.csv).
**You get:** root-cause patterns, a ranked weak-area list, and a 1–3 day remediation plan.

```text
You are a CompTIA Network+ N10-009 instructor and a learning coach. Diagnose my practice test.

TEST: {{name, e.g. "Practice exam 3"}}   DATE: {{date}}   SCORE: {{%}}
DOMAIN SCORES:
1.0 Concepts {{%}} | 2.0 Implementation {{%}} | 3.0 Operations {{%}} | 4.0 Security {{%}} | 5.0 Troubleshooting {{%}}
PREVIOUS TESTS (optional): {{paste score-tracker rows}}
DAYS UNTIL EXAM: {{N}}   HOURS PER DAY: {{N}}

MISS LOG (codes: K knowledge, D discrimination, A application, R reading, P procedure/PBQ, G lucky guess):
{{PASTE ROWS}}

Do the following:
1. PATTERNS: Group misses by domain, objective, and miss code. Look for a shared underlying concept behind misses that look different on the surface (for example, several misses that are all really "DHCP broadcasts don't cross routers"). Name each root concept.
2. MISS-TYPE PROFILE: Give the percentage of each code. Tell me what that profile says about HOW I'm studying, not just what I don't know.
3. PRIORITY LIST: Rank my top 5 weak areas by (exam domain weight × my miss rate in that area). Show the math briefly.
4. REMEDIATION PLAN: A plan for the next {{1–3}} days. Split time by the priority list. Name exactly which cards to make (with counts) and which audio tracks to generate.
5. HANDOFF: Give me the exact inputs to paste into the trouble-area card prompt (3C) and the miss-driven audio prompt (2C).
6. READINESS: Compare against this gate: three different practice exams >= 85%, no domain < 75%. Say how far I am, and whether my exam date is realistic.

Be direct. If my scores are trending the wrong way, say so.
```

## Prompt 4B — Trend across several tests

```text
Here are my scores across practice tests (overall and per domain), plus my miss-type counts per test.
1. Chart the trend as a simple text table.
2. Which domains are improving, flat, or falling?
3. Which miss types are shrinking or growing?
4. Using this rule, tell me how to split tomorrow's study time:
   <70% = priority (40–50% of time), 70–79% = active, 80–89% = maintain, >=90% = coast. Weight by domain exam weight.
5. Am I at risk of overfitting to one vendor's question style? If all my tests come from one source, say so and suggest a mix.

{{PASTE score-tracker.csv}}
```

## Prompt 4C — I didn't pass. Build the retake plan.

```text
I took CompTIA Network+ N10-009 and scored {{SCORE}} (720 needed).
My score report lists these objectives as areas to improve:
{{PASTE OBJECTIVES FROM SCORE REPORT}}

1. Group them by domain and weight them by exam percentage.
2. Tell me which are likely knowledge gaps vs. application gaps, based on how the objective is worded ("Explain" vs "Given a scenario").
3. Build a {{N}}-day retake plan using the adaptive loop: coverage of the weak objectives, new trouble-area cards, audio, and a full practice test every 1–2 days.
4. Give a readiness gate I must hit before rebooking.
Keep it encouraging but honest.
```

## Prompt 4D — Explain one question I still don't get

```text
I missed a practice question on this concept and the explanation didn't click.
Concept (in my words): {{describe it; don't paste the vendor question}}
My answer and why I chose it: {{}}
The correct answer: {{}}

Explain it three ways: (1) in plain language with an everyday analogy, (2) the technical explanation at Network+ depth, (3) a packet-level walk-through of what actually happens on the wire.
Then give me two new scenario questions on the same concept, with answers hidden until I reply.
```
