# Audio Course

About **3 hours 13 minutes of car-ready MP3s** for CompTIA Network+ N10-009. Questions pause so you can **answer out loud** before you hear the answer.

**Download:** the MP3s are attached to the [Releases page](../../../releases/latest), not stored in the repo. That keeps the repo small to clone. The scripts are here in [`scripts/`](scripts/), so you can read along, fix a line, or re-render any track.

## Tracks

**Protocol course** (one voice)

| # | Track | Length |
|---|---|---|
| 01 | Orientation: how the course works | 3.2 min |
| 02 | Ports, part 1 (the official port list) | 8.6 min |
| 03 | Ports, part 2 | 9.2 min |
| 04 | Port drill: pure recall, both directions | 9.6 min |
| 05 | Core protocols: TCP, UDP, ICMP, GRE, IPsec | 10.2 min |
| 06 | Addressing and name resolution: ARP, NDP, DHCP, DNS | 13.7 min |
| 07 | Routing | 11.5 min |
| 08 | Switching and VLANs | 11.5 min |
| 09 | Security and AAA | 12.7 min |
| 10 | Management, monitoring, and voice | 11.8 min |
| 11 | Confusion killers: the pairs people mix up | 18.1 min |
| 12 | Final drill: 50 questions | 11.9 min |

**Domain drills** (two voices: one asks, one answers and explains why the wrong options are wrong)

| # | Track | Length |
|---|---|---|
| 13 | Domain 2 Implementation, part 1: routing, NAT, FHRP, QoS | 15.5 min |
| 14 | Domain 2 Implementation, part 2: switching, wireless, power | 14.3 min |
| 15 | Domain 5 Troubleshooting, part 1: method, physical layer, tools | 14.5 min |
| 16 | Domain 5 Troubleshooting, part 2: switching, IP, performance, wireless | 15.5 min |
| 00 | Sample: secure swaps drill (built from examples/) | 1.6 min |

Tracks 13–16 are 100 questions on the two domains most candidates find hardest: **Implementation** and **Troubleshooting**. Track 11 is the best single track if you're short on time.

## How to listen

1. Put the files on your phone or a USB stick. Track numbers are in the MP3 tags, so they play in order.
2. **Answer out loud in every pause.** That's the whole trick. Passive listening does little.
3. Replay on a schedule: day 1, 2, 4, 7.
4. After each practice test, make a drill from your own misses with [Prompt 2C](../prompts/02-audio-scripts.md#prompt-2c--miss-driven-drill). That's the most useful track you'll ever hear.

## How these were made

1. AI wrote each script for the ear, using the prompts in [`prompts/02-audio-scripts.md`](../prompts/02-audio-scripts.md). Numbers are spoken the way techs say them, and every drill question has a pause.
2. [`tools/make_audio.py`](../tools/make_audio.py) rendered them locally with Kokoro voices **am_michael** (asks) and **bm_george** (answers).
3. A local speech recognizer transcribed each sentence of four or more words and compared it to the script. Any sentence it misheard by 20% or more was re-rendered, and the clearest take was kept.
4. The lines still flagged after that were reviewed by reading the recognizer's transcripts.

**QA numbers for this release:** 2,727 sentences checked. 32 re-rendered automatically. 42 still flagged. Review showed most of those were spelling differences in the transcript ("TACAX Plus", "Multi-factor"), not unclear speech. The review also caught four real fixes: "IPSec" was mispronounced (17 times across the course), "CompTIA" was read letter by letter, one long line lost its middle phrase, and two lines contained homophone traps ("a PDU in a rack" heard as "in Iraq"). Those were fixed and the affected tracks re-rendered.

**Version 1 had a problem.** The first render used two Piper voices, and some lines came out slurred. The voices were swapped after a measured comparison. See [how the voices were chosen](../docs/04-audio-pipeline.md#choosing-voices-measure-dont-guess).

## Make your own

See [docs/04 — Audio pipeline](../docs/04-audio-pipeline.md). Short version:

```bash
pip install -r tools/requirements.txt
python tools/make_audio.py audio/scripts/04_port_drill.txt --kokoro models/kokoro-en-v0_19 --out build/
```

## Credits

Voices: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache 2.0), run through [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx). Clarity check: NVIDIA [Parakeet TDT 0.6B v2](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2) (CC BY 4.0).
