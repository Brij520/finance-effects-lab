"""Hypothetical counterparty network default cascade.

Node names and exposures are invented for education; they do not represent actual firms.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from finance_effects_lab.common import SOURCE_NOTE,export_results,heatmap_chart,model_root,read_assumptions

SLUG="contagion_effect"
NODES=["Bank A","Bank B","Fund C","Insurer D","Company E","Market SPV"]
BASE_CAPITAL=np.array([12.,10.,8.,11.,7.,6.])
# exposure[i,j] is the amount lender i loses if borrower j defaults before recovery.
EXPOSURES=np.array([[0,3,2,0,1,2],[4,0,2,1,0,1],[2,4,0,1,1,2],[1,3,2,0,2,0],[2,1,1,2,0,1],[3,2,3,1,1,0]],dtype=float)

def simulate(shock_node:int,initial_shock_loss:float,recovery_rate:float,capital_multiplier:float=1.0,liquidity_loss_rate:float=0.0):
    capital=BASE_CAPITAL*capital_multiplier;losses=np.zeros(len(NODES));defaults={shock_node};new={shock_node};round_no=0;events=[]
    losses[shock_node]+=initial_shock_loss
    while new:
        next_new=set()
        for borrower in new:
            for lender in range(len(NODES)):
                loss=EXPOSURES[lender,borrower]*(1-recovery_rate)
                losses[lender]+=loss
                if loss: events.append({"round":round_no,"borrower":NODES[borrower],"lender":NODES[lender],"loss":loss})
        # Common liquidity loss translates cascade size into mark-to-market pressure.
        losses += liquidity_loss_rate*len(new)
        for i in range(len(NODES)):
            if i not in defaults and losses[i]>=capital[i]: next_new.add(i)
        defaults|=next_new;new=next_new;round_no+=1
        if round_no>len(NODES):break
    status=pd.DataFrame({"institution":NODES,"capital":capital,"loss":losses,"defaulted":[i in defaults for i in range(len(NODES))]})
    return status,pd.DataFrame(events)

def _calc(r):
    status,events=simulate(int(r["shock_node"]),r["initial_shock_loss"],r["recovery_rate"],r["capital_multiplier"],r["liquidity_loss_rate"])
    return {"system_loss":status.loss.sum(),"defaults":int(status.defaulted.sum()),"capital_loss_pct":min(1,status.loss.sum()/status.capital.sum()),"propagation_events":len(events)}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**_calc(r)} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for recovery in [0,.2,.4,.6,.8]:
        for capital in [.5,.75,1,1.25,1.5]:
            r={"shock_node":5,"initial_shock_loss":8,"recovery_rate":recovery,"capital_multiplier":capital,"liquidity_loss_rate":.5}
            rows.append({"recovery_rate":recovery,"capital_multiplier":capital,**_calc(r)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts";d.mkdir(parents=True,exist_ok=True)
    G=nx.DiGraph();
    for i,n in enumerate(NODES):G.add_node(n)
    for i in range(len(NODES)):
        for j in range(len(NODES)):
            if EXPOSURES[i,j]>0:G.add_edge(NODES[j],NODES[i],weight=EXPOSURES[i,j])
    pos=nx.spring_layout(G,seed=17);fig,ax=plt.subplots(figsize=(9,6));
    nx.draw_networkx_nodes(G,pos,node_color="#2364AA",node_size=1800,ax=ax);nx.draw_networkx_labels(G,pos,font_color="white",font_size=8,ax=ax)
    nx.draw_networkx_edges(G,pos,width=[G[u][v]["weight"]*.45 for u,v in G.edges],alpha=.48,arrows=True,arrowstyle="-|>",ax=ax)
    ax.set_title("Hypothetical Exposure Network (Borrower → Lender)");ax.axis("off");fig.text(.01,.01,SOURCE_NOTE+" Exposures are synthetic.",fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"contagion_network.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="capital_multiplier",columns="recovery_rate",values="defaults");p.columns=[f"{x:.0%}" for x in p.columns];p.index=[f"{x:.2f}x" for x in p.index]
    heatmap_chart(p,"Network Defaults after Market-SPV Shock","Recovery rate","Capital multiplier","Number of defaults",d/"contagion_sensitivity.png")
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
