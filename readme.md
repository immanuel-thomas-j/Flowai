# FlowAI: Multi-Agent Conversational Router
**FAIC 2026 Hackathon Submission**

FlowAI is an intent-aware customer support router that sends each user message to the right AI specialist in real time. Instead of relying on one generic chatbot, FlowAI classifies the message first and then routes it to a dedicated Sales, Support, or Customer Care agent.

🌐 **Live Demo Frontend:** [https://flowai-demo.vercel.app/](https://flowai-demo.vercel.app/)
⚙️ **Deployed Backend API:** [https://flowai-w1rx.onrender.com](https://flowai-w1rx.onrender.com)
📚 **Repository:** [https://github.com/immanuel-thomas-j/Flowai](https://github.com/immanuel-thomas-j/Flowai)

## Key Innovation
FlowAI uses a two-step LLM pipeline powered by `Llama 3.1` through the Groq API.

1. **Classification Node:** analyzes the user's message and returns structured JSON with intent and confidence.
2. **Specialized Worker Node:** routes the message to the right persona and generates the final reply with the right tone and context.

## Technical Architecture
- **Backend Engine:** FastAPI handles the `/chat` endpoint and returns structured responses.
- **LLM Integration:** Groq API powers classification and response generation.
- **State Management:** in-memory conversation history keeps the assistant context-aware.
- **Frontend UI:** a polished vanilla HTML/CSS/JS interface with Markdown rendering, confidence feedback, and responsive layout.

## Architecture Flow
```text
User Input -> FastAPI Backend -> Llama 3.1 Classifier
                                     |
             +-----------------------+-----------------------+
             |                       |                       |
             v                       v                       v
        Sales Worker           Support Worker        Customer Care Worker
      (pricing, upsell)      (bugs, troubleshooting)   (refunds, complaints)
             +-----------------------+-----------------------+
                                     |
                                     v
                          Final contextual response
```

## UI Highlights
- A clear empty state explains the architecture before the user starts typing.
- The sidebar includes quick prompts for sales, support, and care scenarios.
- A `View Architecture Docs` link jumps straight to the full GitHub README.
- The chat bubbles support Markdown, so bold text and bullet lists render properly.

## Hackathon Evaluation Alignment
- **Model Innovation:** FlowAI uses a two-stage Llama 3.1 pipeline with intent classification followed by specialized routing.
- **Real-World Applicability:** The assistant handles realistic business flows like pricing, troubleshooting, refunds, and human escalation.
- **Technical Architecture:** The project uses FastAPI, a clean `/chat` JSON API, env-based configuration, and a responsive vanilla frontend.
- **Documentation Clarity:** The README includes live links, architecture flow, setup instructions, and judge-facing test cases.

## Verification & Test Cases
Use these prompts during the demo so judges can test each route quickly:
1. `Sales` test: "Can you recommend the best plan for a growing business?"
2. `Support` test: "I'm seeing an error when I try to connect my account."
3. `Customer Care` test: "I'd like a refund because the experience was disappointing."
4. `Context pivot` test: ask a support question, then immediately ask for pricing.
5. `Human escalation` test: "I want to speak to a real person."

## Environment Setup
Create `backend/.env` for your Groq API key:
```env
GROQ_API_KEY=your-groq-api-key
```

Optional frontend config lives in `frontend/.env`:
```env
FLOWAI_API_URL=https://flowai-w1rx.onrender.com/chat
```

## Run Locally
### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
Open `frontend/index.html` in your browser, or serve the folder with a simple static server.

## Repository Structure
```text
flowai/
├── backend/
│   ├── app.py
│   ├── agents.py
│   └── requirements.txt
├── frontend/
│   └── index.html
└── readme.md
```
