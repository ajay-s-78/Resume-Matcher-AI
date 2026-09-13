import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from app.utils.helpers import setup_nltk

logger = logging.getLogger(__name__)

# Run setup to ensure NLTK resources are available
setup_nltk()

class TextPreprocessor:
    """
    Text preprocessing service for resumes and job descriptions using NLTK.
    """
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            logger.warning("NLTK stopwords unavailable. Using fallback English stopword list.")
            self.stop_words = {
                'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
                'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been', 'before', 'being',
                'below', 'between', 'both', 'but', 'by', 'can', 'could', 'did', 'do', 'does',
                'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had',
                'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself',
                'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me',
                'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on',
                'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
                'same', 'she', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their',
                'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
                'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were',
                'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'you',
                'your', 'yours', 'yourself', 'yourselves'
            }

    def clean_text(self, text: str, remove_stop_words: bool = True) -> str:
        """
        Cleans and normalizes input text.
        Steps:
        1. Lowercase text
        2. Replace special characters while preserving alphanumerics & technical markers (e.g., C++, .NET)
        3. Tokenize text
        4. Remove stopwords
        5. Remove extra whitespace

        Args:
            text (str): Raw input text.
            remove_stop_words (bool): Whether to filter out stopwords.

        Returns:
            str: Preprocessed clean string.
        """
        if not text or not isinstance(text, str):
            return ""

        # 1. Lowercase
        text_lower = text.lower()

        # 2. Preserve essential characters for tech names like C++, C#, .net, node.js
        # Replace punctuation other than +, #, ., - with spaces
        cleaned = re.sub(r'[^a-z0-9\s\+#\.\-]', ' ', text_lower)

        # 3. Tokenize
        try:
            tokens = word_tokenize(cleaned)
        except Exception:
            # Fallback regex tokenization if NLTK tokenizer fails
            tokens = cleaned.split()

        # 4. Filter tokens & Stopwords
        processed_tokens = []
        for token in tokens:
            # Strip trailing dots or dashes from single word tokens
            token = token.strip('.').strip('-')
            if not token:
                continue

            if remove_stop_words and token in self.stop_words:
                continue

            processed_tokens.append(token)

        # 5. Remove extra spaces
        return " ".join(processed_tokens)
