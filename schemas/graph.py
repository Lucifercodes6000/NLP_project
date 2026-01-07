from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class State:
    """Represents a discrete state in the FSM (e.g., an action step)."""
    id: str
    description: str
    is_start: bool = False
    is_terminal: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "is_start": self.is_start,
            "is_terminal": self.is_terminal
        }

@dataclass
class Transition:
    """Represents a transition between states, potentially guarded by a condition."""
    source_id: str
    target_id: str
    condition: Optional[str] = None  # None implies an unconditional transition (default path)
    action: Optional[str] = None     # explicit action required to transit

    def to_dict(self):
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "condition": self.condition,
            "action": self.action
        }

@dataclass
class FSM:
    """Finite State Machine container."""
    states: Dict[str, State] = field(default_factory=dict)
    transitions: List[Transition] = field(default_factory=list)
    start_state_id: Optional[str] = None

    def add_state(self, state: State):
        self.states[state.id] = state
        if state.is_start:
            self.start_state_id = state.id

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def to_dict(self):
        return {
            "start_state_id": self.start_state_id,
            "states": [s.to_dict() for s in self.states.values()],
            "transitions": [t.to_dict() for t in self.transitions]
        }
