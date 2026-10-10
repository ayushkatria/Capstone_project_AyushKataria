# Mamaearth Returns & Growth Intelligence Pipeline

## Project Overview

A reproducible data analytics pipeline for analyzing Mamaearth's e-commerce performance, including order returns, payment methods, and monthly revenue trends. The project combines SQL, Python, data visualization, and AI-generated business insights.

## 1. Database Setup and SQL Reports

Use SQLite to initialize the database and execute the SQL scripts from the repository root in this order:

1. Run `sql/schema.sql` to create the `customers`, `products`, and `orders` tables.
2. Run `sql/seed_data.sql` to load the sample data. If importing CSV files using SQLite `.import`, clean blank strings in `discount_pct` and `rating` where required.
3. Run `sql/reports.sql` to generate baseline business reports and metrics.

Ensure the database is populated correctly before running the analysis scripts.

## 2. Data Cleaning, EDA, and Visualization

Run the following commands from the repository root:

```bash
python analysis/clean_and_eda.py
python analysis/visualize.py
```

The cleaning script processes missing values, duplicate records, and inconsistent payment-method casing. It reconciles revenue and performs exploratory data analysis. Task 5 of Part 2 writes the verified findings to `narrator/findings.json`. The visualization script generates `visualizations/return_rate_by_payment.png` and `visualizations/monthly_revenue_trend.png`.

## 3. Generate the Business Narrative

**Online mode:** Set your Gemini API key as an environment variable and run the narrative generator.

```bash
export GEMINI_API_KEY="your_api_key"
python narrator/generate_narrative.py
```

On Windows PowerShell, use `$env:GEMINI_API_KEY="your_api_key"` instead.

**Offline mode:** Unset the API key and run the same Python command. The script uses its deterministic offline narrative template, if implemented, without requiring Gemini API access.

## Reproducibility

Execute all steps sequentially using the same source data and database configuration. Confirm that `narrator/findings.json` is refreshed before generating the narrative. Verify reported metrics against the SQL reports and Python analysis outputs.
