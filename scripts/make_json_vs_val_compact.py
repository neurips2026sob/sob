"""Compact dumbbell variant of json_vs_val.png.

Each model gets one row: a faded grey segment between Value Accuracy (purple dot)
and JSON Pass (black dot). The segment IS the structured-output hallucination
gap — wider segment = more "valid JSON but wrong values".

Sorted by JSON Pass descending, same source data as the wide bar chart.
"""

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent.parent

# Register Inter so matplotlib resolves it without restart.
_INTER_DIR = Path.home() / ".local/share/fonts/Inter"
for weight in ("Regular", "Medium", "SemiBold", "Bold"):
    f = _INTER_DIR / f"Inter-{weight}.ttf"
    if f.exists():
        fm.fontManager.addfont(str(f))

mpl.rcParams["font.family"] = "Inter"
mpl.rcParams["font.sans-serif"] = ["Inter", "DejaVu Sans"]
# Inter ships kerning/feature tags; tighten letter spacing slightly.
mpl.rcParams["axes.unicode_minus"] = False

MODELS = [
    ("GPT-5.4", "openai-gpt-5-4"),
    ("GPT-5", "openai-gpt-5"),
    ("GPT-5-Mini", "openai-gpt-5-mini"),
    ("GPT-4.1", "openai-gpt-4.1"),
    ("Gemini-2.5-Flash", "gemini-2.5-flash"),
    ("Gemini-3-Flash-Preview", "gemini-3-flash"),
    ("Gemma-3-27B", "gemma-3-27b-it"),
    ("Gemma-4-31B", "gemma-4-31b-it"),
    ("Claude-Sonnet-4.6", "claude-sonnet-4-6"),
    ("GLM-4.7", "zai-org-GLM-4.7"),
    ("Qwen3-235B", "Qwen3-235B-A22B-Instruct-2507"),
    ("Qwen3-30B", "Qwen3-30B-A3B-Instruct-2507"),
    ("Qwen3.5-35B", "Qwen3.5-35B-A3B"),
    ("Phi-4", "phi-4"),
    ("Nemotron-3-Nano-30B", "NVIDIA-Nemotron-3-Nano-30B-A3B-BF16"),
    ("DS-R1-Distill-32B", "DeepSeek-R1-Distill-Qwen-32B"),
    ("Ministral-3-14B", "Ministral-3-14B-Instruct-2512"),
    ("GPT-OSS-20B", "gpt-oss"),
    ("Schematron-8B", "inference-net-Schematron-8B"),
    ("IBM-Granite-4.0", "ibm-granite-4.0-h-small"),
    ("Interfaze-Beta", "interfaze-beta"),
    ("GPT-5.5", "gpt-5.5"),
    ("Claude-Opus-4.6", "claude-opus-4-6"),
    ("Gemini-3.1-Pro", "gemini-3.1-pro-preview"),
    ("Claude-Opus-4.7", "claude-opus-4-7"),
    ("DeepSeek-V4-Pro", "deepseek_deepseek-v4-pro"),
    ("GLM-5.1", "z-ai_glm-5.1"),
    ("Kimi-2.6", "moonshotai_kimi-k2.6"),
]

W = {"text": 13054, "image": 602, "audio": 343}


def load_metric(slug: str, key: str):
    vals = []
    for domain, w in W.items():
        p = REPO / "data" / "evaluation" / domain / slug / "eval_summary.json"
        if not p.exists():
            continue
        m = json.load(open(p))["summary"]["overall_weighted"]["metrics"]
        if key in m:
            vals.append((m[key]["mean"], w))
    if not vals:
        return None
    tw = sum(w for _, w in vals)
    return sum(v * w for v, w in vals) / tw


def main():
    rows = []
    for label, slug in MODELS:
        jp = load_metric(slug, "schema_compliance")
        va = load_metric(slug, "leaf_value_em")
        if jp is None or va is None:
            continue
        rows.append((label, jp * 100, va * 100))
    rows.sort(key=lambda r: -r[1])

    n = len(rows)
    # ~0.24" per row => ~7" tall for 28 rows (vs ~13" before).
    # constrained_layout=True so suptitle centers correctly across the figure
    # without bbox_inches="tight" cropping it asymmetrically.
    fig, ax = plt.subplots(
        figsize=(6.8, 0.24 * n + 1.0), dpi=200, constrained_layout=True
    )

    PURPLE = "#A461E8"
    BLACK = "#111111"
    GAP_GREY = "#E0E0E0"

    for i, (label, jp, va) in enumerate(rows):
        # gap segment between Val.Acc and JSON Pass
        ax.plot(
            [va, jp],
            [i, i],
            color=GAP_GREY,
            linewidth=5,
            solid_capstyle="round",
            zorder=2,
        )
        # dots
        ax.scatter(
            va, i, s=42, color=PURPLE, zorder=4, edgecolors="white", linewidths=0.8
        )
        ax.scatter(
            jp, i, s=42, color=BLACK, zorder=4, edgecolors="white", linewidths=0.8
        )
        # value labels just past the dots, anchored away from the segment
        ax.text(
            va - 0.6,
            i,
            f"{va:.1f}",
            va="center",
            ha="right",
            fontsize=7,
            color=PURPLE,
            fontweight="semibold",
        )
        ax.text(
            jp + 0.6,
            i,
            f"{jp:.1f}",
            va="center",
            ha="left",
            fontsize=7,
            color=BLACK,
            fontweight="semibold",
        )

    # Y axis
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0, pad=4)

    # X axis
    ax.set_xlim(58, 106)
    ax.set_xticks([60, 70, 80, 90, 100])
    ax.set_xticklabels([f"{t}%" for t in (60, 70, 80, 90, 100)], fontsize=7.5)
    ax.tick_params(axis="x", length=3, pad=3)

    # Light vertical grid
    ax.grid(axis="x", which="major", color="#EEEEEE", linewidth=0.6, zorder=1)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#BBBBBB")
    ax.spines["bottom"].set_color("#BBBBBB")
    ax.spines["left"].set_linewidth(0.6)
    ax.spines["bottom"].set_linewidth(0.6)

    # Title centered on the figure. constrained_layout reserves space above
    # the axes for the suptitle and recenters across the cropped output.
    fig.suptitle(
        "JSON Pass Rate vs Value Accuracy",
        fontsize=13,
        fontweight="semibold",
        fontfamily="Inter",
    )

    # Custom legend with the dumbbell vocabulary
    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color=PURPLE,
            linestyle="",
            markersize=6,
            markeredgecolor="white",
            markeredgewidth=0.8,
            label="Value Accuracy",
        ),
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color=BLACK,
            linestyle="",
            markersize=6,
            markeredgecolor="white",
            markeredgewidth=0.8,
            label="JSON Pass",
        ),
        plt.Line2D(
            [0],
            [0],
            color=GAP_GREY,
            linewidth=5,
            solid_capstyle="round",
            label="Hallucination gap",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.02 - 0.6 / (0.24 * n + 1.0)),
        ncol=3,
        frameon=False,
        fontsize=8.5,
        handletextpad=0.6,
        columnspacing=1.6,
    )

    out = REPO / "json_vs_val_compact.png"
    plt.savefig(out, dpi=200, facecolor="white")
    print(f"wrote {out} ({n} models)")


if __name__ == "__main__":
    main()
