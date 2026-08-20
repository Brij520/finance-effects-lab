"""Generate the 18 model README files from curated finance research metadata."""
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
META={
"leverage_effect":{
"title":"Leverage Effect","area":"Corporate finance / capital structure",
"definition":"Debt financing concentrates operating gains and losses into a smaller equity base after contractual interest expense.",
"intuition":"When return on assets exceeds the after-tax cost of debt, leverage lifts ROE; when operating return falls below financing cost, the same fixed claim accelerates equity losses.",
"formulas":["Interest = Debt × interest rate","Net income = (EBIT − Interest) × (1 − tax rate), when pre-tax income is positive","ROE = Net income ÷ (Assets − Debt)"],
"variables":"EBIT is operating profit; Debt is interest-bearing borrowing; tax rate is the modeled cash tax rate; ROE is return on book equity.",
"base":"At $100m of assets, 10% ROA, 6% debt cost, and 25% tax, compare 0%, 25%, 50%, and 75% debt/assets. The smaller equity denominator raises base-case ROE, but the stress loss becomes progressively worse.",
"sensitivity":"ROA from -8% to 16% against debt/assets of 0%, 25%, 50%, and 75%.",
"limitations":"One-period book-value model; no distress costs, covenants, refinancing, tax-loss carryforwards, or endogenous interest spread.",
"examples":[("Documented context","Berkshire Hathaway","Annual reports disclose operating earnings, debt, and capital allocation; the model does not substitute those values.","https://www.berkshirehathaway.com/reports.html"),("Documented context","Amazon","SEC filings provide debt and interest disclosures useful for an analyst-built leverage bridge.","https://www.sec.gov/edgar/browse/?CIK=1018724&owner=exclude"),("Illustrative application","KKR","A buyout underwriting team could use this framework with deal-specific debt schedules; no KKR data are used.","https://ir.kkr.com/financial-information/annual-reports")],
"roles":{"CFO":"compare financing capacity with downside interest coverage and ROE volatility","FP&A analyst":"bridge operating plan changes through interest, tax, net income, and ROE","Equity analyst":"separate operating improvement from financial leverage in peer ROE"},
"questions":[("Why can leverage increase ROE?","Compare ROA with debt cost and focus on the equity denominator.","Debt is accretive to ROE when the incremental after-tax operating return exceeds the financing burden; it also makes negative outcomes larger.","Would your answer change when EBIT is negative?"),("At what operating return does leverage stop helping?","Set levered ROE equal to unlevered ROE and solve for the break-even return.","In the simplified pre-tax model, the crossover is near the cost of debt; taxes, loss treatment, and changing spreads alter it.","How would a floating-rate loan change the sensitivity?"),("How would you extend this for an LBO?","Add time, mandatory amortization, cash sweeps, changing rates, exit value, and IRR/MOIC.","Build a multi-period debt schedule linked to cash flow and covenant tests, then solve sponsor returns across exit scenarios.","Which covenant would bind first in the stress case?")]},
"financial_accelerator":{
"title":"Financial Accelerator Effect","area":"Financial economics / credit",
"definition":"Changes in borrower net worth alter collateral capacity and the external-finance premium, amplifying an initial economic or asset-price shock.",
"intuition":"A lower collateral value reduces borrowing capacity precisely when firms may need financing, causing investment to fall by more than the original wealth shock.",
"formulas":["Shocked net worth = Initial net worth × (1 + asset-price shock)","Borrowing capacity = max(0, collateral multiplier × net worth − existing debt)","Investment = baseline investment + credit sensitivity × borrowing capacity"],
"variables":"The collateral multiplier converts net worth into gross secured capacity; existing debt consumes capacity; credit sensitivity maps available finance to investment.",
"base":"A hypothetical borrower starts with $50m net worth and $50m debt. With 2.5× collateral capacity, available borrowing supports investment; a 20%–40% collateral loss sharply reduces that support.",
"sensitivity":"Asset-price shocks from -40% to +20% against collateral multipliers from 1.5× to 3.0×.",
"limitations":"Reduced-form one-period relationship; no lender optimization, maturity wall, covenant cure, default option, or general-equilibrium feedback.",
"examples":[("Documented research","NBER","Bernanke, Gertler, and Gilchrist formalized balance-sheet amplification; this implementation is deliberately simpler.","https://www.nber.org/papers/w6455"),("Documented context","JPMorgan Chase","Public credit-risk and allowance disclosures show why borrower quality and collateral matter; no bank data enter the simulation.","https://www.jpmorganchase.com/ir/annual-report"),("Illustrative application","ICICI Bank","A credit analyst could replace hypothetical inputs with sanctioned exposure and collateral data.","https://www.icicibank.com/about-us/annual")],
"roles":{"CFO":"protect liquidity before collateral values weaken","FP&A analyst":"link financing availability to capex scenarios","Risk analyst":"stress collateral, borrower net worth, and credit availability jointly"},
"questions":[("What is the accelerator?","Describe amplification rather than the initial shock.","A net-worth loss worsens financing terms and lowers credit-funded activity, making the ultimate output effect larger than the original shock.","What could dampen it?"),("Why does collateral matter?","Connect pledgeable assets to agency costs and loss given default.","More collateral lowers lender downside and can increase capacity or reduce the external-finance premium.","How would unsecured borrowers differ?"),("How would you validate the coefficient?","Seek panel data and identify exogenous collateral shocks.","Estimate investment sensitivity using borrower-level credit and collateral data, control for demand, and test out of sample.","What endogeneity remains?")]},
"liquidity_spiral":{
"title":"Liquidity Spiral","area":"Market risk / funding liquidity",
"definition":"A price decline tightens funding constraints, forces asset sales, and causes further market-price declines through price impact.",
"intuition":"A levered holder must sell into a thin market to restore margin; the sale itself lowers prices and can create another margin breach.",
"formulas":["Equity = Marked asset value − Debt","Margin ratio = Equity ÷ Marked asset value","Price impact = Forced units ÷ (Initial units × market-liquidity parameter)"],
"variables":"Leverage fixes initial equity; required margin is minimum equity/assets; market liquidity scales the price response to forced sales.",
"base":"A $100m position financed at 3× leverage absorbs a 5% shock. The model solves required sales, applies linear price impact, repays debt with proceeds, and repeats until compliant or exhausted.",
"sensitivity":"Initial shocks from 2% to 20% against leverage from 2× to 6×.",
"limitations":"Linear impact, one representative holder, no order-book recovery, hedges, new capital, cross-asset liquidation, or strategic counterparties. It is not a prediction engine.",
"examples":[("Documented context","Federal Reserve","The Financial Stability Report discusses interactions among leverage, funding risk, and market liquidity.","https://www.federalreserve.gov/publications/financial-stability-report.htm"),("Documented context","BIS","BIS research documents margining practices and liquidity demand during stress.","https://www.bis.org/bcbs/publ/d537.htm"),("Illustrative application","BlackRock","An asset manager could use position-level liquidity and financing terms; no BlackRock positions are modeled.","https://ir.blackrock.com/financials/annual-reports-and-proxy")],
"roles":{"Treasurer":"hold enough liquidity to avoid selling into impaired markets","Risk analyst":"combine funding and market-liquidity stresses instead of shocking them independently","Portfolio manager":"size leverage using liquidation cost, not only ex-ante volatility"},
"questions":[("What creates the feedback loop?","Trace price, margin, sale, and price impact in order.","Losses reduce margin equity, the holder sells to comply, and market impact causes another loss.","When does the loop stop?"),("Why can a small shock become nonlinear?","Identify the constraint threshold and thin-market impact.","Nothing is sold before the threshold; once breached, forced volume and impact can jump discontinuously.","How would central clearing affect it?"),("How would you calibrate liquidity?","Use observed depth, bid-ask spreads, and stressed liquidation data.","Estimate impact by asset and horizon, then validate against historical stress windows without treating history as a hard bound.","How would you model multiple funds?")]},
"margin_spiral":{
"title":"Margin Spiral","area":"Counterparty and market risk",
"definition":"Rising volatility or haircuts reduces debt capacity, forcing deleveraging that can lower asset values and trigger still higher margin needs.",
"intuition":"Risk-sensitive financing terms are procyclical: secured funding is abundant in calm markets but contracts when measured risk rises.",
"formulas":["Haircut = base haircut + sensitivity × volatility shock × round","Maximum debt = Asset value × (1 − haircut)","Forced sale = max(0, Debt − Maximum debt)"],
"variables":"Haircut is borrower equity required against collateral; price impact is the incremental loss per dollar sold.",
"base":"A $100m portfolio with $75m debt, a 20% initial haircut, and a 6% volatility shock recalculates debt capacity over sequential margin rounds.",
"sensitivity":"Volatility shocks from 2% to 20% against sale-price impact from 5% to 50%.",
"limitations":"Haircut rule is illustrative; real agreements use asset-specific schedules, variation margin, netting, collateral substitution, and intraday calls.",
"examples":[("Documented case","Credit Suisse / Archegos","The Federal Reserve enforcement release describes counterparty risk-management deficiencies related to Archegos.","https://www.federalreserve.gov/newsevents/pressreleases/enforcement20230724a.htm"),("Documented context","BIS","BIS work on margining during stress provides institutional context.","https://www.bis.org/bcbs/publ/d537.htm"),("Illustrative application","Goldman Sachs","A prime broker could apply client-level financing terms; this model uses no Goldman Sachs data.","https://www.goldmansachs.com/investor-relations/financials/current/annual-reports")],
"roles":{"CFO/Treasurer":"monitor collateral calls and unencumbered assets","Risk analyst":"stress haircut migration together with gap risk and concentration","Investment banker":"assess financing resilience where transaction funding relies on pledged securities"},
"questions":[("How is a margin spiral different from an ordinary loss?","Emphasize endogenous financing terms.","The initial loss raises required collateral or haircut, forcing balance-sheet action that creates additional losses.","How is variation margin different from initial margin?"),("Why are haircuts procyclical?","Connect measured volatility and lender risk limits.","Volatility and correlation rise in stress, so lenders demand more protection just as borrower equity falls.","What policy can reduce procyclicality?"),("What would a prime-broker model add?","Mention netting sets, wrong-way risk, liquidity horizon, and concentration.","Model legal-netting sets, collateral eligibility, intraday variation margin, liquidation horizon, and correlated client defaults.","How would you test gap risk?")]},
"cash_flow_waterfall":{
"title":"Cash Flow Waterfall","area":"Private equity / project finance",
"definition":"A contractual sequence allocates operating cash first to taxes and senior claims, then subordinated debt, preferred return, catch-up, carry, and residual equity.",
"intuition":"Priority, not just total project cash, determines which stakeholder receives value in each scenario.",
"formulas":["CFADS = EBITDA − cash taxes","Debt service = interest paid + scheduled principal paid, subject to available cash","GP catch-up = LP preferred return × carry ÷ (1 − carry), capped by cash"],
"variables":"CFADS is cash flow available for debt service; LP is limited partner; GP/sponsor receives catch-up and carry after senior tiers.",
"base":"Base revenue is $155m and opex $72m. Cash pays tax, senior interest/principal, mezzanine interest/principal, an 8% LP preference, sponsor catch-up, then an 80/20 residual split.",
"sensitivity":"Revenue from $90m to $150m against carried-interest rates from 10% to 30%.",
"limitations":"Single-period distributable cash; no opening arrears, reserve account, PIK toggle, IRR hurdle, European/American waterfall distinction, or clawback.",
"examples":[("Documented context","Blackstone","Annual reports disclose incentive-fee and carried-interest economics; this hypothetical waterfall is not a Blackstone fund model.","https://ir.blackstone.com/financial-information/annual-reports-and-proxy-statements/default.aspx"),("Documented context","KKR","Public reports describe carried interest and fund economics at a high level.","https://ir.kkr.com/financial-information/annual-reports"),("Illustrative application","Apollo","A deal team could substitute governing-document tiers and asset-level debt terms.","https://ir.apollo.com/financials/annual-reports-and-proxies/default.aspx")],
"roles":{"CFO":"forecast covenant headroom and distributable cash after debt service","FP&A analyst":"trace operating variance into stakeholder distributions","Investment banker":"structure debt sizing and sponsor returns around payment priority"},
"questions":[("Why does payment priority matter?","Separate enterprise cash generation from claimant allocation.","Senior claims can be fully paid while junior equity receives nothing; upside reaches junior tiers only after hurdles.","What is cash flow available for debt service?"),("What is a GP catch-up?","Explain how distributions move the GP toward the agreed profit share after LP preference.","After the LP preferred tier, a defined share may flow to the GP until cumulative sharing reaches the carry split.","How does a European waterfall differ?"),("How would you model an IRR hurdle?","Use dated cash flows and solve tier-by-tier distributions.","Accrue the preferred balance by actual dates, allocate cash iteratively, and include clawback/escrow provisions.","How would PIK interest affect the exit waterfall?")]},
"interest_rate_effect":{
"title":"Interest Rate Effect","area":"Fixed income / treasury",
"definition":"A bond's present value changes inversely with its discount yield because fixed cash flows are discounted at the new market rate.",
"intuition":"When required yield rises, the same coupons and principal are worth less today; longer-dated cash flows usually move more.",
"formulas":["Bond price = Σ CFₜ ÷ (1 + y/m)^(m×t)","Coupon per period = Face value × coupon rate ÷ m","Price change % = Shocked price ÷ Initial price − 1"],
"variables":"CF is coupon or principal cash flow; y is yield to maturity; m is payments per year; t is time in years.",
"base":"A $1,000 face, 5% coupon, 10-year semiannual bond is priced at a 5% yield and fully repriced at -2%, 0%, +1%, and +2% parallel shifts.",
"sensitivity":"Maturity from 2 to 30 years against yield shifts from -2% to +2%.",
"limitations":"Parallel deterministic shifts; no spread movement, optionality, default, tax, liquidity premium, reinvestment risk, or curve-key-rate exposure.",
"examples":[("Documented context","JPMorgan Chase","Annual reports disclose interest-rate risk and earnings/value sensitivity; this model is an independent bond example.","https://www.jpmorganchase.com/ir/annual-report"),("Documented context","BlackRock","Public reports discuss investment portfolios and market risk without providing inputs to this simulation.","https://ir.blackrock.com/financials/annual-reports-and-proxy"),("Illustrative application","HDFC Bank","A treasury analyst could reprice an actual securities book using instrument-level cash flows.","https://www.hdfcbank.com/personal/about-us/investor-relations/annual-reports")],
"roles":{"CFO/Treasurer":"measure debt and investment exposure to rate scenarios","Equity analyst":"translate rate moves into funding cost and securities valuation","Risk analyst":"supplement parallel shocks with curve, spread, and optionality stress"},
"questions":[("Why do bond prices fall when yields rise?","Use discounted cash flow.","A higher required return increases discount factors, reducing the present value of fixed contractual cash flows.","Which cash flow is most sensitive?"),("Why is the response nonlinear?","Discuss convexity.","The price-yield curve is curved, so equal up/down yield moves produce asymmetric price changes.","When can convexity be negative?"),("How would you hedge a portfolio?","Move from full repricing to duration and key-rate exposures.","Match DV01 or key-rate durations with swaps/futures, then test basis, convexity, and nonparallel shifts.","What risk remains after a DV01 hedge?")]},
"duration_effect":{
"title":"Duration Effect","area":"Fixed income risk",
"definition":"Modified duration approximates a bond's percentage price sensitivity to a small yield change; convexity improves the estimate for larger moves.",
"intuition":"Duration is a PV-weighted timing measure: lower coupons and longer maturities defer value and generally increase rate sensitivity.",
"formulas":["Macaulay duration = Σ(t × PV(CFₜ)) ÷ Price","Modified duration = Macaulay duration ÷ (1 + y/m)","ΔP/P ≈ −Modified duration × Δy + ½ × Convexity × (Δy)²"],
"variables":"t is payment time; y is yield; m is coupon frequency; convexity captures curvature of the price-yield function.",
"base":"The model computes exact price, Macaulay duration, modified duration, and convexity for a 10-year 4% bond yielding 5%, then compares approximation with full repricing.",
"sensitivity":"Coupons from 2% to 8% against maturities from 2 to 30 years; all cells show modified duration.",
"limitations":"Yield-to-maturity framework assumes fixed cash flows; it is insufficient for callable securities, mortgage prepayments, credit spread changes, and curve twists.",
"examples":[("Documented case","Silicon Valley Bank","The Federal Reserve review discusses interest-rate and liquidity risk-management weaknesses; this is not a reconstruction of SVB's portfolio.","https://www.federalreserve.gov/publications/review-of-the-federal-reserves-supervision-and-regulation-of-silicon-valley-bank.htm"),("Documented context","BlackRock","Fixed-income portfolios disclose rate risk in public reporting.","https://ir.blackrock.com/financials/annual-reports-and-proxy"),("Illustrative application","SBI","A bank treasury could map actual holdings into duration buckets.","https://sbi.co.in/web/investor-relations/annual-report")],
"roles":{"Treasurer":"align asset and liability duration within risk appetite","Portfolio manager":"size rate hedges and express curve views","Risk analyst":"monitor DV01, key-rate duration, convexity, and stress loss"},
"questions":[("What does modified duration mean?","Give a percentage-price interpretation with sign.","A modified duration of 7 implies roughly a 7% price decline for a 100 bp yield rise, before convexity.","When is that approximation poor?"),("Why do low-coupon bonds have longer duration?","Locate more PV in principal.","Less value arrives through early coupons, so the PV-weighted average payment time is later.","Can duration exceed maturity?"),("Duration matched—are you hedged?","Discuss curve and convexity mismatch.","Not necessarily: equal aggregate duration can hide key-rate, spread, basis, optionality, and convexity differences.","How would you test a twist?")]},
"tax_shield":{
"title":"Tax Shield Effect","area":"Corporate finance / valuation",
"definition":"Deductible interest can reduce taxable income and cash taxes, creating value relative to an otherwise similar unlevered company.",
"intuition":"The tax authority effectively shares part of interest cost, but only when deductions are usable and legally permitted.",
"formulas":["Interest expense = Debt × interest rate","Annual tax shield = min(Interest, taxable capacity) × tax rate","PV of perpetual constant-debt shield ≈ Debt × tax rate"],
"variables":"Taxable capacity reflects positive pre-interest taxable income; the perpetuity shortcut assumes debt and tax rate remain constant and shield risk matches debt.",
"base":"Compare $25m EBIT with $100m debt at 6% and a 25% tax rate. The schedule shows EBIT, interest, taxable income, tax, net income, shield, and levered/unlevered FCF.",
"sensitivity":"Debt from $0m to $125m against statutory tax rates from 10% to 35%.",
"limitations":"No interest-deduction limits, NOL timing, jurisdiction mix, deferred tax, distress cost, changing debt, or tax-rate uncertainty.",
"examples":[("Documented context","Amazon","SEC filings disclose interest and income-tax items; this model uses no Amazon figures.","https://www.sec.gov/edgar/browse/?CIK=1018724&owner=exclude"),("Documented context","Berkshire Hathaway","Annual reports disclose debt and tax information relevant to independent analysis.","https://www.berkshirehathaway.com/reports.html"),("Illustrative application","Apollo","A deal model would apply instrument and jurisdiction-specific deductibility rules.","https://ir.apollo.com/financials/annual-reports-and-proxies/default.aspx")],
"roles":{"CFO":"balance tax benefit against distress, ratings, and flexibility","FP&A analyst":"forecast cash tax with interest limitations and NOLs","Investment banker":"include usable shields—not gross interest—in capital-structure valuation"},
"questions":[("What creates an interest tax shield?","Start with deductible interest lowering taxable income.","Each usable dollar of interest saves roughly the marginal tax rate in current tax.","What if EBIT is below interest?"),("Is the shield always Debt × tax rate?","Challenge the perpetuity assumptions.","No; that shortcut requires permanent constant debt, full deductibility, stable tax rate, and an appropriate discount-rate assumption.","How do NOLs change timing?"),("How would you value a changing shield?","Forecast annual usable deductions and discount them.","Build jurisdiction-level taxable-income schedules, apply caps/carryforwards, and discount scenario-weighted cash tax savings.","Which discount rate is defensible?")]},
"wealth_effect":{
"title":"Wealth Effect","area":"Financial economics / consumer demand",
"definition":"A change in household net worth can alter consumption because households spend a fraction of gains or cut spending after losses.",
"intuition":"Asset appreciation relaxes lifetime budget constraints, though the response depends on liquidity, permanence, distribution, and household type.",
"formulas":["Wealth change = Initial wealth × asset return","Consumption change = MPC out of wealth × Wealth change","Consumption change % = Consumption change ÷ Baseline consumption"],
"variables":"MPC is marginal propensity to consume from a dollar of wealth change; it is an assumption, not a universal constant.",
"base":"A household segment has $500k wealth, $80k annual consumption, and 4% MPC. The model applies returns from +20% to -30% and converts wealth changes to spending.",
"sensitivity":"Wealth returns from -30% to +30% against MPC estimates from 2% to 6%.",
"limitations":"Representative household, symmetric linear MPC, no income shock, debt, age, asset liquidity, distributional heterogeneity, or confidence channel.",
"examples":[("Documented data","Federal Reserve","Distributional Financial Accounts provide household wealth context; no series is embedded in the hypothetical base case.","https://www.federalreserve.gov/releases/z1/dataviz/dfa/"),("Illustrative application","Visa","An analyst could compare modeled spending sensitivity with disclosed payment-volume trends; this is not a Visa forecast.","https://annualreport.visa.com/"),("Illustrative application","Mastercard","The framework could support consumer-spending scenarios using separately sourced data.","https://investor.mastercard.com/financials-and-sec-filings/annual-reports-and-proxy/default.aspx")],
"roles":{"FP&A analyst":"link macro wealth scenarios to category demand with explicit elasticity","Equity analyst":"test consumer-exposed revenue against asset-price shocks","Risk analyst":"avoid applying one MPC to every household or spending category"},
"questions":[("What is the wealth effect?","Separate wealth from current income.","Households may adjust consumption when asset values change because perceived lifetime resources change.","Which assets generate the largest response?"),("Why might losses matter more than gains?","Discuss constraints and precautionary saving.","Liquidity constraints, debt, and confidence can make consumption responses asymmetric.","How would you model asymmetry?"),("How would you estimate MPC?","Use household panels or quasi-experimental shocks.","Segment by wealth composition and liquidity, control for income, and test lagged and nonlinear responses.","What identification problem remains?")]},
"contagion_effect":{
"title":"Contagion Effect","area":"Systemic risk / network finance",
"definition":"Losses propagate across connected institutions when a default impairs creditors and newly weakened creditors then fail.",
"intuition":"The same initial loss can remain contained in a well-capitalized sparse network or cascade through concentrated, low-recovery exposures.",
"formulas":["Creditor lossᵢⱼ = Exposureᵢⱼ × (1 − recovery rate)","Institution i defaults if cumulative lossᵢ ≥ capitalᵢ","System loss = Σ institution losses"],
"variables":"Exposure i,j is lender i's claim on borrower j; capital is loss-absorbing capacity; recovery is value retained after default.",
"base":"Six synthetic nodes—two banks, a fund, insurer, company, and market SPV—have explicitly hypothetical exposures. A Market-SPV shock propagates until no new node breaches capital.",
"sensitivity":"Recovery rates from 0% to 80% against capital multipliers from 0.5× to 1.5×.",
"limitations":"Static known bilateral exposures; no netting, collateral, maturity, liquidity hoarding, central counterparty, endogenous recovery, or behavioral response. Not a prediction engine.",
"examples":[("Documented case","Lehman Brothers","The Financial Crisis Inquiry Commission report documents interconnected distress during the financial crisis.","https://www.govinfo.gov/app/details/GPO-FCIC"),("Documented case","AIG","The same public inquiry provides evidence on counterparty and derivatives linkages.","https://www.govinfo.gov/app/details/GPO-FCIC"),("Illustrative application","JPMorgan Chase","A bank would use confidential counterparty and collateral data; no JPMorgan exposures are represented.","https://www.jpmorganchase.com/ir/annual-report")],
"roles":{"Risk analyst":"identify concentrated counterparties and second-round loss paths","Treasurer":"prepare liquidity for indirect network shocks","Regulator/systemic-risk analyst":"stress common exposures and capital jointly"},
"questions":[("What is financial contagion?","Describe transmission rather than simultaneous correlation.","A loss at one node causes losses at connected nodes, potentially creating further defaults.","How is a common shock different?"),("What makes a network fragile?","Mention concentration, low capital, low recovery, and common holdings.","Large exposures to central nodes and thin buffers can turn a local default into a cascade.","Can more connections ever stabilize it?"),("How would you model real exposures?","Address netting, collateral, uncertainty, and privacy.","Aggregate by legal netting set, model collateral and recovery, infer missing links with ranges, and run reverse stress tests.","How would fire sales enter?")]},
"minsky_moment":{
"title":"Minsky Moment","area":"Financial stability / credit cycles",
"definition":"A long expansion in credit and risk-taking can create fragile financing structures that reverse abruptly when debt service becomes unsustainable.",
"intuition":"Stability can encourage more leverage; after a threshold, tighter credit and selling reinforce declining prices and deleveraging.",
"formulas":["Debt-service ratio = Leverage × Asset price × Interest rate ÷ Income","Credit growth after trigger = −tightening strength","Asset-price change = credit beta × credit growth + risk-taking term − tightening term"],
"variables":"Trigger DSR is an assumed fragility threshold; credit beta and tightening strength are educational mechanism parameters, not estimated forecasts.",
"base":"A 12-period synthetic cycle starts at price index 100 and 2.5× leverage. The 80% debt-service trigger keeps the base case in expansion, while pessimistic and stress cases breach their thresholds and reverse; this makes trigger behavior explicit rather than treating every scenario as a crash.",
"sensitivity":"Easy-credit growth from 2% to 16% against interest rates from 2% to 10%.",
"limitations":"Highly simplified deterministic cycle, arbitrary reduced-form coefficients, no expectations, defaults, policy reaction, sector heterogeneity, or empirical forecasting power.",
"examples":[("Documented research context","BIS","BIS research on financial cycles and credit provides empirical context, not calibration for this model.","https://www.bis.org/publ/work395.htm"),("Documented context","IMF","Global Financial Stability Reports analyze leverage and financial-stability risks.","https://www.imf.org/en/Publications/GFSR"),("Illustrative application","Federal Reserve","A policymaker could use richer stress models; this notebook is not a Federal Reserve method.","https://www.federalreserve.gov/publications/financial-stability-report.htm")],
"roles":{"Risk analyst":"track nonlinear combinations of leverage, debt service, and collateral","CFO/Treasurer":"avoid funding long-lived assets with fragile short-term debt","Equity analyst":"distinguish sustainable growth from credit-dependent multiple expansion"},
"questions":[("What is a Minsky moment?","Explain the transition from stability to fragility.","Accumulated leverage and speculative financing make a system vulnerable to an abrupt tightening and forced deleveraging.","Is every downturn a Minsky moment?"),("Why can calm periods increase risk?","Discuss endogenous risk-taking.","Low observed volatility and easy credit can encourage leverage, weakening resilience to later shocks.","Which indicators would you monitor?"),("Why is this not a forecast?","Identify unestimated parameters and omitted behavior.","The equations illustrate a mechanism; credible forecasting requires calibrated data, expectations, policy, heterogeneity, and uncertainty.","How would you backtest without overfitting?")]},
"flight_to_safety":{
"title":"Flight-to-Safety Effect","area":"Asset allocation / market stress",
"definition":"Investors reallocate from risky or illiquid assets toward instruments perceived as safer or more liquid during stress.",
"intuition":"Risk tolerance falls and balance-sheet constraints tighten, producing safe-asset inflows, risky-asset outflows, and wider relative returns or spreads.",
"formulas":["Flow to safe = Portfolio value × risk-aversion shock × reallocation sensitivity","Safe return impact = Flow ÷ Safe-market depth","Risky return impact = −Flow ÷ Risky-market depth"],
"variables":"Market depth is a reduced-form dollar scale translating flow into price return; it is not trading volume.",
"base":"A $100m allocation starts 30% safe. A 5% risk-aversion shock reallocates assets according to 0.8 sensitivity, bounded by risky holdings.",
"sensitivity":"Risk-aversion shock from 0% to 25% against safe-market depth from $500m to $2,000m.",
"limitations":"Two asset buckets, linear and immediate impact, no yield/price conversion, FX, central-bank action, collateral convenience yield, or reversal dynamics.",
"examples":[("Documented context","Federal Reserve","Financial Stability Reports discuss safe-asset demand and market liquidity in stress.","https://www.federalreserve.gov/publications/financial-stability-report.htm"),("Documented context","BIS","BIS publications analyze safe-haven flows and dollar funding conditions.","https://www.bis.org/publ/qtrpdf/r_qt2009.htm"),("Illustrative application","BlackRock","A portfolio team could replace depth assumptions with asset-specific execution estimates.","https://ir.blackrock.com/financials/annual-reports-and-proxy")],
"roles":{"Portfolio manager":"pre-plan liquidity and safe-asset capacity before stress","Risk analyst":"stress correlations, depth, and crowding simultaneously","CFO/Treasurer":"understand how flight-to-safety changes funding spreads and investment values"},
"questions":[("What is flight to safety?","Describe allocation and relative pricing.","Investors shift toward perceived safety/liquidity, often supporting safe assets while pressuring risky ones.","Is cash always safe?"),("Why does market depth matter?","Connect a fixed flow to impact.","The same dollar flow moves prices more in a shallow market than a deep one.","Can the safest market become illiquid?"),("How would you distinguish safety from liquidity?","Use multiple instruments and event data.","Compare credit-risk-free but less liquid assets with liquid but risky assets and decompose spread changes.","What role does collateral demand play?")]},
"risk_on_risk_off":{
"title":"Risk-on/Risk-off Effect","area":"Portfolio management",
"definition":"Broad changes in risk appetite create regimes in which risky assets tend to gain or lose together while defensive assets behave differently.",
"intuition":"A portfolio's regime result is the sum of each asset return times its allocation, so defensive weights can reduce stress loss at the cost of upside.",
"formulas":["Portfolio return = Σ weightᵢ × returnᵢ","Asset contribution = weightᵢ × returnᵢ","Risk-asset weight = Equity weight in this simplified three-asset model"],
"variables":"Weights sum to 100%; modeled assets are equity, bonds, and cash; return assumptions are scenario inputs, not forecasts.",
"base":"The base portfolio is 60% equity, 30% bonds, and 10% cash with 7%, 3%, and 2% assumed returns. Stress shifts weights defensively and changes all asset returns.",
"sensitivity":"Equity weight from 20% to 80% against equity return from -25% to +15%, holding 10% cash.",
"limitations":"Single period, deterministic returns, no covariance, transaction costs, FX, credit spread, path dependence, or estimation uncertainty.",
"examples":[("Documented context","BlackRock","Public market outlooks discuss portfolio regimes; no BlackRock allocation is copied here.","https://www.blackrock.com/corporate/insights/blackrock-investment-institute/publications/outlook"),("Documented context","Federal Reserve","Financial Stability Reports provide risk-appetite indicators for broader analysis.","https://www.federalreserve.gov/publications/financial-stability-report.htm"),("Illustrative application","Berkshire Hathaway","An analyst could classify public holdings by factor exposure; this model is not Berkshire's portfolio.","https://www.berkshirehathaway.com/reports.html")],
"roles":{"Portfolio manager":"quantify return contribution by regime and allocation","Equity analyst":"separate beta-driven rerating from company fundamentals","Risk analyst":"challenge assumed defensive correlations during inflation or liquidity shocks"},
"questions":[("What does risk-on mean?","Define behavior, not a permanent asset label.","Risk tolerance rises, often supporting equities and credit relative to defensive assets.","Can bonds fall in risk-off?"),("How do contributions differ from returns?","Multiply each asset return by its weight.","A high-return small position can contribute less than a moderate-return large position.","How should cash be treated?"),("How would you identify regimes?","Use transparent indicators and avoid look-ahead bias.","Combine volatility, spreads, correlations, and flows, estimate regimes on available data, and test stability out of sample.","How would transaction costs alter switching?")]},
"leverage_cycle":{
"title":"Leverage Cycle","area":"Financial economics / collateral",
"definition":"Leverage expands in rising markets as collateral values increase and haircuts fall, then contracts in falling markets as both mechanisms reverse.",
"intuition":"Collateral-based debt capacity moves with prices, so lender terms and borrower balance-sheet adjustment reinforce asset cycles.",
"formulas":["Dynamic haircut = Base haircut − procyclicality × asset return","Debt capacity = Collateral value × (1 − haircut)","Leverage = Collateral value ÷ (Collateral value − Debt)"],
"variables":"Procyclicality translates asset return into haircut movement; debt closes 65% of the gap to capacity each modeled period.",
"base":"$100m collateral and $70m debt evolve for eight periods. A 2% return changes collateral, haircut, debt capacity, debt, equity, and leverage sequentially.",
"sensitivity":"Periodic asset return from -15% to +15% against procyclicality from 0.2 to 1.0.",
"limitations":"Constant repeated return, mechanical haircut, no defaults, new equity, lender capital, interest, maturity, fire-sale feedback, or equilibrium price formation.",
"examples":[("Documented research","Federal Reserve","FEDS research on collateralized lending discusses leverage-cycle mechanisms; coefficients here are not taken from the paper.","https://www.federalreserve.gov/econres/feds/files/2022052pap.pdf"),("Documented context","BIS","BIS credit-cycle research links financing conditions and asset prices.","https://www.bis.org/publ/work395.htm"),("Illustrative application","Goldman Sachs","A secured-financing desk could calibrate actual collateral haircuts; no firm data are used.","https://www.goldmansachs.com/investor-relations/financials/current/annual-reports")],
"roles":{"Risk analyst":"stress collateral and haircut jointly","CFO/Treasurer":"preserve borrowing headroom through the cycle","Equity analyst":"recognize when asset growth is financed by procyclical debt capacity"},
"questions":[("What drives the leverage cycle?","Trace price, haircut, capacity, and debt.","Rising collateral and lower haircuts expand debt capacity; the reverse forces deleveraging in downturns.","How is this different from operating leverage?"),("Why include gradual adjustment?","Real balance sheets cannot instantly move to maximum capacity.","The close-rate represents execution, governance, and funding frictions and avoids assuming immediate optimization.","How would a covenant change it?"),("How would you add equilibrium?","Introduce borrowers, lenders, and endogenous prices.","Let lender capital set haircuts, borrower demand set leverage, and forced sales clear through a price-impact function.","What data identify procyclicality?")]},
"dilution_effect":{
"title":"Dilution Effect","area":"Equity capital markets",
"definition":"Issuing new shares reduces existing owners' percentage ownership and can reduce EPS unless proceeds generate enough incremental income.",
"intuition":"The earnings pie may grow after an issuance, but it is divided among more shares; accretion requires the return on proceeds to clear the earnings yield implied by the issue economics.",
"formulas":["Pro forma shares = Existing shares + New shares","Pro forma EPS = (Net income + Proceeds × return on proceeds) ÷ Pro forma shares","EPS dilution % = Pro forma EPS ÷ Existing EPS − 1"],
"variables":"Issue price times new shares equals gross proceeds; return on proceeds is first-year after-tax income yield in this simplified model.",
"base":"A company earns $100m on 100m shares and issues 20m shares at $20. At a 4% first-year return on proceeds, the model compares old/new EPS and ownership.",
"sensitivity":"New shares from 0m to 50m against return on proceeds from 0% to 8%.",
"limitations":"No fees, taxes, issue discount dynamics, option dilution, buybacks, time-weighted shares, signaling, debt reduction, or multi-year deployment.",
"examples":[("Documented context","Tesla","SEC filings document historical equity offerings; this model does not reproduce any specific offering.","https://www.sec.gov/edgar/browse/?CIK=1318605&owner=exclude"),("Documented context","AMC Entertainment","SEC filings provide issuance and share-count disclosures for independent analysis.","https://www.sec.gov/edgar/browse/?CIK=1411579&owner=exclude"),("Illustrative application","Amazon","An ECM analyst could model a hypothetical issuance; no announced Amazon transaction is implied.","https://www.sec.gov/edgar/browse/?CIK=1018724&owner=exclude")],
"roles":{"CFO":"weigh dilution against liquidity, leverage reduction, and growth returns","Investment banker":"size issuance and communicate EPS/ownership effects","Equity analyst":"separate mechanical dilution from value created with proceeds"},
"questions":[("What is share dilution?","Distinguish ownership and EPS dilution.","New shares lower an existing holder's percentage; EPS also falls unless incremental earnings offset the larger denominator.","Can ownership dilute while EPS rises?"),("What is the EPS break-even return?","Set new EPS equal to old EPS.","Incremental net income must equal existing EPS times new shares; divide by proceeds to get the required yield.","How does issue price affect it?"),("How would you model options and convertibles?","Use treasury-stock and if-converted methods plus timing.","Build basic and diluted weighted-average shares, apply anti-dilution rules, and scenario conversion economics.","How do buybacks interact?")]},
"ma_accretion_dilution":{
"title":"M&A Accretion/Dilution","area":"Investment banking / M&A",
"definition":"The model compares an acquirer's standalone EPS with pro forma EPS after adding target earnings, synergies, financing cost, and new shares.",
"intuition":"A deal can be strategically attractive yet EPS dilutive; accretion is an accounting output driven by price, funding mix, rates, target earnings, and synergies—not proof of value creation.",
"formulas":["Pro forma net income = Acquirer NI + Target NI + after-tax synergies − after-tax interest","Pro forma EPS = Pro forma net income ÷ (Acquirer shares + New shares)","Accretion/(dilution) = Pro forma EPS ÷ Acquirer EPS − 1"],
"variables":"Target NI equals target EPS times target shares; funding check confirms debt plus equity equals purchase price; all amounts are hypothetical $m except per-share data.",
"base":"The acquirer has $2.50 EPS and 100m shares; the target has $1.20 EPS and 20m shares. A $400m purchase uses $240m debt and $160m equity, with 6% debt cost and $25m pre-tax synergies.",
"sensitivity":"Purchase price from $300m to $550m against pre-tax synergies from $0m to $50m at 60/40 debt/equity funding.",
"limitations":"One-year EPS, no purchase accounting, amortization, step-ups, fees, lost interest, refinancing, integration cost, synergy timing, tax attributes, or deal close timing.",
"examples":[("Documented transaction","ExxonMobil / Pioneer","SEC filings document transaction terms; this model is not a reconstruction.","https://www.sec.gov/edgar/browse/?CIK=34088&owner=exclude"),("Documented transaction","Microsoft / Activision Blizzard","SEC filings document the transaction; no figures are imported here.","https://www.sec.gov/edgar/browse/?CIK=789019&owner=exclude"),("Illustrative application","Goldman Sachs","An advisory team would use detailed purchase accounting and financing assumptions.","https://www.goldmansachs.com/investor-relations/financials/current/annual-reports")],
"roles":{"CFO":"judge financing, integration, and strategic returns beyond headline EPS","Investment banker":"build transparent pro forma EPS and sensitivity cases","Equity analyst":"challenge synergy timing and distinguish accretion from economic value"},
"questions":[("What drives M&A accretion?","List target earnings, price, financing cost, new shares, tax, and synergies.","Pro forma earnings per share rises when incremental after-tax earnings exceed financing and dilution burden.","Can an all-stock deal be accretive?"),("Why is accretion not value creation?","Compare accounting EPS with NPV and return on invested capital.","Cheap financing or P/E differences can create EPS accretion even if the premium exceeds synergy value.","What metric would you add?"),("What does a full model need?","Cover purchase accounting and timing.","Add sources/uses, debt schedule, new shares, target adjustments, amortization, fees, integration costs, synergy ramp, and closing-date weighting.","How would you model circular interest?")]},
"compound_interest":{
"title":"Compound Interest Effect","area":"Investments / time value of money",
"definition":"Returns earn subsequent returns, causing wealth to grow exponentially rather than linearly when gains remain invested.",
"intuition":"Time and return interact multiplicatively; recurring contributions made earlier also receive more compounding periods.",
"formulas":["Principal FV = Principal × (1 + r/m)^(m×years)","Contribution FV = Payment × ((1 + r/m)^n − 1) ÷ (r/m)","Effective annual rate = (1 + r/m)^m − 1"],
"variables":"r is nominal annual return, m is compounds per year, n is total periods, and payment is end-of-period contribution.",
"base":"A $10,000 starting balance receives $2,000 annual contributions for 20 years, allocated monthly, under 0%, 4%, 7%, and 10% return scenarios.",
"sensitivity":"Years from 5 to 30 against annual returns from 2% to 10%.",
"limitations":"Constant deterministic return, end-of-period contributions, no volatility drag, fees, tax, inflation, withdrawals, sequence risk, or contribution growth.",
"examples":[("Documented context","Berkshire Hathaway","Shareholder letters discuss long-term compounding; the modeled returns are not Berkshire forecasts.","https://www.berkshirehathaway.com/letters/letters.html"),("Illustrative application","BlackRock","An investment calculator could use product-specific fees and return ranges.","https://ir.blackrock.com/financials/annual-reports-and-proxy"),("Illustrative application","HDFC Bank","A savings product illustration could apply contractual rates and cash-flow timing.","https://www.hdfcbank.com/personal/about-us/investor-relations/annual-reports")],
"roles":{"FP&A analyst":"discount or compound multi-year plan cash flows consistently","Investment analyst":"separate contributions from investment growth","CFO/Treasurer":"compare effective annual funding and investment rates"},
"questions":[("What is compounding?","Contrast interest on principal with interest on accumulated returns.","Reinvested gains enlarge the balance that earns the next period's return.","How does simple interest differ?"),("Why does frequency matter?","Convert nominal rate to periodic rate and exponent.","More frequent compounding raises effective annual return for a fixed positive nominal rate, though the gain diminishes.","What is continuous compounding?"),("How does volatility change realized compounding?","Use geometric versus arithmetic return.","For volatile returns, geometric growth is below the arithmetic average; sequence also matters with external cash flows.","How would fees enter?")]},
"fisher_effect":{
"title":"Fisher Effect","area":"Financial economics / macro rates",
"definition":"Nominal interest rates reflect real required returns and expected inflation, with an interaction term in the exact relationship.",
"intuition":"A lender cares about purchasing power: higher expected inflation generally requires a higher nominal rate to preserve a given real return.",
"formulas":["1 + nominal rate = (1 + real rate) × (1 + expected inflation)","Exact real rate = (1 + nominal) ÷ (1 + expected inflation) − 1","Approximate real rate ≈ nominal rate − expected inflation"],
"variables":"Expected—not realized—inflation belongs in the ex-ante relationship; approximation error is the omitted interaction term.",
"base":"At a 6% nominal rate and 3% expected inflation, the model calculates exact and approximate real rates, then stresses inflation to 9%.",
"sensitivity":"Nominal rates from 2% to 12% against expected inflation from 0% to 10%.",
"limitations":"Static ex-ante identity, no risk premium, tax, term premium, liquidity premium, inflation uncertainty, or distinction between expected and realized holding-period returns.",
"examples":[("Documented data","Federal Reserve / FRED","Nominal Treasury and inflation-indexed yields support market-based real-rate analysis; no live data are embedded in the base case.","https://fred.stlouisfed.org/series/DFII10"),("Documented context","Reserve Bank of India","Policy publications discuss inflation and interest-rate conditions.","https://www.rbi.org.in/Scripts/AnnualReportPublications.aspx"),("Illustrative application","HDFC Bank","A treasury analyst could use scenario inflation and instrument-specific rates; no bank forecast is implied.","https://www.hdfcbank.com/personal/about-us/investor-relations/annual-reports")],
"roles":{"CFO/Treasurer":"compare nominal borrowing cost with expected real burden","Equity analyst":"separate inflation compensation from changes in real discount rates","Risk analyst":"stress expected inflation, real rates, and risk premia separately"},
"questions":[("State the Fisher relationship.","Use gross rates for the exact identity.","One plus nominal equals one plus real times one plus expected inflation.","When is subtraction adequate?"),("Can the real rate be negative?","Compare nominal with inflation using the exact formula.","Yes; if expected inflation exceeds nominal yield, the ex-ante real rate is negative.","What about realized real return?"),("Why can nominal yields move more than inflation expectations?","Decompose term and risk premia.","Yields also contain real-rate, term-premium, liquidity, tax, and credit components, so Fisher is not a complete pricing model.","How would you infer expected inflation?")]},
}

FIVE_INSIGHTS=[
"The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.",
"A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.",
"The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.",
"Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.",
"The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.",
]
PRACTICAL=["budgeting, valuation, or transaction scenario design","risk-limit and downside-capacity review","investment memo or finance-interview discussion"]
MISTAKES=["Treating hypothetical scenario outputs as observed company performance.","Entering percentages as whole numbers rather than decimals.","Quoting the headline output without checking assumptions, units, thresholds, and omitted risks."]

def table_from_base(slug):
    with (ROOT/"models"/slug/"sample_data.csv").open() as f:
        rows=list(csv.DictReader(f))
    base=next(x for x in rows if x["scenario"]=="Base")
    return "\n".join(["| Input | Base assumption |","|---|---:|"]+[f"| `{k}` | {v} |" for k,v in base.items() if k!="scenario"])

def render(slug,m):
    formulas="\n".join(f"{i}. **{x}**" for i,x in enumerate(m["formulas"],1))
    examples="\n".join(f"- **{kind} — {name}:** {text} [Primary/public reference]({url})" for kind,name,text,url in m["examples"])
    roles="\n".join(f"- **{role}:** {text}." for role,text in m["roles"].items())
    insights="\n".join(f"{i}. {x}" for i,x in enumerate(FIVE_INSIGHTS,1))
    applications="\n".join(f"- {x.capitalize()}." for x in PRACTICAL)
    mistakes="\n".join(f"- {x}" for x in MISTAKES)
    q=[]
    levels=["Beginner","Intermediate","Advanced"]
    for level,(question,thinking,answer,follow) in zip(levels,m["questions"]):
        q.append(f"### {level}: {question}\n\n- **Expected thinking:** {thinking}\n- **Model answer:** {answer}\n- **Follow-up:** {follow}")
    return f'''# {m["title"]}

> **Area:** {m["area"]}<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

{m["definition"]}

### Financial intuition and why it occurs

{m["intuition"]}

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

{m["limitations"]}

## 2. Mathematical Model

{formulas}

**Variable definitions.** {m["variables"]}

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/{slug}.py`](../../src/finance_effects_lab/effects/{slug}.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

{table_from_base(slug)}

### Calculation and output

{m["base"]} Run `python models/{slug}/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/{slug}.xlsx`](outputs/{slug}.xlsx).

### Business interpretation

The base case is a decision anchor, not a conclusion. Compare it with the optimistic, pessimistic, and stress cases, identify the driver that crosses a risk or return threshold, and state which omitted factor could change the recommendation.

## 4. Scenario Analysis

| Scenario | Intended interpretation |
|---|---|
| Optimistic | Favorable operating, market, or financing conditions |
| Base | Central planning assumption—not a statistical forecast |
| Pessimistic | Material but manageable deterioration |
| Stress | Severe educational reverse stress; tests mechanism and resilience |

Major assumptions can be changed directly in `sample_data.csv`. Input validation rejects malformed scenario sets and selected nonsensical values.

## 5. Sensitivity Analysis

{m["sensitivity"]} The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

{examples}

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

{roles}

## 9. Key Takeaways

### Five key insights

{insights}

### Three formulas to remember

{formulas}

### Three practical applications

{applications}

### Three common mistakes

{mistakes}

## 10. Interview Questions

{chr(10).join(q)}

## Reproduce

```bash
python -m pip install -e .
python models/{slug}/model.py
jupyter lab models/{slug}/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
'''

def main():
    if len(META)!=18: raise RuntimeError(f"Expected 18 modules, got {{len(META)}}")
    for slug,m in META.items():
        (ROOT/"models"/slug/"README.md").write_text(render(slug,m))
    print("Generated",len(META),"model READMEs")
if __name__=="__main__":main()
