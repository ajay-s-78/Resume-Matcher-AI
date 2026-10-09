import os
from pathlib import Path
from dotenv import load_dotenv

# Set PyTorch thread limits early to prevent multi-thread memory overhead on Render
os.environ.setdefault("TORCH_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

# Load environment variables from .env file if present
load_dotenv()


# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Application Configuration
APP_NAME = "Resume Matcher using BERT"
MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip() or None

# File Paths
SKILLS_CSV_PATH = os.getenv("SKILLS_CSV_PATH", str(BASE_DIR / "data" / "skills.csv"))
