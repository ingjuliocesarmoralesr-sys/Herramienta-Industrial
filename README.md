# ViralTrendFinder

ViralTrendFinder is a web application that discovers potentially viral content using **only public sources**:

- Reddit API
- YouTube Data API
- Google News RSS

> The project intentionally does **not** scrape Facebook or Instagram.

## Stack

- Backend: FastAPI (Python)
- Frontend: Next.js
- Database: PostgreSQL
- Scheduler: APScheduler cron (daily alerts)

## Features

1. Search keywords across all supported providers
2. Trending dashboard with multi-keyword aggregation
3. Viral score ranking based on engagement + recency
4. Save ideas to PostgreSQL
5. Export saved ideas as CSV
6. Daily alert job scaffold (runs at 09:00)

## Run with Docker

```bash
docker compose up --build
```

App URLs:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Local development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment variables

Backend (`backend/.env`):

- `DATABASE_URL` (PostgreSQL SQLAlchemy URL)
- `YOUTUBE_API_KEY` (optional but needed for YouTube ingestion)
- `ALLOWED_ORIGINS`
- `REDDIT_USER_AGENT`

Frontend (`frontend/.env.local`):

- `NEXT_PUBLIC_API_BASE_URL`
