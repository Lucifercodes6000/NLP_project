# Technical Manual to Finite State Machine (FSM) Compiler

This project implements a compiler that translates natural language technical instructions into formal Finite State Machines (FSMs). It addresses the challenge of converting human-readable procedural manuals into machine-executable logic.

## Overview

Technical manuals often describe complex procedures involving conditions, loops, and checks. This tool parses these instructions, identifies state transitions, and generates a structured FSM. This allows for automated verification, simulation, and execution of otherwise static text documentation.

## Key Features

*   **NLP-Driven Parsing**: Uses `spaCy` to identify imperative actions, objects, and conditional clauses.
*   **FSM Synthesis**: Constructs a directed graph representing the procedural flow.
*   **Branching Logic**: Handles conditional control flow (e.g., "If X, do Y; otherwise, do Z").
*   **Validation**: Automatically detects unreachable states, dead ends, and missing start nodes.
*   **Dual Output**:
    *   **Visualization**: Generates Graphviz DOT files for flowchart rendering.
    *   **Serialization**: Exports JSON for integration with downstream applications.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Lucifercodes6000/NLP_project.git
    cd NLP_project/manual_to_fsm
    ```

2.  **Install dependencies**:
    ```bash
    pip install spacy graphviz
    python -m spacy download en_core_web_sm
    ```

## Usage

Run the compiler by providing an input text file containing the logic steps.

```bash
python main.py --input data/example.txt --output fsm_output
```

### Arguments
*   `--input`: Path to the text file containing the manual instructions.
*   `--output`: Base name for the generated output files (extension will be appended automatically).

## Architecture

The compilation pipeline consists of four stages:

1.  **Preprocessing**: Text normalization and step segmentation.
2.  **NLP Analysis**: Dependency parsing to extract Actions (Verbs), Objects (Targets), and Guards (Conditions).
3.  **Synthesis**: Graph construction, linking states via transitions and handling branching.
4.  **Validation & Export**: Integrity checks followed by JSON and DOT generation.

## Example

### Input (`data/example.txt`)
```text
1. Power up the system.
2. If the red light blinks, check the battery connection.
3. Otherwise, proceed to system initialization.
4. Wait for the green signal.
5. Press the Start button to begin operation.
```

### Output

**JSON (`fsm_output.json`)**:
```json
{
  "start_state_id": "START",
  "states": [ ... ],
  "transitions": [
    {
      "source_id": "S1",
      "target_id": "S2",
      "condition": "If the red light blinks",
      "action": null
    },
    ...
  ]
}
```

**Visualization**:
The tool generates a `.dot` file which can be visualized using Graphviz.


