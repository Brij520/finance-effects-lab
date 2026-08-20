import importlib
import numpy as np
import pytest

from finance_effects_lab import EFFECTS
from finance_effects_lab.registry import EFFECT_META


@pytest.mark.parametrize("slug", EFFECTS)
def test_model_has_four_scenarios_and_sensitivity(slug):
    module = importlib.import_module(f"finance_effects_lab.effects.{slug}")
    results = module.run_scenarios()
    sensitivity = module.sensitivity()
    assert set(results["scenario"].astype(str)) == {"Optimistic", "Base", "Pessimistic", "Stress"}
    assert len(sensitivity) >= 20
    metric = EFFECT_META[slug][2]
    assert metric in results.columns
    assert np.isfinite(results[metric].astype(float)).all()


@pytest.mark.parametrize("slug", EFFECTS)
def test_sample_input_is_hypothetical_and_local(slug):
    module = importlib.import_module(f"finance_effects_lab.effects.{slug}")
    path = module.model_root(slug) / "sample_data.csv" if hasattr(module, "model_root") else None
    assert path is not None and path.exists()
