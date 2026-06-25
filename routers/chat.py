from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from groq import Groq
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from database import get_db
from models import ChatMessage as ChatMessageModel
from schemas.chat import ChatMessage

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
router = APIRouter()


def get_conversation_history(session_id: str, db: Session):
    messages = (
        db.query(ChatMessageModel)
        .filter(ChatMessageModel.session_id == session_id)
        .order_by(ChatMessageModel.created_at)
        .all()
    )
    return [{"role": m.role, "content": m.content} for m in messages]


def save_message(session_id: str, role: str, content: str, db: Session):
    msg = ChatMessageModel(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()


@router.post("/chat/memory")
def chat_with_memory(body: ChatMessage, db: Session = Depends(get_db)):
    # save user's new message first
    save_message(body.session_id, "user", body.message, db)

    # fetch FULL conversation history including the new message
    history = get_conversation_history(body.session_id, db)

    # send entire history to the LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history
    )

    reply = response.choices[0].message.content

    # save bot's reply too — needed for NEXT request's history
    save_message(body.session_id, "assistant", reply, db)

    return {"response": reply}