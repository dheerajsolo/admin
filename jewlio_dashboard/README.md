# Jewlio Operations Dashboard

Modular Streamlit dashboard inside one folder: `jewlio_dashboard`.

## Streamlit Cloud

Main file path:

```text
jewlio_dashboard/app.py
```

## Local run

```bash
cd jewlio_dashboard
pip install -r requirements.txt
streamlit run app.py
```

Default demo login password:

```text
admin
```

## Folder structure

```text
jewlio_dashboard/
├── app.py
├── config.py
├── controllers/
├── components/
├── modules/
├── services/
├── adapters/
└── utils/
```

## Security

Do not commit `.env` or `.streamlit/secrets.toml`.
Use Streamlit Secrets for real API credentials.
