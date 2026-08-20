"""Private-equity style cash waterfall from operations through carried interest."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from finance_effects_lab.common import SOURCE_NOTE, export_results, heatmap_chart, model_root, read_assumptions

SLUG="cash_flow_waterfall"


def calculate(revenue,operating_expenses,tax_rate,senior_debt,senior_rate,scheduled_senior_principal,
              mezzanine_debt,mezzanine_rate,scheduled_mezz_principal,lp_contribution,preferred_return_rate,carry_rate):
    ebitda=revenue-operating_expenses
    senior_interest=senior_debt*senior_rate; mezz_interest=mezzanine_debt*mezzanine_rate
    taxes=max(0.0,(ebitda-senior_interest-mezz_interest)*tax_rate)
    cash=ebitda-taxes
    senior_interest_paid=min(cash,senior_interest);cash-=senior_interest_paid
    senior_principal_paid=min(cash,scheduled_senior_principal,senior_debt);cash-=senior_principal_paid
    mezz_interest_paid=min(cash,mezz_interest);cash-=mezz_interest_paid
    mezz_principal_paid=min(cash,scheduled_mezz_principal,mezzanine_debt);cash-=mezz_principal_paid
    lp_preferred=min(cash,lp_contribution*preferred_return_rate);cash-=lp_preferred
    required_catch_up=lp_preferred*carry_rate/(1-carry_rate) if carry_rate<1 else 0
    sponsor_catch_up=min(cash,required_catch_up);cash-=sponsor_catch_up
    sponsor_carry=cash*carry_rate;lp_residual=cash*(1-carry_rate)
    sponsor_distribution=sponsor_catch_up+sponsor_carry;lp_distribution=lp_preferred+lp_residual
    return {"ebitda":ebitda,"taxes":taxes,"senior_interest":senior_interest_paid,
            "senior_principal":senior_principal_paid,"mezzanine_interest":mezz_interest_paid,
            "mezzanine_principal":mezz_principal_paid,"lp_preferred_return":lp_preferred,
            "sponsor_catch_up":sponsor_catch_up,"sponsor_carry":sponsor_carry,
            "lp_residual":lp_residual,"lp_distribution":lp_distribution,
            "sponsor_distribution":sponsor_distribution,"total_equity_distribution":lp_distribution+sponsor_distribution,
            "unpaid_debt_service":max(0,senior_interest-senior_interest_paid)+max(0,mezz_interest-mezz_interest_paid)}


def _args(r):return [r[x] for x in ["revenue","operating_expenses","tax_rate","senior_debt","senior_rate","scheduled_senior_principal","mezzanine_debt","mezzanine_rate","scheduled_mezz_principal","lp_contribution","preferred_return_rate","carry_rate"]]

def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path)
    return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(*_args(r))} for r in d.to_dict("records")])

def sensitivity():
    base=read_assumptions(SLUG);r=base[base.scenario=="Base"].iloc[0].to_dict();rows=[]
    for revenue in [90,105,120,135,150]:
        for carry in [.10,.15,.20,.25,.30]:
            z=r|{"revenue":revenue,"carry_rate":carry};rows.append({"revenue":revenue,"carry_rate":carry,**calculate(*_args(z))})
    return pd.DataFrame(rows)

def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data
    d=model_root(SLUG)/"charts";d.mkdir(parents=True,exist_ok=True);base=results[results.scenario=="Base"].iloc[0]
    labels=["Revenue","Opex","Taxes","Senior int.","Senior prin.","Mezz. int.","Mezz. prin.","LP dist.","Sponsor dist."]
    flows=[base.revenue,-base.operating_expenses,-base.taxes,-base.senior_interest,-base.senior_principal,-base.mezzanine_interest,-base.mezzanine_principal,-base.lp_distribution,-base.sponsor_distribution]
    starts=[];ends=[];running=0.0
    for value in flows:
        starts.append(running);running+=value;ends.append(running)
    bottoms=[min(a,b) for a,b in zip(starts,ends)];heights=[abs(b-a) for a,b in zip(starts,ends)]
    fig,ax=plt.subplots(figsize=(11,5.5)); colors=["#2364AA"]+["#C73E4D"]*6+["#16856C","#E59F23"]
    bars=ax.bar(labels,heights,bottom=bottoms,color=colors,width=.72)
    for i in range(len(flows)-1):ax.plot([i+.36,i+1-.36],[ends[i],ends[i]],color="#5D6774",lw=.8,alpha=.6)
    labels_value=[f"{v:+.1f}" if i else f"{v:.1f}" for i,v in enumerate(flows)]
    ax.bar_label(bars,labels=labels_value,label_type="center",fontsize=8,color="white",fontweight="bold")
    ax.axhline(0,color="#273444",lw=.8);ax.set(title="Base-Case Cash Flow Waterfall by Payment Priority",ylabel="Remaining cash ($m)",xlabel="Waterfall tier");ax.tick_params(axis="x",rotation=35)
    fig.text(.01,.01,SOURCE_NOTE,fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"cash_flow_waterfall.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="revenue",columns="carry_rate",values="sponsor_distribution");p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Sponsor Distribution Sensitivity","Carry rate","Revenue ($m)","Sponsor distribution ($m)",d/"waterfall_sensitivity.png")

def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
