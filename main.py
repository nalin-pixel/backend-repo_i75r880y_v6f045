import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Appointment, Review

app = FastAPI(title="Lady Salon Brașov API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Lady Salon Brașov API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# ----- Reviews (seed + list) -----
class ReviewOut(BaseModel):
    name: str
    text: str
    rating: int
    avatar_url: str | None = None

@app.get("/api/reviews", response_model=List[ReviewOut])
def list_reviews():
    # Try fetch from DB; if empty, return seeded examples (do not insert automatically)
    items = []
    try:
        items = get_documents("review")
        # Convert ObjectId to string-safe dicts
        cleaned = []
        for it in items:
            cleaned.append({
                "name": it.get("name", ""),
                "text": it.get("text", ""),
                "rating": int(it.get("rating", 5)),
                "avatar_url": it.get("avatar_url")
            })
        if cleaned:
            return cleaned
    except Exception:
        pass

    # Fallback static examples
    return [
        {"name": "Ana M.", "text": "Servicii impecabile și o atmosferă deosebită.", "rating": 5, "avatar_url": None},
        {"name": "Ioana P.", "text": "Cel mai frumos salon din Brașov! Recomand cu drag.", "rating": 5, "avatar_url": None},
        {"name": "Maria C.", "text": "Profesionalism și multă grijă pentru detalii.", "rating": 5, "avatar_url": None}
    ]

# ----- Appointments -----

@app.post("/api/appointments")
def create_appointment(payload: Appointment):
    try:
        appt_id = create_document("appointment", payload)
        return {"ok": True, "id": appt_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# SEO helper endpoint (optional for frontend pre-render hints)
@app.get("/api/seo/keywords")
def seo_keywords():
    return {
        "keywords": [
            "salon înfrumusețare Brașov",
            "coafor Brașov",
            "manichiură Brașov",
            "tratamente faciale Brașov",
            "masaj Brașov",
            "laminare sprâncene Brașov"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
