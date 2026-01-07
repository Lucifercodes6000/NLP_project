from dataclasses import dataclass
from typing import Optional

@dataclass
class Instruction:
    """
    Intermediate representation of a parsed instruction step.
    Example: "If the light is red, press the button."
    - action: "press"
    - target: "button"
    - condition: "the light is red"
    - type: "conditional" | "imperative"
    """
    id: int
    text: str
    action: Optional[str] = None
    target: Optional[str] = None
    condition: Optional[str] = None
    type: str = "imperative"  # imperative, conditional, branch_start, branch_end, etc.
