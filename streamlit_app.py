import streamlit as st
from sauce_utils import (
    load_sauces,
    load_reviews,
    recommend_sauces,
    get_top_sauces,
    summarize_reviews,
)

st.set_page_config(page_title="SauceFinders", page_icon="🌶")

st.title("🌶 SauceFinders Marketplace")
st.write("Discover unique sauces from around the world.")

# Load data
sauces = load_sauces()
reviews = load_reviews()

# Tabs for browsing and quiz
browse_tab, quiz_tab, league_tab, spotlight_tab = st.tabs([
    "Browse Sauces",
    "Flavor Finder Quiz",
    "Heat League",
    "Sauce Spotlight",
])

with browse_tab:
    st.subheader("All Sauces")
    max_heat = st.slider("Maximum heat", 1, 10, 10)
    filtered = sauces[sauces["heat"] <= max_heat]
    st.dataframe(
        filtered[["name", "heat", "region", "flavor", "price", "rating"]],
        use_container_width=True,
    )

with quiz_tab:
    st.subheader("Find your perfect sauce")
    heat_pref = st.slider("Preferred heat", 1, 10, 5)
    region_options = ["Any"] + sorted(sauces["region"].unique().tolist())
    region_pref = st.selectbox("Preferred region", region_options)
    flavor_options = ["Any"] + sorted(sauces["flavor"].unique().tolist())
    flavor_pref = st.selectbox("Flavor profile", flavor_options)

    if st.button("Recommend"):
        results = recommend_sauces(sauces, heat_pref, region_pref, flavor_pref)
        for _, row in results.iterrows():
            st.markdown(f"### {row['name']}")
            st.write(row['description'])
            st.write(f"Price: ${row['price']:.2f}")
            st.progress(row['heat'] / 10, text=f"Heat {row['heat']}/10")
            st.write(f"Rating: {row['rating']}/5")
            st.write("---")

with league_tab:
    st.subheader("Heat League - Top Sauces")
    top = get_top_sauces(sauces, reviews)
    for _, row in top.iterrows():
        st.markdown(f"### {row['name']}")
        st.progress(row['heat'] / 10, text=f"Heat {row['heat']}/10")
        st.write(f"Average rating: {row['avg_rating']:.1f}/5")
        st.write("---")

with spotlight_tab:
    st.subheader("Sauce Spotlight")
    choice = st.selectbox("Select a sauce", sauces['name'])
    sel = sauces[sauces['name'] == choice].iloc[0]
    st.markdown(f"### {sel['name']} by {sel['creator']}")
    st.write(sel['description'])
    st.video(sel['video'])
    st.progress(sel['heat'] / 10, text=f"Heat {sel['heat']}/10")
    st.write(f"Rating: {sel['rating']}/5")
    st.write(summarize_reviews(reviews, sel['name']))

