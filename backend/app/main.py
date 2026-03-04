import csv
from io import StringIO

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .alerts import start_scheduler
from .config import settings
from .database import Base, engine, get_db
from .models import SavedIdea
from .schemas import SaveIdeaRequest, SavedIdeaResponse, TrendItem
from .trends import collect_trends

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    start_scheduler()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/search", response_model=list[TrendItem])
async def search(keyword: str = Query(..., min_length=2, max_length=100)):
    return await collect_trends(keyword)


@app.get("/api/dashboard", response_model=list[TrendItem])
async def dashboard():
    focus_keywords = ["ai", "startups", "ecommerce"]
    output = []
    for keyword in focus_keywords:
        output.extend(await collect_trends(keyword))
    output.sort(key=lambda x: x["viral_score"], reverse=True)
    return output[:30]


@app.post("/api/ideas", response_model=SavedIdeaResponse)
def save_idea(payload: SaveIdeaRequest, db: Session = Depends(get_db)):
    idea = SavedIdea(**payload.model_dump(), url=str(payload.url))
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return idea


@app.get("/api/ideas", response_model=list[SavedIdeaResponse])
def list_ideas(db: Session = Depends(get_db)):
    return db.scalars(select(SavedIdea).order_by(SavedIdea.created_at.desc())).all()


@app.delete("/api/ideas/{idea_id}")
def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    idea = db.get(SavedIdea, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    db.delete(idea)
    db.commit()
    return {"deleted": True}


@app.get("/api/export.csv")
def export_csv(db: Session = Depends(get_db)):
    ideas = db.scalars(select(SavedIdea).order_by(SavedIdea.created_at.desc())).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "source", "keyword", "url", "viral_score", "created_at"])
    for idea in ideas:
        writer.writerow([idea.id, idea.title, idea.source, idea.keyword, idea.url, idea.viral_score, idea.created_at.isoformat()])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=viral-trend-ideas.csv"},
    )
