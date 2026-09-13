import os
import logging
import pandas as pd
import nltk

logger = logging.getLogger(__name__)

def setup_nltk():
    """
    Downloads required NLTK resources safely.
    Silently handles cases where data is already available.
    """
    resources = ['stopwords', 'punkt', 'punkt_tab']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception as e:
            logger.warning(f"Could not download NLTK resource '{resource}': {e}")

def load_skills_from_csv(csv_path: str) -> list:
    """
    Loads skills list from a CSV file.
    
    Args:
        csv_path (str): Path to skills.csv
        
    Returns:
        list: List of skill strings
    """
    if not os.path.exists(csv_path):
        logger.warning(f"Skills file not found at {csv_path}. Using fallback default skills.")
        return [
            "Python", "Java", "C++", "JavaScript", "TypeScript", "SQL", "Pandas", "NumPy",
            "Power BI", "Tableau", "Machine Learning", "Deep Learning", "Scikit-learn",
            "TensorFlow", "PyTorch", "AWS", "Azure", "Google Cloud", "Git", "Docker",
            "Kubernetes", "FastAPI"
        ]
    
    try:
        df = pd.read_csv(csv_path)
        if 'skill' in df.columns:
            skills = df['skill'].dropna().astype(str).str.strip().tolist()
            return sorted(list(set(skills)), key=len, reverse=True)
    except Exception as e:
        logger.error(f"Error reading skills CSV at {csv_path}: {e}")
        
    return []
