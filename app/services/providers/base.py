from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, Any, List

Message = Dict[str, str]

class ChatProvider(ABC):
    @abstractmethod
    async def astream(self, messages: List[Message], **kwargs) -> AsyncIterator[str]:
        ...

    @abstractmethod
    async def ainvoke(self, messages: List[Message], **kwargs) -> str:
        ...
