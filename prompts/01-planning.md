# 01 · Planning Prompts

## Prompt 1A — Build my study calendar

**Paste in:** your filled-in target template from [docs/01](../docs/01-define-the-target.md).
**You get:** a day-by-day calendar with daily tasks, practice-test dates, and a readiness gate.

```text
You are an experienced CompTIA Network+ instructor and a learning-science coach.

Build me a day-by-day study plan for CompTIA Network+ N10-009.

MY SITUATION
- Target exam date: {{DATE}}
- Today: {{TODAY}}
- Baseline practice-test score: {{SCORE or "not taken yet"}}
- Hours available: weekdays {{H}}, weekends {{H}}, commute {{MIN}} minutes each way
- Background: {{e.g. "A+ certified", "no networking experience", "Army comms"}}
- Resources I have: {{e.g. Professor Messer videos, Dion Training practice exams, Anki, this kit's decks and audio}}
- Known weak areas: {{or "unknown"}}

RULES FOR THE PLAN
1. Weight time by the N10-009 domain weights: 1.0 Concepts 23%, 2.0 Implementation 20%, 3.0 Operations 19%, 4.0 Security 14%, 5.0 Troubleshooting 24%.
2. Every day includes: Anki reviews, one audio block sized to my commute, and one "new learning or practice" block.
3. Put a cold baseline test on day 1 if I haven't taken one.
4. Cover every domain once before the first full practice test.
5. After coverage, schedule a full practice test every 1–2 days, each followed by a 60-minute miss-log review.
6. Subnetting practice by hand at least 4 days a week.
7. Include one rest or light day per week if the timeline is longer than 10 days.
8. End with a readiness gate: three different practice exams >= 85%, no domain < 75%. If the gate isn't met by the target date, say so and recommend how many days to push.

OUTPUT
- A table: Day | Date | Commute audio | Main block | Anki | Practice | Notes
- Then a short list of the 3 biggest risks to this plan and how to reduce each.
- Be realistic. If my hours are too few for my timeline, tell me plainly.
```

## Prompt 1B — Turn my plan into calendar events

**Paste in:** the table from 1A.
**You get:** an `.ics` file you can import into Google Calendar, Outlook, or Apple Calendar.

```text
Convert this study plan into a valid iCalendar (.ics) file.
- One event per study block, with the task in the title and details in the description.
- Commute audio blocks at {{TIME}} and {{TIME}}. Evening blocks at {{TIME}}.
- Time zone: {{e.g. America/Los_Angeles}}.
- Output only the .ics content in one code block so I can save it as study-plan.ics.

{{PASTE PLAN TABLE}}
```

## Prompt 1C — Re-plan after a practice test

**Paste in:** your current plan and the output from [Prompt 4A](04-practice-test-analysis.md).
**You get:** an updated plan for the days you have left.

```text
Here is my current study plan and the diagnosis of my latest practice test.
Rewrite the remaining days so study time shifts toward my weakest areas, weighted by exam weight × miss rate.
Keep daily Anki and commute audio. Keep full practice tests every 1–2 days.
Show only the remaining days, and list what changed and why in 3–5 bullets.

CURRENT PLAN:
{{PASTE}}

DIAGNOSIS:
{{PASTE}}
```
