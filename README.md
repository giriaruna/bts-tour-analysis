# 💜 BTS: The Quantum Leap | Predictive Engineering Audit

**Team:** Aruna Giri, Jane Manalu, KJ Moses  
**Course:** Data Bootcamp Midterm  
**Date:** March 2026

---

## Quick Links

- **Live Dashboard:** https://bts-tour-analysis.streamlit.app  
- **Full Project Report (PDF):** https://drive.google.com/file/d/1YxZj1AZXis_vz1zJXsGqI6uqOIhtWXwJ/view?usp=sharing

---

## Executive Summary

This project analyzes the global touring ecosystem of BTS using data-driven methods.  
Using the **2018 Love Yourself Tour** as a baseline, we project the potential impact of the upcoming **2026 Arirang World Tour**.

By combining music streaming data, economic indicators, and tour information, the project explores how large-scale music events influence tourism, consumer spending, and regional economic activity.

The analysis demonstrates how global concerts can function as measurable economic drivers across multiple countries.

---

## Research Questions

### 1. Infrastructure Scaling
How has the global touring footprint expanded from **14 countries in 2018** to a projected **23 countries in 2026**?

### 2. The BTS Economic Effect
What measurable changes occurred in tourism and local consumption during the 2018 tour period?

### 3. Predictive Modeling
Can historical demand trends and a **USD 183 average ticket price** be used to estimate future tour revenue?

---

## Key Findings

| Metric | 2018 (Baseline) | 2026 (Projected) | Change |
|------|------|------|------|
| Total Shows | 62 | 82 | +32.3% |
| Geographic Reach | 14 Countries | 23 Countries | +64.0% |
| South Korea Tourism | Baseline | +15.1% | +15.1% |
| Brazil Consumption | Baseline | +2.4% | +2.4% |
| France Revenue | USD 4.5M | USD 51.0M | +1000% |

**Fandom Multiplier:**  
A 2.8× demand effect was applied to represent accumulated fan demand following a multi-year hiatus.

**Projected 2026 Revenue:**  
**USD 108M** across three primary markets:
- South Korea
- France
- Brazil

---

## Project Structure

The project is organized into modular scripts:

- **tour_processor.py**  
  Collects historical tour revenue data.

- **ly_2018_short_growth.py**  
  Analyzes economic indicators during the 2018 tour period.

- **arirang_predictor.py**  
  Generates revenue projections using historical trends.

- **app.py**  
  Interactive Streamlit dashboard for visualization.

---

## Modeling Approach

The prediction model considers three main factors:

### Capacity Expansion
Example: France transitions from a 20,000-seat arena to an 80,000-seat stadium, increasing total revenue potential.

### Market Maturity
In South Korea, attendance capacity slightly decreases but revenue rises due to higher ticket pricing.

### Operational Scaling
Brazil’s growth is modeled by increasing the number of concert dates within existing venues.

---

## How to Reproduce

### 1. Clone Repository
```bash
git clone https://github.com/giriaruna/bts-tour-analysis.git
