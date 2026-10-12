#!/usr/bin/env python3
"""
make_audio.py — turn an AI-written study script into a tagged MP3 you can play in the car.

Runs 100% locally. No API keys. No per-minute fees.
Default voices: Kokoro (via sherpa-onnx). Piper voices also work.
Optional: --verify checks every sentence with a local speech recognizer and
re-renders any sentence it can't understand.

Script format (plain text, one directive or paragraph per block):

    # TITLE: Track 04 - Port Drill
    [A] What port does SSH use?
    [PAUSE 4]
    [B] Twenty-two. TCP. SSH replaced Telnet on twenty-three.

    Paragraphs with no [A]/[B] tag are read by voice A.
    [PAUSE n] inserts n seconds of silence: your time to answer out loud.
    Lines starting with // are comments and are skipped.

Usage:
    python tools/make_audio.py script.txt --kokoro models/kokoro-en-v0_19
    python tools/make_audio.py scripts/*.txt --kokoro models/kokoro-en-v0_19 \\
        --voice-a am_michael --voice-b bm_george \\
        --lexicon examples/lexicon.json --verify models/parakeet --out audio/
    python tools/make_audio.py script.txt --piper voices/en_US-lessac-high.onnx

Segments are cached by content hash in .tts-cache/, so an interrupted run
resumes where it stopped and an edited script only re-renders what changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

try:
    import numpy as np
except ImportError:  # pragma: no cover
    sys.exit("Missing dependencies. Run: pip install -r tools/requirements.txt")

TAG = re.compile(r"^\[(A|B)\]\s*", re.I)
PAUSE = re.compile(r"^\[PAUSE\s+(\d+(?:\.\d+)?)\]$", re.I)
TITLE = re.compile(r"^#\s*TITLE:\s*(.+)$", re.I)
BREATH_SEC = 0.45      # silence between paragraphs
SENTENCE_GAP = 0.18    # silence between sentences
FLAG_WER = 0.20        # --verify: re-render a sentence if >= 20% of its words are misheard
RETRY_SPEEDS = (0.90, 1.0, 0.85)

# Kokoro v0.19 speaker ids
KOKORO = {"af": 0, "af_bella": 1, "af_nicole": 2, "af_sarah": 3, "af_sky": 4, "am_adam": 5,
          "am_michael": 6, "bf_emma": 7, "bf_isabella": 8, "bm_george": 9, "bm_lewis": 10}


# --------------------------------------------------------------------------- script parsing
def parse_script(text: str) -> tuple[str | None, list[tuple[str, str | float]]]:
    """Return (title, [(kind, value)]) where kind is 'A', 'B' or 'PAUSE'."""
    title, blocks = None, []
    for raw in re.split(r"\n\s*\n", text.strip()):
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip() and not ln.strip().startswith("//")]
        if not lines:
            continue
        first = lines[0]
        if m := TITLE.match(first):
            title = m.group(1).strip()
            lines = lines[1:]
            if not lines:
                continue
            first = lines[0]
        if m := PAUSE.match(first):
            blocks.append(("PAUSE", float(m.group(1))))
            continue
        voice = "A"
        if m := TAG.match(first):
            voice = m.group(1).upper()
            lines[0] = TAG.sub("", first)
        blocks.append((voice, " ".join(lines)))
    return title, blocks


ACRONYM = re.compile(r"\b([A-Z]{2,6})(s?)\b")


def apply_lexicon(text: str, lexicon: dict[str, str], spell: bool = True) -> str:
    """Swap written forms for spoken forms (longest keys first), then spell out any
    remaining all-caps acronym letter by letter: 'EIGRP' -> 'E I G R P'."""
    for written in sorted(lexicon, key=len, reverse=True):
        text = re.sub(rf"(?<![\w-]){re.escape(written)}(?![\w+-])", lexicon[written], text)
    if spell:
        text = ACRONYM.sub(lambda m: " ".join(m.group(1)) + ("'s" if m.group(2) else ""), text)
    return text


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.?!])\s+", text) if s]


# --------------------------------------------------------------------------- engines
class Kokoro:
    def __init__(self, model_dir: Path):
        import sherpa_onnx
        d = model_dir
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=str(d / "model.onnx"), voices=str(d / "voices.bin"),
                    tokens=str(d / "tokens.txt"), data_dir=str(d / "espeak-ng-data")),
                num_threads=2),
            max_num_sentences=1)
        self.tts = sherpa_onnx.OfflineTts(cfg)
        self.rate = self.tts.sample_rate

    def speak(self, text: str, voice: str, speed: float) -> np.ndarray:
        sid = KOKORO[voice] if voice in KOKORO else int(voice)
        return np.asarray(self.tts.generate(text, sid=sid, speed=speed).samples, dtype=np.float32)


class Piper:
    def __init__(self, model: Path):
        from piper import PiperVoice
        self.voice = PiperVoice.load(str(model))
        self.rate = self.voice.config.sample_rate

    def speak(self, text: str, voice: str, speed: float) -> np.ndarray:
        from piper import SynthesisConfig
        sid = int(voice) if str(voice).isdigit() else None  # None = single-speaker model
        cfg = SynthesisConfig(speaker_id=sid, length_scale=1.0 / speed)
        return np.concatenate([c.audio_int16_array for c in self.voice.synthesize(text, cfg)]).astype(np.float32) / 32768


# --------------------------------------------------------------------------- verification
class Verifier:
    """Local speech recognizer (NVIDIA Parakeet TDT via sherpa-onnx) used as an intelligibility check."""

    def __init__(self, model_dir: Path):
        import sherpa_onnx
        d = model_dir
        enc = next(d.glob("encoder*.onnx"))
        self.rec = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=str(enc), decoder=str(next(d.glob("decoder*.onnx"))),
            joiner=str(next(d.glob("joiner*.onnx"))), tokens=str(d / "tokens.txt"),
            model_type="nemo_transducer", num_threads=2)

    def hear(self, audio: np.ndarray, rate: int) -> str:
        if rate != 16000:
            n = int(len(audio) * 16000 / rate)
            audio = np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio).astype(np.float32)
        s = self.rec.create_stream()
        s.accept_waveform(16000, audio)
        self.rec.decode_stream(s)
        return s.result.text


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _num(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " " + ("" if n % 100 == 0 else _num(n % 100))
    if n < 10000 and n % 100:                 # ports are said in pairs: 5060 -> "fifty sixty"
        return _num(n // 100) + " " + _num(n % 100)
    if n < 10000 and n % 1000:                # 4500 -> "forty five hundred"
        return _num(n // 100)
    return _num(n // 1000) + " thousand " + ("" if n % 1000 == 0 else _num(n % 1000))


def _words(t: str) -> list[str]:
    t = re.sub(r"\bvs\b\.?", " versus ", t.lower())
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)                     # 16,000 -> 16000
    t = re.sub(r"'s\b", "", t)                                  # possessives: "SSH's" == "S S H's"
    t = re.sub(r"(?<=\d)-(?=\d)", " dash ", t).replace("-", " ")
    t = re.sub(r"\b0+(?=\d)", lambda m: " zero " * len(m.group()), t)  # "009" -> "zero zero nine"
    t = t.replace("/", " slash ").replace("+", " plus ").replace("%", " percent")
    t = re.sub(r"(?<=\d)\.(?=\d)", " dot ", t)
    t = re.sub(r"\d+", lambda m: f" {_num(int(m.group()))} " if len(m.group()) < 7 else m.group(), t)
    t = re.sub(r"[.,;:?!()]", " | ", t)                          # punctuation ends a spelled-out acronym
    w = re.sub(r"[^a-z'| ]", " ", t).replace("'", "").split()
    out, run = [], []
    for x in w + ["|"]:             # "s s h" and "ssh" compare equal; a lone "a" or "i" stays a word
        if len(x) == 1 and x != "|":
            run.append(x)
            continue
        if run:
            out += ["".join(run)] if len(run) > 1 or run[0] not in ("a", "i") else run
            run = []
        if x != "|":
            out.append(x)
    return [x for x in out if x not in ("hundred", "and", "uh", "um")]


def word_error_rate(ref: str, hyp: str) -> float:
    r, h = _words(ref), _words(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = d[j]
            d[j] = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev = cur
    return d[len(h)] / max(1, len(r))


# --------------------------------------------------------------------------- rendering
class Renderer:
    def __init__(self, engine, voices: dict, speed: float, lexicon: dict, cache: Path,
                 verifier: Verifier | None, spell: bool = True):
        self.engine, self.voices, self.speed, self.lexicon, self.spell = engine, voices, speed, lexicon, spell
        self.cache, self.verifier = cache, verifier
        self.rate = engine.rate
        self.stats = {"sentences": 0, "retried": 0, "flagged": []}
        cache.mkdir(parents=True, exist_ok=True)

    def _synth(self, text: str, voice: str, speed: float) -> np.ndarray:
        key = hashlib.sha1(f"{type(self.engine).__name__}|{voice}|{speed}|{text}".encode()).hexdigest()
        hit = self.cache / f"{key}.npy"
        if hit.exists():
            return np.load(hit)
        audio = self.engine.speak(text, voice, speed)
        np.save(hit, audio)
        return audio

    def paragraph(self, who: str, text: str) -> np.ndarray:
        voice, parts = self.voices[who], []
        for sent in sentences(text):
            spoken = apply_lexicon(sent, self.lexicon, self.spell)
            audio = self._synth(spoken, voice, self.speed)
            self.stats["sentences"] += 1
            if self.verifier and len(sent.split()) >= 4:
                # score against the spoken form, so "IPv4" -> "I P version four" isn't counted as an error
                best = (self._score(spoken, audio), audio)
                for sp in RETRY_SPEEDS:
                    if best[0] < FLAG_WER:
                        break
                    alt = self._synth(spoken, voice, sp)
                    score = self._score(spoken, alt)
                    if score < best[0]:
                        best = (score, alt)
                if best[1] is not audio:
                    self.stats["retried"] += 1
                if best[0] >= FLAG_WER:
                    self.stats["flagged"].append(sent)
                audio = best[1]
            parts += [audio, self.silence(SENTENCE_GAP)]
        return np.concatenate(parts)

    def _score(self, spoken: str, audio: np.ndarray) -> float:
        """Word error rate of what the recognizer heard vs. what we asked the voice to say.
        The transcript goes through the same lexicon, so "SSH" and "S S H" compare equal."""
        heard = apply_lexicon(self.verifier.hear(audio, self.rate), self.lexicon, self.spell)
        return word_error_rate(spoken, heard)

    def silence(self, seconds: float) -> np.ndarray:
        return np.zeros(int(self.rate * seconds), dtype=np.float32)


def render(path: Path, r: Renderer, out_dir: Path, album: str, artist: str, bitrate: str) -> Path:
    title, blocks = parse_script(path.read_text(encoding="utf-8"))
    title = title or path.stem.replace("_", " ").title()
    parts = []
    for kind, value in blocks:
        if kind == "PAUSE":
            parts.append(r.silence(value))
        else:
            parts += [r.paragraph(kind, value), r.silence(BREATH_SEC)]
    audio = np.concatenate(parts) if parts else r.silence(1)
    audio = audio / max(1e-6, float(np.abs(audio).max())) * 0.89

    out_dir.mkdir(parents=True, exist_ok=True)
    wav_path = r.cache / f"{path.stem}.wav"
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(r.rate)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())

    mp3_path = out_dir / f"{path.stem}.mp3"
    track = re.match(r"^(\d+)", path.stem)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path),
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(r.rate),
           "-codec:a", "libmp3lame", "-b:a", bitrate,
           "-metadata", f"title={title}", "-metadata", f"album={album}", "-metadata", f"artist={artist}"]
    if track:
        cmd += ["-metadata", f"track={int(track.group(1))}"]
    subprocess.run(cmd + [str(mp3_path)], check=True)
    wav_path.unlink(missing_ok=True)
    print(f"{mp3_path.name:40s} {len(audio) / r.rate / 60:5.1f} min")
    return mp3_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scripts", nargs="+", type=Path, help="one or more .txt scripts")
    eng = ap.add_mutually_exclusive_group(required=True)
    eng.add_argument("--kokoro", type=Path, help="Kokoro model folder (model.onnx, voices.bin, tokens.txt, espeak-ng-data)")
    eng.add_argument("--piper", type=Path, help="Piper .onnx voice model")
    ap.add_argument("--voice-a", default="am_michael", help="Kokoro voice name, or Piper speaker id")
    ap.add_argument("--voice-b", default="bm_george", help="Kokoro voice name, or Piper speaker id")
    ap.add_argument("--speed", type=float, default=0.95, help="1.0 = normal; 0.95 ≈ 155 wpm")
    ap.add_argument("--lexicon", type=Path, help="JSON map of written -> spoken forms")
    ap.add_argument("--no-spell", action="store_true", help="don't auto-spell ALL-CAPS acronyms")
    ap.add_argument("--verify", type=Path, help="Parakeet ASR model folder; re-renders sentences it can't understand")
    ap.add_argument("--album", default="Network+ N10-009 Audio Course")
    ap.add_argument("--artist", default="netplus-ai-study-kit")
    ap.add_argument("--bitrate", default="64k", help="64k is plenty for speech")
    ap.add_argument("--out", type=Path, default=Path("audio"))
    ap.add_argument("--cache", type=Path, default=Path(".tts-cache"))
    args = ap.parse_args()

    try:
        engine = Kokoro(args.kokoro) if args.kokoro else Piper(args.piper)
        verifier = Verifier(args.verify) if args.verify else None
    except ImportError:
        sys.exit("Missing dependencies. Run: pip install -r tools/requirements.txt")
    voices = {"A": args.voice_a, "B": args.voice_b}
    if args.piper:
        voices = {k: (v if str(v).isdigit() else "") for k, v in voices.items()}
    lexicon = json.loads(args.lexicon.read_text(encoding="utf-8")) if args.lexicon else {}
    r = Renderer(engine, voices, args.speed, lexicon, args.cache, verifier, spell=not args.no_spell)
    for script in sorted(args.scripts):
        render(script, r, args.out, args.album, args.artist, args.bitrate)
    if verifier:
        s = r.stats
        print(f"verified {s['sentences']} sentences · re-rendered {s['retried']} · still unclear {len(s['flagged'])}")
        for f in s["flagged"]:
            print(f"  CHECK: {f}")


if __name__ == "__main__":
    main()
