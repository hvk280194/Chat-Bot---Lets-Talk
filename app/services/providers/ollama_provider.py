import aiohttp
from typing import AsyncIterator, List, Dict
from .base import ChatProvider, Message
from app.core.config import settings

class OllamaProvider(ChatProvider):
    async def astream(self, messages: List[Message], **kwargs) -> AsyncIterator[str]:
        payload = {"model": settings.OLLAMA_MODEL, "messages": messages, "stream": True}
        async with aiohttp.ClientSession() as sess:
            async with sess.post(f"{settings.OLLAMA_BASE_URL}/v1/chat/completions", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.content:
                    if not line:
                        continue
                    yield line.decode("utf-8", errors="ignore")

    async def ainvoke(self, messages: List[Message], **kwargs) -> str:
        payload = {"model": settings.OLLAMA_MODEL, "messages": messages, "stream": False}
        async with aiohttp.ClientSession() as sess:
            async with sess.post(f"{settings.OLLAMA_BASE_URL}/v1/chat/completions", json=payload) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
