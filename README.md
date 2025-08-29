# Supermarket Food Waste Reduction — Simulation Capstone

This project simulates perishable inventory under different operational policies to reduce food waste while protecting sales and margin.

## Why
Perishables drive revenue but cause high spoilage. We compare donation policies, markdown strategies, and replenishment thresholds to find waste–profit trade-offs.

## How it works
1) Generate/ingest demand series and shelf-life by SKU  
2) Apply policy set (donate-by-day, markdown ladder, reorder point)  
3) Simulate inventory flows over a 90-day horizon  
4) Report KPIs: sales, revenue, waste (kg/%), service level, donations

## Quickstart
```bash
# 1) setup
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# 2) run baseline experiment
python main.py --config configs/baseline.yaml

# 3) launch dashboard
streamlit run app/streamlit_app.py
