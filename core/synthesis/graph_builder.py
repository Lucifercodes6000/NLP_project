from schemas.graph import FSM, State, Transition
from schemas.annotation import Instruction
from core.nlp_engine.dependency_parser import DependencyParser
from typing import List

class GraphBuilder:
    """
    Synthesizes the FSM from text instructions.
    """
    def __init__(self):
        self.parser = DependencyParser()

    def build_fsm(self, instructions_text: List[str]) -> FSM:
        fsm = FSM()
        
        previous_state_id = "START"
        
        # Create Start Node
        start_node = State(id="START", description="Start", is_start=True)
        fsm.add_state(start_node)

        # Context for branching: stack of (condition_state_id, condition_text)
        # This is a very simplified version.
        # NOTE: Currently generates a mostly linear chain. 
        # "If" and "Otherwise" are linked sequentially, which is a visual approximation.
        # True FSM branching would require a stack to link "Otherwise" back to the parent of "If".
        
        for i, text in enumerate(instructions_text):
            # Parse the instruction
            instruction = self.parser.parse_instruction(text, i)
            
            # Create a state for this instruction
            current_state_id = f"S{i+1}"
            description = instruction.text
            if instruction.action: # Enrich description if parsed well
                description = f"[{instruction.action}] {instruction.target or ''}"
            
            # If full text is better for reading
            state = State(id=current_state_id, description=instruction.text)
            fsm.add_state(state)

            # Determine Transition Logic
            # 1. Standard Sequence
            # 2. Conditional
            
            condition = instruction.condition
            
            # Add Transition from Previous to Current
            fsm.add_transition(Transition(
                source_id=previous_state_id,
                target_id=current_state_id,
                condition=condition
            ))

            previous_state_id = current_state_id
            
        # Add End Node
        end_node = State(id="END", description="End", is_terminal=True)
        fsm.add_state(end_node)
        
        # Link last state to End
        fsm.add_transition(Transition(source_id=previous_state_id, target_id="END"))

        return fsm
