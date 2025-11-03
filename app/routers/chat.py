from fastapi import APIRouter, Query
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.config import settings
from app.services.providers.hfhub_provider import HFHubProvider
from app.services.providers.ollama_provider import OllamaProvider
from app.services.chain_builder import build_prompt
from app.utils.memory import get_history, append_message
from app.utils.sse import sse_response
from typing import AsyncIterator

router = APIRouter(prefix="/chat", tags=["chat"])

def _provider():
    if settings.PROVIDER == "hfhub":
        return HFHubProvider()
    return OllamaProvider()

@router.post("/invoke", response_model=ChatResponse)
async def invoke(body: ChatRequest):
    provider = _provider()
    history = get_history(body.session_id)
    append_message(body.session_id, "user", body.message)
    messages = build_prompt(body.message, history)
    normalized = [m.dict() if hasattr(m, "dict") else {"role": m.type, "content": m.content} for m in messages]
    text = await provider.ainvoke(normalized)
    append_message(body.session_id, "assistant", text)
    return ChatResponse(session_id=body.session_id, output=text)

@router.get("/stream")
async def stream(session_id: str = Query(...), q: str = Query(...)):
    provider = _provider()
    history = get_history(session_id)
    append_message(session_id, "user", q)
    messages = build_prompt(q, history)
    normalized = [m.dict() if hasattr(m, "dict") else {"role": m.type, "content": m.content} for m in messages]

    async def gen() -> AsyncIterator[str]:
        async for chunk in provider.astream(normalized):
            yield chunk

    return await sse_response(gen())
