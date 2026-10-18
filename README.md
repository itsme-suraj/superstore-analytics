# Superstore Business Intelligence Dashboard

Single-page Streamlit dashboard with global header filters, light/dark theme and 8 tabs:
Overview, Sales, Profit, Regions, Products & Customers, Shipping, Data Explorer, Guide & About.

## Project structure
```
app.py              # the whole dashboard (entry point)
Superstore.csv      # your dataset (keep your existing file here)
requirements.txt
.streamlit/config.toml
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
If `Superstore.csv` is missing, the app shows an upload box instead of crashing.

## Deploy (Streamlit Community Cloud)
Main file path: `app.py`. Do NOT keep an old `pages/` folder, Streamlit would show it in navigation.
