"""Download optional official FRED series for empirical extensions.

These data do not feed the committed hypothetical model runs. No API key is needed.
"""
from pathlib import Path
import pandas as pd

SERIES={
    "DGS10":"10-Year Treasury Constant Maturity Rate",
    "DFII10":"10-Year Treasury Inflation-Indexed Constant Maturity Rate",
    "CPIAUCSL":"Consumer Price Index for All Urban Consumers",
}
ROOT=Path(__file__).resolve().parent

def download():
    target=ROOT/"public";target.mkdir(exist_ok=True)
    for series,name in SERIES.items():
        url=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
        frame=pd.read_csv(url);frame.columns=["date",series.lower()]
        frame["date"]=pd.to_datetime(frame["date"]);frame[series.lower()]=pd.to_numeric(frame[series.lower()],errors="coerce")
        if series in {"DGS10","DFII10"}:frame[f"{series.lower()}_decimal"]=frame[series.lower()]/100
        if series=="CPIAUCSL":frame["cpi_yoy"]=frame[series.lower()].pct_change(12)
        frame["source"]="Federal Reserve Bank of St. Louis (FRED)";frame["series_name"]=name
        frame.to_csv(target/f"{series.lower()}.csv",index=False)
        print(f"Wrote {len(frame):,} observations to {target/f'{series.lower()}.csv'}")
if __name__=="__main__":download()
