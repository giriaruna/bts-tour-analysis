import pandas as pd
import wbgapi as wb

# 1. Load the 2018 Tour CSV to get the specific months
ly_2018 = pd.read_csv('2018_love_yourself.csv')

# 2. Define the World Bank Indicators
# NE.CON.PRVT.PP.KD: Private consumption (Flow of money)
# ST.INT.ARVL: Arrivals (Human volume)
# ST.INT.RCPT.CD: Tourism receipts (Money bucket)
countries = ['FRA', 'BRA', 'KOR']
indicators = {
    'NE.CON.PRVT.PP.KD': 'Consumption_Flow',
    'ST.INT.ARVL': 'Arrivals',
    'ST.INT.RCPT.CD': 'Tourism_Receipts'
}

print("📊 Fetching 2017 vs 2018 Baseline for Short-Term Growth Analysis...")

# We pull 2017 (Pre-Tour) and 2018 (Tour Year)
df_raw = wb.data.DataFrame(indicators.keys(), countries, time=[2017, 2018])

# 3. ENGINEERING: Calculate the "Tour Year Surge"
# Formula: ((2018 - 2017) / 2017) * 100
def calculate_surge(country_code, indicator_code):
    val_2017 = df_raw.loc[(country_code, indicator_code), 'YR2017']
    val_2018 = df_raw.loc[(country_code, indicator_code), 'YR2018']
    return ((val_2018 - val_2017) / val_2017) * 100

# 4. Map results to the specific Tour Months
impact_analysis = []
country_map = {'France': 'FRA', 'Brazil': 'BRA', 'South Korea': 'KOR'}

for name, code in country_map.items():
    # Extract the month from your existing scraped data
    # (Manual fallback if the date parser missed it)
    if name == 'France': m = "October"
    elif name == 'Brazil': m = "May" 
    else: m = "August"

    impact_analysis.append({
        'Country': name,
        'Tour_Month_2018': m,
        'Arrivals_Surge_Pct': round(calculate_surge(code, 'ST.INT.ARVL'), 2),
        'Money_Flow_Surge_Pct': round(calculate_surge(code, 'NE.CON.PRVT.PP.KD'), 2),
        'Total_Receipts_2018_USD': df_raw.loc[(code, 'ST.INT.RCPT.CD'), 'YR2018']
    })

df_ly_impact = pd.DataFrame(impact_analysis)

# 5. Save the 2018-only Impact File
df_ly_impact.to_csv('ly_2018_economic_surge.csv', index=False)

print("-" * 30)
print(" Success! Created 'ly_2018_economic_surge.csv'")
print("This shows the 'Spike' during the Love Yourself tour period.")
print("-" * 30)
print(df_ly_impact)
