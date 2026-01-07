import graphviz
from schemas.graph import FSM

class GraphPlotter:
    """Visualizes the FSM using Graphviz."""

    @staticmethod
    def create_dot(fsm: FSM) -> graphviz.Digraph:
        """Creates and returns the Graphviz Digraph object."""
        dot = graphviz.Digraph(comment='Technical Manual FSM', format='png')
        dot.attr(rankdir='LR') # Left to Right layout

        # Add Nodes
        for state_id, state in fsm.states.items():
            shape = 'box'
            style = ''
            if state.is_start:
                shape = 'ellipse'
                style = 'filled'
            elif state.is_terminal:
                shape = 'doublecircle'
                style = 'filled'
            
            dot.node(state.id, state.description, shape=shape, style=style)

        # Add Edges
        for transition in fsm.transitions:
            label = transition.condition if transition.condition else ""
            dot.edge(transition.source_id, transition.target_id, label=label)
        
        return dot

    @staticmethod
    def plot_fsm(fsm: FSM, output_path: str = "fsm_output"):
        dot = GraphPlotter.create_dot(fsm)

        # Render
        try:
            output_file = dot.render(output_path, view=False)
            return output_file
        except graphviz.backend.execute.ExecutableNotFound:
            print("Warning: Graphviz system executable 'dot' not found.")
            print("Please install Graphviz (https://graphviz.org/download/) and add it to your PATH.")
            print(f"Saving source to {output_path}.dot instead.")
            # Save the source manually
            with open(f"{output_path}.dot", "w", encoding='utf-8') as f:
                f.write(dot.source)
            return f"{output_path}.dot"
        except Exception as e:
             print(f"An error occurred during graph rendering: {e}")
             return None
