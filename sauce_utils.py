import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "sauces.csv"
REVIEWS_PATH = Path(__file__).parent / "data" / "reviews.csv"


def load_sauces(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the sauce dataset."""
    return pd.read_csv(path)


def load_reviews(path: Path = REVIEWS_PATH) -> pd.DataFrame:
    """Load user reviews."""
    return pd.read_csv(path)


def get_average_ratings(reviews: pd.DataFrame) -> pd.Series:
    """Return average rating per sauce."""
    return reviews.groupby("sauce")['rating'].mean()


def summarize_reviews(reviews: pd.DataFrame, sauce: str) -> str:
    """Return a short summary of reviews for a sauce."""
    subset = reviews[reviews["sauce"] == sauce]
    if subset.empty:
        return "No reviews yet."
    comments = subset.sort_values(by="rating", ascending=False)["comment"].head(2)
    return " | ".join(comments.tolist())


def recommend_sauces(df: pd.DataFrame, heat_pref: int, region_pref: str | None = None,
                     flavor_pref: str | None = None, n: int = 3) -> pd.DataFrame:
    """Return top n recommended sauces based on preferences."""

    def score(row: pd.Series) -> float:
        score_val = -abs(row["heat"] - heat_pref)
        if region_pref and region_pref != "Any":
            score_val += 1 if row["region"] == region_pref else 0
        if flavor_pref and flavor_pref != "Any":
            score_val += 1 if row["flavor"] == flavor_pref else 0
        score_val += row.get("rating", 0) / 2
        return score_val

    scored = df.copy()
    scored["score"] = scored.apply(score, axis=1)
    return scored.sort_values(by="score", ascending=False).head(n)


def get_top_sauces(df: pd.DataFrame, reviews: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return top sauces by average rating."""
    avg = get_average_ratings(reviews)
    merged = df.set_index("name").join(avg.rename("avg_rating"))
    merged["avg_rating"].fillna(0, inplace=True)
    return merged.sort_values(by="avg_rating", ascending=False).head(n).reset_index()
