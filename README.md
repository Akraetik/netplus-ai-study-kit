# Network+ AI Study Kit

**Handy dandy lil repo to use your own AI (agnostic) to turn CompTIA Network+ (N10-009) into car audio, Anki flashcards, and a study plan that adapts to your practice-test misses.**

![Exam](https://img.shields.io/badge/CompTIA-Network%2B%20N10--009-c8202f)
![Status](https://img.shields.io/badge/status-building%20in%20public-orange)
![License](https://img.shields.io/badge/code-MIT-green)
![Content](https://img.shields.io/badge/content-CC%20BY--NC--SA%204.0-lightgrey)

I built this system while preparing for Network+. I had a job, a long commute, and little desk time. So I used AI to turn the exam objectives into audio I could drill while driving and flashcards I could review in spare minutes between life. Then I fed my practice-test misses back to the AI and rebuilt the material around my weak spots.

I'm publishing the finished materials and the system that made them, when I have time between doing other things. The system works around your real life. A certificate is just flair to a career and learning track.

I added Anthropic's Claude as a contributor. I used them to create the AI flashcards and Audio. Fair disclosure. A feature not a bug. 

## Roadmap

- [x] Project scope and licenses
- [x] The method: define the target, how learning works, study plans
- [x] Tracking templates: miss log, score tracker, study plan
- [x] `make_deck.py` — CSV → Anki deck, with CI
- [x] ~2,000 Anki cards: core, rapid recall, trouble areas, quick decks
- [ ] `make_audio.py` — local two-voice TTS for car drills
- [ ] Audio drills (GitHub Release)
- [ ] Prompt library for any AI model
- [ ] The adaptive loop: practice test → miss log → rebuilt material
- [ ] Exam-week guide and reuse for the next cert
- [ ] v1.0 + video walkthrough

Watch or star the repo to follow along.

## License

Code: [MIT](LICENSE). Study content: [CC BY-NC-SA 4.0](LICENSE-CONTENT.md).

CompTIA and Network+ are trademarks of CompTIA, Inc. This project is independent and not affiliated with or endorsed by CompTIA.
