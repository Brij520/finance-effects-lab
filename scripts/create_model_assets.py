"""Regenerate model folders' wrappers and notebooks from the source package.

Documentation and input CSVs are curated separately; this script intentionally does not
replace them. Run from the repository root.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = [
    "leverage_effect", "financial_accelerator", "liquidity_spiral", "margin_spiral",
    "cash_flow_waterfall", "interest_rate_effect", "duration_effect", "tax_shield",
    "wealth_effect", "contagion_effect", "minsky_moment", "flight_to_safety",
    "risk_on_risk_off", "leverage_cycle", "dilution_effect", "ma_accretion_dilution",
    "compound_interest", "fisher_effect",
]
TITLES = {
    "leverage_effect":"Leverage Effect", "financial_accelerator":"Financial Accelerator Effect",
    "liquidity_spiral":"Liquidity Spiral", "margin_spiral":"Margin Spiral",
    "cash_flow_waterfall":"Cash Flow Waterfall", "interest_rate_effect":"Interest Rate Effect",
    "duration_effect":"Duration Effect", "tax_shield":"Tax Shield Effect", "wealth_effect":"Wealth Effect",
    "contagion_effect":"Contagion Effect", "minsky_moment":"Minsky Moment",
    "flight_to_safety":"Flight-to-Safety Effect", "risk_on_risk_off":"Risk-on/Risk-off Effect",
    "leverage_cycle":"Leverage Cycle", "dilution_effect":"Dilution Effect",
    "ma_accretion_dilution":"M&A Accretion/Dilution", "compound_interest":"Compound Interest Effect",
    "fisher_effect":"Fisher Effect",
}

def code_cell(source):
    return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[x+"\n" for x in source.splitlines()]}

def markdown_cell(source):
    return {"cell_type":"markdown","metadata":{},"source":[x+"\n" for x in source.splitlines()]}

def main():
    for slug in SLUGS:
        model_dir=ROOT/"models"/slug
        for child in [model_dir/"outputs",model_dir/"charts"]: child.mkdir(parents=True,exist_ok=True)
        wrapper=f'''"""Runnable wrapper for the {TITLES[slug]} model."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from finance_effects_lab.effects.{slug} import *  # noqa: F401,F403,E402

if __name__ == "__main__":
    scenarios, sensitivity_results = run_model()
    print(scenarios.to_string(index=False))
'''
        (model_dir/"model.py").write_text(wrapper)
        nb={
          "cells":[
            markdown_cell(f"# {TITLES[slug]}\n\n**Finance Effects Lab** | Reproducible scenario notebook\n\nThis notebook uses hypothetical, explicitly labeled assumptions from `sample_data.csv`. It is an educational finance model, not investment advice or actual company performance. See the module README for theory, formula definitions, limitations, professional interpretation, evidence links, and interview questions."),
            markdown_cell("## Setup and assumptions\n\nChange values in `sample_data.csv` to run a new case. Rates are decimals (for example, `0.06` means 6%)."),
            code_cell(f"from pathlib import Path\nimport sys\nROOT = Path.cwd().resolve()\nwhile not (ROOT / 'src').exists() and ROOT != ROOT.parent:\n    ROOT = ROOT.parent\nsys.path.insert(0, str(ROOT / 'src'))\nfrom finance_effects_lab.effects.{slug} import run_scenarios, sensitivity, create_charts\ninputs = ROOT / 'models' / '{slug}' / 'sample_data.csv'"),
            code_cell("import pandas as pd\nassumptions = pd.read_csv(inputs)\nassumptions"),
            markdown_cell("## Scenario analysis\n\nThe four cases isolate important drivers. Review every input before interpreting model output."),
            code_cell("results = run_scenarios(inputs)\nresults"),
            markdown_cell("## Sensitivity analysis\n\nThe sensitivity grid changes two major drivers while holding other assumptions constant."),
            code_cell("sensitivity_results = sensitivity()\nsensitivity_results.head(12)"),
            markdown_cell("## Visualization and exports\n\nCharts include labels, units, and an assumption note. `model.py` produces CSV and Excel outputs for Power BI and Excel."),
            code_cell("create_charts(results, sensitivity_results)\nprint('Charts refreshed. Run model.py or the portfolio runner for CSV/XLSX exports.')"),
            markdown_cell("## Interpretation checklist\n\n1. Identify the mechanism and direction of change.\n2. Separate operating assumptions from financing assumptions.\n3. Compare the stress case with risk capacity, covenant, liquidity, or valuation thresholds.\n4. Test whether the result is robust to the sensitivity grid.\n5. State what this simplified model omits before making a recommendation."),
        ],
        "metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11"}},
        "nbformat":4,"nbformat_minor":5}
        (model_dir/"notebook.ipynb").write_text(json.dumps(nb,indent=1))
        # A second, discoverable notebook location satisfies users who browse /notebooks first.
        (ROOT/"notebooks").mkdir(exist_ok=True)
        (ROOT/"notebooks"/f"{slug}.ipynb").write_text(json.dumps(nb,indent=1))

if __name__ == "__main__": main()
