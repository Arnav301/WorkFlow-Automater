# backend/app/services/workflow.py
from typing import Dict, Any, List
from .llm import LLMService
import asyncio

# Make vision optional to avoid hard dependency on OpenCV/EasyOCR at startup
try:
    from .vision import UIVisionService  # may import cv2/easyocr
    HAS_VISION = True
except Exception:  # ImportError or downstream errors
    UIVisionService = None
    HAS_VISION = False

class WorkflowEngine:
    def __init__(self):
        self.vision = UIVisionService() if HAS_VISION and UIVisionService else None
        self.llm = LLMService()
        # Execution state keyed by workflow_id
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        # Store original workflow definitions (LLM output) keyed by workflow_id
        self.workflow_definitions: Dict[str, Dict[str, Any]] = {}
        # Simple extracted data store keyed by workflow_id
        self.extracted_data: Dict[str, Any] = {}
    
    async def execute_workflow(self, workflow_definition: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow based on its definition"""
        # retain definition
        self.workflow_definitions[workflow_id] = workflow_definition
        self.active_workflows[workflow_id] = {
            "status": "running",
            "progress": 0,
            "steps": []
        }
        
        try:
            # Simulate workflow execution
            steps = workflow_definition.get("steps", [])
            total_steps = len(steps)
            
            for i, step in enumerate(steps, 1):
                # Update progress
                progress = int((i / max(total_steps, 1)) * 100)
                self.active_workflows[workflow_id]["progress"] = progress
                self.active_workflows[workflow_id]["current_step"] = step
                
                # Simulate step execution
                await asyncio.sleep(1)  # Simulate work
                
                # If step is an extract, put something into extracted_data
                if step.get("action") == "extract":
                    save_as = step.get("save_as", "extracted_data")
                    self.extracted_data.setdefault(workflow_id, {})[save_as] = {
                        "sample": True,
                        "detail": f"Extracted from {step.get('target')}"
                    }
                
                # Add step result
                self.active_workflows[workflow_id]["steps"].append({
                    "step": step.get("action"),
                    "status": "completed",
                    "details": f"Executed {step.get('action')} on {step.get('target')}",
                })
            
            self.active_workflows[workflow_id].update({
                "status": "completed",
                "progress": 100,
                "result": "Workflow executed successfully",
                "vision_enabled": bool(self.vision)
            })
        except Exception as e:
            self.active_workflows[workflow_id].update({
                "status": "failed",
                "result": str(e),
                "vision_enabled": bool(self.vision)
            })
        
        return self.active_workflows[workflow_id]
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the status of a workflow"""
        return self.active_workflows.get(workflow_id, {"error": "Workflow not found"})
    def list_workflows(self) -> List[Dict[str, Any]]:
        items = []
        for wid, definition in self.workflow_definitions.items():
            items.append({
                "workflow_id": wid,
                "name": definition.get("name"),
                "description": definition.get("description"),
                "steps_count": len(definition.get("steps", [])),
            })
        # latest first by naive string (UUID timestamp not guaranteed). Keep insertion order as-is.
        return list(reversed(items))

    def list_executions(self) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        for wid, state in self.active_workflows.items():
            items.append({
                "workflow_id": wid,
                "status": state.get("status"),
                "progress": state.get("progress", 0),
                "last_step": state.get("current_step", {}),
                "steps_completed": len(state.get("steps", [])),
            })
        # Show running first, then others
        items.sort(key=lambda x: (x["status"] != "running", -x.get("progress", 0)))
        return items
    
    def get_execution(self, workflow_id: str) -> Dict[str, Any]:
        return self.active_workflows.get(workflow_id, {"error": "Execution not found"})

    def list_extracted(self) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        for wid, data in self.extracted_data.items():
            items.append({
                "workflow_id": wid,
                "data": data,
            })
        return list(reversed(items))

    def reset_all(self) -> Dict[str, Any]:
        """Clear all in-memory data: definitions, executions, extracted data."""
        self.active_workflows.clear()
        self.workflow_definitions.clear()
        self.extracted_data.clear()
        return {"status": "cleared"}