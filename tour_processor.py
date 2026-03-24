import requests
from bs4 import BeautifulSoup
import pandas as pd

class TourEconomicProcessor:
    def __init__(self, url):
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def clean_numeric(self, value):
        if not value: return 0
        return float(value.replace('$', '').replace(',', '').strip())

    def fetch_2018_stats(self):
        print(f"🌐 Scraping 2018 Baseline from: {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            all_tour_data = []

            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        all_tour_data.append({
                            'city': cols[0].text.strip(),
                            'revenue_usd': self.clean_numeric(cols[3].text.strip()),
                            'era': 'LY_2018' # Matches App
                        })

            df = pd.DataFrame(all_tour_data)
            return df[df['revenue_usd'] > 0].reset_index(drop=True)
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()

    def project_2026_growth(self, df_2018):
        if df_2018.empty: return df_2018
        print("Projecting Arirang 2026 Growth...")
        df_2026 = df_2018.copy()
        # Engineering Multiplier: 2.8x for 2026
        df_2026['revenue_usd'] = df_2026['revenue_usd'] * 2.8
        df_2026['era'] = 'ARIRANG_2026' # Matches App
        return pd.concat([df_2018, df_2026])

if __name__ == "__main__":
    url = "https://touringdata.org/2019/02/16/bts-love-yourself-tour/"
    processor = TourEconomicProcessor(url)
    raw_2018 = processor.fetch_2018_stats()
    master_econ = processor.project_2026_growth(raw_2018)
    # This filename must match what is in app.py
    master_econ.to_csv('tour_economics.csv', index=False)
    print("tour_economics.csv generated with matched names.")
