<div align="center">
  <h1>The Structured Output Benchmark</h1>
  <h3>SOB · A multi-source benchmark for evaluating structured-output quality in LLMs</h3>
</div>

<p align="center">
  <a href="https://huggingface.co/datasets/neurips2026sob/sob">
    <img alt="HF Dataset" src="https://img.shields.io/badge/🤗_Dataset-neurips2026sob/sob-yellow">
  </a>
  <a href="LICENSE">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-blue">
  </a>
</p>

<p align="center">
  <a href="#leaderboard">Leaderboard</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#running-inference">Inference</a> ·
  <a href="#evaluation">Evaluation</a>
</p>

> **Anonymous code release for NeurIPS 2026 Evaluations and Datasets Track double-blind review.**
> Author identities, lab affiliations, and project funding sources are withheld until the review period ends.

---

**SOB** measures **value-level correctness** of LLM-generated JSON, not just *whether the JSON is valid*. We evaluate models across **three source modalities** — text, images, and audio — under a single unified evaluation framework.

## Leaderboard

Top 5 by **Overall** (coverage-adjusted aggregate across text + image + audio):

| Rank | Model              | Overall   | Val. Acc. | Faithful. | JSON Pass | Path Rec. | Str. Cov. | Type Saf. | Perfect |
| :--- | :----------------- | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-----: |
|   1  | **GPT-5.4**        | **0.870** |   0.798   | **0.869** | **0.993** | **0.988** | **0.981** | **0.993** |  0.469  |
|   2  | GLM-4.7            |   0.861   | **0.804** |   0.868   |   0.965   |   0.959   |   0.957   |   0.965   | **0.508** |
|   3  | Qwen3.5-35B        |   0.861   |   0.801   |   0.863   |   0.969   |   0.962   |   0.960   |   0.969   |  0.500  |
|   4  | Gemini-2.5-Flash   |   0.860   |   0.796   |   0.856   |   0.972   |   0.967   |   0.961   |   0.972   |  0.498  |
|   5  | Qwen3-235B         |   0.857   |   0.786   |   0.854   |   0.978   |   0.970   |   0.968   |   0.978   |  0.463  |

Per-modality bests: **text 0.845 (DeepSeek-V4-Pro) · image 0.672 (Gemma-4-31B) · audio 0.237 (Gemini-2.5-Flash)** — see paper Tables 2–4. Perfect Response is aggregated over text + image only.

The full set of evaluated models and per-modality leaderboards are produced from `data/evaluation/` by [`scripts/build_leaderboard.py`](scripts/build_leaderboard.py).

## Quickstart

Load the dataset directly:

```python
from datasets import load_dataset
text  = load_dataset("neurips2026sob/sob", split="test")           # 5,000 records
image = load_dataset("neurips2026sob/sob", "image", split="train") #   209 records
audio = load_dataset("neurips2026sob/sob", "audio", split="train") #   115 records
```

Or run a 5-record smoke test end-to-end:

```bash
make install
export OPENROUTER_API_KEY=...
python -m sob.run --provider openrouter --modality text \
    --model-id google/gemma-4-31b-it --sample-size 5
python evaluate.py data/text_responses/response_google_gemma-4-31b-it.jsonl
```

## Installation

Python 3.12, clean virtualenv:

```bash
uv venv && source .venv/bin/activate
make install
```

`make install` uses `uv sync` if available, otherwise falls back to `pip install -r requirements.txt`. Other targets:

```bash
make format    # ruff format .
make lint      # ruff check .
```

For local vLLM inference (NVIDIA GPU, CUDA 12.8, ≥ 24 GB VRAM):

```bash
uv pip install vllm --extra-index-url https://download.pytorch.org/whl/cu128
```

### API keys

```bash
export OPENROUTER_API_KEY=...
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GEMINI_API_KEY=...
export HF_TOKEN=...               # only if the dataset is private
```

### Git LFS

Response files and per-model evaluations under `data/` are LFS-tracked:

```bash
git lfs install
```

## Running inference

`--modality text` runs the **test** split (5,000 records); `image` and `audio` use the single `train` split for those configs (209 / 115). Omit `--sample-size` for the full run.

**OpenRouter:**

```bash
python -m sob.run --provider openrouter --modality text \
  --model-id google/gemma-4-31b-it --sample-size 100
```

**OpenAI:**

```bash
python -m sob.run --provider openai --modality image --model-id gpt-5
```

**Anthropic:**

```bash
python -m sob.run --provider anthropic --modality audio --model-id claude-sonnet-4-6
```

**Gemini:**

```bash
python -m sob.run --provider gemini --modality text --model-id gemini-2.5-flash
```

**vLLM** (open-weight, your GPU):

```bash
python -m sob.run --provider vllm --modality text \
  --model-id Qwen/Qwen3.5-35B-A3B --use-structured-decoding
```

`--use-structured-decoding` is the schema-constrained ablation from the paper §6.2; the headline leaderboard runs without it.

Outputs:

- `data/text_responses/response_<model>.jsonl`
- `data/images_responses/response_<model>_image.jsonl`
- `data/audio_responses/response_<model>_audio.jsonl`

## Evaluation

Score a single response file:

```bash
python evaluate.py data/text_responses/response_google_gemma-4-31b-it.jsonl
```

Produces `data/evaluation/<modality>/<model>/{eval_records.jsonl, eval_summary.json}` — every paper number is reproducible from these summaries. Or score a whole directory:

```bash
python evaluate.py data/text_responses/                # all response_*.jsonl
python evaluate.py data/audio_responses/ --modality audio
```

## Submitting a new model (post-review)

The leaderboard is rebuilt from `data/evaluation/` by [`scripts/build_leaderboard.py`](scripts/build_leaderboard.py).

1. Run inference + `evaluate.py` for one or more modalities, and drop the resulting `eval_summary.json` files into `data/evaluation/{text,image,audio}/<your_model_dir>/`.
2. Add an entry for `<your_model_dir>` in [`data/evaluation/display_names.json`](data/evaluation/display_names.json). The `_comment` key is ignored — paste your `"<dir>": "<Pretty Name>"` alongside the others.

Preview locally:

```bash
python scripts/build_leaderboard.py --output leaderboard.json
```

## License

[MIT License](LICENSE). Source datasets retain their original licenses: HotpotQA (CC-BY-SA-4.0), AMI Meeting Corpus (CC-BY-4.0), olmOCR-bench / olmOCR (ODC-BY / Apache-2.0).

## Acknowledgments

The HotpotQA team, the AMI Meeting Corpus team, and the Allen AI olmOCR team for releasing their datasets.

## Contact

Author contact details and issue-tracker links are withheld during double-blind review and will be added in the camera-ready version.
