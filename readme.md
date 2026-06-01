# 🌊 FlowAI: Multi-Agent Conversational Router
**FAIC 2026 Hackathon Submission**

FlowAI is an intelligent, intent-aware routing engine designed to solve the critical problem of single-dimensional B2B customer service bots. By dynamically analyzing user intent in real-time, FlowAI seamlessly routes conversational payloads to specialized AI workers: **Sales**, **Technical Support**, or **Customer Care**.

🌐 **Live Demo Frontend:** [Add your deployed frontend URL here](https://example.com)
⚙️ **Deployed Backend API:** [Add your deployed backend URL here](https://example.com)

## 🚀 Key Innovation
Rather than relying on a single, generalized system prompt, FlowAI utilizes a two-step AI pipeline powered by the cutting-edge `Llama 3.1` model (via Groq API). 
1. **Classification Node:** Strictly outputs structured JSON analyzing user emotion, technical complexity, and buying intent.
2. **Specialized Worker Node:** Adopts the context and specialized prompt instructions (Sales, Support, or Care) to generate the final payload, retaining full conversational memory across intent switches.

## 🛠️ Technical Architecture
* **Backend Engine:** High-performance `FastAPI` (Python) built for async non-blocking operations.
* **LLM Integration:** `Groq API` leveraging `Llama-3.1-8b-instant` for ultra-low latency response times.
* **State Management:** In-memory contextual array retention mapped via API payload injection.
* **Frontend UI:** Zero-dependency Vanilla JS/CSS implementation, featuring real-time Markdown rendering (`marked.js`), dynamic confidence metrics, and glassmorphism styling.

## 🧭 Architecture Flow
```text
User Input ──> [ FastAPI Backend ] ──> [ Llama 3.1 Classifier Node ]
                                                   │
                 ┌─────────────────────────────────┼────────────────────────────────┐
                 ▼                                 ▼                                ▼
         [ Sales Worker ]                  [ Support Worker ]               [ Customer Care ]
     (Buying / Discount Intent)          (Technical / API Bugs)           (Refunds / Complaints)
                 │                                 │                                │
                 └─────────────────────────────────┼────────────────────────────────┘
                                                   ▼
                                     [ Final Contextual Response ]
```

## 🧪 Verification & Test Cases
Use these prompts during the demo so judges can verify each route quickly:
1. `Sales` test: "Can you recommend the best plan for a growing business?"
2. `Support` test: "I'm seeing an error when I try to connect my account."
3. `Customer Care` test: "I'd like a refund because the experience was disappointing."
4. `Context pivot` test: ask a support question, then immediately ask for pricing.
5. `Human escalation` test: "I want to speak to a real person."

## 🔐 Environment Setup
Create a `backend/.env` file with your Groq API key:
```env
GROQ_API_KEY=your-groq-api-key
```

Optional frontend config lives in `frontend/.env`:
```env
FLOWAI_API_URL=http://localhost:8000/chat
```

## 📂 Repository Structure
```text
flowai/
├── backend/
│   ├── app.py             # FastAPI entry point & CORS configuration
│   ├── agents.py          # AI Routing logic, Groq integration, and Memory state
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html         # Consolidated UI (HTML, CSS, Vanilla JS)
└── README.md              # Architecture documentation
