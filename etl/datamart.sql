-- explode genero (separado por |) em linhas
CREATE OR REPLACE VIEW dm_movie_genre AS
SELECT m.movie_id, m.title,
       unnest(string_to_array(COALESCE(m.genre,''), '|'))::text AS genre
FROM dw_movies m;

CREATE OR REPLACE VIEW dm_top10_by_genre AS
SELECT g.genre,
       m.title,
       AVG(r.score) AS avg_score,
       COUNT(r.rating_id) AS total_ratings
FROM dm_movie_genre g
JOIN dw_ratings r ON r.movie_id = g.movie_id
JOIN dw_movies  m ON m.movie_id = g.movie_id
GROUP BY g.genre, m.title
HAVING COUNT(r.rating_id) >= 1
ORDER BY g.genre, avg_score DESC, total_ratings DESC
LIMIT 100;

CREATE OR REPLACE VIEW dm_avg_by_ageband AS
SELECT CASE
         WHEN u.age IS NULL          THEN 'unknown'
         WHEN u.age < 18             THEN '<18'
         WHEN u.age BETWEEN 18 AND 24 THEN '18-24'
         WHEN u.age BETWEEN 25 AND 34 THEN '25-34'
         WHEN u.age BETWEEN 35 AND 44 THEN '35-44'
         WHEN u.age BETWEEN 45 AND 54 THEN '45-54'
         ELSE '55+'
       END AS age_band,
       AVG(r.score) AS avg_score,
       COUNT(*)     AS n
FROM dw_users u
JOIN dw_ratings r ON r.user_id = u.user_id
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE VIEW dm_ratings_by_country AS
SELECT u.country, COUNT(r.rating_id) AS total_ratings
FROM dw_users u
JOIN dw_ratings r ON r.user_id = u.user_id
GROUP BY u.country
ORDER BY total_ratings DESC;

CREATE OR REPLACE VIEW dm_top5_popular AS
SELECT m.title, COUNT(r.rating_id) AS n
FROM dw_ratings r
JOIN dw_movies m ON m.movie_id = r.movie_id
GROUP BY m.title
ORDER BY n DESC, m.title ASC
LIMIT 5;

CREATE OR REPLACE VIEW dm_best_genre AS
SELECT g.genre, AVG(r.score) AS avg_score, COUNT(*) AS n
FROM dm_movie_genre g
JOIN dw_ratings r ON r.movie_id = g.movie_id
GROUP BY g.genre
HAVING COUNT(*) >= 3
ORDER BY avg_score DESC
LIMIT 1;

CREATE OR REPLACE VIEW dm_top_country AS
SELECT country, SUM(n) AS total_ratings
FROM (
  SELECT u.country, COUNT(r.rating_id) AS n
  FROM dw_users u
  JOIN dw_ratings r ON r.user_id = u.user_id
  GROUP BY u.country
) t
GROUP BY country
ORDER BY total_ratings DESC
LIMIT 1;
