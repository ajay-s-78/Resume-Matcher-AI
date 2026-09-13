from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import FileResponse
from app.models.schemas import MatchRequest, MatchResponse, HealthResponse, RootResponse
from app.services.bert_matcher import BertMatcherService
from app.services.skill_matcher import SkillMatcherService
from app.services.feedback_generator import FeedbackGeneratorService

router = APIRouter()

# Instantiate services
bert_matcher = BertMatcherService()
skill_matcher = SkillMatcherService()
feedback_generator = FeedbackGeneratorService()

@router.get("/", response_model=RootResponse, tags=["General"])
def root(request: Request):
    """
    Root endpoint returning frontend UI for web browsers and JSON status message for API clients.
    """
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return FileResponse(
            "frontend/index.html",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    return RootResponse(message="Resume Matcher API is running")

@router.get("/health", response_model=HealthResponse, tags=["General"])
def health():
    """
    Health check endpoint to verify backend status.
    """
    return HealthResponse(status="healthy")

@router.post("/match", response_model=MatchResponse, tags=["Matching"])
def match_resume(request: MatchRequest):
    """
    Calculates semantic similarity between resume and job description,
    extracts matched and missing skills, and generates feedback.
    """
    if not request.resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="resume_text cannot be empty."
        )
    if not request.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="job_description cannot be empty."
        )

    try:
        # 1. BERT Similarity Match Score
        score = bert_matcher.calculate_similarity(
            request.resume_text,
            request.job_description
        )

        # 2. Skill Extraction & Comparison
        matched_skills, missing_skills = skill_matcher.match_skills(
            request.resume_text,
            request.job_description
        )

        # 3. Feedback Generation (LLM or Rule-based)
        feedback = feedback_generator.generate_feedback(
            request.candidate_name,
            score,
            matched_skills,
            missing_skills
        )

        return MatchResponse(
            candidate_name=request.candidate_name,
            match_score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            feedback=feedback
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during resume matching: {str(e)}"
        )
