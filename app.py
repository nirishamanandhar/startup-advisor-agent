import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from chat_logic import LLMService, ConversationManager

load_dotenv()

app = FastAPI(title="Irish Startup Advisor API")

# Global storage
conversations = {}

api_key = os.getenv("groq_key")
base_url = "https://api.groq.com/openai/v1"
llm_engine = LLMService(api_key, base_url)

SYSTEM_PROMPT = """You are an expert Startup Ecosystem Advisor specializing in the Irish startup landscape. 
Your role is to guide startup founders through their entrepreneurial journey in Ireland, providing tailored advice on navigating the local ecosystem and scaling globally.

Key areas of expertise:
- Irish startup funding landscape: Government grants (SBIR, R&D Tax Credits), venture capital, angel investment networks
- Support organizations: Enterprise Ireland, Local Enterprise Offices, IDA Ireland, Irish startups Association
- Incubators and accelerators: LaunchPad, Dogpatch Labs, NDRC, StartupWorks
- Regulatory compliance: Irish Company Registration, GDPR, employment law, tax incentives
- Networking: Irish tech hubs (Dublin, Cork, Galway), industry events, founder communities
- Global scaling: EU market access, post-Brexit considerations, US expansion paths

When responding:
1. Ask clarifying questions about the founder's stage, industry, and goals
2. Provide Ireland-specific insights and resources
3. Connect them to relevant local organizations and funding opportunities
4. Give actionable next steps they can take immediately
5. Be encouraging but realistic about challenges
6. Mention relevant Irish success stories when relevant

Always be practical, informed, and supportive of the Irish startup vision."""


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@app.get("/")
def root():
    return {
        "message": "Irish Startup Ecosystem Advisor API",
        "endpoints": {
            "/chat": "POST - Send a message",
            "/history/{session_id}": "GET - Get conversation history",
            "/reset/{session_id}": "DELETE - Reset conversation",
            "/health": "GET - Health check"
        }
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Get or create conversation
        if request.session_id not in conversations:
            conversations[request.session_id] = ConversationManager(SYSTEM_PROMPT)

        chat_session = conversations[request.session_id]
        chat_session.add_message("user", request.message)

        # Get response
        response_stream = llm_engine.get_response(chat_session.get_history())

        full_reply = ""
        for chunk in response_stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                full_reply += content

        chat_session.add_message("assistant", full_reply)

        return {"response": full_reply, "session_id": request.session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/history/{session_id}")
def get_history(session_id: str):
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "messages": conversations[session_id].get_history()
    }


@app.delete("/reset/{session_id}")
def reset(session_id: str):
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session not found")

    del conversations[session_id]
    return {"message": f"Session {session_id} reset successfully"}


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)