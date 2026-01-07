from schemas.graph import FSM
from typing import List, Set

class FSMChecker:
    """
    Validates the integrity of the FSM.
    """
    
    def __init__(self, fsm: FSM):
        self.fsm = fsm

    def validate(self) -> List[str]:
        errors = []
        
        if not self.fsm.start_state_id:
            errors.append("FSM has no Start state.")
            return errors # Cannot proceed

        # 1. Reachability Check (BFS/DFS)
        reachable = self._get_reachable_states(self.fsm.start_state_id)
        all_states = set(self.fsm.states.keys())
        unreachable = all_states - reachable
        
        if unreachable:
            errors.append(f"Unreachable states found: {unreachable}")

        # 2. Dead End Check (States that are not Terminal but have no outgoing transitions)
        # Identify states with outgoing transitions
        states_with_outgoing = set(t.source_id for t in self.fsm.transitions)
        
        for state_id, state in self.fsm.states.items():
            if not state.is_terminal and state_id not in states_with_outgoing:
                errors.append(f"Dead end found at state: {state_id} ({state.description}). Expected transition or Terminal.")

        return errors

    def _get_reachable_states(self, start_id: str) -> Set[str]:
        visited = set()
        queue = [start_id]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            # Find neighbors
            # Inefficient for large graphs but fine here
            neighbors = [t.target_id for t in self.fsm.transitions if t.source_id == current]
            for n in neighbors:
                if n not in visited:
                    queue.append(n)
        
        return visited
