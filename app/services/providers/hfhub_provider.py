from typing import AsyncIterator, List
import asyncio
from huggingface_hub import InferenceClient
from .base import ChatProvider, Message
from app.core.config import settings
import re


def clean_model_output(text: str) -> str:
    """
    Removes artifacts like [199/200], [ ], or trailing brackets 
    common in raw model outputs.
    """
    # Remove bracketed numeric counters or empty brackets
    text = re.sub(r"\[\s*\d+\/\d+\s*\]", "", text)  # remove [199/200]
    text = re.sub(r"\[\s*\]", "", text)             # remove empty [ ]
    text = re.sub(r"^\[|\]$", "", text.strip())     # remove wrapping brackets
    # Clean double spaces and trim
    return text.strip()

def strip_reasoning_tags(text: str) -> str:
    """Remove <think>...</think> reasoning traces (used by some chat models)."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def _format_messages_as_prompt(messages: List[Message]) -> List[dict]:
    """Format chat messages for the chat_completion API."""
    out = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        out.append({"role": role, "content": content})
    return out


class HFHubProvider(ChatProvider):
    def __init__(self):
        # Initialize the client only with token; model will be passed at call time
        self.client = InferenceClient(token=settings.HFHUB_API_TOKEN)

    async def astream(self, messages: List[Message], **kwargs) -> AsyncIterator[str]:
        """Stream response character by character (for SSE)."""
        text = await self.ainvoke(messages, **kwargs)
        for ch in text:
            yield ch
            if settings.SSE_CHUNK_DELAY_MS > 0:
                await asyncio.sleep(settings.SSE_CHUNK_DELAY_MS / 1000.0)
                
    async def ainvoke(self, messages: List[Message], **kwargs) -> str:
        formatted = _format_messages_as_prompt(messages)
        loop = asyncio.get_event_loop()

        def run():
            client = InferenceClient(token=settings.HFHUB_API_TOKEN)  # create per request
            response = client.chat_completion(
                model=settings.HFHUB_REPO_ID,
                messages=formatted,
                max_tokens=settings.MAX_TOKENS,
                temperature=0.7,
            )
            return response.choices[0].message["content"]

        result = await loop.run_in_executor(None, run)
        result = clean_model_output(result)

        return result.strip()
    