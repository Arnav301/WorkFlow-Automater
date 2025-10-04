# Update backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from .services.workflow import WorkflowEngine
from .services.llm import LLMService
import uuid
import json
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow_engine = WorkflowEngine()
llm_service = LLMService()

class WorkflowRequest(BaseModel):
    description: str
    parameters: Optional[dict] = None

class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    steps: List[dict]

@app.post("/api/workflows/execute", response_model=WorkflowResponse)
async def execute_workflow(request: WorkflowRequest):
    try:
        # Parse the workflow using LLM
        workflow_definition = await llm_service.parse_workflow(request.description)
        
        # Execute workflow asynchronously
        workflow_id = f"wf_{str(uuid.uuid4())}"

        async def _execute_and_update():
            result = await workflow_engine.execute_workflow(workflow_definition, workflow_id)

        asyncio.create_task(_execute_and_update())
        
        return {
            "workflow_id": workflow_id,
            "status": "started",
            "steps": [{"step": s["action"], "status": "pending"} for s in workflow_definition.get("steps", [])]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workflows/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    try:
        status = workflow_engine.get_workflow_status(workflow_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

# Listing endpoints
@app.get("/api/workflows")
def list_workflows():
    try:
        return {"items": workflow_engine.list_workflows()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/executions")
def list_executions():
    try:
        return {"items": workflow_engine.list_executions()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/executions/{workflow_id}")
def get_execution(workflow_id: str):
    try:
        data = workflow_engine.get_execution(workflow_id)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/api/extracted")
def list_extracted():
    try:
        return {"items": workflow_engine.list_extracted()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
def reset_all():
    try:
        return workflow_engine.reset_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))