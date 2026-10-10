# Tools

Two small, dependency-light Python tools. Python 3.10+.

```bash
pip install -r tools/requirements.txt
```

| Tool | Input | Output | Guide |
|---|---|---|---|
| `make_deck.py` | Card CSV (`front,back,extra,tags,deck,reverse`) | Anki `.apkg` | [docs/05](../docs/05-flashcard-pipeline.md) |
| `make_audio.py` | Script `.txt` with `[A]`, `[B]`, `[PAUSE n]` | Tagged `.mp3` | [docs/04](../docs/04-audio-pipeline.md) |

`make_audio.py` also needs **ffmpeg** on your PATH and the Kokoro voice model. The optional `--verify` clarity check needs the Parakeet speech recognizer. Download commands are in [docs/04](../docs/04-audio-pipeline.md#install-one-time).

## Try them

```bash
python tools/make_deck.py examples/sample-cards.csv --name "Network+ N10-009::Sample" --out build/sample.apkg

python tools/make_audio.py examples/sample-audio-script.txt \
  --kokoro models/kokoro-en-v0_19 \
  --lexicon examples/lexicon.json \
  --verify models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8 --out build/
```

## Engineering notes

- **Idempotent deck builds.** Deck, model, and note IDs are derived from hashes of their names and front text. Rebuilding never creates duplicates, and re-importing updates cards in place while keeping review history.
- **Resumable audio renders.** Every spoken segment is cached as a NumPy array keyed by a hash of (voice, speaker, speed, text). Kill a long render and rerun it. Edit one line and only that line re-synthesizes.
- **Speech-recognition QA.** With `--verify`, every sentence is transcribed by a local ASR model and scored by word error rate against the script. Sentences at 20% or worse are re-synthesized at alternate speeds and the clearest take wins. The same metric picked the default voices (see [docs/04](../docs/04-audio-pipeline.md#choosing-voices-measure-dont-guess)).
- **Pure local.** No network calls, no API keys. Kokoro runs at about 2× real-time on a two-core laptop CPU.
- **CI.** `.github/workflows/build-decks.yml` lints the tools and builds every CSV in `cards/` on each push.
