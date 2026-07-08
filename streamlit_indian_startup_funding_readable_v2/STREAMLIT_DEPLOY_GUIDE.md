# Streamlit Deployment Guide

Upload these files to the root of your GitHub repository:

```text
streamlit_app.py
requirements.txt
.streamlit/config.toml
```

Keep the cleaned dataset in:

```text
data/startup_funding_cleaned.csv
```

Deploy on Streamlit Community Cloud with:

```text
Main file path: streamlit_app.py
```

Local run:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
