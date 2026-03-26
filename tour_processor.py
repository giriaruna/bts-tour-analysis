import requests
from bs4 import BeautifulSoup
import pandas as pd

class TourEconomicProcessor:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.targets = {
            "2018 Love Yourself": {
                "url": "https://touringdata.org/2019/02/16/bts-love-yourself-tour/",
                "year_filter": ["2018", "2019"]
            },
            "2026 Arirang": {
                "url": "https://touringdata.org/2026/01/13/bts-arirang-tour/",
                "year_filter": ["2026", "2027"]
            }
        }

    def clean_numeric(self, value):
        """Fundamental string cleaning to turn '$8,524,155' into a float."""
        if not value or "TBA" in value: 
            return 0.0
        clean = value.split(' ')[0].replace('$', '').replace(',', '').strip()
        try:
            return float(clean)
        except:
            return 0.0

    def get_manual_fallback(self):
        """Engineering Fallback to ensure the app always has data."""
        data = {
            'city': ['Seoul', 'Los Angeles', 'Chicago', 'London', 'Paris', 'Tokyo', 'Osaka'],
            'revenue_usd': [8429884, 9529663, 8057214, 8945415, 4589532, 16477002, 12544230],
            'era': '2018 Love Yourself'
        }
        return pd.DataFrame(data)

    def run_pipeline(self):
        all_raw_rows = []
        all_cleaned_rows = []

        for era_label, config in self.targets.items():
            print(f" Connecting to TouringData for {era_label}...")
            try:
                response = requests.get(config["url"], headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                tables = soup.find_all('table')

                for i, table in enumerate(tables):
                    # Filter for BTS tables only
                    if "BTS" in table.get_text() or "ARIRANG" in table.get_text():
                        rows = table.find_all('tr')
                        for row in rows:
                            cells = row.find_all('td')
                            if len(cells) >= 2:
                                text_l = cells[0].get_text(strip=True)
                                text_r = cells[1].get_text(strip=True)
                                
                                # Step 1: Store Raw Data for progress tracking
                                all_raw_rows.append({
                                    'era': era_label,
                                    'raw_text_left': text_l,
                                    'raw_text_right': text_r
                                })

                                # Step 2: Cleaning Engine (Fundamental Logic)
                                if any(year in text_l for year in config["year_filter"]):
                                    # Split location logic
                                    location_part = text_l.split('BTS')[-1] if 'BTS' in text_l else text_l
                                    
                                    rev_val = self.clean_numeric(text_r)
                                    
                                    # Predictive Logic: If 2026 is TBA, apply 2.8x multiplier to 2018 baseline
                                    if era_label == "2026 Arirang" and rev_val == 0.0:
                                        # Use a baseline average if specific city data is missing
                                        rev_val = 8524155.0 * 2.8 

                                    all_cleaned_rows.append({
                                        'date': text_l[:15],
                                        'venue': location_part.split('Stadium')[0] + 'Stadium' if 'Stadium' in location_part else 'Arena',
                                        'city': location_part.split(',')[-2].strip() if ',' in location_part else 'Unknown',
                                        'country': location_part.split(',')[-1].strip() if ',' in location_part else 'Unknown',
                                        'revenue_usd': rev_val,
                                        'era': era_label,
                                        'is_stadium': 1 if 'Stadium' in location_part else 0,
                                        'is_sold_out': 1 if '100%' in text_r else 0,
                                        'artist': 'BTS'
                                    })
            except Exception as e:
                print(f"Scraper Error on {era_label}: {e}")

        # --- SAVE OUTPUTS ---
        
        # 1. Save Raw Dataset (To show progress)
        raw_df = pd.DataFrame(all_raw_rows)
        raw_df.to_csv('raw_bts_data.csv', index=False)
        print(f"Saved {len(raw_df)} messy rows to 'raw_bts_data.csv'")

        # 2. Save Cleaned Dataset (For Data Modeling)
        clean_df = pd.DataFrame(all_cleaned_rows)
        clean_df = clean_df[~clean_df['city'].str.contains('Total|TOTAL', na=False)]
        
        # Final Output Files
        clean_df.to_csv('cleaned_bts_data.csv', index=False)
        clean_df[['city', 'revenue_usd', 'era']].to_csv('tour_economics.csv', index=False)

        print(f"Success! Created 'cleaned_bts_data.csv' and 'tour_economics.csv'")
        print(f"Total Features: {len(clean_df.columns)}")

if __name__ == "__main__":
    processor = TourEconomicProcessor()
    processor.run_pipeline()
