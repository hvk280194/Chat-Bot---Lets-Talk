from typing import Dict, List

_STORE: Dict[str, List[dict]] = {}

def get_history(session_id: str) -> List[dict]:
    return _STORE.setdefault(session_id, [])

def append_message(session_id: str, role: str, content: str):
    _STORE.setdefault(session_id, []).append({"role": role, "content": content})
