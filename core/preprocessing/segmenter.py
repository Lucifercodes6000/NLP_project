import re
from typing import List

class Segmenter:
    """Splits raw text into individual instruction steps."""

    @staticmethod
    def segment_lines(text: str) -> List[str]:
        """
        Splits text based on newlines and numbered lists.
        Example: "1. Do this. 2. Do that." -> ["Do this.", "Do that."]
        """
        # Naive splitting on newlines first
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        cleaned_lines = []
        for line in lines:
            # Remove leading numbers like "1.", "2)", "Step 1:"
            cleaned = re.sub(r'^(Step\s+)?\d+[\.\)]\s*', '', line)
            if cleaned:
                cleaned_lines.append(cleaned)
        
        return cleaned_lines
