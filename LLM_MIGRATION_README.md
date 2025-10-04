# LLM Service Migration: OpenAI to Gemini

## Changes Made

1. **Updated Dependencies**: Replaced `openai==1.3.5` with `google-generativeai==0.3.2` in `requirements.txt`
2. **Modified LLM Service**: Updated `backend/app/services/llm.py` to use Google's Gemini API instead of OpenAI
3. **Environment Variables**: Changed from `OPENAI_API_KEY` to `GEMINI_API_KEY`

## Setup Instructions

### 1. Install New Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Set Environment Variable
Create a `.env` file in your project root with:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Alternative: Hugging Face Integration
If you prefer to use Hugging Face models instead, you can modify the LLM service to use the `transformers` library:

```python
# Alternative implementation using Hugging Face
from transformers import pipeline

class LLMService:
    def __init__(self):
        self.model = pipeline("text-generation", model="microsoft/DialoGPT-medium")
    
    async def parse_workflow(self, user_input: str) -> Dict[str, Any]:
        # Implementation using Hugging Face models
        pass
```

## Key Differences

- **Gemini**: Uses `google.generativeai` library with `gemini-pro` model
- **Prompt Structure**: Changed from chat messages to a single prompt string
- **Response Handling**: Gemini returns text that can be parsed for structured data
- **API Key**: Uses `GEMINI_API_KEY` environment variable

## Testing

The service maintains the same interface, so existing code should work without changes. The `parse_workflow` method still returns the same structured workflow format.
