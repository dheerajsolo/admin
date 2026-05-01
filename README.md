# Admin Operations Dashboard

A fast, reusable Streamlit operations dashboard for WooCommerce + Shiprocket workflows.

## Features

- Demo mode works without API keys
- Reusable service/adapter architecture
- Orders, inventory, shipping, returns and reports pages
- Custom dark sidebar and modern cards
- WooCommerce and Shiprocket adapter placeholders
- Secrets-safe setup for GitHub and Streamlit Cloud

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Secrets

Do not commit `.env` or `.streamlit/secrets.toml`.
Use `.env.example` as a template.

For Streamlit Cloud, add secrets in App Settings > Secrets.
