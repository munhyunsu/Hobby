import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI(title="OpenAI Responses API Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-5")


class ChatRequest(BaseModel):
    message: str
    previous_response_id: str | None = None


class ChatResponse(BaseModel):
    response_id: str
    message: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        params = {
            "model": MODEL,
            "instructions": (
                "You are a helpful assistant. "
                "Answer the user clearly and concisely. "
                "Respond in Korean unless the user asks for another language."
            ),
            "input": request.message,
        }

        # 이전 OpenAI Response와 대화 연결
        if request.previous_response_id:
            params["previous_response_id"] = request.previous_response_id

        response = client.responses.create(**params)

        return ChatResponse(
            response_id=response.id,
            message=response.output_text,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

