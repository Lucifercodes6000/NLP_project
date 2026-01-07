import argparse
import os
from core.preprocessing.cleaner import Cleaner
from core.preprocessing.segmenter import Segmenter
from core.synthesis.graph_builder import GraphBuilder
from visualization.graph_plotter import GraphPlotter
from core.validation.fsm_checker import FSMChecker

def main():
    parser = argparse.ArgumentParser(description="Compile Technical Manual to FSM")
    parser.add_argument("--input", type=str, help="Path to input text file", required=True)
    parser.add_argument("--output", type=str, default="output_fsm", help="Output filename for graph")
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File {args.input} not found.")
        return

    # 1. Read
    with open(args.input, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    print("--- RAW TEXT ---")
    print(raw_text)
    print("----------------")

    # 2. Preprocess
    # We pass raw_text because Segmenter requires newlines to split steps.
    # A global 'clean_text' (flattening) would break structure.
    
    steps = Segmenter.segment_lines(raw_text)
    
    print(f"Identified {len(steps)} steps.")
    for s in steps:
        print(f"- {s}")

    # 3. Build FSM
    builder = GraphBuilder()
    fsm = builder.build_fsm(steps)
    
    print(f"FSM Built: {len(fsm.states)} states, {len(fsm.transitions)} transitions.")

    # 3.5 Validation
    checker = FSMChecker(fsm)
    errors = checker.validate()
    if errors:
        print("\n[WARNING] Validation Issues Found:")
        for e in errors:
            print(f" - {e}")
    else:
        print("\n[INFO] FSM Validation Passed.")

    # 4. Visualize
    output_file = GraphPlotter.plot_fsm(fsm, args.output)
    print(f"FSM Diagram saved to: {output_file}")

    # 5. Export JSON
    import json
    json_path = args.output + ".json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fsm.to_dict(), f, indent=2)
    print(f"FSM Data saved to: {json_path}")

if __name__ == "__main__":
    main()
