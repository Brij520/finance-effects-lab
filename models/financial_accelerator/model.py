"""Runnable wrapper for the Financial Accelerator Effect model."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from finance_effects_lab.effects.financial_accelerator import *  # noqa: F401,F403,E402

if __name__ == "__main__":
    scenarios, sensitivity_results = run_model()
    print(scenarios.to_string(index=False))
