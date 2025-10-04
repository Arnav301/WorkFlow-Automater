# backend/app/services/llm.py
from typing import Dict, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def parse_workflow(self, user_input: str) -> Dict[str, Any]:
        """Convert natural language to structured workflow"""
        try:
            # Create the prompt for Gemini
            prompt = f"""You are a workflow automation assistant. Convert the user's request into a structured workflow.

User request: {user_input}

Please provide a structured workflow in JSON format with the following structure:
{{
    "name": "Generated Workflow",
    "description": "Brief description of the workflow",
    "steps": [
        {{"action": "navigate", "target": "target_element", "description": "what this step does"}},
        {{"action": "input", "target": "input_field", "value": "{{variable_name}}", "description": "what this step does"}},
        {{"action": "click", "target": "button_element", "description": "what this step does"}},
        {{"action": "extract", "target": "data_element", "save_as": "variable_name", "description": "what this step does"}}
    ]
}}

Available actions: navigate, input, click, extract, wait, scroll
Make sure to use appropriate actions based on the user's request."""

            response = self.model.generate_content(prompt)
            
            # For now, return a structured workflow based on the user input
            # In a production environment, you'd parse the Gemini response
            workflow = {
                "name": "Generated Workflow",
                "description": user_input,
                "steps": [
                    {"action": "navigate", "target": "login_page", "description": "Navigate to login page"},
                    {"action": "input", "target": "username", "value": "{{username}}", "description": "Enter username"},
                    {"action": "input", "target": "password", "value": "{{password}}", "sensitive": True, "description": "Enter password"},
                    {"action": "click", "target": "login_button", "description": "Click login button"},
                    {"action": "extract", "target": "data_table", "save_as": "extracted_data", "description": "Extract data from table"}
                ]
            }
            return workflow
        except Exception as e:
            raise Exception(f"Failed to parse workflow: {str(e)}")