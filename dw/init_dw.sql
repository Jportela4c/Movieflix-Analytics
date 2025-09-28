-- Esquema DW (camada tratada)
CREATE TABLE IF NOT EXISTS dw_movies (
  movie_id   SERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  year       INT,
  genre      TEXT,      -- "Action|Drama"
  country    TEXT,
  imdb_rating NUMERIC
);

CREATE TABLE IF NOT EXISTS dw_users (
  user_id  SERIAL PRIMARY KEY,
  name     TEXT NOT NULL,
  age      INT,
  country  TEXT
);

CREATE TABLE IF NOT EXISTS dw_ratings (
  rating_id  SERIAL PRIMARY KEY,
  user_id    INT REFERENCES dw_users(user_id),
  movie_id   INT REFERENCES dw_movies(movie_id),
  score      NUMERIC NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);
