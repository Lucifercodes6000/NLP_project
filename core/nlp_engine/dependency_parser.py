import spacy
from schemas.annotation import Instruction

class DependencyParser:
    """
    NLP Engine that uses Spacy to parse instructions.
    """
    def __init__(self, model: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            # Fallback or prompt user; assuming installed for now
            print(f"Model '{model}' not found. Please install it.")
            raise

    def parse_instruction(self, text: str, index: int) -> Instruction:
        """
         Parses a single line of text into an Instruction object.
        """
        doc = self.nlp(text)
        
        # 1. Identify instruction type (Simple check for conditional)
        # "If the light is red, press the button."
        type_ = "imperative"
        condition = None
        action_verb = None
        target_obj = None

        # Check for initial conditional clause (very naive heuristic)
        # In a real dependency parse, we'd look for 'mark' dependencies (like 'if')
        
        # Split by comma to separate condition from action provided it creates a valid split
        parts = [p.strip() for p in text.split(',')]
        
        if parts[0].lower().startswith("if ") or parts[0].lower().startswith("when "):
            type_ = "conditional"
            condition = parts[0]
            # The rest is likely the action
            action_part = ", ".join(parts[1:]) if len(parts) > 1 else ""
        elif parts[0].lower().startswith("otherwise"):
            type_ = "branch_alternative" # else case
            condition = "otherwise"
            action_part = ", ".join(parts[0:]).replace("Otherwise", "", 1).strip(" ,")
        else:
            action_part = text

        # Parse the action part to find Verb and Object
        if action_part:
            action_doc = self.nlp(action_part)
            for token in action_doc:
                if token.pos_ == "VERB" and not action_verb:
                    action_verb = token.lemma_  # Use lemma for normalization
                if token.dep_ == "dobj" and not target_obj:
                    target_obj = token.text
        
        return Instruction(
            id=index,
            text=text,
            action=action_verb,
            target=target_obj,
            condition=condition,
            type=type_
        )
