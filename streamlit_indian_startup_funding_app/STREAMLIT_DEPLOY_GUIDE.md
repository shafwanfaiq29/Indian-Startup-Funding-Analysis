# Streamlit Deployment Guide

## Repository Structure

Upload these files to the root of your GitHub repository:

```text
Indian-Startup-Funding-Analysis/
├── streamlit_app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── data/
│   └── startup_funding_cleaned.csv
├── notebook/
│   └── Indian_Startup_Funding_EDA.ipynb
└── README.md
```

## Deploy to Streamlit Community Cloud

1. Open Streamlit Community Cloud: https://share.streamlit.io/
2. Sign in with GitHub.
3. Click **Create app** or **New app**.
4. Select repository: `shafwanfaiq29/Indian-Startup-Funding-Analysis`.
5. Set main file path: `streamlit_app.py`.
6. Click **Deploy**.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
