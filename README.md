# 🌶 SauceFinders Prototype

This project contains a small proof‑of‑concept application for the **SauceFinders** marketplace. The app is built with [Streamlit](https://streamlit.io/) and showcases a sample catalogue of sauces plus a simple "Flavor Finder" quiz that recommends sauces based on heat, region and flavor profile.

![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

## Running locally

1. Install the requirements

```bash
pip install -r requirements.txt
```

2. Start the application

```bash
streamlit run streamlit_app.py
```

The datasets used by the demo live in `data/sauces.csv` and `data/reviews.csv`. Feel free to modify or expand them.

### Features

- Browse sauces with heat and rating filters
- Flavor Finder quiz for personalized picks
- Heat League rankings based on community reviews
- Sauce Spotlight pages with videos and review summaries
