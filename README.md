# RESUME MATCHER USING BERT

An AI-powered Resume Matcher application that compares a candidate's resume with a target job description, calculates semantic match similarity scores using **BERT** (Sentence Transformers), extracts matched and missing technical skills, and generates actionable improvement suggestions.

---

## 📌 Project Features

- **BERT Semantic Matching**: Uses Hugging Face's `all-MiniLM-L6-v2` Sentence Transformer model to convert resumes and job descriptions into high-dimensional embeddings and calculate cosine similarity scores.
- **NLTK Text Preprocessing**: Tokenizes, normalizes, lowercases, and removes noise/stopwords from text inputs.
- **Skill Extraction Engine**: Automated skill parser using a curated skills database (`data/skills.csv`) to identify **Matched Skills** and **Missing Skills**.
- **Dual Feedback System**:
  - **Rule-Based Engine**: Generates intelligent, structured feedback out-of-the-box (no API key required).
  - **Optional LLM Integration**: Generates personalized AI feedback using GPT if an `OPENAI_API_KEY` is provided in `.env`.
- **FastAPI RESTful Backend**: High-performance asynchronous API endpoints with Pydantic request/response validation and CORS enabled.
- **Modern Web Dashboard**: SaaS-style clean frontend UI (`HTML5`, `Vanilla CSS`, `JavaScript ES6`) built right into FastAPI.

---

## 🛠️ Technologies Used

- **Programming Language**: Python 3.9+
- **AI / NLP Models**:
  - `sentence-transformers` (`all-MiniLM-L6-v2`)
  - `transformers` & `torch`
  - `nltk` (Natural Language Toolkit)
- **Data Handling**: `pandas`, `scikit-learn`
- **Backend & Web Server**: `FastAPI`, `uvicorn`, `pydantic`
- **Frontend**: HTML5, Vanilla CSS, Modern JavaScript (Fetch API)
- **Configuration & Utilities**: `python-dotenv`, `requests`

---

## 📂 Project Structure

```
resume-matcher/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application & static server entry point
│   ├── config.py                # Environment and configuration settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py            # API endpoints (/, /health, /match)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── text_preprocessor.py # NLTK text cleaner & tokenizer
│   │   ├── bert_matcher.py      # BERT embedding & similarity calculator
│   │   ├── skill_matcher.py     # Skill parser (matched & missing)
│   │   └── feedback_generator.py # Dual rule-based & LLM feedback engine
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic schemas
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # Helper utilities (NLTK downloader, CSV reader)
│
├── frontend/
│   ├── index.html               # Web UI layout
│   ├── style.css                # SaaS dashboard styles
│   └── script.js                # Frontend API client script
│
├── data/
│   ├── sample_resumes/          # Text sample resumes for testing
│   ├── sample_job_descriptions/ # Text sample job descriptions
│   └── skills.csv               # Technical skills database
│
├── tests/
│   ├── __init__.py
│   └── test_matcher.py          # Pytest suite
│
├── requirements.txt             # Project dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
└── README.md                    # Project documentation
```

---

## 🚀 Installation & Setup Guide

### 1. Clone or Open Project Directory

Navigate to the project root directory:

```bash
cd "c:/Users/ELCOT/OneDrive/Desktop/Resume Matcher"
```

### 2. Create a Virtual Environment

#### On Windows (PowerShell / Command Prompt):
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## 📥 NLTK Resource Initialization

The application automatically downloads required NLTK data packages (`stopwords`, `punkt`, `punkt_tab`) on startup. You can also manually download them in Python:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
```

---

## ⚙️ Environment Configuration (Optional)

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. *(Optional)* Add your OpenAI API key if you want LLM-generated feedback:

```env
MODEL_NAME=all-MiniLM-L6-v2
OPENAI_API_KEY=your_openai_api_key_here
```

*Note: If no API key is provided, the application automatically uses the built-in rule-based feedback generator.*

---

## 🏃 Running the Application & Web UI

### 1. Start FastAPI Server
Start the Uvicorn server in reload mode:

```bash
uvicorn app.main:app --reload
```

### 2. Open the Web UI
Open your web browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

### 3. Match a Resume
1. Enter Candidate Name (e.g., `Ajay`).
2. Paste the candidate's resume text in the **Candidate Resume** card.
3. Paste the target job description in the **Job Description** card.
4. Click **Match Resume**.
5. View the interactive **Match Result**: BERT Similarity Score %, Matched Skills (green), Missing Skills (red/orange), and AI Career Feedback.

---

## 📡 API Endpoints & Usage

- **Web Dashboard**: `http://127.0.0.1:8000/`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc UI**: `http://127.0.0.1:8000/redoc`

### 1. Root Endpoint
- **URL**: `GET /`
- **Response** (for API / JSON Clients):
```json
{
  "message": "Resume Matcher API is running"
}
```

### 2. Health Check Endpoint
- **URL**: `GET /health`
- **Response**:
```json
{
  "status": "healthy"
}
```

### 3. Match Resume Endpoint
- **URL**: `POST /match`
- **Content-Type**: `application/json`

#### Example Request Body:
```json
{
  "candidate_name": "Ajay",
  "resume_text": "Python, SQL, Pandas, Machine Learning",
  "job_description": "Looking for a Python developer with SQL, Machine Learning, Docker and AWS."
}
```

#### Example Response:
```json
{
  "candidate_name": "Ajay",
  "match_score": 82.5,
  "matched_skills": [
    "Machine Learning",
    "Python",
    "SQL"
  ],
  "missing_skills": [
    "AWS",
    "Docker"
  ],
  "feedback": "Hello Ajay, your resume is a good match for this position (82.5%). You have strong skills in Machine Learning, Python, SQL. Consider learning or highlighting AWS and Docker to improve your match."
}
```

---

## 🧪 Running Unit Tests

Run the test suite using `pytest`:

```bash
pytest
```

---

## 💡 Future Improvements

- **PDF & DOCX Resume Parser**: Add support for uploading PDF and Word documents directly.
- **Experience Level Matching**: Parse years of experience (e.g. 3+ years vs 5+ years required).
- **Custom Fine-Tuned Model**: Fine-tune SentenceTransformer on domain-specific job market datasets.

---

## 📄 License

This project is open source and available under the MIT License.
