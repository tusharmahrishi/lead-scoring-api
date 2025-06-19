from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Input schema
def clean_string(s):
    return s.strip().lower() if s else ""

class LeadInput(BaseModel):
    industry: Optional[str] = ""
    title: Optional[str] = ""
    lead_source: Optional[str] = ""

# Simple rule-based scoring logic (can be replaced with ML later)
def score_lead(industry, title, lead_source):
    score = 50
    explanation = []

    if clean_string(industry) == "finance":
        score += 20
        explanation.append("Finance industry (+20)")
    elif clean_string(industry) == "technology":
        score += 10
        explanation.append("Technology industry (+10)")

    if clean_string(title) and ("director" in title.lower() or "vp" in title.lower()):
        score += 15
        explanation.append("Senior title (+15)")

    if clean_string(lead_source) == "web":
        score += 5
        explanation.append("Lead source is Web (+5)")

    category = "Hot" if score >= 80 else "Warm" if score >= 60 else "Cold"
    return score, category, "; ".join(explanation)

@app.post("/score-lead")
def api_score_lead(lead: LeadInput):
    score, category, reason = score_lead(lead.industry, lead.title, lead.lead_source)
    return {
        "score": score,
        "category": category,
        "reason": reason
    }

# Run with: uvicorn lead_scoring_api:app --reload
if __name__ == "__main__":
    uvicorn.run("lead_scoring_api:app", host="0.0.0.0", port=8000, reload=True)
