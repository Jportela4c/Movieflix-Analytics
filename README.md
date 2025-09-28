# MovieFlix Analytics

Plataforma simples de cadastro e avaliação de filmes + pipeline de dados (Data Lake → DW → Data Mart) para análises. Infra com Docker, Nginx reverse proxy e CI/CD (GitHub Actions → Docker Hub).

## Arquitetura
- **App Web**: FastAPI + SQLite (cadastro de filmes/usuários/ratings)
- **Proxy**: Nginx → encaminha tráfego para o app
- **Data Lake**: CSVs (movies/users/ratings)
- **DW**: PostgreSQL (tabelas tratadas)
- **Data Mart**: views analíticas (top filmes, melhores gêneros, etc.)
- **ETL**: scripts Python (gera CSV via OMDb ou fallback e carrega no DW/DM)

## Rodando local
```bash
cp .env.example .env
# (opcional) export OMDB_API_KEY=xxxxx
docker compose up -d --build
curl http://localhost/health
```
Acesse `http://localhost`.

## Endpoints principais
- `GET /health`
- `POST /movies` `{ "title": "Inception", "year": 2010, "genre": "Action|Sci-Fi", "country": "USA" }`
- `GET /movies`
- `POST /users` `{ "name": "Alice", "age": 23, "country": "USA" }`
- `POST /ratings` `{ "user_id": 1, "movie_id": 1, "score": 5 }`

## ETL (Data Lake → DW → DM)
O serviço `etl` do Compose cria CSVs e carrega tudo no Postgres (dw). Use `queries.sql` para explorar as visões.

## CI/CD
Workflow em `.github/workflows/ci.yml`:
- Build imagem do app
- Teste `/health`
- Push no Docker Hub (`latest` e `SHA`)

### Secrets necessários
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- (opcional) `IMAGE_NAME` (default `movieflix-app`)

## Deploy com domínio (opcional)
- Use DuckDNS para um subdomínio → aponte para seu IP
- Exponha porta 80 (Nginx)
- (Opcional) Configure TLS com nginx-proxy-manager ou certbot

## Consultas analíticas
Veja `queries.sql`.
