import pytest
from httpx import Client


class TestQuestionsAPI:
    def test_get_questions_empty(self, test_client: Client):
        response = test_client.get("/api/v1/questions")

        assert response.status_code == 200
        assert response.json() == []

    def test_create_question(self, test_client: Client):
        question_data = {"text": "blabla"}

        response = test_client.post("/api/v1/questions/", json=question_data)

        assert response.status_code == 201

    def test_get_questions(self, test_client: Client, test_question):
        response = test_client.get("/api/v1/questions")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == test_question.id
        assert data[0]["text"] == test_question.text

    def test_get_question_by_id(self, test_client: Client, test_question):
        response = test_client.get(f"/api/v1/questions/{test_question.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_question.id
        assert data["text"] == test_question.text
        assert "answers" in data

    def test_get_nonexistent_question(self, test_client: Client):
        response = test_client.get("/api/v1/questions/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Question not found"

    def test_delete_question(self, test_client: Client, test_question):
        response = test_client.delete(f"/api/v1/questions/{test_question.id}")

        assert response.status_code == 204

        response = test_client.get(f"/api/v1/questions/{test_question.id}")
        assert response.status_code == 404

    def test_delete_nonexistent_question(self, test_client: Client):
        response = test_client.delete("/api/v1/questions/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Question not found"

    def test_create_question_validation_error(self, test_client: Client):
        invalid_data = {"text": ""}  # Empty text

        response = test_client.post("/api/v1/questions/", json=invalid_data)

        assert response.status_code == 422

    def test_get_question_with_answers(self, test_client: Client, test_question, test_answer):
        response = test_client.get(f"/api/v1/questions/{test_question.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_question.id
        assert len(data["answers"]) == 1
        assert data["answers"][0]["id"] == test_answer.id