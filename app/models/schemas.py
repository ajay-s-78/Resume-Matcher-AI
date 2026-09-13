from pydantic import BaseModel, Field
from typing import List

class MatchRequest(BaseModel):
    """Request model for resume and job description matching."""
    candidate_name: str = Field(..., description="Name of the candidate", json_schema_extra={"example": "Ajay"})
    resume_text: str = Field(..., description="Content of the candidate's resume", json_schema_extra={"example": "Python, SQL, Pandas, Machine Learning"})
    job_description: str = Field(..., description="Target job description text", json_schema_extra={"example": "Looking for a Python developer with SQL, Machine Learning, Docker and AWS."})

class MatchResponse(BaseModel):
    """Response model containing match results and recommendations."""
    candidate_name: str = Field(..., description="Name of the candidate")
    match_score: float = Field(..., description="Similarity match score percentage (0-100)")
    matched_skills: List[str] = Field(default_factory=list, description="Skills present in both resume and job description")
    missing_skills: List[str] = Field(default_factory=list, description="Required skills missing from candidate's resume")
    feedback: str = Field(..., description="AI or rule-based improvement suggestions")

class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., json_schema_extra={"example": "healthy"})

class RootResponse(BaseModel):
    """Root endpoint response schema."""
    message: str = Field(..., json_schema_extra={"example": "Resume Matcher API is running"})
