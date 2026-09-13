import logging
from typing import List
import requests
from app.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class FeedbackGeneratorService:
    """
    Feedback generator service supporting rule-based evaluation and optional LLM feedback.
    """

    def __init__(self, api_key: str = OPENAI_API_KEY):
        self.api_key = api_key

    def generate_feedback(
        self,
        candidate_name: str,
        match_score: float,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """
        Generates resume feedback using LLM if API key is provided, or rule-based fallback.

        Args:
            candidate_name (str): Name of candidate.
            match_score (float): BERT match score percentage.
            matched_skills (List[str]): List of matched skills.
            missing_skills (List[str]): List of missing skills.

        Returns:
            str: Generated feedback statement.
        """
        if self.api_key:
            llm_feedback = self._generate_llm_feedback(
                candidate_name, match_score, matched_skills, missing_skills
            )
            if llm_feedback:
                return llm_feedback

        return self._generate_rule_based_feedback(
            candidate_name, match_score, matched_skills, missing_skills
        )

    def _generate_rule_based_feedback(
        self,
        candidate_name: str,
        match_score: float,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """
        Generates deterministic, clear rule-based feedback.
        """
        feedback_parts = []

        # Tiered match summary
        if match_score >= 85:
            feedback_parts.append(f"Hello {candidate_name}, your resume is an excellent match for this position ({match_score}%).")
        elif match_score >= 65:
            feedback_parts.append(f"Hello {candidate_name}, your resume is a good match for this position ({match_score}%).")
        elif match_score >= 45:
            feedback_parts.append(f"Hello {candidate_name}, your resume shows a moderate match for this position ({match_score}%).")
        else:
            feedback_parts.append(f"Hello {candidate_name}, your resume currently has a low match score for this position ({match_score}%).")

        # Matched skills highlights
        if matched_skills:
            matched_str = ", ".join(matched_skills[:5])
            feedback_parts.append(f"You have strong skills in {matched_str}.")
        else:
            feedback_parts.append("Few matching key technical skills were detected in your resume.")

        # Missing skills improvement advice
        if missing_skills:
            missing_str = " and ".join([", ".join(missing_skills[:-1]), missing_skills[-1]]) if len(missing_skills) > 1 else missing_skills[0]
            feedback_parts.append(f"Consider learning or highlighting {missing_str} to improve your match.")
        else:
            feedback_parts.append("You possess all key technical skills listed in the job description.")

        return " ".join(feedback_parts)

    def _generate_llm_feedback(
        self,
        candidate_name: str,
        match_score: float,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """
        Attempts to call OpenAI ChatCompletion API if API key is provided.
        Returns None if request fails or key is invalid.
        """
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            prompt = (
                f"Candidate Name: {candidate_name}\n"
                f"BERT Match Score: {match_score}%\n"
                f"Matched Skills: {', '.join(matched_skills)}\n"
                f"Missing Skills: {', '.join(missing_skills)}\n"
                "Provide a brief 2-3 sentence feedback summary for the candidate, "
                "highlighting their strengths and recommending key missing skills to learn."
            )
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are an expert technical HR consultant."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.warning(f"OpenAI API call failed with status {response.status_code}: {response.text}")
        except Exception as e:
            logger.warning(f"Failed to generate LLM feedback: {e}")

        return None
