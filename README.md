
# Mamaearth Returns & Growth Intelligence Pipeline

A fully reproducible end-to-end data analytics and GenAI intelligence pipeline investigating order returns, payment risk segments, and revenue trends for Mamaearth.

---

## Execution Guide

Follow these steps in strict chronological order to reproduce every number from scratch:

### Step 1: SQL Relational Layer (`sql/`)
1. Initialize your SQLite database and run `sql/schema.sql` to build the tables.
2. Run `sql/seed_data.sql` to load raw CSV data into `customers`, `products`, and `orders`.
   *(If using SQLite `.import`, run the blank string cleanup script for `discount_pct` and `rating` cells immediately after).*
3. Execute `sql/reports.sql` to generate baseline metrics.

### Step 2: Python Data Wrangling & EDA (`analysis/`)
Run the independent Python data cleaning and exploratory pipeline:
```bash
python analysis/clean_and_eda.py
python analysis/visualize.py
clean_and_eda.py cleans payment casing, removes duplicates, handles missing values, reconciles total revenue (₹97,358.30), and automatically completes Task 5 by writing verified metrics to narrator/findings.json.

visualize.py saves output charts (return_rate_by_payment.png, monthly_revenue_trend.png) to visualizations/.

### Step 3: GenAI Insight Narrator (narrator/)
Generate the executive business narrative based on verified figures:

Online Mode (Gemini API): Set your API key and run the script:

Bash
export GEMINI_API_KEY="your_api_key"
python narrator/generate_narrative.py

Offline Path (Keyless Fallback): Run the script with no API key configured. It automatically utilizes the deterministic offline template (generate_scr_narrative_offline) with zero network access required.
