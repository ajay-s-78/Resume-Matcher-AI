import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.text_preprocessor import TextPreprocessor
from app.services.skill_matcher import SkillMatcherService
from app.services.feedback_generator import FeedbackGeneratorService

client = TestClient(app)

def test_root_endpoint():
    """Test GET / endpoint returns 200 and correct payload."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Resume Matcher API is running"}

def test_health_endpoint():
    """Test GET /health endpoint returns 200 and status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_text_preprocessor():
    """Test NLTK text preprocessor functionality."""
    preprocessor = TextPreprocessor()
    text = "Looking for a Python Developer with SQL, Pandas & Machine Learning!"
    cleaned = preprocessor.clean_text(text)
    
    # Verify lowercasing and stopword removal ("for", "with", "a" are NLTK stopwords)
    assert "for" not in cleaned
    assert "with" not in cleaned
    assert "python" in cleaned
    assert "sql" in cleaned
    assert "machine" in cleaned


def test_skill_matcher():
    """Test skill extraction and matching logic."""
    matcher = SkillMatcherService()
    resume_text = "Experienced in Python, SQL, Pandas, and Machine Learning."
    job_desc = "Looking for a Python developer with SQL, Machine Learning, Docker, and AWS."

    matched, missing = matcher.match_skills(resume_text, job_desc)

    assert "Python" in matched
    assert "SQL" in matched
    assert "Machine Learning" in matched
    assert "Docker" in missing
    assert "AWS" in missing

def test_feedback_generator_rule_based():
    """Test rule-based feedback generator without API key."""
    generator = FeedbackGeneratorService(api_key="")
    feedback = generator.generate_feedback(
        candidate_name="Ajay",
        match_score=85.0,
        matched_skills=["Python", "SQL", "Machine Learning"],
        missing_skills=["Docker", "AWS"]
    )

    assert "Ajay" in feedback
    assert "Python" in feedback
    assert "Docker" in feedback

def test_match_post_endpoint():
    """Test POST /match endpoint with valid payload."""
    payload = {
        "candidate_name": "Ajay",
        "resume_text": "Python, SQL, Pandas, Machine Learning",
        "job_description": "Looking for a Python developer with SQL, Machine Learning, Docker and AWS."
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["candidate_name"] == "Ajay"
    assert "match_score" in data
    assert isinstance(data["match_score"], float)
    assert "Python" in data["matched_skills"]
    assert "Docker" in data["missing_skills"]
    assert len(data["feedback"]) > 0
