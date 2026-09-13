import logging
from sentence_transformers import SentenceTransformer, util
from app.config import MODEL_NAME
from app.services.text_preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)

class BertMatcherService:
    """
    BERT-based semantic similarity matcher using SentenceTransformers.
    """
    
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.preprocessor = TextPreprocessor()
        self._model = None  # Lazy loading

    @property
    def model(self) -> SentenceTransformer:
        """Loads and returns the SentenceTransformer model on demand."""
        if self._model is None:
            logger.info(f"Loading SentenceTransformer model '{self.model_name}'...")
            try:
                self._model = SentenceTransformer(self.model_name)
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model {self.model_name}: {e}")
                raise e
        return self._model

    def calculate_similarity(self, resume_text: str, job_description: str) -> float:
        """
        Preprocesses texts, generates BERT embeddings, calculates cosine similarity,
        and returns a percentage score.

        Args:
            resume_text (str): Candidate's resume text.
            job_description (str): Target job description text.

        Returns:
            float: Similarity match percentage score rounded to 2 decimal places.
        """
        # Step 1 & 3: Preprocess texts
        clean_resume = self.preprocessor.clean_text(resume_text, remove_stop_words=True)
        clean_job = self.preprocessor.clean_text(job_description, remove_stop_words=True)

        if not clean_resume or not clean_job:
            return 0.0

        # Step 4: Generate embeddings
        embeddings = self.model.encode([clean_resume, clean_job], convert_to_tensor=True)

        # Step 5: Cosine similarity calculation
        similarity_tensor = util.cos_sim(embeddings[0], embeddings[1])
        raw_score = float(similarity_tensor[0][0].cpu().item())

        # Step 6: Convert to percentage score (0 to 100)
        # Cosine similarity range is -1 to 1; for semantic embeddings it's generally > 0.
        score_percentage = max(0.0, min(100.0, raw_score * 100.0))

        # Step 7: Return rounded match score
        return round(score_percentage, 1)
