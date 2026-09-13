import re
import logging
from typing import Set, Tuple, List
from app.config import SKILLS_CSV_PATH
from app.utils.helpers import load_skills_from_csv

logger = logging.getLogger(__name__)

class SkillMatcherService:
    """
    Skill extraction and matching service.
    """
    
    def __init__(self, skills_csv_path: str = SKILLS_CSV_PATH):
        self.skills_list = load_skills_from_csv(skills_csv_path)

    def extract_skills(self, text: str) -> Set[str]:
        """
        Extracts technical skills present in the text using word boundary matching.

        Args:
            text (str): Input text (resume or job description).

        Returns:
            Set[str]: Set of identified skills.
        """
        if not text:
            return set()

        found_skills = set()
        text_lower = f" {text.lower()} "

        for skill in self.skills_list:
            skill_clean = skill.strip()
            if not skill_clean:
                continue
            
            # Escape regex characters except special tech symbols like +, #, .
            pattern = re.escape(skill_clean.lower())
            
            # Allow for word boundaries. For special symbols like C++, C#, .NET handle boundaries carefully.
            regex = r'(?:^|[\s,.\(\)\[\]:;/])' + pattern + r'(?:$|[\s,.\(\)\[\]:;/])'
            
            if re.search(regex, text_lower):
                found_skills.add(skill_clean)

        return found_skills

    def match_skills(self, resume_text: str, job_description: str) -> Tuple[List[str], List[str]]:
        """
        Identifies matched and missing skills between resume and job description.

        Args:
            resume_text (str): Text from candidate resume.
            job_description (str): Text from target job description.

        Returns:
            Tuple[List[str], List[str]]: (matched_skills, missing_skills)
        """
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)

        # Matched: Skills required by job AND present in resume
        matched = sorted(list(job_skills.intersection(resume_skills)))

        # Missing: Skills required by job BUT NOT present in resume
        missing = sorted(list(job_skills.difference(resume_skills)))

        return matched, missing
