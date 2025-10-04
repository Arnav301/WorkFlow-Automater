# backend/app/models/workflow.py
from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from ..database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, index=True)
    status = Column(String, default="pending")  # pending, running, completed, failed
    input_parameters = Column(JSON)
    output_data = Column(JSON, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)