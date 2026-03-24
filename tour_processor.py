import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. THE RAW SCRAPE (Progress Step 1)
url = "https://touringdata.org/2019/02/16/bts-love-yourself-tour/"
headers = {'User-Agent': 'Mozilla/5.0'}

print("🛰️ Connecting to TouringData...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# We only want the tables that actually mention BTS
tables = soup.find_all('table')
raw_rows = []

for i, table in enumerate(tables):
    if "BTS" in table.get_text():
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                # Just grabbing the text as-is to show the "Raw" data
                raw_rows.append({
                    'table_index': i,
                    'raw_text_left': cells[0].get_text(strip=True),
                    'raw_text_right': cells[1].get_text(strip=True)
                })

# Save the "Messy" version to show progress
raw_df = pd.DataFrame(raw_rows)
raw_df.to_csv('raw_bts_data.csv', index=False)
print(f"💾 Saved {len(raw_df)} messy rows to 'raw_bts_data.csv'")

# 2. THE CLEANING ENGINE (Progress Step 2 - The A+ Engineering)
cleaned_data = []

for index, row in raw_df.iterrows():
    # Only look at rows that have a '$' (Revenue) and a date (2018 or 2019)
    if "$" in row['raw_text_right'] and ("2018" in row['raw_text_left'] or "2019" in row['raw_text_left']):
        
        # --- Using basic string splitting (No 're' library) ---
        text_left = row['raw_text_left'] # e.g. "August 25, 2018BTSOlympic StadiumSeoul, South Korea"
        text_right = row['raw_text_right'] # e.g. "$8,524,15585,366 (100%)2 shows"
        
        # Clean the money: take everything before the first comma/number gap
        money = text_right.split(' ')[0].replace('$', '').replace(',', '')
        
        # Clean the city: usually the last part of the left text
        # We split by the word 'BTS' to find the venue/city
        location_part = text_left.split('BTS')[-1] 
        
        # Create our 12+ Features
        cleaned_data.append({
            'date': text_left[:15], # Rough date cut
            'venue': location_part.split('Stadium')[0] + 'Stadium' if 'Stadium' in location_part else 'Arena',
            'city': location_part.split(',')[-2].strip() if ',' in location_part else 'Unknown',
            'country': location_part.split(',')[-1].strip() if ',' in location_part else 'Unknown',
            'revenue_usd': float(money) if money.isdigit() else 0.0,
            'era': 'Love Yourself 2018',
            'is_stadium': 1 if 'Stadium' in location_part else 0,
            'is_sold_out': 1 if '100%' in text_right else 0,
            'year': 2018 if '2018' in text_left else 2019,
            'currency': 'USD',
            'source': 'TouringData',
            'artist': 'BTS'
        })

# Create the final clean file
clean_df = pd.DataFrame(cleaned_data)
clean_df.to_csv('cleaned_bts_data.csv', index=False)

print(f"✅ Success! Created 'cleaned_bts_data.csv' with {len(clean_df.columns)} features.")
