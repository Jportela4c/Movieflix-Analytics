import os
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
PG_HOST = os.getenv("POSTGRES_HOST", "dw")
PG_DB = os.getenv("POSTGRES_DB", "movieflix_dw")
PG_USER = os.getenv("POSTGRES_USER", "movieflix")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "movieflix")

engine = create_engine(f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:5432/{PG_DB}")

ROOT = Path(__file__).parent
DATA = ROOT / "datalake"

with engine.begin() as con:
    sql = (Path(__file__).parents[1] / "dw" / "init_dw.sql").read_text()
    con.execute(text(sql))

movies = pd.read_csv(DATA/"movies.csv")
movies.columns = [c.strip().lower() for c in movies.columns]
movies.to_sql("dw_movies", engine, if_exists="append", index=False)

users = pd.read_csv(DATA/"users.csv")
users.columns = [c.strip().lower() for c in users.columns]
users.to_sql("dw_users", engine, if_exists="append", index=False)

ratings = pd.read_csv(DATA/"ratings.csv")
ratings.columns = [c.strip().lower() for c in ratings.columns]

with engine.begin() as con:
    user_map = dict(con.execute(text("SELECT name, user_id FROM dw_users")).fetchall())
    movie_map = dict(con.execute(text("SELECT title, movie_id FROM dw_movies")).fetchall())

ratings["user_id"] = ratings["user_name"].map(user_map)
ratings["movie_id"] = ratings["movie_title"].map(movie_map)
ratings = ratings.drop(columns=["user_name", "movie_title"])
ratings.to_sql("dw_ratings", engine, if_exists="append", index=False)

with engine.begin() as con:
    dm_sql = (ROOT / "datamart.sql").read_text()
    con.execute(text(dm_sql))

print("Carga DW/DM concluída.")
