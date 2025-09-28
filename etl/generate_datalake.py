import os
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # crie grátis em http://www.omdbapi.com/
OUT = Path(__file__).parent / "datalake"
OUT.mkdir(parents=True, exist_ok=True)

TITLES = [
    "Inception", "Spirited Away", "City of God", "The Dark Knight", "Parasite"
]

movies = []
for t in TITLES:
    if OMDB_API_KEY:
        r = requests.get("https://www.omdbapi.com/", params={"t": t, "apikey": OMDB_API_KEY})
        data = r.json()
        if data.get("Response") == "True":
            movies.append({
                "title": data.get("Title"),
                "year": int(data.get("Year", "0")[:4]) if data.get("Year") else None,
                "genre": "|".join([g.strip() for g in data.get("Genre"," ").split(",") if g.strip()]),
                "country": data.get("Country"),
                "imdb_rating": float(data.get("imdbRating")) if data.get("imdbRating") not in ("N/A", None, "") else None
            })
        else:
            movies.append({"title": t, "year": None, "genre": None, "country": None, "imdb_rating": None})
    else:
        fallback = {
            "Inception": (2010, "Action|Sci-Fi", "USA", 8.8),
            "Spirited Away": (2001, "Animation|Fantasy", "Japan", 8.6),
            "City of God": (2002, "Crime|Drama", "Brazil", 8.6),
            "The Dark Knight": (2008, "Action|Crime", "USA", 9.0),
            "Parasite": (2019, "Drama|Thriller", "South Korea", 8.6),
        }
        y, g, c, r = fallback[t]
        movies.append({"title": t, "year": y, "genre": g, "country": c, "imdb_rating": r})

pd.DataFrame(movies).to_csv(OUT/"movies.csv", index=False)

users = [
    {"name": "Alice", "age": 23, "country": "USA"},
    {"name": "Bruno", "age": 31, "country": "Brazil"},
    {"name": "Chen", "age": 29, "country": "China"},
    {"name": "Davi", "age": 19, "country": "Brazil"},
    {"name": "Eiko", "age": 41, "country": "Japan"},
]
pd.DataFrame(users).to_csv(OUT/"users.csv", index=False)

ratings = [
    {"user_name": "Alice", "movie_title": "Inception", "score": 5},
    {"user_name": "Bruno", "movie_title": "City of God", "score": 4},
    {"user_name": "Chen", "movie_title": "Parasite", "score": 5},
    {"user_name": "Davi", "movie_title": "The Dark Knight", "score": 4},
    {"user_name": "Eiko", "movie_title": "Spirited Away", "score": 5},
]
pd.DataFrame(ratings).to_csv(OUT/"ratings.csv", index=False)

print("CSV gerados em:", OUT)
