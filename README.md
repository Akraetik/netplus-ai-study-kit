# Network+ AI Study Kit

**Handy dandy lil repo to use your own AI (agnostic) to turn CompTIA Network+ (N10-009) into car audio, Anki flashcards, and a study plan that adapts to your practice-test misses.**

![Exam](https://img.shields.io/badge/CompTIA-Network%2B%20N10--009-c8202f)
![Status](https://img.shields.io/badge/status-building%20in%20public-orange)
![License](https://img.shields.io/badge/code-MIT-green)
![Content](https://img.shields.io/badge/content-CC%20BY--NC--SA%204.0-lightgrey)

I built this system while preparing for Network+. I had a job, a long commute, and little desk time. So I used AI to turn the exam objectives into audio I could drill while driving and flashcards I could review in spare minutes between life. Then I fed my practice-test misses back to the AI and rebuilt the material around my weak spots.

I'm publishing the finished materials and the system that made them, when I have time between doing other things. The system works around your real life. A certificate is just flair to a career and learning track.

I added Anthropic's Claude as a contributor. I used them to create the AI flashcards and Audio. Fair disclosure. A feature not a bug. 

## My Study Log

I passed Network+ (N10-009) on September 24, 2026. This log covers the 22 days before the exam.

Before September 3 I was watching videos and taking in information passively. I don't count that time. The count starts when I began studying on purpose.

### The numbers

| | |
|---|---|
| Window | Sep 3 – Sep 24, 2026 (22 days) |
| Study days | 19 |
| Days off | 3 |
| Total study time | 105 h 15 m |
| Average per study day | 5 h 32 m |

### Time by method

| Method | Time (h:mm) | Share | Days used |
|---|---:|---:|---:|
| Flashcards | 36:15 | 34.4% | 17 |
| Udemy* | 31:00 | 29.5% | 16 |
| AI audio | 16:15 | 15.4% | 6 |
| Practice tests | 8:00 | 7.6% | 6 |
| YouTube* | 7:15 | 6.9% | 4 |
| Podcast | 2:00 | 1.9% | 1 |
| Dion study guide | 2:00 | 1.9% | 1 |
| AI prompting | 1:30 | 1.4% | 3 |
| Reviewing past tests | 1:00 | 1.0% | 1 |
| **Total** | **105:15** | **100%** | **19** |

\* Video time is adjusted for playback speed. I logged video by content length and watched at a mix of 1x and 2x. I count it at 1.5x: content hours ÷ 1.5, rounded down to the nearest 15 minutes. 57 h 45 m of video took 38 h 15 m to watch.

Flashcards took the most time. Flashcards, practice tests and test review together were 45 h 15 m, or 43% of the total.

### How it went

- **Sep 3. Started studying on purpose.** I stopped passively taking in videos. Flashcards every day. Practice tests from Sep 5.
- **Sep 6. Started this repo.** I could see progress with the AI help. I decided to put the setup in a git repo. This was also my first day using AI audio.
- **Sep 7. 76% on practice tests.** I figured I would pass at that point.
- **Sep 9. Job offer.** I got a job offer and mentally dropped everything. Two hours of flashcards that day. Nothing on Sep 10.
- **Sep 11. Back to work.** I studied 12 of the next 14 days. Mostly Udemy and flashcards.
- **Sep 24. Passed.**

## Roadmap

- [x] Project scope and licenses
- [x] The method: define the target, how learning works, study plans
- [x] Tracking templates: miss log, score tracker, study plan
- [x] `make_deck.py` — CSV → Anki deck, with CI
- [x] ~2,000 Anki cards: core, rapid recall, trouble areas, quick decks
- [x] `make_audio.py` — local two-voice TTS for car drills
- [x] Audio drills (GitHub Release)
- [x] Prompt library for any AI model
- [ ] The adaptive loop: practice test → miss log → rebuilt material
- [ ] Exam-week guide and reuse for the next cert
- [ ] v1.0 + video walkthrough
- [x] Add metrics to README

Watch or star the repo to follow along.

## License

Code: [MIT](LICENSE). Study content: [CC BY-NC-SA 4.0](LICENSE-CONTENT.md).

CompTIA and Network+ are trademarks of CompTIA, Inc. This project is independent and not affiliated with or endorsed by CompTIA.
