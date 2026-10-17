# Contributing

Thanks for helping. The bar is simple: **accurate, on-objective, and original.**

## Report a wrong fact
Open an issue with the **Content correction** template. Include the file (or deck and card front), what's wrong, and a source: the official N10-009 objectives, an RFC, an IEEE standard, or vendor documentation.

## Improve a prompt
Open a PR that edits the prompt and include one short before/after sample of the output. Say which model you tested with.

## Add cards
1. Put your cards in `cards/<topic>.csv` using the header `front,back,extra,tags,deck,reverse`.
2. Follow the card rules in [docs/05](docs/05-flashcard-pipeline.md).
3. Tag every card with its objective (`obj2.3`) and domain (`domain2`).
4. CI builds every CSV in `cards/` on your PR. Fix any errors it reports.

## Hard rules
- **No practice-exam questions from any vendor**, reworded or not. Write new cards that test the concept.
- **No content from paid courses or books** beyond short factual statements.
- **N10-009 only.** Material from older exams (N10-008) goes in a clearly named separate folder, if at all.

## Adapt it for another cert
Fork it. Rename it. Link back. Tell me, and I'll list it in the README.
