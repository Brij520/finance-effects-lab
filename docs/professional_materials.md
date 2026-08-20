# Professional Portfolio Materials

## LinkedIn Project Description

**Finance Effects Lab** is a Python-based finance research and modelling portfolio covering 18 mechanisms across corporate finance, fixed income, banking, private markets, investment analysis, and systemic risk. I translated each concept into an auditable numerical model with four scenarios, two-way sensitivities, professional charts, Excel-compatible workbooks, Power BI-ready CSVs, documented assumptions, tests, and interview questions. Special builds include an iterative liquidity spiral, a private-equity cash waterfall, a fixed-income duration/convexity engine, an M&A accretion/dilution model, and a synthetic counterparty contagion network. All committed data are clearly labeled hypothetical; public references are cataloged with sources and access dates.

## LinkedIn Launch Post

I built **Finance Effects Lab**—a portfolio of 18 practical financial models designed to move beyond memorizing definitions.

The question behind the project was simple: *Can I explain a finance effect, calculate it, stress it, visualize it, and translate it into a decision?*

Highlights:

- Leverage bridge from debt → interest → net income → ROE
- Iterative liquidity and margin spirals with forced-sale feedback
- Private-equity cash waterfall from revenue through debt service, preferred return, catch-up, and carry
- Bond full repricing plus duration and convexity
- Share dilution and M&A EPS accretion/dilution sensitivities
- Synthetic contagion network and a clearly labeled educational Minsky-cycle model
- Excel workbooks, Power BI-ready CSVs, Jupyter notebooks, and automated tests

The repository uses Python, pandas, NumPy, Matplotlib, Plotly, and NetworkX. Every assumption is editable, every public source is documented, and hypothetical outputs are never presented as actual company performance.

Repository: [YOUR_GITHUB_URL]

I would value feedback from people working in FP&A, investment banking, equity research, treasury, risk, and private markets. Which model would you extend first?

#CorporateFinance #FinancialModeling #Python #InvestmentBanking #EquityResearch #RiskManagement #PortfolioProject

## Resume Bullet Points

- Built **Finance Effects Lab**, a Python/Jupyter portfolio of 18 corporate-finance and markets models spanning leverage, valuation, fixed income, M&A, liquidity, contagion, and macro-financial effects.
- Developed editable base/optimistic/pessimistic/stress cases and two-way sensitivity analyses, exporting audit-ready results to Excel and Power BI-compatible CSV.
- Implemented full bond repricing, Macaulay/modified duration and convexity, iterative forced-sale mechanics, priority cash waterfalls, and M&A EPS accretion/dilution bridges.
- Created a synthetic six-institution exposure network to test default propagation under recovery, capital, and liquidity scenarios; clearly separated mechanism simulation from prediction.
- Added formula and invariant tests across all 18 modules, public-source governance, professional visualizations, and role-specific business interpretations.

## 5-Minute Interview Explanation

### 0:00–0:40 — Objective

I built Finance Effects Lab to demonstrate that I can move from finance theory to an auditable decision model. It covers 18 effects across corporate finance, fixed income, private markets, macro-finance, and risk. The purpose is not to build a trading terminal; it is to show clear assumptions, correct formulas, scenario thinking, and business interpretation.

### 0:40–1:25 — Common modelling process

Every module starts with a formula and variable definitions. I then create four editable scenarios, calculate intermediate lines rather than only the final answer, run a two-way sensitivity, and generate a chart with units and an assumption note. The same Python function feeds the notebook, CSV, Excel workbook, and test suite, so there is one source of truth. All sample values are hypothetical, and documented versus illustrative company examples are clearly separated.

### 1:25–2:20 — Corporate-finance examples

The leverage model bridges debt to interest expense, taxable income, net income, and ROE at zero, 25%, 50%, and 75% debt. It shows the core interview insight: leverage improves ROE when asset returns clear debt cost but magnifies downside when they do not. The tax-shield model compares levered and unlevered cash tax without recognizing benefits beyond taxable capacity. The dilution model calculates ownership and EPS dilution after issuance, while the M&A model bridges acquirer and target earnings, synergies, after-tax interest, and new shares into pro forma EPS.

### 2:20–3:15 — Markets and risk examples

For fixed income, I fully reprice coupon cash flows under minus 200 to plus 200 basis-point shocks. A separate module calculates Macaulay duration, modified duration, convexity, and approximation error. For liquidity risk, I built an iterative model: a price shock lowers margin equity, required sales repay debt, those sales move price, and the calculation repeats. The margin model separately makes haircuts volatility-sensitive. These are educational mechanisms and I explicitly state that they are not prediction engines.

### 3:15–4:05 — Private markets and systemic risk

The cash waterfall takes revenue through opex, tax, senior and mezzanine interest/principal, LP preference, sponsor catch-up, carry, and residual distributions. This demonstrates payment priority, not just arithmetic. The contagion model uses a synthetic six-node exposure matrix. A default creates creditor losses net of recovery; any creditor whose cumulative loss exceeds capital defaults in the next round. Sensitivity shows how capital and recovery can contain or amplify the same initial shock.

### 4:05–4:40 — Quality controls and outputs

I wrote tests for known identities and finance invariants—for example, a coupon-equals-yield bond prices at par, a waterfall cannot distribute more cash than remains, bond price moves inversely to yield, and stronger capital does not increase defaults in a fixed network. A single runner refreshes all 18 models, 36 charts, model-level workbooks, consolidated Power BI CSVs, and an interactive Plotly dashboard.

### 4:40–5:00 — Close

The main lesson is that a model is useful only when the assumptions, mechanism, and limitations are as clear as the output. If I extended the project, I would calibrate selected models with versioned FRED, SEC XBRL, RBI, or BIS data and add probabilistic scenarios—but I would preserve the same audit trail and evidence standards.
