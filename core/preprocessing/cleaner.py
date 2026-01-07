import re

class Cleaner:
    """Basic text cleaning utility."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Normalizes text by removing excessive whitespace and artifacts.
        """
        if not text:
            return ""
        
        # Remove multiple spaces and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        return text
