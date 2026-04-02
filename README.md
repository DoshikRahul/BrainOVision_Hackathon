# Aarogya Saathi - AI-Driven Public Health Chatbot

Aarogya Saathi is a Telegram chatbot powered by Dialogflow CX and FastAPI, designed as a public health awareness tool for the BrainOVision Hackathon. 

## Project Execution Phases & Deliverables

This roadmap breaks down the tasks so the team can divide and conquer parallel tracks.

### Phase 1: Backend & Database Boilerplate
**Goal**: Establish the base architecture and database schemas.
**Deliverables**:
- `[x]` FastAPI application structure defined in `backend/app/`.
- `[x]` Database Configuration scaffolding (PostgreSQL + Redis).
- `[x]` SQLAlchemy Data Models (`user.py`, `reminder.py`, `disease.py`).
- `[x]` Initial dependencies mapped inside `requirements.txt`.

### Phase 2: Conversational UI & Telegram Webhook
**Goal**: Get the messaging interfaces talking to our backend.
**Deliverables**:
- `[ ]` Telegram Bot created via the BotFather and Token secured.
- `[ ]` Dialogflow CX Agent initialized in Google Cloud.
- `[ ]` Core Dialogflow CX Intents (Greeting, Disease Info, Symptom Checker) and Entities (@disease, @symptom) trained.
- `[ ]` Local server connected to Telegram via ngrok webhook registration (targeting `POST /telegram-webhook`).

### Phase 3: Knowledge Base & AI Model Integrations
**Goal**: Empower the chatbot with real local data and predictive ML models.
**Deliverables**:
- `[ ]` Disease Knowledge Base populated with structured data (symptoms, precautions, treatments).
- `[ ]` Integration of symptom-to-disease prediction **models** (e.g. Random Forest, BERT, or other classifiers that the team incorporates) into the backend flow.
- `[ ]` Government health portal APIs (IDSP/MOHFW) integration logic implemented in `outbreak_api.py`.
- `[ ]` Multilingual translation pipeline (IndicTrans/Google Translate) hooked into the Dialogflow request structure.

### Phase 4: Proactive Features (Reminders & Alerts)
**Goal**: Transform the bot from reactive to proactive.
**Deliverables**:
- `[ ]` Celery + Redis task pipeline configured for background reminder jobs.
- `[ ]` Reminder API routes activated so users receive scheduled push notifications for medicines and vaccines.
- `[ ]` Session management enabled for multi-turn contextual tracking in Redis.

### Phase 5: Production Deployment & Verification
**Goal**: Make the project robust and presentation-ready for BrainOVision.
**Deliverables**:
- `[ ]` Backend and webhook deployed to a live server (Railway/Google Cloud Run/Render).
- `[ ]` Live Database hosted.
- `[ ]` (Optional Hackathon Innovation) Google Maps API integrated for "nearest hospital" searches.
- `[ ]` (Optional Hackathon Innovation) Voice fallback implementation.
- `[ ]` Final Presentation UI / Architecture diagrams.

---

## Local Development Backend Setup

1. **Navigate to backend**: 
   ```bash
   cd backend
   ```
2. **Setup Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Server Local**:
   ```bash
   uvicorn app.main:app --reload
   ```