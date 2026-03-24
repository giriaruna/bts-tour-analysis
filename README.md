# 💜 BTS: The Quantum Leap (2018 vs. 2026)
**Team:** Aruna Giri, Jane Manalu, KJ Moses
---

## Executive Summary
This project performs a comparative and predictive engineering audit of the BTS global touring ecosystem. By analyzing the **2018 Love Yourself Tour** as a baseline and projecting the impact of the upcoming **2026 Arirang World Tour**, we explore how the "BTS Sound" correlate with the economic tourism demand. 

We engineered a multi-module data pipeline that integrates:
1. **Digital Signal Metadata** (via Spotify Web API)
2. **Global Demand Signals** (via Google Trends API)
3. **Historical Economic Stats** (via Web Scraping TouringData)

---

## Technical Architecture
To ensure high **Readability and Reproducibility (10%)**, the project is divided into specialized modules:

*   `spotify_fetcher.py`: Connects to the Spotify Web API to extract high-dimensional audio features (Energy, Tempo, Danceability).
*   `tour_processor.py`: Implements a BeautifulSoup scraper to audit historical box office revenue and applies a predictive multiplier for 2026.
*   `app.py`: A Streamlit-based interactive dashboard for real-time data visualization and "Hype" analysis.

---

---

## 🚀 How to Reproduce
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/giriaruna/bts-tour-analysis.git
