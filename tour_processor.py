import requests
from bs4 import BeautifulSoup
import pandas as pd

class TourEconomicProcessor:
    def __init__(self, url):
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def fetch_2018_stats(self):
        print(f" Attempting to scrape: {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            
            if not tables:
                print(" Scraper blocked or no tables found. Using manual fallback data.")
                return self.get_manual_data()

            all_tour_data = []
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        all_tour_data.append({
                            'city': cols[0].text.strip(),
                            'revenue_usd': self.clean_numeric(cols[3].text.strip()),
                            'era': 'LY_2018'
                        })
            
            df = pd.DataFrame(all_tour_data)
            return df[df['revenue_usd'] > 0]
        except Exception as e:
            print(f" Scraper Error: {e}. Using manual fallback.")
            return self.get_manual_data()

    def clean_numeric(self, value):
        return float(value.replace('$', '').replace(',', '').strip()) if value else 0

    def get_manual_data(self):
        # Professional Fallback: Hardcoded data from TouringData link
        data = {
            'city': ['Seoul', 'Los Angeles', 'Chicago', 'London', 'Paris', 'Tokyo', 'Osaka'],
            'revenue_usd': [8429884, 9529663, 8057214, 8945415, 4589532, 16477002, 12544230],
            'era': 'LY_2018'
        }
        return pd.DataFrame(data)

    def project_2026_growth(self, df_2018):
        print("Projecting 2026 Arirang Growth...")
        df_2026 = df_2018.copy()
        df_2026['revenue_usd'] = df_2026['revenue_usd'] * 2.8
        df_2026['era'] = 'ARIRANG_2026'
        return pd.concat([df_2018, df_2026])

if __name__ == "__main__":
    url = "https://touringdata.org/2019/02/16/bts-love-yourself-tour/"
    processor = TourEconomicProcessor(url)
    raw_df = processor.fetch_2018_stats()
    master_df = processor.project_2026_growth(raw_df)
    master_df.to_csv('tour_economics.csv', index=False)
    print(f"tour_economics.csv generated with {len(master_df)} rows.")
