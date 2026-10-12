# 05 · Tutor and Drill Prompts

Interactive prompts. Run them in a live chat and answer as you go.

---

## Prompt 5A — Socratic tutor

```text
Act as my CompTIA Network+ N10-009 tutor on {{TOPIC}}.
Don't lecture. Ask me one question at a time, starting easy and getting harder.
After each answer: tell me if I'm right, correct any gap in one or two sentences, then ask the next question.
If I miss two in a row, step back and teach the concept briefly before continuing.
After 10 questions, summarize what I know solidly and what I should turn into flashcards.
```

## Prompt 5B — Subnetting drill

```text
Give me IPv4 subnetting practice for CompTIA Network+.
One problem at a time. Mix these types:
- Given an IP and CIDR, find network address, broadcast address, first and last usable host.
- Given a host requirement, pick the smallest CIDR.
- Given a subnet mask, convert to CIDR and back.
- Are these two hosts on the same subnet?
Wait for my answer. Then show the fastest mental method (block size / magic number), not binary long-hand, unless I ask.
Track my accuracy. After 10 problems, report my score and the type I'm weakest on.
```

## Prompt 5C — Performance-based question simulator

```text
Simulate a CompTIA Network+ N10-009 performance-based question (PBQ) on {{TOPIC e.g. "configure VLANs and a trunk on a switch", "match cable types to use cases", "order the troubleshooting steps", "place devices in a network diagram", "read a routing table"}}.
Describe the scenario, the exhibit (as text or an ASCII diagram), and exactly what I must do.
Let me answer fully before you grade.
Grade each part, explain what a partial-credit answer would have missed, and give me a harder variant.
```

## Prompt 5D — Explain it like…

```text
Explain {{CONCEPT}} for CompTIA Network+ at three levels:
1. To a 12-year-old, with an analogy.
2. To a help-desk tech.
3. At exact exam depth, with the terms CompTIA uses.
Finish with the one sentence I should remember for exam day.
```

## Prompt 5E — Fact-check generated material

Run this on every script and CSV before you study it. Better: run it in a **different** model than the one that wrote the material.

```text
You are a meticulous CompTIA Network+ N10-009 technical reviewer.
Check the material below for factual errors. Focus on: port numbers and transport protocols, IEEE standards and their speeds/frequencies, cable categories and distances, PoE wattages, OSI layer assignments, protocol behavior, and CompTIA's exact troubleshooting methodology steps.
Also flag anything that is NOT on the N10-009 objectives.
Return a table: Location | Claim | Problem | Correct version | Confidence (high/medium/low).
If nothing is wrong, say so. Do not rewrite anything that is correct.

{{PASTE SCRIPT OR CSV}}
```

## Prompt 5F — Lab ideas with free tools

```text
Suggest {{N}} hands-on labs for CompTIA Network+ N10-009 using only free tools (Cisco Packet Tracer, GNS3, Wireshark, VirtualBox, and built-in OS commands).
For each lab: objective(s) covered, time needed, step-by-step setup, what to observe, and three questions to answer afterward.
Prioritize my weak areas: {{LIST}}.
```
