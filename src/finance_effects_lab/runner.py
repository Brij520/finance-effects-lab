"""CLI that refreshes every model and consolidated Power BI-ready outputs."""
from __future__ import annotations
import argparse
import importlib
from pathlib import Path

import pandas as pd

from finance_effects_lab import EFFECTS
from finance_effects_lab.dashboard import build_dashboard
from finance_effects_lab.registry import EFFECT_META

ROOT=Path(__file__).resolve().parents[2]

def run_all(build_dashboard_file=True):
    scenario_frames=[];sensitivity_frames=[];summary=[]
    for slug in EFFECTS:
        module=importlib.import_module(f"finance_effects_lab.effects.{slug}")
        scenarios,sensitivity=module.run_model(export=True)
        scenarios=scenarios.copy();scenarios.insert(0,"effect",slug);scenario_frames.append(scenarios)
        sensitivity=sensitivity.copy();sensitivity.insert(0,"effect",slug);sensitivity_frames.append(sensitivity)
        title,area,metric=EFFECT_META[slug]
        base=scenarios[scenarios["scenario"].astype(str)=="Base"]
        stress=scenarios[scenarios["scenario"].astype(str)=="Stress"]
        if slug=="leverage_effect":
            base=base[base["debt_ratio"]==.5];stress=stress[stress["debt_ratio"]==.5]
        summary.append({"effect":slug,"title":title,"finance_area":area,"primary_metric":metric,
                        "base_value":float(base.iloc[0][metric]),"stress_value":float(stress.iloc[0][metric])})
    output=ROOT/"outputs";output.mkdir(exist_ok=True)
    all_scenarios=pd.concat(scenario_frames,ignore_index=True,sort=False)
    all_sensitivities=pd.concat(sensitivity_frames,ignore_index=True,sort=False)
    summary_df=pd.DataFrame(summary)
    all_scenarios.to_csv(output/"power_bi_all_scenarios.csv",index=False)
    all_sensitivities.to_csv(output/"power_bi_all_sensitivities.csv",index=False)
    summary_df.to_csv(output/"model_summary.csv",index=False)
    # Tidy key/value alternatives avoid the sparse union of model-specific columns and
    # are convenient for a Power BI star schema. Case IDs preserve each original row.
    scenario_indexed=all_scenarios.reset_index(names="scenario_case_id")
    scenario_numeric=list(scenario_indexed.select_dtypes(include="number").columns)
    scenario_numeric.remove("scenario_case_id")
    scenario_long=scenario_indexed.melt(id_vars=["scenario_case_id","effect","scenario"],value_vars=scenario_numeric,var_name="field",value_name="value").dropna(subset=["value"])
    sensitivity_indexed=all_sensitivities.reset_index(names="sensitivity_case_id")
    sensitivity_numeric=list(sensitivity_indexed.select_dtypes(include="number").columns)
    sensitivity_numeric.remove("sensitivity_case_id")
    sensitivity_long=sensitivity_indexed.melt(id_vars=["sensitivity_case_id","effect"],value_vars=sensitivity_numeric,var_name="field",value_name="value").dropna(subset=["value"])
    scenario_long.to_csv(output/"power_bi_scenario_metrics_long.csv",index=False)
    sensitivity_long.to_csv(output/"power_bi_sensitivity_metrics_long.csv",index=False)
    with pd.ExcelWriter(output/"finance_effects_lab.xlsx",engine="openpyxl") as writer:
        summary_df.to_excel(writer,sheet_name="Model Summary",index=False)
        all_scenarios.to_excel(writer,sheet_name="All Scenarios",index=False)
        all_sensitivities.to_excel(writer,sheet_name="All Sensitivities",index=False)
        scenario_long.to_excel(writer,sheet_name="Scenario Metrics Long",index=False)
        sensitivity_long.to_excel(writer,sheet_name="Sensitivity Long",index=False)
    if build_dashboard_file:build_dashboard(summary_df)
    return summary_df

def main():
    parser=argparse.ArgumentParser(description="Run all Finance Effects Lab models")
    parser.add_argument("--no-dashboard",action="store_true",help="skip consolidated dashboard")
    args=parser.parse_args();summary=run_all(not args.no_dashboard)
    print(f"Completed {len(summary)} models. Outputs: {ROOT/'outputs'}")

if __name__=="__main__":main()
