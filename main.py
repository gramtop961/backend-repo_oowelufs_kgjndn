import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Pro, Skill, Request

app = FastAPI(title="Campus Karma Exchange API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Campus Karma Exchange Backend Running"}

# Health and DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Seed demo content endpoint (idempotent little helper)
@app.post("/seed")
def seed_demo():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    # Only seed if empty
    if db["pro"].count_documents({}) == 0:
        demo_pros = [
            Pro(name="Aisha Khan", university="State University", department="CS", bio="ML tutor and Python mentor.", tags=["Python","ML","Data"], rating=4.9, reviews=112, verified=True, karma_rate=25),
            Pro(name="Marco Silva", university="Tech U", department="Design", bio="Figma and UI polish.", tags=["Figma","UI","Branding"], rating=4.8, reviews=76, verified=True, karma_rate=20),
            Pro(name="Yuki Tanaka", university="Polytechnic", department="Math", bio="Calculus made friendly.", tags=["Calculus","Linear Algebra"], rating=4.7, reviews=54, verified=False, karma_rate=15),
        ]
        for p in demo_pros:
            create_document("pro", p)

    if db["skill"].count_documents({}) == 0:
        skills = [
            Skill(title="Intro to Python", category="Coding", level="Beginner", owner_name="Aisha", featured=True),
            Skill(title="Figma Essentials", category="Design", level="Intermediate", owner_name="Marco"),
            Skill(title="Exam Prep: Calc I", category="Tutoring", level="Advanced", owner_name="Yuki"),
        ]
        for s in skills:
            create_document("skill", s)

    if db["request"].count_documents({}) == 0:
        reqs = [
            Request(title="Debug my JS app", category="Coding", urgency="High", requester_name="Sam", offered_karma=30),
            Request(title="Logo critique", category="Design", urgency="Normal", requester_name="Priya", offered_karma=15),
            Request(title="Calc homework help", category="Tutoring", urgency="Low", requester_name="Leo", offered_karma=10),
        ]
        for r in reqs:
            create_document("request", r)

    return {"status": "ok", "message": "Seeded if collections were empty"}

# Public listing endpoints
@app.get("/pros", response_model=List[Pro])
def list_pros(limit: int = 12):
    docs = get_documents("pro", {}, limit)
    # Convert Mongo docs to model compatible dicts
    return [Pro(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.get("/skills", response_model=List[Skill])
def list_skills(limit: int = 20):
    docs = get_documents("skill", {}, limit)
    return [Skill(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.get("/requests", response_model=List[Request])
def list_requests(limit: int = 20):
    docs = get_documents("request", {}, limit)
    return [Request(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
