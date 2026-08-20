"""Specialized chart helpers shared by a few model modules."""
from pathlib import Path
import matplotlib.pyplot as plt

from finance_effects_lab.common import SOURCE_NOTE


def line_chart(frame, x, ys, labels, title, xlabel, ylabel, path):
    fig, ax = plt.subplots(figsize=(9, 5.2))
    colors = ["#2364AA", "#16856C", "#C73E4D", "#E59F23"]
    for col, label, color in zip(ys, labels, colors):
        ax.plot(frame[x], frame[col], marker="o", linewidth=2, label=label, color=color)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=0.22)
    if len(ys) > 1:
        ax.legend(frameon=False)
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=7.5, color="#5D6774")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
