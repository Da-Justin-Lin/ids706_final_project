import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_get(client):
    # Test GET request to the index route
    response = client.get("/")
    assert response.status_code == 200
    assert b"email_draft" not in response.data


def test_index_post(client, monkeypatch):
    # Mock OpenAI response
    def mock_openai_chat_completion(*args, **kwargs):
        return {"choices": [{"message": {"content": "Generated email content."}}]}

    monkeypatch.setattr("openai.ChatCompletion.create", mock_openai_chat_completion)

    # Test POST request with form data
    response = client.post(
        "/",
        data={
            "purpose": "Follow-up Meeting",
            "tone": "Professional",
            "details": "Please confirm your availability.",
        },
    )
    assert response.status_code == 200
    assert b"Generated email content." in response.data
