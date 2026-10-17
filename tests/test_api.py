"""API tests.

The heavy parts (embedding models, ChromaDB, Gemini) are replaced with
small fakes, so these tests run in a second and need no API key.
"""

import sys
import types

import pytest
from fastapi.testclient import TestClient


# ---- Fake modules (must exist before backend.main is imported) ----

fake_generator = types.ModuleType("backend.generator")


class MissingAPIKeyError(RuntimeError):
    pass


fake_generator.MissingAPIKeyError = MissingAPIKeyError

fake_rag = types.ModuleType("backend.rag")
fake_rag.ask = lambda question: f"Answer to: {question}"

sys.modules["backend.generator"] = fake_generator
sys.modules["backend.rag"] = fake_rag

from backend import main  # noqa: E402


@pytest.fixture(autouse=True)
def clean_state(monkeypatch):
    main._request_log.clear()
    monkeypatch.setattr(main, "RATE_LIMIT_REQUESTS", 3)
    monkeypatch.setattr(main, "ask", fake_rag.ask)


@pytest.fixture
def client():
    return TestClient(main.app)


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_answer(client):
    response = client.post("/ask", json={"question": "What is a path parameter?"})

    assert response.status_code == 200
    assert response.json()["answer"] == "Answer to: What is a path parameter?"


def test_ask_rejects_empty_question(client):
    assert client.post("/ask", json={"question": ""}).status_code == 422


def test_ask_rejects_too_long_question(client):
    too_long = "x" * (main.MAX_QUESTION_LENGTH + 1)

    assert client.post("/ask", json={"question": too_long}).status_code == 422


def test_rate_limit(client):
    for _ in range(3):
        assert client.post("/ask", json={"question": "hi"}).status_code == 200

    assert client.post("/ask", json={"question": "hi"}).status_code == 429


def test_missing_api_key_returns_503(client, monkeypatch):
    def raise_missing_key(question):
        raise MissingAPIKeyError("no key")

    monkeypatch.setattr(main, "ask", raise_missing_key)

    assert client.post("/ask", json={"question": "hi"}).status_code == 503


def test_unexpected_error_returns_502(client, monkeypatch):
    def raise_error(question):
        raise ValueError("boom")

    monkeypatch.setattr(main, "ask", raise_error)

    assert client.post("/ask", json={"question": "hi"}).status_code == 502
