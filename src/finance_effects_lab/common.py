"""Shared reporting helpers; financial logic lives in each effect module."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCENARIO_ORDER = ["Optimistic", "Base", "Pessimistic", "Stress"]
COLORS = {"Optimistic": "#16856C", "Base": "#2364AA", "Pessimistic": "#E59F23", "Stress": "#C73E4D"}
SOURCE_NOTE = "Source: Finance Effects Lab; hypothetical assumptions, not actual company performance."


def model_root(slug: str) -> Path:
    """Return repository model directory, independent of current working directory."""
    return Path(__file__).resolve().parents[2] / "models" / slug


def read_assumptions(slug: str, input_path: str | Path | None = None) -> pd.DataFrame:
    path = Path(input_path) if input_path else model_root(slug) / "sample_data.csv"
    data = pd.read_csv(path)
    if "scenario" not in data.columns:
        raise ValueError(f"{path} must contain a scenario column")
    if set(data["scenario"]) != set(SCENARIO_ORDER):
        raise ValueError(f"Scenarios must be exactly {SCENARIO_ORDER}")
    return data


def validate_rates(frame: pd.DataFrame, columns: Iterable[str]) -> None:
    """Rates are decimal inputs. Permit negatives, reject nonsensical values."""
    for column in columns:
        if column in frame and (frame[column].abs() > 2).any():
            raise ValueError(f"{column} must be a decimal rate (for example, 0.08 for 8%)")


def safe_divide(numerator, denominator):
    return np.where(np.asarray(denominator) != 0, np.asarray(numerator) / np.asarray(denominator), np.nan)


def ordered(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["scenario"] = pd.Categorical(result["scenario"], SCENARIO_ORDER, ordered=True)
    return result.sort_values("scenario").reset_index(drop=True)


def scenario_chart(
    results: pd.DataFrame,
    metric: str,
    ylabel: str,
    title: str,
    path: str | Path,
    percent: bool = False,
) -> None:
    """Create a consistent recruiter-ready scenario chart."""
    data = ordered(results)
    values = data[metric].astype(float)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    bars = ax.bar(
        data["scenario"].astype(str), values,
        color=[COLORS[str(x)] for x in data["scenario"]], width=0.62,
    )
    ax.axhline(0, color="#273444", linewidth=0.8)
    ax.set(title=title, xlabel="Scenario", ylabel=ylabel)
    ax.grid(axis="y", alpha=0.22)
    labels = [f"{v:.1%}" if percent else f"{v:,.2f}" for v in values]
    ax.bar_label(bars, labels=labels, padding=3, fontsize=9)
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=7.5, color="#5D6774")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def heatmap_chart(
    pivot: pd.DataFrame,
    title: str,
    xlabel: str,
    ylabel: str,
    cbar_label: str,
    path: str | Path,
    percent: bool = False,
) -> None:
    values = pivot.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    image = ax.imshow(values, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)), [str(x) for x in pivot.columns])
    ax.set_yticks(range(len(pivot.index)), [str(x) for x in pivot.index])
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(cbar_label)
    threshold = (np.nanmax(values) + np.nanmin(values)) / 2
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            value = values[i, j]
            label = f"{value:.1%}" if percent else f"{value:,.2f}"
            ax.text(j, i, label, ha="center", va="center", fontsize=8,
                    color="white" if abs(value - np.nanmin(values)) > abs(threshold - np.nanmin(values)) else "#17202A")
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=7.5, color="#5D6774")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def export_results(slug: str, results: pd.DataFrame, sensitivity_data: pd.DataFrame) -> dict[str, Path]:
    """Write CSV (Power BI), Excel, and model-local output files."""
    root = model_root(slug)
    output_dir = root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    scenario_csv = output_dir / "scenario_results.csv"
    sensitivity_csv = output_dir / "sensitivity_results.csv"
    workbook = output_dir / f"{slug}.xlsx"
    ordered(results).to_csv(scenario_csv, index=False)
    sensitivity_data.to_csv(sensitivity_csv, index=False)
    with pd.ExcelWriter(workbook, engine="openpyxl") as writer:
        ordered(results).to_excel(writer, sheet_name="Scenarios", index=False)
        sensitivity_data.to_excel(writer, sheet_name="Sensitivity", index=False)
    return {"scenarios": scenario_csv, "sensitivity": sensitivity_csv, "workbook": workbook}
