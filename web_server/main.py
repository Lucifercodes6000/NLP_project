from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel # Deprecated for this endpoint
import uvicorn
import sys
import os

# ... (Imports remain same) ...
# Add parent directory to path to allow importing 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.preprocessing.segmenter import Segmenter
from core.synthesis.graph_builder import GraphBuilder
from visualization.graph_plotter import GraphPlotter
from core.validation.fsm_checker import FSMChecker

app = FastAPI(title="Manual to FSM API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "FSM Compiler API is running"}

@app.post("/compile")
async def compile_manual(file: UploadFile = File(None), text: str = Form(None)):
    try:
        input_text = ""
        if file:
            content = await file.read()
            input_text = content.decode("utf-8")
        elif text:
            input_text = text
        else:
            raise HTTPException(status_code=400, detail="Either 'file' or 'text' must be provided.")

        # Pipeline
        steps = Segmenter.segment_lines(input_text)
        
        builder = GraphBuilder()
        fsm = builder.build_fsm(steps)
        
        # Validate
        checker = FSMChecker(fsm)
        errors = checker.validate()
        
        # Visualization
        dot = GraphPlotter.create_dot(fsm)
        dot_source = dot.source
        
        return {
            "status": "success",
            "fsm_stats": {
                "states": len(fsm.states),
                "transitions": len(fsm.transitions)
            },
            "validation_errors": errors,
            "dot_source": dot_source,
            "fsm_data": fsm.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("web_server.main:app", host="0.0.0.0", port=8000, reload=True)
