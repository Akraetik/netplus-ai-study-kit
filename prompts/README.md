# Prompt Library

Copy-paste prompts for any capable chat model: Claude, ChatGPT, Gemini, Copilot, or a local model. Each prompt says what to paste in and what you get back.

| File | Use it when |
|---|---|
| [01-planning.md](01-planning.md) | You're starting. You want a day-by-day calendar. |
| [02-audio-scripts.md](02-audio-scripts.md) | You want MP3 drills for the car. |
| [03-flashcards.md](03-flashcards.md) | You want Anki cards as CSV. |
| [04-practice-test-analysis.md](04-practice-test-analysis.md) | You just finished a practice test. |
| [05-tutor-and-drills.md](05-tutor-and-drills.md) | You're stuck on a concept, or want subnetting and PBQ practice. |

## How to get good output

1. **Give it the objectives.** Paste the relevant section of the official CompTIA N10-009 objectives PDF. Models know Network+, but they drift between exam versions. The objectives keep them on N10-009.
2. **Work in chunks.** One objective or one domain at a time. Long outputs get sloppy at the end.
3. **Keep the conversation.** Run the planning, analysis, and card prompts in the same chat so the model remembers your weak spots.
4. **Always run the fact-check prompt** ([5E](05-tutor-and-drills.md#prompt-5e--fact-check-generated-material)) on generated material before you study it. Or check numbers yourself.
5. **Fill every `{{PLACEHOLDER}}`.** Delete lines that don't apply.

## Conventions

- `{{DOUBLE_BRACES}}` = replace with your info.
- Output formats are strict (CSV headers, script tags) so the output feeds straight into [`tools/`](../tools/).
- Prompts ask the model to say when it's unsure rather than guess.
