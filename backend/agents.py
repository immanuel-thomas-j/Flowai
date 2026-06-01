import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv

# Configure simple logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load backend environment values from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise RuntimeError("GROQ_API_KEY is not set")

# Initialize Groq client from environment
client = Groq(api_key=groq_api_key)

# --- HACKATHON IN-MEMORY STORE ---
conversation_history = []

# --- PROMPT TEMPLATES ---
CLASSIFIER_PROMPT = """
Analyze the user's message and classify their intent into exactly ONE of these categories:
- SALES: Buying, pricing, product recommendations, upgrades.
- SUPPORT: Bugs, technical issues, how-to troubleshooting, system errors.
- CUSTOMER_CARE: Refunds, complaints, apologies, emotional support.
- ESCALATE: The user explicitly asks to speak to a human, a real person, or an agent.

Respond ONLY with a valid JSON object in this format:
{"intent": "SALES|SUPPORT|CUSTOMER_CARE|ESCALATE", "confidence": 99}
"""

SYSTEM_PROMPTS = {
    "SALES": """You are the Sales Bot for FlowAI. 
Your goal is to recommend products, suggest alternatives, and use persuasive but ethical sales language. 
Be enthusiastic and concise. Do not hallucinate prices unless asked to estimate. Format with Markdown.""",
    
    "SUPPORT": """You are the Technical Support Bot for FlowAI.
Your goal is to solve user issues step-by-step. Ask clarifying questions if needed.
Provide clear troubleshooting instructions. Be professional, logical, and highly structured. Format with Markdown.""",
    
    "CUSTOMER_CARE": """You are the Customer Care Bot for FlowAI.
Your goal is customer retention and satisfaction. Handle refund requests, apologize for bad experiences, 
and provide deep reassurance. Be empathetic, polite, and heavily focus on rebuilding trust. Format with Markdown."""
}

def classify_intent(message: str) -> dict:
    """Uses Groq (Llama 3) to classify the user's intent into structured JSON."""
    logging.info(f"Classifying message: {message}")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", # <-- Update this line
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        logging.info(f"Classification Result: {result}")
        return result
    except Exception as e:
        logging.error(f"Failed to parse classification JSON. Error: {e}")
        return {"intent": "SUPPORT", "confidence": 0}

def generate_response(intent: str, message: str) -> str:
    """Routes to the correct specialized agent and includes conversation history."""
    global conversation_history
    system_instruction = SYSTEM_PROMPTS.get(intent, SYSTEM_PROMPTS["SUPPORT"])
    
    # 1. Format system prompt
    formatted_messages = [{"role": "system", "content": system_instruction}]
    
    # 2. Add history (Mapping 'model' to 'assistant' for Groq's API)
    for turn in conversation_history:
        role = "assistant" if turn["role"] == "model" else "user"
        formatted_messages.append({"role": role, "content": turn["text"]})
        
    # 3. Append current user message
    formatted_messages.append({"role": "user", "content": message})
    
    # 4. Generate response
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", # <-- Update this line
        messages=formatted_messages,
        temperature=0.6 
    )
    
    reply_text = response.choices[0].message.content
    
    # 5. Save interaction to memory
    conversation_history.append({"role": "user", "text": message})
    conversation_history.append({"role": "model", "text": reply_text})
    
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
        
    return reply_text
