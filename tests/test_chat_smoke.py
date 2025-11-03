from fastapi.testclient import TestClient
from app.main import app

def test_invoke_smoke(monkeypatch):
    from app.routers import chat as chat_router
    class DummyProv:
        async def ainvoke(self, messages, **kw): return "ok"
        async def astream(self, messages, **kw):
            yield "o"; yield "k"
    monkeypatch.setattr(chat_router, "_provider", lambda: DummyProv())

    c = TestClient(app)
    r = c.post("/chat/invoke", json={"session_id":"s1","message":"hi"})
    assert r.status_code == 200
    assert r.json()["output"] == "ok"
