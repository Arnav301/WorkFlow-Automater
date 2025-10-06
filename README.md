# 🚀 UI-Agnostic Intelligent Workflow Automator

A system that demonstrates the ability to automate workflows on any application UI without explicit API integration, by combining Python, Gemini API (LLM), Computer Vision, and React-based monitoring — directly aligned with Emma Robot’s mission.

# 🎯 Goal

Enable end-to-end automation of UI-driven workflows, where a user can simply describe a task in natural language (e.g., “Log in, download the last invoice, and upload it to Google Drive”), and the system autonomously executes it — without APIs.

# 🔹 Key Features

# 🖥️ Autonomous UI Navigation (Core Demo)

Detect & interpret UI components (buttons, fields, tables) with OpenCV + Python

Execute flows like: Login → Extract Data → Process → Upload

# 🧠 LLM-Driven Task Understanding (Gemini API)

Accepts natural language commands.

Uses Gemini API to translate tasks into structured workflow plans.

# 🔍 AI-Powered Data Extraction

OCR-based text recognition (Tesseract / EasyOCR).

Pass extracted data directly to workflows (no DB needed).

# ⚙️ Backend Workflow Engine (Python + FastAPI/Flask)

Orchestrates automation tasks.

Exposes REST APIs for workflow execution & monitoring.

# 📊 Frontend Dashboard (React/Next.js)

Real-time monitoring of active automations, logs, and errors.

Config panel to “teach” new workflows without coding.

# 🌟 Bonus (Differentiator)

Integrate multimodal VLMs (Gemini multimodal / LLaVA) for visual UI comprehension.

# 🔹 Tech Stack

Python → Backend + CV automation logic

FastAPI / Flask → Workflow engine + REST APIs

OpenCV + OCR (Tesseract / EasyOCR) → UI understanding & data extraction

React / Next.js → Monitoring dashboard

Gemini API → Natural language → workflow plan

Optional VLMs → Multimodal visual understanding

# 🔹 Why This Project Works for Emma Robot

✔ Demonstrates independence from APIs → UI navigation via vision
✔ Uses Gemini LLM for reasoning & automation planning
✔ End-to-end system: backend + frontend
✔ Great example of rapid prototyping in a complex domain
✔ Enterprise simulation possible (VPN logins, secure data handling)

# 🚀 Getting Started
1️⃣ Clone the Repo
git clone https://github.com/your-username/ui-agnostic-automator.git
cd ui-agnostic-automator

2️⃣ Backend Setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

4️⃣ Gemini API Setup

Get API Key from Google AI Studio

Add it to your .env file:

GEMINI_API_KEY=your_api_key_here

# 📌 Example Workflow

Command:

“Log in to the portal, download the last invoice, and upload it to Google Drive.”

System Execution Flow:

Parse command → Gemini API → workflow plan

Navigate UI → detect login form → enter credentials

Find & download last invoice (OCR validation)

Upload file to configured storage / location

Log completion in dashboard
