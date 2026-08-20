"""Build the interactive and static cross-model portfolio dashboard."""
from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT=Path(__file__).resolve().parents[2]
RELATIONSHIPS={
"Macro & rates":["Interest Rate Effect","Duration Effect","Fisher Effect","Wealth Effect"],
"Balance sheet":["Leverage Effect","Tax Shield Effect","Financial Accelerator","Leverage Cycle"],
"Funding stress":["Margin Spiral","Liquidity Spiral","Flight-to-Safety Effect"],
"System risk":["Contagion Effect","Minsky Moment","Risk-on/Risk-off Effect"],
"Corporate actions":["Cash Flow Waterfall","Dilution Effect","M&A Accretion/Dilution","Compound Interest Effect"],
}
THEME_COLORS={"Macro & rates":"#2364AA","Balance sheet":"#16856C","Funding stress":"#C73E4D","System risk":"#7A5195","Corporate actions":"#E59F23"}

def _static_map(path):
    graph=nx.Graph()
    for theme,effects in RELATIONSHIPS.items():
        graph.add_node(theme,kind="theme")
        for effect in effects:graph.add_node(effect,kind="effect");graph.add_edge(theme,effect)
    # Mechanism links communicate how effects interact, not causal estimates.
    cross=[("Interest Rate Effect","Duration Effect"),("Fisher Effect","Interest Rate Effect"),("Leverage Effect","Tax Shield Effect"),
           ("Leverage Cycle","Margin Spiral"),("Margin Spiral","Liquidity Spiral"),("Liquidity Spiral","Contagion Effect"),
           ("Financial Accelerator","Minsky Moment"),("Wealth Effect","Financial Accelerator"),("Flight-to-Safety Effect","Risk-on/Risk-off Effect"),
           ("Dilution Effect","M&A Accretion/Dilution"),("Cash Flow Waterfall","Leverage Effect")]
    graph.add_edges_from(cross)
    # A fixed five-row layout is easier to scan in a portfolio README than an unstable
    # force layout. Cross-theme mechanism links remain visible as dashed diagonals.
    theme_y=[4.8,2.4,0,-2.4,-4.8];pos={}
    for y,(theme,effects) in zip(theme_y,RELATIONSHIPS.items()):
        pos[theme]=(0,y)
        x_positions=[2.2,4.5,6.8,9.1]
        for x,effect in zip(x_positions,effects):pos[effect]=(x,y)
    fig,ax=plt.subplots(figsize=(17,10),facecolor="#F7F9FC")
    for theme,effects in RELATIONSHIPS.items():
        nx.draw_networkx_nodes(graph,pos,nodelist=[theme],node_size=3900,node_color=THEME_COLORS[theme],node_shape="s",ax=ax)
        nx.draw_networkx_nodes(graph,pos,nodelist=effects,node_size=2300,node_color="#FFFFFF",edgecolors=THEME_COLORS[theme],linewidths=2,ax=ax)
    group_edges=[e for e in graph.edges if e not in cross and tuple(reversed(e)) not in cross]
    nx.draw_networkx_edges(graph,pos,edgelist=group_edges,alpha=.24,width=1.5,ax=ax)
    nx.draw_networkx_edges(graph,pos,edgelist=cross,alpha=.35,width=1.7,style="dashed",edge_color="#5D6774",ax=ax)
    for node,(x,y) in pos.items():
        color="white" if node in RELATIONSHIPS else "#17202A"
        wrap_width=10 if node in RELATIONSHIPS else 18
        ax.text(x,y,"\n".join(textwrap.wrap(node,wrap_width)),ha="center",va="center",fontsize=8.5 if node not in RELATIONSHIPS else 9.5,color=color,fontweight="bold" if node in RELATIONSHIPS else "normal")
    ax.set_title("Finance Effects Lab — Relationship Map",fontsize=20,fontweight="bold",loc="left",pad=24)
    ax.text(-.9,5.85,"Solid links group finance areas; dashed links show modeled mechanism relationships (not estimated causality).",fontsize=10,color="#5D6774")
    ax.set_xlim(-1.1,10.25);ax.set_ylim(-5.8,6.1);ax.axis("off");fig.tight_layout();path.parent.mkdir(parents=True,exist_ok=True);fig.savefig(path,dpi=180,bbox_inches="tight");plt.close(fig)

def build_dashboard(summary:pd.DataFrame):
    output=ROOT/"outputs";charts=ROOT/"charts";output.mkdir(exist_ok=True);charts.mkdir(exist_ok=True)
    _static_map(charts/"portfolio_relationship_map.png")
    # Normalize each model's stress movement to its own base scale; raw values remain in hover/table.
    chart=summary.copy();denom=chart.base_value.abs().clip(lower=1e-9);chart["stress_delta_scaled"]=(chart.stress_value-chart.base_value)/denom
    fig=make_subplots(rows=2,cols=1,row_heights=[.48,.52],specs=[[{"type":"bar"}],[{"type":"table"}]],vertical_spacing=.11)
    colors=[THEME_COLORS.get(next((t for t,e in RELATIONSHIPS.items() if row.title in e),""),"#2364AA") for row in chart.itertuples()]
    fig.add_trace(go.Bar(x=chart.title,y=chart.stress_delta_scaled,marker_color=colors,
                         customdata=chart[["base_value","stress_value","finance_area"]],
                         hovertemplate="<b>%{x}</b><br>Area: %{customdata[2]}<br>Base: %{customdata[0]:,.4f}<br>Stress: %{customdata[1]:,.4f}<br>Scaled change: %{y:.1%}<extra></extra>"),row=1,col=1)
    fig.add_trace(go.Table(header=dict(values=["Effect","Finance area","Metric","Base","Stress"],fill_color="#172B4D",font=dict(color="white"),align="left"),
                           cells=dict(values=[chart.title,chart.finance_area,chart.primary_metric,chart.base_value.round(4),chart.stress_value.round(4)],fill_color="#F3F6FA",align="left",height=24)),row=2,col=1)
    fig.update_yaxes(title_text="Stress change / |base|",tickformat=".0%",zeroline=True,row=1,col=1)
    fig.update_xaxes(tickangle=-35,row=1,col=1)
    fig.update_layout(title="Finance Effects Lab — 18-Model Portfolio Dashboard",height=1120,template="plotly_white",showlegend=False,
                      margin=dict(l=60,r=35,t=90,b=35),annotations=[dict(text="Metrics have different units; compare direction within each model, not bar height across models.",x=.5,y=.52,xref="paper",yref="paper",showarrow=False,font=dict(size=11,color="#5D6774"))])
    html=fig.to_html(include_plotlyjs=True,full_html=True)
    html=html.replace("</body>","<p style='font-family:Arial;color:#5D6774;margin:24px'>Source: Finance Effects Lab hypothetical assumptions. Educational models; not actual company performance or investment advice. Accessed/generated 20 August 2026.</p></body>")
    # Plotly's embedded JavaScript contains harmless trailing spaces; strip them so
    # repository whitespace checks stay useful without changing dashboard behavior.
    html="\n".join(line.rstrip() for line in html.splitlines())+"\n"
    (output/"portfolio_dashboard.html").write_text(html)
    return output/"portfolio_dashboard.html"
