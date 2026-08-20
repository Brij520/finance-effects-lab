# Notebooks

This directory provides a discoverable copy of all 18 notebooks. The canonical model folder also contains its notebook beside `sample_data.csv`, outputs, charts, and detailed README.

Notebooks do not duplicate formula logic: they import the corresponding module from `src/finance_effects_lab/effects/`. Change model assumptions in `models/<effect>/sample_data.csv`, then rerun the notebook.

```bash
jupyter lab
```

For a non-interactive refresh of every model and output, run `python -m finance_effects_lab` after installation.
