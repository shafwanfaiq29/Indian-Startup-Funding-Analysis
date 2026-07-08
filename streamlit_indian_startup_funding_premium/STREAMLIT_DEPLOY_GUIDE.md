# Streamlit Dashboard Deployment Guide

## Recommended Repository Structure

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

## Deploy on Streamlit Community Cloud

1. Go to Streamlit Community Cloud.
2. Sign in with GitHub.
3. Create a new app.
4. Choose repository:
   `shafwanfaiq29/Indian-Startup-Funding-Analysis`
5. Set main file path:
   `streamlit_app.py`
6. Click Deploy.

## Local Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Notes

The app expects the cleaned dataset to be located at:

```text
data/startup_funding_cleaned.csv
```
