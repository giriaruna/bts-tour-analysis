import pandas as pd

# 1. Updated Venue & Volume Constraints based on your corrections
# South Korea: 2 shows, Brazil: 3 shows
tour_specs = {
    'South Korea': {
        '2018_cap': 45000, '2018_shows': 2, '2018_total_att': 90000,
        '2026_cap': 41000, '2026_shows': 2, 
        'label': 'Geographic Shift'
    },
    'France': {
        '2018_cap': 20300, '2018_shows': 2, '2018_total_att': 40600,
        '2026_cap': 80000, '2026_shows': 2, 
        'label': 'Hardware Upgrade'
    },
    'Brazil': {
        '2018_cap': 42364, '2018_shows': 2, '2018_total_att': 84728,
        '2026_cap': 45000, '2026_shows': 3, 
        'label': 'Volume Optimization'
    }
}

# 2. Load Data
ly_2018 = pd.read_csv('2018_love_yourself.csv')
surge_data = pd.read_csv('ly_2018_economic_surge.csv')

# 3. Engineering Sanitization
def sanitize_revenue(val):
    s = str(val)
    return float(s[:7]) if len(s) > 10 else val

ly_2018['revenue_usd_clean'] = ly_2018['revenue_usd'].apply(sanitize_revenue)

# 4. Corrected Predictive Engine
def run_corrected_model(row):
    country = row['country']
    if country not in tour_specs: return None
    
    spec = tour_specs[country]
    
    # A. Multipliers
    capacity_multiplier = spec['2026_cap'] / spec['2018_cap']
    volume_multiplier = spec['2026_shows'] / spec['2018_shows']
    econ_surge = surge_data[surge_data['Country'] == country]['Money_Flow_Surge_Pct'].values[0] / 100
    FANDOM_COEFFICIENT = 2.8 
    
    # B. Revenue Projection
    # (2018 Rev / 2018 Shows) * 2026 Shows * Capacity Scaling * Econ Factor * Fandom Factor
    rev_per_show_2018 = row['revenue_usd_clean'] / spec['2018_shows']
    
    proj_rev = (rev_per_show_2018 * spec['2026_shows']) * \
               capacity_multiplier * (1 + econ_surge) * FANDOM_COEFFICIENT
                               
    proj_att = spec['2026_cap'] * spec['2026_shows']
    
    return pd.Series([
        spec['2018_total_att'],
        spec['2018_shows'], 
        spec['2026_shows'], 
        proj_rev, 
        proj_att
    ])

# 5. Execute
targets = ['South Korea', 'France', 'Brazil']
df_final = ly_2018[ly_2018['country'].isin(targets)].copy()

model_cols = ['2018_Total_Attendance', '2018_Shows', '2026_Shows', '2026_Proj_Revenue_USD', '2026_Proj_Attendance']
df_final[model_cols] = df_final.apply(run_corrected_model, axis=1)

# 6. Final Cleaning
df_final = df_final.drop_duplicates(subset=['country'])
df_final.to_csv('arirang_final_forecast.csv', index=False)

# Display the Final Result Table
print(df_final[['country', '2018_Total_Attendance', '2026_Proj_Attendance', '2018_Shows', '2026_Shows', '2026_Proj_Revenue_USD']])
