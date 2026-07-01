<p align="center">
  <img src="TinyTTS.png" alt="TinyTTS" width="480"/>
</p>

<h1 align="center">TinyTTS</h1>

<p align="center">
  <b>Ultra-lightweight English Text-to-Speech — only 1.6M parameters, ~3.4 MB ONNX</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/tiny-tts/"><img src="https://img.shields.io/pypi/v/tiny-tts?label=PyPI&color=blue" alt="PyPI"></a>
  <a href="https://pypi.org/project/tiny-tts/"><img src="https://img.shields.io/pypi/dm/tiny-tts?label=PyPI%20downloads&color=blue" alt="PyPI Downloads"></a>
  <a href="https://www.npmjs.com/package/tiny-tts"><img src="https://img.shields.io/npm/v/tiny-tts?label=npm&color=green" alt="npm"></a>
  <a href="https://www.npmjs.com/package/tiny-tts"><img src="https://img.shields.io/npm/dm/tiny-tts?label=npm%20downloads&color=green" alt="npm Downloads"></a>
  <a href="https://huggingface.co/spaces/backtracking/tiny-tts-demo">
    <img src="https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md-dark.svg" alt="Open in Spaces">
  </a>
</p>

---

## Highlights

TinyTTS is an end-to-end text-to-speech model that delivers natural-sounding speech with a fraction of the resources required by conventional TTS systems.

| Metric | TinyTTS | Typical TTS Models |
|---|---|---|
| **Parameters** | **~1.6M** | 50M–200M+ |
| **Checkpoint size** | **~3.4 MB** (ONNX FP16) | 200 MB–1 GB+ |
| **Sample rate** | 44.1 kHz | 22.05–44.1 kHz |
| **End-to-end** | Yes | Often requires separate vocoder |

With only **1.6 million parameters** and an ONNX model of just **~3.4 MB** (FP16), TinyTTS runs comfortably on CPU-only machines, edge devices, and embedded systems — making real-time speech synthesis accessible without a GPU.

## Installation

### Python (PyPI)

```bash
pip install tiny-tts
```

> **PyPI**: [https://pypi.org/project/tiny-tts/](https://pypi.org/project/tiny-tts/)

Or install from source:

```bash
git clone https://github.com/tronghieuit/tiny-tts.git
cd tiny-tts
pip install -e .
```

After installing, the `tiny-tts` command is available globally:

```bash
tiny-tts --checkpoint G.pth --text "Hello world" --device cuda
```

### Node.js (npm)

```bash
npm install tiny-tts
```

> **npm**: [https://www.npmjs.com/package/tiny-tts](https://www.npmjs.com/package/tiny-tts)

Pure Node.js inference via ONNX Runtime — **zero Python dependency**. The ONNX model (~6 MB) is auto-downloaded from HuggingFace on first use.

### Dependencies (Python, source install only)

```bash
pip install torch torchaudio soundfile g2p-en transformers numba
```

---

## Quick Start (Python)

> Installed from npm? The CLI takes different flags there.
See [CLI (Node.js)](#cli-nodejs) below.

### Basic inference

```bash
tiny-tts \
  --text "The weather is nice today, and I feel very relaxed." \
  --checkpoint G.pth \
  --output output.wav \
  --speaker MALE \
  --speed 1.0 \
  --device cuda
```

### CPU inference

```bash
tiny-tts \
  --text "The weather is nice today, and I feel very relaxed." \
  --checkpoint G.pth \
  --device cpu
```

Output files are saved to `infer_outputs/`.

---

## Python API

You can easily use TinyTTS directly in your Python code:

```python
from tiny_tts import TinyTTS

# Initialize the TTS model (auto-detects device and downloads default checkpoint if missing)
tts = TinyTTS()
# OR specify a custom checkpoint: tts = TinyTTS(checkpoint_path="...")

# Synthesize a single sentence
tts.speak("Hello, this is a test of the Python API.", output_path="hello.wav")

# Adjust speech speed (1.0=normal, 1.5=faster, 0.7=slower)
tts.speak("This is faster speech.", output_path="fast.wav", speed=1.5)
tts.speak("This is slower speech.", output_path="slow.wav", speed=0.7)

# Synthesize a long paragraph (5 sentences)
paragraph = (
    "TinyTTS is an ultra-lightweight text-to-speech model. "
    "It has only one point six million parameters, which makes it extremely fast. "
    "You can run it easily on your local CPU without a dedicated graphics card. "
    "The audio quality remains surprisingly clear despite the small model size. "
    "I hope you enjoy building exciting applications with it!"
)
tts.speak(paragraph, output_path="paragraph.wav")
```

---

## Inference Benchmarks

Benchmarked on real hardware with the sentence:  
*"The weather is nice today, and I feel very relaxed."* (~4.9s of audio at 44.1kHz)

- **CPU**: Intel Core (laptop, no GPU)
- **PyTorch**: 2.5.1+cu121
- **Model**: 1.62M parameters

| Backend | Synthesis Time | Audio | RTFx |
|:---|---:|---:|---:|
| **ONNX Runtime (CPU)** | **92 ms** | 4.88s | **~53x** 🚀 |
| PyTorch (CPU) | 272 ms | 4.88s | ~18x |

> RTFx = Audio Duration ÷ Synthesis Time (higher = faster).  
> With only 1.62M params, TinyTTS synthesizes ~5s of 44.1kHz audio in **92ms via ONNX** — approximately **53× real-time** on a laptop CPU.

---

## Comparison with Other TTS Engines

All numbers are **CPU-only inference** benchmarked on the **same machine** (Intel Core laptop, no GPU).  
Text: *"The weather is nice today, and I feel very relaxed."*  
Protocol: 5 warm-up runs + 20 timed runs (median). Model load time excluded.

| ENGINE | Params | TTFA (ms) | TOTAL (s) | AUDIO (s) | RTFx | 🔊 |
|:---|---:|---:|---:|---:|---:|:---:|
| **TinyTTS (ONNX)** | **1.6M** | **86** | **0.092** | **4.88** | **~53x 🚀** | [▶](samples/tinytts.wav) |
| Piper (ONNX, 22kHz) | ~63M | 114 | 0.112 | 2.91 | ~26x | [▶](samples/piper.wav) |
| **TinyTTS (PyTorch)** | **1.6M** | **295** | **0.272** | **4.88** | **~18x** | [▶](samples/tinytts.wav) |
| KittenTTS nano | ~10M | 298 | 0.286 | 4.87 | ~17x | [▶](samples/kittentts_nano.wav) |
| Supertonic (2-step) | ~82M | 260 | 0.249 | 3.69 | ~15x | [▶](samples/supertonic.wav) |
| Pocket-TTS | 100M | 1055 | 0.928 | 3.68 | ~4x | [▶](samples/pocket_tts.wav) |
| Kokoro ONNX | 82M | 943 | 0.933 | 3.16 | ~3x | [▶](samples/kokoro.wav) |
| KittenTTS mini | ~25M | 1965 | 2.047 | 4.17 | ~2x | [▶](samples/kittentts_mini.wav) |

> **TTFA** = Time To First Audio. **RTFx** = Audio Duration ÷ Synthesis Time (higher = faster).  
> ⚠️ Output sample rates differ: Piper 22kHz, KittenTTS 24kHz, TinyTTS/Supertonic 44.1kHz.  
> **TinyTTS achieves the best speed-to-size ratio**: only **1.6M params** / **3.4 MB** ONNX yet ~53× real-time at 44.1kHz.

### CPU vs GPU vs ONNX Summary

```text
Backend          | Synthesis Time | Audio  | RTFx
-----------------|----------------|--------|----------
CPU (ONNX)       | 0.092 s        | 4.88s  | ~53x 🚀
CPU (PyTorch)    | 0.272 s        | 4.88s  | ~18x
GPU (CUDA, est.) | ~0.015 s       | 4.88s  | ~325x
```

> **ONNX Runtime** is the recommended backend for CPU deployment — it provides **~3× speedup** over PyTorch eager mode by fusing ops and eliminating Python dispatch overhead.

### Run benchmarks yourself

```bash
python benchmark.py
```

> Compares TinyTTS (PyTorch + ONNX) against Piper, Kokoro, KittenTTS, Pocket-TTS and Supertonic on CPU.

---

## CLI Arguments

| Argument | Short | Default | Description |
|---|---|---|---|
| `--text` | `-t` | *"The weather is nice today..."* | Text to synthesize |
| `--checkpoint` | `-c` | *(optional)* | Path to `G.pth`. Auto-downloads if omitted. |
| `--output` | `-o` | `output.wav` | Output audio filename |
| `--speaker` | `-s` | `MALE` | Speaker ID |
| `--speed` | | `1.0` | Speech speed (1.0=normal, 1.5=faster, 0.7=slower) |
| `--device` | | `cuda` | Device: `cuda` or `cpu` |

---

## Project Structure

```
tiny-tts/
├── infer.py                  # Main inference script
├── TinyTTS.png               # Project logo
├── setup.py                  # Package setup (pip install)
├── pyproject.toml            # Build configuration
├── G.pth              # Pre-trained checkpoint (FP16: ~17 MB)
├── tinytts_fp16.onnx         # ONNX FP16 model (~3.4 MB)
├── models/
│   └── synthesizer.py        # Model definition
├── nn/
│   ├── attentions.py         # Attention layers
│   ├── modules.py            # Neural network modules
│   ├── commons.py            # Utility functions
│   └── transforms.py         # Flow transforms
├── text/
│   ├── english.py            # English G2P pipeline
│   ├── symbols.py            # Phoneme symbol tables
│   ├── cmudict.rep           # CMU Pronouncing Dictionary
│   └── english_utils/        # Text normalization
├── alignment/
│   └── core.py               # Viterbi alignment
└── utils/
    └── config.py             # Model hyperparameters
```

---

## Node.js API

```javascript
const TinyTTS = require('tiny-tts');

const tts = new TinyTTS();
await tts.speak('Hello world!', 'output.wav');

// With options
await tts.speak('Fast speech test.', {
  output: 'fast.wav',
  speaker: 'MALE',
  speed: 1.5
});

await tts.dispose();
```

### CLI (Node.js)

```bash
npx tiny-tts "Hello world" -o hello.wav
```

---

## Python vs Node.js G2P Comparison

Both the Python (PyPI) and Node.js (npm) packages share the same ONNX model and CMU pronunciation dictionary (123,463 entries). The G2P (Grapheme-to-Phoneme) pipelines were tested on **542 diverse sentences** spanning everyday conversation, academic/scientific text, technical vocabulary, tongue twisters, and complex compound sentences.

| | Python (PyPI) | Node.js (npm) |
|---|---|---|
| **G2P backend** | BERT tokenizer + g2p_en + full CMU dict | Apostrophe-aware split + neural G2P + full CMU dict |
| **CMU dict entries** | ~123K (NLTK cmudict + syllable boundaries) | 123K (merged NLTK + cmudict.rep) |
| **Unknown word fallback** | `g2p_en` neural model (GRU seq2seq) | Ported `g2p_en` neural model (identical weights) |
| **Model** | PyTorch / ONNX | ONNX only |
| **Phone ID match rate** | — | **100%** exact match (542/542 sentences) ✅ |

> Since v5.0.0, the Node.js package includes a **pure-JS port of the g2p_en neural G2P model** (GRU encoder-decoder, ~4.4 MB weights), achieving **100% phoneme-level match** with the Python implementation across all 542 test sentences.

---

## TODO

- [ ] Public source code for training
- [ ] Add more English speakers
- [ ] Add ultra-lightweight zero-shot voice cloning
- [x] Release an even smaller model version while maintaining high accuracy

---

## Links

- **PyPI**: [https://pypi.org/project/tiny-tts/](https://pypi.org/project/tiny-tts/)
- **npm**: [https://www.npmjs.com/package/tiny-tts](https://www.npmjs.com/package/tiny-tts)
- **HuggingFace Model**: [https://huggingface.co/backtracking/tiny-tts](https://huggingface.co/backtracking/tiny-tts)
- **HuggingFace Demo**: [https://huggingface.co/spaces/backtracking/tiny-tts-demo](https://huggingface.co/spaces/backtracking/tiny-tts-demo)

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=tronghieuit/tiny-tts&type=Date)](https://star-history.com/#tronghieuit/tiny-tts&Date)
